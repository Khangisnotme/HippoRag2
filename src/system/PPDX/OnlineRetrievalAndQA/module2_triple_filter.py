"""
OnlineRetrievalAndQA/module2_triple_filter.py
Module 2: LLM Triple Filtering (Lọc Triple bằng LLM)
Sử dụng LLM để lọc và đánh giá relevance của triples với query

Mô tả chi tiết:
    Module này nhận raw triples từ Module 1 và sử dụng LLM để:
    1. Đánh giá relevance với query người dùng
    2. Lọc ra những triples chất lượng cao  
    3. Scoring và ranking theo mức độ liên quan
    4. Backup system với multiple LLM providers

Kiến trúc chính:
    - TripleFilterConfig: Cấu hình filtering parameters
    - LLMTripleFilter: Core filtering logic với primary/backup LLMs
    - FilteredTriple: Output data structure với rich metadata
    - RelevanceScorer: Scoring mechanism và level classification
    - BackupManager: Fallback LLM handling và error recovery

Workflow:
    Raw Triples + Query → LLM Evaluation → Relevance Scoring → Filtered Triples
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple
import logging
import time
import json
import re
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime

# LLM integrations
import openai
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import requests

# Shared utilities
from utils.utils_shared_general import (
    setup_logger,
    log_performance,
    validate_query,
    clean_text,
    save_json,
    load_json,
    get_api_key,
    load_environment_variables,
    PerformanceStats
)

# Module 1 imports
from module1_dual_retrieval import RetrievedItem

from huggingface_hub import InferenceClient

# Setup logger with file output
log_file = Path("outputs/log/module2_triple_filter_{}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
logger = setup_logger(__name__, log_file=log_file)

# ==================== ENUMS AND CONSTANTS ====================

class RelevanceLevel(Enum):
    """
    Các mức độ liên quan của triple với query
    """
    HIGHLY_RELEVANT = "highly_relevant"          # Điểm 0.8-1.0
    MODERATELY_RELEVANT = "moderately_relevant"  # Điểm 0.5-0.8
    SLIGHTLY_RELEVANT = "slightly_relevant"      # Điểm 0.2-0.5
    NOT_RELEVANT = "not_relevant"               # Điểm 0.0-0.2

    def get_score_range(self) -> Tuple[float, float]:
        """Lấy khoảng điểm số tương ứng với mức độ relevance"""
        ranges = {
            RelevanceLevel.HIGHLY_RELEVANT: (0.8, 1.0),
            RelevanceLevel.MODERATELY_RELEVANT: (0.5, 0.8),
            RelevanceLevel.SLIGHTLY_RELEVANT: (0.2, 0.5),
            RelevanceLevel.NOT_RELEVANT: (0.0, 0.2)
        }
        return ranges[self]
    
    def get_description(self) -> str:
        """Lấy mô tả chi tiết về mức độ relevance"""
        descriptions = {
            RelevanceLevel.HIGHLY_RELEVANT: "Rất liên quan - Trả lời trực tiếp câu hỏi",
            RelevanceLevel.MODERATELY_RELEVANT: "Liên quan vừa phải - Cung cấp context hữu ích",
            RelevanceLevel.SLIGHTLY_RELEVANT: "Ít liên quan - Thông tin phụ trợ",
            RelevanceLevel.NOT_RELEVANT: "Không liên quan - Thông tin nhiễu"
        }
        return descriptions[self]

class FilteringStrategy(Enum):
    """Các chiến lược filtering khác nhau"""
    STRICT = "strict"          # Threshold ≥ 0.7
    MODERATE = "moderate"      # Threshold ≥ 0.3
    LENIENT = "lenient"        # Threshold ≥ 0.1
    ADAPTIVE = "adaptive"      # Tự động điều chỉnh threshold

    def get_threshold(self) -> float:
        """Lấy ngưỡng điểm số để lọc triples"""
        thresholds = {
            FilteringStrategy.STRICT: 0.7,
            FilteringStrategy.MODERATE: 0.3,
            FilteringStrategy.LENIENT: 0.1,
            FilteringStrategy.ADAPTIVE: 0.3
        }
        return thresholds[self]

class LLMProvider(Enum):
    """Các nhà cung cấp LLM được hỗ trợ"""
    QWEN = "qwen2.5-7b-instruct"
    GPT3_5 = "gpt-3.5-turbo"
    HUGGINGFACE_API = "huggingface-api"

# ==================== DATA CLASSES ====================

@dataclass
class TripleFilterConfig:
    """Cấu hình toàn diện cho hệ thống lọc triple bằng LLM"""
    # LLM configuration
    primary_llm: LLMProvider = LLMProvider.QWEN
    backup_llm: LLMProvider = LLMProvider.GPT3_5
    
    # Batch processing parameters
    max_triples_per_batch: int = 8
    relevance_threshold: float = 0.3
    
    # Filtering strategy
    filtering_strategy: FilteringStrategy = FilteringStrategy.MODERATE
    
    # Reliability & performance
    max_retries: int = 3
    timeout_seconds: int = 45
    enable_caching: bool = True
    enable_backup: bool = True
    parallel_processing: bool = False
    
    # LLM generation parameters
    temperature: float = 0.1
    max_tokens: int = 800
    
    # Advanced parameters
    confidence_boost_factor: float = 1.2
    
    # API credentials
    huggingface_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    def __post_init__(self):
        """Tự động tải API keys từ environment variables"""
        env_vars = load_environment_variables()
        
        if self.huggingface_api_key is None:
            self.huggingface_api_key = get_api_key("huggingface", env_vars)
            
        if self.openai_api_key is None:
            self.openai_api_key = get_api_key("openai", env_vars)
        
        logger.info("🔑 Đã tải cấu hình API keys từ environment")
        logger.info(f"   📊 HuggingFace API: {'✅ Có' if self.huggingface_api_key else '❌ Không'}")
        logger.info(f"   🤖 OpenAI API: {'✅ Có' if self.openai_api_key else '❌ Không'}")

@dataclass
class FilteredTriple:
    """Triple đã được lọc và đánh giá bởi LLM với metadata đầy đủ"""
    triple_id: str
    subject: str
    predicate: str
    object: str
    original_text: str
    query_relevance_score: float
    relevance_level: RelevanceLevel
    confidence_score: float
    llm_explanation: str
    source_passage_id: str
    original_hybrid_retrieval_score: float
    filtering_metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi FilteredTriple object thành dictionary"""
        result = asdict(self)
        result['relevance_level'] = self.relevance_level.value
        return result
    
    def is_relevant(self, threshold: Optional[float] = None) -> bool:
        """Kiểm tra triple có relevant với query không"""
        if threshold is None:
            threshold = 0.3
        return self.query_relevance_score >= threshold
    
    def get_quality_score(self) -> float:
        """Tính điểm chất lượng tổng hợp của triple"""
        quality_score = (0.7 * self.query_relevance_score + 0.3 * self.confidence_score)
        return min(quality_score, 1.0)
    
    def get_summary(self) -> str:
        """Tạo summary ngắn gọn về triple"""
        return (f"({self.subject} → {self.predicate} → {self.object}) "
                f"| Relevance: {self.query_relevance_score:.3f} "
                f"| Level: {self.relevance_level.value} "
                f"| Quality: {self.get_quality_score():.3f}")

@dataclass
class FilteringResult:
    """Kết quả hoàn chỉnh của quá trình filtering"""
    filtered_triples: List[FilteredTriple]
    original_count: int
    filtered_count: int
    filtering_time: float
    query: str
    statistics: Dict[str, Any]
    errors: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi FilteringResult thành dictionary"""
        return {
            'filtered_triples': [triple.to_dict() for triple in self.filtered_triples],
            'original_count': self.original_count,
            'filtered_count': self.filtered_count,
            'filtering_time': self.filtering_time,
            'query': self.query,
            'statistics': self.statistics,
            'errors': self.errors
        }
    
    def save_to_file(self, filepath: Path):
        """Lưu kết quả filtering vào file JSON"""
        save_json(self.to_dict(), filepath, indent=2)
        logger.info(f"💾 Đã lưu kết quả filtering vào file: {filepath}")
        logger.info(f"   📊 Tổng triples: {self.original_count} → {self.filtered_count}")
        logger.info(f"   ⏱️ Thời gian: {self.filtering_time:.2f} giây")
    
    def get_filtering_efficiency(self) -> float:
        """Tính hiệu suất filtering"""
        if self.original_count == 0:
            return 0.0
        return self.filtered_count / self.original_count
    
    def get_relevance_distribution(self) -> Dict[str, int]:
        """Thống kê phân bố các mức độ relevance"""
        distribution = {}
        for level in RelevanceLevel:
            count = sum(1 for triple in self.filtered_triples 
                       if triple.relevance_level == level)
            distribution[level.value] = count
        return distribution

# ==================== LLM PROVIDERS ====================

class QwenTripleFilter:
    """LLM filter implementation sử dụng Qwen2.5-7B-Instruct model qua API"""
    
    def __init__(self, config: TripleFilterConfig):
        """Khởi tạo Qwen filter với cấu hình"""
        self.config = config
        self.client = InferenceClient(
            model="Qwen/Qwen2.5-7B-Instruct",
            token=self.config.huggingface_api_key
        )
        self.cache = {} if config.enable_caching else None
        
        logger.info(f"🧠 Khởi tạo QwenTripleFilter với HuggingFace Inference API...")
        logger.info(f"   💾 Caching: {'Bật' if config.enable_caching else 'Tắt'}")
        logger.info(f"   🌡️ Temperature: {config.temperature}")
        logger.info(f"   📏 Max tokens: {config.max_tokens}")
    
    def filter_triples_batch(self, query: str, triples: List[RetrievedItem]) -> List[Dict[str, Any]]:
        """Filter một batch triples sử dụng Qwen API"""
        logger.info(f"🧠 Bắt đầu filtering {len(triples)} triples với Qwen API...")
        
        # Check cache nếu enabled
        cache_key = None
        if self.cache is not None:
            cache_key = self._generate_cache_key(query, triples)
            if cache_key in self.cache:
                logger.info("💾 Tìm thấy kết quả trong cache, sử dụng cached result")
                return self.cache[cache_key]
        
        start_time = time.time()
        
        try:
            # Tạo prompt
            prompt = self.create_filtering_prompt(query, triples)
            
            # Gọi API với chat completion
            logger.info("   🔄 Đang gửi request đến HuggingFace Inference API (chat completion)...")
            completion = self.client.chat.completions.create(
                model="Qwen/Qwen2.5-7B-Instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=0.01
            )
            
            response_text = completion.choices[0].message.content
            
            logger.info(f"   📄 API response length: {len(response_text)} characters")
            logger.info(f"   🔍 Response preview: {response_text[:150]}...")
            
            # Parse response thành structured data
            evaluations = self.parse_llm_response(response_text, triples)
            
            # Cache result nếu enabled
            if self.cache is not None and cache_key is not None:
                self.cache[cache_key] = evaluations
                logger.info("💾 Đã cache kết quả filtering")
            
            end_time = time.time()
            log_performance("Qwen API batch filtering", start_time, end_time, {
                "batch_size": len(triples),
                "response_length": len(response_text),
                "evaluations_count": len(evaluations)
            })
            
            return evaluations
            
        except Exception as e:
            logger.error(f"❌ Lỗi trong Qwen API filtering: {e}")
            logger.exception("Chi tiết lỗi:")
            
            # Return fallback evaluations
            return self._create_fallback_evaluations(triples, f"qwen_api_error: {str(e)}")
    
    def create_filtering_prompt(self, query: str, triples: List[RetrievedItem]) -> str:
        """Tạo prompt chi tiết cho LLM để đánh giá relevance của triples"""
        logger.info(f"📝 Tạo filtering prompt cho {len(triples)} triples...")
        
        prompt = f"""Bạn là một chuyên gia đánh giá thông tin với khả năng phân tích sâu về mức độ liên quan của dữ liệu. Nhiệm vụ của bạn là đánh giá mức độ liên quan của các triple tri thức với câu hỏi của người dùng.

THÔNG TIN ĐÁNH GIÁ:
====================
CÂUHỎI: "{query}"

CÁC TRIPLE CẦN ĐÁNH GIÁ:
========================"""
        
        for i, triple in enumerate(triples, 1):
            subject = triple.metadata.get('subject', '').strip()
            predicate = triple.metadata.get('predicate', '').strip()
            obj = triple.metadata.get('object', '').strip()
            confidence = triple.metadata.get('confidence', 1.0)
            
            prompt += f"""

TRIPLE {i}:
-----------
✓ Chủ thể (Subject): {subject}
✓ Quan hệ (Predicate): {predicate}  
✓ Đối tượng (Object): {obj}
✓ Độ tin cậy gốc: {confidence:.3f}
✓ Text gốc: {triple.text}
"""
        
        prompt += f"""

HƯỚNG DẪN ĐÁNH GIÁ CHI TIẾT:
============================
Cho mỗi triple, hãy đánh giá mức độ liên quan với câu hỏi theo các tiêu chí sau:

📊 THANG ĐIỂM 0.0 → 1.0:
• 0.8-1.0: HIGHLY_RELEVANT 
  → Trả lời trực tiếp câu hỏi, thông tin cốt lõi cần thiết
  → Ví dụ: Câu hỏi về "lợi ích táo" → Triple "táo chứa vitamin C"

• 0.5-0.8: MODERATELY_RELEVANT
  → Liên quan và hữu ích, cung cấp context quan trọng
  → Ví dụ: Câu hỏi về "lợi ích táo" → Triple "vitamin C tốt cho sức khỏe"

• 0.2-0.5: SLIGHTLY_RELEVANT  
  → Có liên quan nhưng ít quan trọng, thông tin phụ trợ
  → Ví dụ: Câu hỏi về "lợi ích táo" → Triple "táo có màu đỏ"

• 0.0-0.2: NOT_RELEVANT
  → Không liên quan hoặc nhiễu, không đóng góp vào câu trả lời
  → Ví dụ: Câu hỏi về "lợi ích táo" → Triple "cam có vị chua"

🔍 TIÊU CHÍ ĐÁNH GIÁ:
1. Mức độ trả lời trực tiếp câu hỏi
2. Tính hữu ích của thông tin với người dùng
3. Chất lượng và độ chính xác của triple
4. Context và background information value

💡 LƯU Ý QUAN TRỌNG:
• Đánh giá dựa trên nội dung, không phải cú pháp
• Xem xét cả subject, predicate và object
• Ưu tiên thông tin trả lời trực tiếp câu hỏi
• Confidence gốc chỉ mang tính tham khảo

TRẢ LỜI THEO ĐỊNH DẠNG JSON CHÍNH XÁC:
=====================================
```json
{{
  "evaluations": [
    {{
      "triple_id": 1,
      "relevance_score": 0.85,
      "relevance_level": "highly_relevant",
      "explanation": "Triple này trả lời trực tiếp về lợi ích dinh dưỡng của táo, cung cấp thông tin cốt lõi mà người dùng đang tìm kiếm. Vitamin C là một lợi ích sức khỏe quan trọng của táo.",
      "confidence": 0.9
    }},
    {{
      "triple_id": 2,
      "relevance_score": 0.65,
      "relevance_level": "moderately_relevant", 
      "explanation": "Triple cung cấp thông tin bổ sung hữu ích về cơ chế tác động của vitamin C đến sức khỏe, giúp làm rõ lợi ích của táo.",
      "confidence": 0.8
    }}
  ]
}}
```

ĐÁNH GIÁ CHI TIẾT:"""
        
        logger.info(f"   📏 Prompt length: {len(prompt)} characters")
        logger.info(f"   🔤 Estimated tokens: ~{len(prompt) // 4}")
        
        return prompt
    
    def parse_llm_response(self, response_text: str, triples: List[RetrievedItem]) -> List[Dict[str, Any]]:
        """Parse và validate response từ LLM thành structured data"""
        logger.info("🔍 Đang parse response từ Qwen LLM...")
        logger.info(f"   📄 Response length: {len(response_text)} characters")
        
        try:
            # Bước 1: Extract JSON block từ response
            json_text = self._extract_json_from_response(response_text)
            
            # Bước 2: Parse JSON
            parsed_data = json.loads(json_text)
            evaluations = parsed_data.get('evaluations', [])
            
            # Bước 3: Validate và clean evaluations
            validated_evaluations = self._validate_evaluations(evaluations, triples)
            
            logger.info(f"✅ Thành công parse {len(validated_evaluations)} evaluations từ LLM")
            logger.info(f"   📊 Chất lượng parse: {len(validated_evaluations)}/{len(triples)} triples")
            
            return validated_evaluations
            
        except Exception as e:
            logger.error(f"❌ Lỗi parse LLM response: {e}")
            logger.error(f"   📄 Response preview: {response_text[:300]}...")
            
            # Fallback: tạo default evaluations
            logger.warning("⚠️ Sử dụng fallback evaluations với moderate relevance...")
            return self._create_fallback_evaluations(triples, "parse_error")
    
    def _extract_json_from_response(self, response_text: str) -> str:
        """Extract JSON block từ LLM response với multiple strategies"""
        # Strategy 1: Tìm ```json block
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            if json_end != -1:
                json_text = response_text[json_start:json_end].strip()
                logger.info("   🎯 Tìm thấy JSON trong ```json block")
                return json_text
        
        # Strategy 2: Tìm JSON object đầu tiên
        start_idx = response_text.find('{')
        if start_idx != -1:
            brace_count = 0
            end_idx = start_idx
            
            for i, char in enumerate(response_text[start_idx:], start_idx):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            
            json_text = response_text[start_idx:end_idx]
            logger.info("   🎯 Tìm thấy JSON object độc lập")
            return json_text
        
        # Strategy 3: Tìm array JSON
        start_idx = response_text.find('[')
        if start_idx != -1:
            bracket_count = 0
            end_idx = start_idx
            
            for i, char in enumerate(response_text[start_idx:], start_idx):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end_idx = i + 1
                        break
            
            json_text = f'{{"evaluations": {response_text[start_idx:end_idx]}}}'
            logger.info("   🎯 Tìm thấy JSON array, đã wrap vào object")
            return json_text
        
        raise ValueError("Không tìm thấy JSON valid trong response")
    
    def _validate_evaluations(self, evaluations: List[Dict], triples: List[RetrievedItem]) -> List[Dict[str, Any]]:
        """Validate và clean evaluations từ LLM"""
        logger.info(f"🔍 Validating {len(evaluations)} evaluations...")
        validated = []
        
        for i, eval_data in enumerate(evaluations):
            try:
                # Validate required fields
                triple_id = eval_data.get('triple_id', i + 1)
                relevance_score = float(eval_data.get('relevance_score', 0.5))
                relevance_level = eval_data.get('relevance_level', 'moderately_relevant')
                explanation = eval_data.get('explanation', 'Không có giải thích')
                confidence = float(eval_data.get('confidence', 0.5))
                
                # Validate và clamp scores
                relevance_score = max(0.0, min(1.0, relevance_score))
                confidence = max(0.0, min(1.0, confidence))
                
                # Validate relevance level
                valid_levels = [level.value for level in RelevanceLevel]
                if relevance_level not in valid_levels:
                    logger.warning(f"   ⚠️ Invalid relevance level '{relevance_level}', using 'moderately_relevant'")
                    relevance_level = 'moderately_relevant'
                
                # Ensure consistency between score and level
                relevance_score = self._adjust_score_to_level(relevance_score, relevance_level)
                
                validated_eval = {
                    'triple_id': triple_id,
                    'relevance_score': relevance_score,
                    'relevance_level': relevance_level,
                    'explanation': explanation,
                    'confidence': confidence
                }
                
                validated.append(validated_eval)
                logger.info(f"   ✅ Triple {triple_id}: {relevance_score:.3f} ({relevance_level})")
                
            except Exception as e:
                logger.error(f"   ❌ Lỗi validate evaluation {i+1}: {e}")
                # Tạo default evaluation
                default_eval = {
                    'triple_id': i + 1,
                    'relevance_score': 0.5,
                    'relevance_level': 'moderately_relevant',
                    'explanation': f'Lỗi validation: {str(e)}',
                    'confidence': 0.3
                }
                validated.append(default_eval)
        
        # Đảm bảo có đủ evaluations cho tất cả triples
        while len(validated) < len(triples):
            missing_id = len(validated) + 1
            logger.warning(f"   ⚠️ Thiếu evaluation cho triple {missing_id}, tạo default")
            default_eval = {
                'triple_id': missing_id,
                'relevance_score': 0.4,
                'relevance_level': 'moderately_relevant',
                'explanation': 'Evaluation bị thiếu, sử dụng giá trị mặc định',
                'confidence': 0.3
            }
            validated.append(default_eval)
        
        logger.info(f"✅ Validation hoàn thành: {len(validated)} evaluations")
        return validated
    
    def _adjust_score_to_level(self, score: float, level: str) -> float:
        """Điều chỉnh score để phù hợp với relevance level"""
        level_enum = RelevanceLevel(level)
        min_score, max_score = level_enum.get_score_range()
        
        # Nếu score nằm ngoài range của level, điều chỉnh về giữa range
        if score < min_score or score > max_score:
            adjusted_score = (min_score + max_score) / 2
            logger.info(f"   🔧 Điều chỉnh score: {score:.3f} → {adjusted_score:.3f} cho level {level}")
            return adjusted_score
        
        return score
    
    def _create_fallback_evaluations(self, triples: List[RetrievedItem], reason: str) -> List[Dict[str, Any]]:
        """Tạo fallback evaluations khi LLM parsing fail"""
        logger.warning(f"🔄 Tạo fallback evaluations (reason: {reason})...")
        
        fallback_evaluations = []
        for i, triple in enumerate(triples, 1):
            # Sử dụng original retrieval score làm base
            base_score = getattr(triple, 'hybrid_score', 0.5)
            # Normalize về moderate range
            fallback_score = 0.3 + (base_score * 0.3)  # Scale to 0.3-0.6 range
            
            fallback_eval = {
                'triple_id': i,
                'relevance_score': fallback_score,
                'relevance_level': 'moderately_relevant',
                'explanation': f'Đánh giá fallback do {reason}. Sử dụng retrieval score làm base.',
                'confidence': 0.3
            }
            fallback_evaluations.append(fallback_eval)
        
        logger.warning(f"   📊 Tạo {len(fallback_evaluations)} fallback evaluations với moderate relevance")
        return fallback_evaluations
    
    def _generate_cache_key(self, query: str, triples: List[RetrievedItem]) -> str:
        """Tạo cache key cho query và triples combination"""
        # Tạo hash từ query và triple contents
        triple_texts = [triple.text for triple in triples]
        content = f"{query}|{'|'.join(triple_texts)}"
        
        # Simple hash để làm cache key
        cache_key = hashlib.md5(content.encode()).hexdigest()[:16]
        return cache_key

class GPTTripleFilter:
    """
    Backup LLM filter implementation sử dụng OpenAI GPT-3.5-Turbo
    
    Class này serve như backup khi Qwen model fail hoặc không available.
    Sử dụng OpenAI API với optimized prompts cho filtering task.
    """
    
    def __init__(self, config: TripleFilterConfig):
        """
        Khởi tạo GPT filter với OpenAI API
        
        Args:
            config (TripleFilterConfig): Cấu hình filter parameters
        """
        self.config = config
        self.client = None
        self.cache = {} if config.enable_caching else None
        
        logger.info(f"🤖 Khởi tạo GPTTripleFilter...")
        logger.info(f"   💾 Caching: {'Bật' if config.enable_caching else 'Tắt'}")
        logger.info(f"   🌡️ Temperature: {config.temperature}")
        logger.info(f"   📏 Max tokens: {config.max_tokens}")
        
        # Initialize OpenAI client
        self._initialize_client()
    
    def _initialize_client(self):
        """Khởi tạo OpenAI client với API key"""
        try:
            if not self.config.openai_api_key:
                raise ValueError("OpenAI API key không được tìm thấy")
            
            openai.api_key = self.config.openai_api_key
            self.client = openai
            
            logger.info("✅ OpenAI client đã sẵn sàng")
            
        except Exception as e:
            logger.error(f"❌ Lỗi khởi tạo OpenAI client: {e}")
            logger.error("💡 Gợi ý:")
            logger.error("   - Kiểm tra OPENAI_API_KEY trong environment")
            logger.error("   - Đảm bảo API key còn hạn và có credit")
            raise
    
    def create_filtering_prompt(self, query: str, triples: List[RetrievedItem]) -> str:
        """
        Tạo prompt tối ưu cho GPT-3.5-Turbo để đánh giá triples
        
        Args:
            query (str): User query
            triples (List[RetrievedItem]): Triples cần đánh giá
            
        Returns:
            str: Optimized prompt cho GPT model
        """
        logger.info(f"📝 Tạo GPT filtering prompt cho {len(triples)} triples...")
        
        # GPT prompt format tối ưu hơn cho instruction following
        prompt = f"""You are an expert information evaluator. Evaluate the relevance of knowledge triples to the user's question.

USER QUESTION: "{query}"

TRIPLES TO EVALUATE:
"""
        
        for i, triple in enumerate(triples, 1):
            subject = triple.metadata.get('subject', '').strip()
            predicate = triple.metadata.get('predicate', '').strip()
            obj = triple.metadata.get('object', '').strip()
            confidence = triple.metadata.get('confidence', 1.0)
            
            prompt += f"""
Triple {i}:
- Subject: {subject}
- Predicate: {predicate}
- Object: {obj}
- Original confidence: {confidence:.3f}
- Source text: {triple.text}
"""
        
        prompt += f"""

EVALUATION GUIDELINES:
- Score 0.8-1.0: HIGHLY_RELEVANT (directly answers the question)
- Score 0.5-0.8: MODERATELY_RELEVANT (provides useful context)
- Score 0.2-0.5: SLIGHTLY_RELEVANT (tangentially related)
- Score 0.0-0.2: NOT_RELEVANT (unrelated or noise)

Return JSON format:
```json
{{
  "evaluations": [
    {{
      "triple_id": 1,
      "relevance_score": 0.85,
      "relevance_level": "highly_relevant",
      "explanation": "This triple directly answers...",
      "confidence": 0.9
    }}
  ]
}}
```

Evaluate each triple:"""
        
        logger.info(f"   📏 GPT prompt length: {len(prompt)} characters")
        return prompt
    
    def filter_triples_batch(self, query: str, triples: List[RetrievedItem]) -> List[Dict[str, Any]]:
        """
        Filter batch triples sử dụng GPT-3.5-Turbo API
        
        Args:
            query (str): User query
            triples (List[RetrievedItem]): Batch triples
            
        Returns:
            List[Dict[str, Any]]: Evaluations từ GPT
        """
        logger.info(f"🤖 Bắt đầu filtering {len(triples)} triples với GPT-3.5-Turbo...")
        
        # Check cache
        cache_key = None
        if self.cache is not None:
            cache_key = self._generate_cache_key(query, triples)
            if cache_key in self.cache:
                logger.info("💾 Sử dụng cached GPT result")
                return self.cache[cache_key]
        
        start_time = time.time()
        
        try:
            # Tạo prompt
            prompt = self.create_filtering_prompt(query, triples)
            
            # API call với retry logic
            logger.info("   🔄 Gửi request đến OpenAI API...")
            
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert at evaluating the relevance of information triples to user questions. Always respond with valid JSON."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout_seconds
            )
            
            response_text = response.choices[0].message.content
            
            logger.info(f"   📄 GPT response length: {len(response_text)} characters")
            logger.info(f"   💰 Tokens used: {response.usage.total_tokens}")
            
            # Parse response
            evaluations = self._parse_gpt_response(response_text, triples)
            
            # Cache result
            if self.cache is not None and cache_key is not None:
                self.cache[cache_key] = evaluations
                logger.info("💾 Đã cache GPT result")
            
            end_time = time.time()
            log_performance("GPT batch filtering", start_time, end_time, {
                "batch_size": len(triples),
                "tokens_used": response.usage.total_tokens,
                "evaluations_count": len(evaluations)
            })
            
            return evaluations
            
        except Exception as e:
            logger.error(f"❌ Lỗi GPT filtering: {e}")
            logger.exception("Chi tiết lỗi GPT:")
            
            # Return fallback
            return self._create_fallback_evaluations(triples, f"gpt_error: {str(e)}")
    
    def _parse_gpt_response(self, response_text: str, triples: List[RetrievedItem]) -> List[Dict[str, Any]]:
        """Parse GPT response với error handling"""
        try:
            # GPT thường return JSON clean hơn
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
            else:
                # Tìm JSON object
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                json_text = response_text[start_idx:end_idx]
            
            parsed_data = json.loads(json_text)
            evaluations = parsed_data.get('evaluations', [])
            
            # Validate basic structure
            validated_evaluations = []
            for i, eval_data in enumerate(evaluations):
                validated_eval = {
                    'triple_id': eval_data.get('triple_id', i + 1),
                    'relevance_score': max(0.0, min(1.0, float(eval_data.get('relevance_score', 0.5)))),
                    'relevance_level': eval_data.get('relevance_level', 'moderately_relevant'),
                    'explanation': eval_data.get('explanation', 'GPT evaluation'),
                    'confidence': max(0.0, min(1.0, float(eval_data.get('confidence', 0.5))))
                }
                validated_evaluations.append(validated_eval)
            
            logger.info(f"✅ Parsed {len(validated_evaluations)} GPT evaluations")
            return validated_evaluations
            
        except Exception as e:
            logger.error(f"❌ Lỗi parse GPT response: {e}")
            return self._create_fallback_evaluations(triples, "gpt_parse_error")
    
    def _generate_cache_key(self, query: str, triples: List[RetrievedItem]) -> str:
        """Tạo cache key cho GPT requests"""
        triple_texts = [triple.text for triple in triples]
        content = f"gpt|{query}|{'|'.join(triple_texts)}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def _create_fallback_evaluations(self, triples: List[RetrievedItem], reason: str) -> List[Dict[str, Any]]:
        """Tạo fallback evaluations cho GPT errors"""
        logger.warning(f"🔄 Tạo GPT fallback evaluations (reason: {reason})...")
        
        fallback_evaluations = []
        for i, triple in enumerate(triples, 1):
            base_score = getattr(triple, 'hybrid_score', 0.5)
            fallback_score = 0.35 + (base_score * 0.25)  # Conservative scoring
            
            fallback_eval = {
                'triple_id': i,
                'relevance_score': fallback_score,
                'relevance_level': 'moderately_relevant',
                'explanation': f'GPT fallback evaluation due to {reason}',
                'confidence': 0.4
            }
            fallback_evaluations.append(fallback_eval)
        
        return fallback_evaluations

# ==================== MAIN TRIPLE FILTER ====================

class LLMTripleFilter:
    """
    Main LLM Triple Filter với primary/backup system
    
    Class chính điều phối việc filtering triples sử dụng multiple LLM providers
    với robust error handling và fallback mechanisms.
    """
    
    def __init__(self, config: Optional[TripleFilterConfig] = None):
        """
        Khởi tạo LLM Triple Filter system
        
        Args:
            config (Optional[TripleFilterConfig]): Cấu hình filtering
        """
        self.config = config or TripleFilterConfig()
        
        logger.info("🚀 Khởi tạo LLMTripleFilter system...")
        logger.info(f"   🧠 Primary LLM: {self.config.primary_llm.value}")
        logger.info(f"   🔄 Backup LLM: {self.config.backup_llm.value}")
        logger.info(f"   📊 Strategy: {self.config.filtering_strategy.value}")
        logger.info(f"   🎯 Threshold: {self.config.relevance_threshold}")
        
        # Initialize LLM providers
        self.primary_filter = None
        self.backup_filter = None
        self.errors = []
        
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Khởi tạo các LLM providers"""
        try:
            # Initialize primary LLM
            if self.config.primary_llm == LLMProvider.QWEN:
                logger.info("   🧠 Khởi tạo Qwen primary filter...")
                self.primary_filter = QwenTripleFilter(self.config)
            elif self.config.primary_llm == LLMProvider.GPT3_5:
                logger.info("   🤖 Khởi tạo GPT-3.5 primary filter...")
                self.primary_filter = GPTTripleFilter(self.config)
            
            # Initialize backup LLM if enabled
            if self.config.enable_backup:
                if self.config.backup_llm == LLMProvider.GPT3_5 and self.config.primary_llm != LLMProvider.GPT3_5:
                    logger.info("   🔄 Khởi tạo GPT-3.5 backup filter...")
                    self.backup_filter = GPTTripleFilter(self.config)
                elif self.config.backup_llm == LLMProvider.QWEN and self.config.primary_llm != LLMProvider.QWEN:
                    logger.info("   🔄 Khởi tạo Qwen backup filter...")
                    self.backup_filter = QwenTripleFilter(self.config)
            
            logger.info("✅ LLM providers đã được khởi tạo thành công")
            
        except Exception as e:
            logger.error(f"❌ Lỗi khởi tạo LLM providers: {e}")
            self.errors.append({
                'timestamp': time.time(),
                'error': 'provider_initialization_failed',
                'message': str(e)
            })
            raise
    
    def filter_triples(self, query: str, raw_triples: List[RetrievedItem]) -> FilteringResult:
        """
        Main method để filter triples sử dụng LLM evaluation
        
        Args:
            query (str): User query
            raw_triples (List[RetrievedItem]): Raw triples từ Module 1
            
        Returns:
            FilteringResult: Kết quả filtering với filtered triples
        """
        logger.info("=" * 60)
        logger.info("🤖 BẮT ĐẦU LLM TRIPLE FILTERING")
        logger.info("=" * 60)
        logger.info(f"📝 Query: '{query}'")
        logger.info(f"📊 Raw triples: {len(raw_triples)}")
        logger.info(f"🎯 Target threshold: {self.config.relevance_threshold}")
        
        start_time = time.time()
        
        # Validate input
        if not validate_query(query):
            logger.error("❌ Invalid query")
            return self._create_empty_result(query, 0, "invalid_query")
        
        if not raw_triples:
            logger.warning("⚠️ Không có raw triples để filter")
            return self._create_empty_result(query, 0, "no_input_triples")
        
        # Process triples in batches
        logger.info(f"\n🔄 PROCESSING TRIPLES IN BATCHES")
        logger.info("-" * 40)
        
        all_evaluations = []
        batch_size = self.config.max_triples_per_batch
        total_batches = (len(raw_triples) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(raw_triples))
            batch_triples = raw_triples[start_idx:end_idx]
            
            logger.info(f"📦 Batch {batch_idx + 1}/{total_batches}: triples {start_idx + 1}-{end_idx}")
            
            # Filter batch với primary LLM
            batch_evaluations = self._filter_batch_with_fallback(query, batch_triples)
            all_evaluations.extend(batch_evaluations)
            
            logger.info(f"   ✅ Hoàn thành batch {batch_idx + 1}, evaluations: {len(batch_evaluations)}")
        
        # Convert evaluations thành FilteredTriple objects
        logger.info(f"\n🔧 CONVERTING TO FILTERED TRIPLES")
        logger.info("-" * 40)
        
        filtered_triples = self._convert_to_filtered_triples(query, raw_triples, all_evaluations)
        
        # Apply filtering strategy
        logger.info(f"\n🎯 APPLYING FILTERING STRATEGY")
        logger.info("-" * 40)
        
        final_filtered_triples = self._apply_filtering_strategy(filtered_triples)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Tạo statistics
        statistics = self._create_statistics(query, raw_triples, final_filtered_triples, total_time)
        
        # Tạo final result
        result = FilteringResult(
            filtered_triples=final_filtered_triples,
            original_count=len(raw_triples),
            filtered_count=len(final_filtered_triples),
            filtering_time=total_time,
            query=query,
            statistics=statistics,
            errors=self.errors.copy()
        )
        
        # Log final summary
        self._log_filtering_summary(result)
        
        return result
    
    def _filter_batch_with_fallback(self, query: str, batch_triples: List[RetrievedItem]) -> List[Dict[str, Any]]:
        """
        Filter batch với primary LLM và fallback nếu cần
        
        Args:
            query (str): User query
            batch_triples (List[RetrievedItem]): Batch triples
            
        Returns:
            List[Dict[str, Any]]: Batch evaluations
        """
        # Try primary LLM first
        try:
            logger.info(f"   🧠 Sử dụng {self.config.primary_llm.value} primary filter...")
            evaluations = self.primary_filter.filter_triples_batch(query, batch_triples)
            
            # Validate evaluations quality
            if self._validate_evaluations_quality(evaluations, batch_triples):
                logger.info("   ✅ Primary LLM filtering thành công")
                return evaluations
            else:
                logger.warning("   ⚠️ Primary LLM evaluations chất lượng thấp, thử backup...")
                raise ValueError("Low quality evaluations from primary LLM")
        
        except Exception as e:
            logger.error(f"   ❌ Primary LLM failed: {e}")
            self.errors.append({
                'timestamp': time.time(),
                'error': 'primary_llm_failed',
                'message': str(e),
                'batch_size': len(batch_triples)
            })
        
        # Try backup LLM
        if self.backup_filter:
            try:
                logger.info(f"   🔄 Sử dụng {self.config.backup_llm.value} backup filter...")
                evaluations = self.backup_filter.filter_triples_batch(query, batch_triples)
                logger.info("   ✅ Backup LLM filtering thành công")
                return evaluations
                
            except Exception as e:
                logger.error(f"   ❌ Backup LLM cũng failed: {e}")
                self.errors.append({
                    'timestamp': time.time(),
                    'error': 'backup_llm_failed',
                    'message': str(e),
                    'batch_size': len(batch_triples)
                })
        
        # Final fallback: create conservative evaluations
        logger.warning("   🔄 Sử dụng final conservative fallback...")
        return self._create_conservative_evaluations(batch_triples)
    
    def _validate_evaluations_quality(self, evaluations: List[Dict], triples: List[RetrievedItem]) -> bool:
        """
        Validate chất lượng evaluations từ LLM
        
        Args:
            evaluations (List[Dict]): Evaluations từ LLM
            triples (List[RetrievedItem]): Original triples
            
        Returns:
            bool: True nếu chất lượng acceptable
        """
        # Check basic requirements
        if len(evaluations) != len(triples):
            logger.warning(f"   ⚠️ Evaluation count mismatch: {len(evaluations)} vs {len(triples)}")
            return False
        
        # Check for valid scores
        valid_scores = 0
        for eval_data in evaluations:
            score = eval_data.get('relevance_score', 0)
            if isinstance(score, (int, float)) and 0 <= score <= 1:
                valid_scores += 1
        
        quality_ratio = valid_scores / len(evaluations)
        logger.info(f"   📊 Evaluation quality: {quality_ratio:.2f} ({valid_scores}/{len(evaluations)} valid)")
        
        return quality_ratio >= 0.8  # Require 80% valid evaluations
    
    def _create_conservative_evaluations(self, triples: List[RetrievedItem]) -> List[Dict[str, Any]]:
        """
        Tạo conservative evaluations khi cả primary và backup fail
        
        Args:
            triples (List[RetrievedItem]): Triples cần evaluate
            
        Returns:
            List[Dict[str, Any]]: Conservative evaluations
        """
        logger.warning("   🛡️ Tạo conservative evaluations...")
        
        conservative_evaluations = []
        for i, triple in enumerate(triples, 1):
            # Use retrieval score as base, but be conservative
            base_score = getattr(triple, 'hybrid_score', 0.5)
            conservative_score = 0.25 + (base_score * 0.35)  # Scale to 0.25-0.6
            
            eval_data = {
                'triple_id': i,
                'relevance_score': conservative_score,
                'relevance_level': 'moderately_relevant',
                'explanation': 'Conservative evaluation - cả primary và backup LLM đều fail',
                'confidence': 0.3
            }
            conservative_evaluations.append(eval_data)
        
        logger.warning(f"   📊 Tạo {len(conservative_evaluations)} conservative evaluations")
        return conservative_evaluations
    
    def _convert_to_filtered_triples(self, query: str, raw_triples: List[RetrievedItem], 
                                   evaluations: List[Dict[str, Any]]) -> List[FilteredTriple]:
        """
        Convert evaluations thành FilteredTriple objects
        
        Args:
            query (str): User query
            raw_triples (List[RetrievedItem]): Original triples
            evaluations (List[Dict]): LLM evaluations
            
        Returns:
            List[FilteredTriple]: Converted filtered triples
        """
        logger.info(f"🔧 Converting {len(evaluations)} evaluations thành FilteredTriple objects...")
        
        filtered_triples = []
        
        for i, (raw_triple, eval_data) in enumerate(zip(raw_triples, evaluations)):
            try:
                # Extract evaluation data
                relevance_score = eval_data.get('relevance_score', 0.5)
                relevance_level_str = eval_data.get('relevance_level', 'moderately_relevant')
                llm_explanation = eval_data.get('explanation', 'Không có giải thích')
                eval_confidence = eval_data.get('confidence', 0.5)
                
                # Convert relevance level string to enum
                try:
                    relevance_level = RelevanceLevel(relevance_level_str)
                except ValueError:
                    logger.warning(f"   ⚠️ Invalid relevance level '{relevance_level_str}', using MODERATELY_RELEVANT")
                    relevance_level = RelevanceLevel.MODERATELY_RELEVANT
                
                # Extract triple metadata
                subject = raw_triple.metadata.get('subject', '')
                predicate = raw_triple.metadata.get('predicate', '')
                obj = raw_triple.metadata.get('object', '')
                source_passage_id = raw_triple.metadata.get('source_passage_id', '')
                original_confidence = raw_triple.metadata.get('confidence', 1.0)
                
                # Create filtering metadata
                filtering_metadata = {
                    'llm_provider': self.config.primary_llm.value,
                    'filtering_strategy': self.config.filtering_strategy.value,
                    'original_hybrid_score': raw_triple.hybrid_score,
                    'original_bm25_score': raw_triple.bm25_score,
                    'original_embedding_score': raw_triple.embedding_score,
                    'eval_confidence': eval_confidence,
                    'processing_timestamp': time.time()
                }
                
                # Create FilteredTriple object
                filtered_triple = FilteredTriple(
                    triple_id=raw_triple.item_id,
                    subject=subject,
                    predicate=predicate,
                    object=obj,
                    original_text=raw_triple.text,
                    query_relevance_score=relevance_score,
                    relevance_level=relevance_level,
                    confidence_score=original_confidence,
                    llm_explanation=llm_explanation,
                    source_passage_id=source_passage_id,
                    original_hybrid_retrieval_score=raw_triple.hybrid_score,
                    filtering_metadata=filtering_metadata
                )
                
                filtered_triples.append(filtered_triple)
                
                if (i + 1) % 10 == 0 or (i + 1) == len(evaluations):
                    logger.info(f"   📦 Converted {i + 1}/{len(evaluations)} triples")
                
            except Exception as e:
                logger.error(f"   ❌ Lỗi convert triple {i + 1}: {e}")
                # Skip invalid triple
                continue
        
        logger.info(f"✅ Hoàn thành conversion: {len(filtered_triples)} FilteredTriple objects")
        return filtered_triples
    
    def _apply_filtering_strategy(self, filtered_triples: List[FilteredTriple]) -> List[FilteredTriple]:
        """
        Áp dụng filtering strategy để lọc final triples
        
        Args:
            filtered_triples (List[FilteredTriple]): All filtered triples
            
        Returns:
            List[FilteredTriple]: Final filtered triples after strategy
        """
        logger.info(f"🎯 Áp dụng filtering strategy: {self.config.filtering_strategy.value}")
        
        if self.config.filtering_strategy == FilteringStrategy.ADAPTIVE:
            # Adaptive strategy: điều chỉnh threshold dựa trên distribution
            threshold = self._calculate_adaptive_threshold(filtered_triples)
            logger.info(f"   🧠 Adaptive threshold: {threshold:.3f}")
        else:
            threshold = self.config.filtering_strategy.get_threshold()
            logger.info(f"   🎯 Fixed threshold: {threshold:.3f}")
        
        # Filter based on threshold
        final_triples = [
            triple for triple in filtered_triples 
            if triple.query_relevance_score >= threshold
        ]
        
        # Sort by quality score (combination of relevance and confidence)
        final_triples.sort(key=lambda t: t.get_quality_score(), reverse=True)
        
        # Log filtering results by relevance level
        distribution = {}
        for level in RelevanceLevel:
            count = sum(1 for triple in final_triples if triple.relevance_level == level)
            distribution[level.value] = count
            logger.info(f"   📊 {level.value}: {count} triples")
        
        logger.info(f"✅ Filtering strategy applied: {len(filtered_triples)} → {len(final_triples)} triples")
        return final_triples
    
    def _calculate_adaptive_threshold(self, filtered_triples: List[FilteredTriple]) -> float:
        """
        Tính adaptive threshold dựa trên score distribution
        
        Args:
            filtered_triples (List[FilteredTriple]): All filtered triples
            
        Returns:
            float: Calculated adaptive threshold
        """
        if not filtered_triples:
            return 0.3  # Default threshold
        
        scores = [triple.query_relevance_score for triple in filtered_triples]
        scores.sort(reverse=True)
        
        # Calculate statistics
        avg_score = sum(scores) / len(scores)
        median_score = scores[len(scores) // 2] if scores else 0.3
        
        # Count high quality triples (≥ 0.7)
        high_quality_count = sum(1 for score in scores if score >= 0.7)
        high_quality_ratio = high_quality_count / len(scores)
        
        logger.info(f"   📊 Score stats: avg={avg_score:.3f}, median={median_score:.3f}")
        logger.info(f"   📈 High quality ratio: {high_quality_ratio:.3f} ({high_quality_count}/{len(scores)})")
        
        # Adaptive logic
        if high_quality_ratio >= 0.3:  # Nhiều triples chất lượng cao
            threshold = 0.6  # Threshold cao để lọc chặt
        elif high_quality_ratio >= 0.1:  # Có một số triples tốt
            threshold = 0.4  # Threshold vừa phải
        else:  # Ít triples chất lượng cao
            threshold = 0.25  # Threshold thấp để giữ nhiều triples
        
        # Không để threshold quá thấp hoặc quá cao
        threshold = max(0.2, min(0.8, threshold))
        
        return threshold
    
    def _create_statistics(self, query: str, raw_triples: List[RetrievedItem], 
                          filtered_triples: List[FilteredTriple], 
                          processing_time: float) -> Dict[str, Any]:
        """
        Tạo comprehensive statistics cho filtering process
        
        Args:
            query (str): Original query
            raw_triples (List[RetrievedItem]): Input triples
            filtered_triples (List[FilteredTriple]): Output triples
            processing_time (float): Total processing time
            
        Returns:
            Dict[str, Any]: Comprehensive statistics
        """
        logger.info("📊 Tạo filtering statistics...")
        
        # Basic counts
        original_count = len(raw_triples)
        filtered_count = len(filtered_triples)
        
        # Relevance distribution
        relevance_distribution = {}
        for level in RelevanceLevel:
            count = sum(1 for triple in filtered_triples if triple.relevance_level == level)
            relevance_distribution[level.value] = count
        
        # Score statistics
        if filtered_triples:
            relevance_scores = [t.query_relevance_score for t in filtered_triples]
            quality_scores = [t.get_quality_score() for t in filtered_triples]
            
            score_stats = {
                'relevance': {
                    'min': min(relevance_scores),
                    'max': max(relevance_scores),
                    'avg': sum(relevance_scores) / len(relevance_scores),
                    'median': sorted(relevance_scores)[len(relevance_scores) // 2]
                },
                'quality': {
                    'min': min(quality_scores),
                    'max': max(quality_scores),
                    'avg': sum(quality_scores) / len(quality_scores),
                    'median': sorted(quality_scores)[len(quality_scores) // 2]
                }
            }
        else:
            score_stats = {
                'relevance': {'min': 0, 'max': 0, 'avg': 0, 'median': 0},
                'quality': {'min': 0, 'max': 0, 'avg': 0, 'median': 0}
            }
        
        # Processing efficiency
        efficiency_stats = {
            'filtering_rate': filtered_count / original_count if original_count > 0 else 0,
            'triples_per_second': original_count / processing_time if processing_time > 0 else 0,
            'avg_time_per_triple': processing_time / original_count if original_count > 0 else 0
        }
        
        # LLM usage statistics
        llm_stats = {
            'primary_llm': self.config.primary_llm.value,
            'backup_llm': self.config.backup_llm.value if self.config.enable_backup else None,
            'total_errors': len(self.errors),
            'error_rate': len(self.errors) / original_count if original_count > 0 else 0
        }
        
        # Configuration used
        config_stats = {
            'filtering_strategy': self.config.filtering_strategy.value,
            'relevance_threshold': self.config.relevance_threshold,
            'max_batch_size': self.config.max_triples_per_batch,
            'temperature': self.config.temperature,
            'max_tokens': self.config.max_tokens
        }
        
        return {
            'query_info': {
                'original_query': query,
                'query_length': len(query),
                'query_words': len(query.split())
            },
            'processing_counts': {
                'original_triples': original_count,
                'filtered_triples': filtered_count,
                'removed_triples': original_count - filtered_count
            },
            'relevance_distribution': relevance_distribution,
            'score_statistics': score_stats,
            'efficiency_metrics': efficiency_stats,
            'llm_usage': llm_stats,
            'configuration': config_stats,
            'performance': {
                'total_time_seconds': processing_time,
                'timestamp': time.time()
            }
        }
    
    def _create_empty_result(self, query: str, original_count: int, reason: str) -> FilteringResult:
        """
        Tạo empty FilteringResult khi có lỗi hoặc không có input
        
        Args:
            query (str): Original query
            original_count (int): Number of original triples
            reason (str): Reason for empty result
            
        Returns:
            FilteringResult: Empty result với error info
        """
        logger.warning(f"🔄 Tạo empty filtering result (reason: {reason})")
        
        error_info = {
            'timestamp': time.time(),
            'error': 'empty_result',
            'reason': reason,
            'original_count': original_count
        }
        
        return FilteringResult(
            filtered_triples=[],
            original_count=original_count,
            filtered_count=0,
            filtering_time=0.0,
            query=query,
            statistics={
                'query_info': {'original_query': query},
                'processing_counts': {'original_triples': original_count, 'filtered_triples': 0},
                'error_info': error_info
            },
            errors=[error_info]
        )
    
    def _log_filtering_summary(self, result: FilteringResult):
        """
        Log comprehensive summary của filtering process
        
        Args:
            result (FilteringResult): Final filtering result
        """
        logger.info("=" * 60)
        logger.info("🎉 LLM TRIPLE FILTERING HOÀN THÀNH")
        logger.info("=" * 60)
        
        # Basic metrics
        logger.info(f"📊 KẾT QUẢ TỔNG QUAN:")
        logger.info(f"   📝 Query: '{result.query}'")
        logger.info(f"   ⏱️ Thời gian xử lý: {result.filtering_time:.2f} giây")
        logger.info(f"   📈 Triples: {result.original_count} → {result.filtered_count}")
        logger.info(f"   📊 Tỷ lệ giữ lại: {result.get_filtering_efficiency():.2%}")
        
        # Relevance distribution
        distribution = result.get_relevance_distribution()
        logger.info(f"\n📊 PHÂN BỐ RELEVANCE:")
        for level, count in distribution.items():
            percentage = (count / result.filtered_count * 100) if result.filtered_count > 0 else 0
            level_desc = RelevanceLevel(level).get_description()
            logger.info(f"   {level}: {count} triples ({percentage:.1f}%) - {level_desc}")
        
        # Top quality triples
        if result.filtered_triples:
            logger.info(f"\n🏆 TOP 5 FILTERED TRIPLES:")
            top_triples = sorted(result.filtered_triples, key=lambda t: t.get_quality_score(), reverse=True)[:5]
            for i, triple in enumerate(top_triples, 1):
                logger.info(f"   {i}. {triple.get_summary()}")
                logger.info(f"      💭 Explanation: {triple.llm_explanation[:100]}...")
        
        # Performance metrics
        stats = result.statistics
        if 'efficiency_metrics' in stats:
            efficiency = stats['efficiency_metrics']
            logger.info(f"\n⚡ PERFORMANCE METRICS:")
            logger.info(f"   🏃 Triples/giây: {efficiency['triples_per_second']:.1f}")
            logger.info(f"   ⏱️ Avg time/triple: {efficiency['avg_time_per_triple']:.3f}s")
        
        # Error summary
        if result.errors:
            logger.info(f"\n⚠️ ERRORS ENCOUNTERED: {len(result.errors)}")
            for error in result.errors[-3:]:  # Show last 3 errors
                logger.info(f"   ❌ {error.get('error', 'unknown')}: {error.get('message', 'no message')}")
        else:
            logger.info(f"\n✅ KHÔNG CÓ LỖI TRONG QUÁ TRÌNH FILTERING")
        
        logger.info("=" * 60)

# ==================== UTILITY FUNCTIONS ====================

def create_default_config() -> TripleFilterConfig:
    """
    Tạo cấu hình mặc định cho Triple Filter
    
    Returns:
        TripleFilterConfig: Default configuration
    """
    logger.info("⚙️ Tạo default TripleFilterConfig...")
    
    config = TripleFilterConfig(
        primary_llm=LLMProvider.QWEN,
        backup_llm=LLMProvider.GPT3_5,
        max_triples_per_batch=8,
        relevance_threshold=0.3,
        filtering_strategy=FilteringStrategy.MODERATE,
        enable_backup=True,
        enable_caching=True,
        temperature=0.1,
        max_tokens=800
    )
    
    logger.info("✅ Default config đã được tạo")
    return config

def quick_filter_triples(query: str, raw_triples: List[RetrievedItem], 
                        strategy: str = "moderate") -> FilteringResult:
    """
    Quick utility function để filter triples với cấu hình đơn giản
    
    Args:
        query (str): User query
        raw_triples (List[RetrievedItem]): Raw triples từ Module 1
        strategy (str): Filtering strategy ("strict", "moderate", "lenient")
        
    Returns:
        FilteringResult: Filtering result
    """
    logger.info(f"🚀 Quick filtering với strategy: {strategy}")
    
    # Create config based on strategy
    config = create_default_config()
    config.filtering_strategy = FilteringStrategy(strategy)
    
    # Initialize filter và process
    filter_system = LLMTripleFilter(config)
    result = filter_system.filter_triples(query, raw_triples)
    
    return result

# ==================== TEST FUNCTIONS ====================

def test_triple_filter_with_mock_data():
    """Test Triple Filter với mock data"""
    print("🧪 BẮT ĐẦU TEST TRIPLE FILTER")
    print("=" * 50)
    
    # Mock RetrievedItem objects
    mock_triples = [
        RetrievedItem(
            item_id="triple_001",
            item_type="triple",
            text="táo chứa vitamin C",
            bm25_score=0.8,
            embedding_score=0.9,
            hybrid_score=0.85,
            metadata={
                'subject': 'táo',
                'predicate': 'chứa',
                'object': 'vitamin C',
                'confidence': 0.9,
                'source_passage_id': 'passage_001'
            }
        ),
        RetrievedItem(
            item_id="triple_002",
            item_type="triple",
            text="vitamin C tốt cho sức khỏe",
            bm25_score=0.6,
            embedding_score=0.7,
            hybrid_score=0.65,
            metadata={
                'subject': 'vitamin C',
                'predicate': 'tốt cho',
                'object': 'sức khỏe',
                'confidence': 0.8,
                'source_passage_id': 'passage_002'
            }
        ),
        RetrievedItem(
            item_id="triple_003",
            item_type="triple",
            text="táo có màu đỏ",
            bm25_score=0.3,
            embedding_score=0.2,
            hybrid_score=0.25,
            metadata={
                'subject': 'táo',
                'predicate': 'có màu',
                'object': 'đỏ',
                'confidence': 0.7,
                'source_passage_id': 'passage_003'
            }
        )
    ]
    
    test_query = "Lợi ích của táo cho sức khỏe là gì?"
    
    print(f"📝 Test query: '{test_query}'")
    print(f"📊 Mock triples: {len(mock_triples)}")
    
    try:
        # Test với different strategies
        strategies = ["lenient", "moderate", "strict"]
        
        for strategy in strategies:
            print(f"\n🎯 Testing với strategy: {strategy}")
            print("-" * 30)
            
            result = quick_filter_triples(test_query, mock_triples, strategy)
            
            print(f"   📊 Kết quả: {result.original_count} → {result.filtered_count} triples")
            print(f"   ⏱️ Thời gian: {result.filtering_time:.2f}s")
            print(f"   📈 Efficiency: {result.get_filtering_efficiency():.2%}")
            
            # Show top filtered triples
            for i, triple in enumerate(result.filtered_triples[:2], 1):
                print(f"   {i}. {triple.get_summary()}")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.exception("Chi tiết lỗi test:")

def test_individual_components():
    """Test các components riêng lẻ"""
    print("\n🧪 TEST INDIVIDUAL COMPONENTS")
    print("=" * 50)
    
    # Test RelevanceLevel enum
    print("📊 Test RelevanceLevel enum:")
    for level in RelevanceLevel:
        min_score, max_score = level.get_score_range()
        description = level.get_description()
        print(f"   {level.value}: [{min_score}-{max_score}] - {description}")
    
    # Test FilteringStrategy enum
    print("\n🎯 Test FilteringStrategy enum:")
    for strategy in FilteringStrategy:
        threshold = strategy.get_threshold()
        print(f"   {strategy.value}: threshold = {threshold}")
    
    # Test TripleFilterConfig
    print("\n⚙️ Test TripleFilterConfig:")
    config = create_default_config()
    print(f"   Primary LLM: {config.primary_llm.value}")
    print(f"   Backup LLM: {config.backup_llm.value}")
    print(f"   Strategy: {config.filtering_strategy.value}")
    print(f"   Threshold: {config.relevance_threshold}")
    print(f"   Batch size: {config.max_triples_per_batch}")

if __name__ == "__main__":
    print("🚀 BẮT ĐẦU CHẠY TẤT CẢ TESTS CHO MODULE 2")
    print("=" * 60)
    
    # Test 1: Individual components
    test_individual_components()
    
    print("\n" + "=" * 60)
    
    # Test 2: Mock data filtering (không cần real LLM)
    print("⚠️ LƯU Ý: Test tiếp theo sẽ tạo mock results thay vì gọi real LLM")
    test_triple_filter_with_mock_data()
    
    print("\n🎉 HOÀN THÀNH TẤT CẢ TESTS CHO MODULE 2!")
    print("=" * 60)
