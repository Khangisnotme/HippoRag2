"""
src/system/PPDX/OnlineRetrievalAndQA/module5_answer_generator.py
Module 5: Answer Generator
Generates answers using LLM based on retrieved passages and filtered triples
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
import time
import json
import os
import logging
import hashlib
import re
import requests
from pathlib import Path
from enum import Enum
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import datetime

# Load environment variables from .env file
load_dotenv()

# Import dependencies
from module1_dual_retrieval import RetrievedItem
from module2_triple_filter import FilteredTriple
from module3_passage_ranker import RankedPassage
from module4_context_expander import ExpandedContext
from utils.utils_shared_general import setup_logger

# Create log directory if it doesn't exist
log_dir = Path("outputs/log")
log_dir.mkdir(parents=True, exist_ok=True)

# Setup logger with file output
log_file = log_dir / f"module5_answer_generator_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logger = setup_logger(__name__, log_file=log_file)

class LLMProvider(Enum):
    """Supported LLM providers"""
    QWEN = "qwen2.5-7b-instruct"
    GPT3_5 = "gpt-3.5-turbo"
    HUGGINGFACE_API = "huggingface-api"

class AnswerQualityLevel(Enum):
    """Answer quality levels"""
    EXCELLENT = "excellent"      # Score 0.8-1.0
    GOOD = "good"               # Score 0.6-0.8
    FAIR = "fair"               # Score 0.4-0.6
    POOR = "poor"               # Score 0.0-0.4

@dataclass
class AnswerGeneratorConfig:
    """Configuration for answer generation"""
    # LLM configuration - CHANGED: Default to GPT-3.5-Turbo
    primary_llm: LLMProvider = LLMProvider.GPT3_5  # CHANGED: Primary is now GPT-3.5
    backup_llm: LLMProvider = LLMProvider.QWEN     # CHANGED: Backup is now Qwen
    
    # Generation parameters
    temperature: float = 0.01
    max_tokens: int = 1000
    top_p: float = 0.9
    
    # Quality thresholds
    min_quality_score: float = 0.4
    min_confidence_score: float = 0.6
    
    # Performance settings
    enable_caching: bool = True
    max_retries: int = 3
    timeout_seconds: int = 60
    
    # API credentials
    huggingface_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    def __post_init__(self):
        """Load API keys from environment variables"""
        if self.huggingface_api_key is None:
            self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        if self.openai_api_key is None:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        logger.info("🔑 Loaded API keys from environment")
        logger.info(f"   📊 HuggingFace API: {'✅ Available' if self.huggingface_api_key else '❌ Not available'}")
        logger.info(f"   🤖 OpenAI API: {'✅ Available' if self.openai_api_key else '❌ Not available'}")

@dataclass
class AnswerResult:
    """Container for generated answer with comprehensive metadata"""
    ai_answer: str
    query: str
    quality_score: float
    quality_level: AnswerQualityLevel
    confidence_score: float
    supporting_passages: List[str]
    supporting_triples: List[str]
    generation_time: float
    llm_provider: str
    generation_metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        result = asdict(self)
        result['quality_level'] = self.quality_level.value
        return result
    
    def is_acceptable(self, min_quality: float = 0.4) -> bool:
        """Check if answer meets minimum quality threshold"""
        return self.quality_score >= min_quality
    
    def get_summary(self) -> str:
        """Generate summary of answer result"""
        return (f"Answer: {self.ai_answer[:100]}... | "
                f"Quality: {self.quality_score:.3f} ({self.quality_level.value}) | "
                f"Confidence: {self.confidence_score:.3f}")

class QwenAnswerGenerator:
    """Answer generation using Qwen LLM via Together AI"""
    
    def __init__(self, config: AnswerGeneratorConfig):
        self.config = config
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Qwen model"""
        try:
            if not self.config.huggingface_api_key:
                raise ValueError("HuggingFace API key not provided")
            
            self.client = InferenceClient(
                provider="together",
                api_key=self.config.huggingface_api_key
            )
            logger.info("🤖 Initialized Qwen model for answer generation")
            logger.info(f"   📊 Model configuration: temperature={self.config.temperature}, max_tokens={self.config.max_tokens}, top_p={self.config.top_p}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Qwen model: {str(e)}")
            raise
    
    def generate_answer(self, query: str, 
                       ranked_passages: List[RankedPassage],
                       filtered_triples: List[FilteredTriple],
                       expanded_context: Optional[ExpandedContext] = None) -> Dict[str, Any]:
        """Generate answer using Qwen"""
        try:
            # Create prompt
            prompt = self._create_generation_prompt(query, ranked_passages, 
                                                 filtered_triples, expanded_context)
            
            # Generate answer
            start_time = time.time()
            response = self._call_qwen_model(prompt)
            generation_time = time.time() - start_time
            
            # Process response
            ai_answer = self._extract_answer_from_response(response)
            
            # Score answer
            quality_score = self._score_answer_quality(ai_answer, query)
            confidence_score = self._calculate_confidence(ai_answer, 
                                                       ranked_passages, 
                                                       filtered_triples)
            
            return {
                'ai_answer': ai_answer,
                'quality_score': quality_score,
                'confidence_score': confidence_score,
                'generation_time': generation_time,
                'llm_provider': self.config.backup_llm.value,  # CHANGED: Now backup
                'generation_metadata': {
                    'prompt': prompt,
                    'prompt_tokens': len(prompt.split()),
                    'response_tokens': len(ai_answer.split()),
                    'model_used': self.config.backup_llm.value,  # CHANGED: Now backup
                    'api_call_successful': True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating answer with Qwen: {str(e)}")
            raise
    
    def _create_generation_prompt(self, query: str,
                                ranked_passages: List[RankedPassage],
                                filtered_triples: List[FilteredTriple],
                                expanded_context: Optional[ExpandedContext]) -> str:
        """Create prompt for Qwen model"""
        # Header và hướng dẫn tổng quát
        prompt = f"""Dựa trên thông tin sau, hãy suy nghĩ chi tiết bên trong (think step by step) nhưng chỉ xuất phần Answer ngắn gọn.

Câu hỏi: {query}

Đoạn văn liên quan:
"""
        # Thêm top 5 passages
        for i, p in enumerate(ranked_passages[:5], 1):
            prompt += f"Đoạn {i}: {p.original_text}\n"

        # Thêm tối đa 10 triples
        prompt += "\nCác thông tin quan trọng (triples):\n"
        for i, t in enumerate(filtered_triples[:10], 1):
            prompt += f"{i}. {t.subject} {t.predicate} {t.object}\n"

        # Thông tin mở rộng nếu có
        if expanded_context and hasattr(expanded_context, 'expanded_contexts'):
            prompt += "\nThông tin bổ sung:\n"
            for i, c in enumerate(expanded_context.expanded_contexts[:5], 1):
                prompt += f"{i}. {c.context_text}\n"

        # Ràng buộc output
        prompt += """

### Answer (chỉ ghi kết quả, không giải thích, tối đa 7 từ hoặc 1 con số (có thể kèm đơn vị))
"""
        return prompt
    
    def _call_qwen_model(self, prompt: str) -> str:
        """Call Qwen model via Together AI"""
        try:
            # Print prompt for debugging on console
            print("\n" + "="*80)
            print("🤖 PROMPT SENT TO QWEN MODEL:")
            print("="*80)
            print(prompt)
            print("="*80 + "\n")
            
            # Log prompt details to file
            logger.info("\n" + "="*80)
            logger.info("🤖 PROMPT SENT TO QWEN MODEL:")
            logger.info("="*80)
            logger.info(f"📝 Prompt length: {len(prompt)} characters")
            logger.info(f"📊 Prompt word count: {len(prompt.split())} words")
            logger.info("-"*40)
            logger.info("PROMPT CONTENT:")
            logger.info("-"*40)
            # Log each line of the prompt separately to make it more readable in log files
            for line in prompt.split('\n'):
                logger.info(line)
            logger.info("="*80 + "\n")
            
            start_time = time.time()
            completion = self.client.chat.completions.create(
                model="Qwen/Qwen2.5-7B-Instruct",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p
            )
            response_time = time.time() - start_time
            
            logger.info(f"⏱️ Qwen API response time: {response_time:.2f}s")
            logger.info(f"📝 Raw response length: {len(completion.choices[0].message.content)} characters")
            
            return completion.choices[0].message.content.strip()
                
        except Exception as e:
            logger.error(f"❌ Qwen API call failed: {str(e)}")
            raise
    
    def _extract_answer_from_response(self, response: str) -> str:
        """Extract answer from model response"""
        # Clean up the response
        answer = response.strip()
        
        # Remove any system prompts or artifacts
        if "Trả lời:" in answer:
            answer = answer.split("Trả lời:")[-1].strip()
        
        # Remove extra whitespace and clean up
        answer = re.sub(r'\s+', ' ', answer)
        answer = answer.strip()
        
        return answer if answer else "Không thể tạo câu trả lời từ thông tin đã cung cấp."
    
    def _score_answer_quality(self, answer: str, query: str) -> float:
        """Score answer quality based on various metrics"""
        score = 0.0
        
        # Length score (avoid too short or too long answers)
        answer_length = len(answer.split())
        if 10 <= answer_length <= 200:
            score += 0.3
            logger.info(f"📏 Length score: +0.3 (length: {answer_length} words)")
        elif 5 <= answer_length < 10 or 200 < answer_length <= 300:
            score += 0.2
            logger.info(f"📏 Length score: +0.2 (length: {answer_length} words)")
        elif answer_length < 5:
            score += 0.1
            logger.info(f"📏 Length score: +0.1 (length: {answer_length} words)")
        
        # Relevance score (simple keyword matching)
        query_words = set(query.lower().split())
        answer_words = set(answer.lower().split())
        overlap = len(query_words.intersection(answer_words))
        if len(query_words) > 0:
            relevance_ratio = overlap / len(query_words)
            score += relevance_ratio * 0.4
            logger.info(f"🎯 Relevance score: +{relevance_ratio * 0.4:.2f} (overlap: {overlap}/{len(query_words)} words)")
        
        # Structure score (check for complete sentences)
        if answer.endswith('.') or answer.endswith('?') or answer.endswith('!'):
            score += 0.1
            logger.info("📝 Structure score: +0.1 (complete sentence)")
        
        # Vietnamese text quality
        if any(char in answer for char in 'àáảãạăắằẳẵặâấầẩẫậêếềểễệîíìỉịôốồổỗộơớờởỡợûúùủũụưứừửữự'):
            score += 0.1
            logger.info("🇻🇳 Vietnamese text score: +0.1 (contains Vietnamese characters)")
        
        # Content quality (avoid generic responses)
        generic_phrases = ['không biết', 'không rõ', 'cần thêm thông tin']
        if not any(phrase in answer.lower() for phrase in generic_phrases):
            score += 0.1
            logger.info("✨ Content quality score: +0.1 (no generic phrases)")
        
        final_score = min(score, 1.0)
        logger.info(f"📊 Final quality score: {final_score:.2f}")
        return final_score
    
    def _calculate_confidence(self, answer: str,
                            ranked_passages: List[RankedPassage],
                            filtered_triples: List[FilteredTriple]) -> float:
        """Calculate confidence score based on supporting evidence"""
        confidence = 0.0
        
        # Base confidence from passage support
        if ranked_passages:
            avg_passage_score = sum(p.final_score for p in ranked_passages[:3]) / min(3, len(ranked_passages))
            confidence += avg_passage_score * 0.4
            logger.info(f"📚 Passage support confidence: +{avg_passage_score * 0.4:.2f} (avg score: {avg_passage_score:.2f})")
        
        # Confidence from triple support
        if filtered_triples:
            avg_triple_relevance = sum(t.query_relevance_score for t in filtered_triples[:5]) / min(5, len(filtered_triples))
            confidence += avg_triple_relevance * 0.3
            logger.info(f"🔍 Triple support confidence: +{avg_triple_relevance * 0.3:.2f} (avg relevance: {avg_triple_relevance:.2f})")
        
        # Answer completeness
        answer_length = len(answer.split())
        if answer_length >= 20:
            confidence += 0.2
            logger.info("📝 Completeness confidence: +0.2 (length >= 20 words)")
        elif answer_length >= 10:
            confidence += 0.1
            logger.info("📝 Completeness confidence: +0.1 (length >= 10 words)")
        
        # Evidence consistency
        evidence_count = len(ranked_passages) + len(filtered_triples)
        if evidence_count >= 5:
            confidence += 0.1
            logger.info(f"🔗 Evidence consistency: +0.1 (total evidence: {evidence_count})")
        
        final_confidence = min(confidence, 1.0)
        logger.info(f"📊 Final confidence score: {final_confidence:.2f}")
        return final_confidence

class GPTAnswerGenerator:
    """Answer generation using GPT models via OpenAI API"""
    
    def __init__(self, config: AnswerGeneratorConfig):
        self.config = config
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client using requests"""
        try:
            if not self.config.openai_api_key:
                raise ValueError("OpenAI API key not provided")
            
            # Use requests instead of openai library
            self.api_key = self.config.openai_api_key
            self.base_url = "https://api.openai.com/v1/chat/completions"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            logger.info("🤖 Initialized OpenAI client for answer generation")
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
            raise
    
    def generate_answer(self, query: str,
                       ranked_passages: List[RankedPassage],
                       filtered_triples: List[FilteredTriple],
                       expanded_context: Optional[ExpandedContext] = None) -> Dict[str, Any]:
        """Generate answer using GPT"""
        try:
            # Create prompt
            prompt = self._create_generation_prompt(query, ranked_passages,
                                                 filtered_triples, expanded_context)
            
            # Generate answer
            start_time = time.time()
            response = self._call_gpt_model(prompt)
            generation_time = time.time() - start_time
            
            # Process response
            ai_answer = self._extract_answer_from_response(response)
            
            # Score answer using same logic as Qwen
            qwen_generator = QwenAnswerGenerator(self.config)
            quality_score = qwen_generator._score_answer_quality(ai_answer, query)
            confidence_score = qwen_generator._calculate_confidence(ai_answer,
                                                                 ranked_passages,
                                                                 filtered_triples)
            
            return {
                'ai_answer': ai_answer,
                'quality_score': quality_score,
                'confidence_score': confidence_score,
                'generation_time': generation_time,
                'llm_provider': self.config.primary_llm.value,  # CHANGED: Now primary
                'generation_metadata': {
                    'prompt': prompt,
                    'prompt_tokens': len(prompt.split()),
                    'response_tokens': len(ai_answer.split()),
                    'model_used': self.config.primary_llm.value,  # CHANGED: Now primary
                    'api_call_successful': True
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating answer with GPT: {str(e)}")
            raise
    
    def _create_generation_prompt(self, query: str,
                                ranked_passages: List[RankedPassage],
                                filtered_triples: List[FilteredTriple],
                                expanded_context: Optional[ExpandedContext]) -> str:
        """Create structured prompt for GPT answer generation"""
        prompt = f"""Dựa trên thông tin sau, hãy suy nghĩ chi tiết bên trong (think step by step) nhưng chỉ xuất phần Answer ngắn gọn.

Câu hỏi: {query}

Đoạn văn liên quan:
"""
        # Thêm top 5 passages
        for i, p in enumerate(ranked_passages[:5], 1):
            prompt += f"Đoạn {i}: {p.original_text}\n"

        # Thêm tối đa 10 triples
        prompt += "\nCác thông tin quan trọng (triples):\n"
        for i, t in enumerate(filtered_triples[:10], 1):
            prompt += f"{i}. {t.subject} {t.predicate} {t.object}\n"

        # Thông tin mở rộng nếu có
        if expanded_context and hasattr(expanded_context, 'expanded_contexts'):
            prompt += "\nThông tin bổ sung:\n"
            for i, c in enumerate(expanded_context.expanded_contexts[:5], 1):
                prompt += f"{i}. {c.context_text}\n"

        # Ràng buộc output
        prompt += """

### Answer (chỉ ghi kết quả, không giải thích, tối đa 7 từ hoặc 1 con số (có thể kèm đơn vị))
"""
        return prompt
    
    def _call_gpt_model(self, prompt: str) -> str:
        """Call GPT model via OpenAI API using requests"""
        try:
            # Print prompt for debugging
            print("\n" + "="*80)
            print("🤖 PROMPT SENT TO GPT MODEL:")
            print("="*80)
            print(prompt)
            print("="*80 + "\n")
            
            # Log prompt details to file
            logger.info("\n" + "="*80)
            logger.info("🤖 PROMPT SENT TO GPT MODEL:")
            logger.info("="*80)
            logger.info(f"📝 Prompt length: {len(prompt)} characters")
            logger.info(f"📊 Prompt word count: {len(prompt.split())} words")
            logger.info("-"*40)
            logger.info("PROMPT CONTENT:")
            logger.info("-"*40)
            # Log each line of the prompt separately to make it more readable in log files
            for line in prompt.split('\n'):
                logger.info(line)
            logger.info("="*80 + "\n")
            
            # Prepare payload
            payload = {
                "model": self.config.primary_llm.value,  # CHANGED: Now primary
                "messages": [
                    {"role": "system", "content": "You are a helpful AI assistant that provides accurate and detailed answers based on the given context."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                "top_p": self.config.top_p
            }
            
            # Make API call
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=self.config.timeout_seconds
            )
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
                
        except Exception as e:
            logger.error(f"❌ GPT API call failed: {str(e)}")
            raise
    
    def _extract_answer_from_response(self, response: str) -> str:
        """Extract answer from GPT response"""
        # Clean up the response
        answer = response.strip()
        
        # Remove any system artifacts
        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()
        
        # Clean up formatting
        answer = re.sub(r'\s+', ' ', answer)
        answer = answer.strip()
        
        return answer if answer else "Không thể tạo câu trả lời từ thông tin đã cung cấp."

class FallbackAnswerGenerator:
    """Fallback answer generator when APIs fail"""
    
    def __init__(self, config: AnswerGeneratorConfig):
        self.config = config
        self.logger = logging.getLogger(__name__ + ".FallbackAnswerGenerator")
        self.logger.info("✅ Fallback Answer Generator initialized")
    
    def generate_answer(self, query: str,
                       ranked_passages: List[RankedPassage],
                       filtered_triples: List[FilteredTriple],
                       expanded_context: Optional[ExpandedContext] = None) -> Dict[str, Any]:
        """Generate simple rule-based answer"""
        self.logger.info("🔄 Using fallback answer generation...")
        
        # Simple rule-based response based on query patterns
        answer = self._generate_rule_based_answer(query, ranked_passages, filtered_triples)
        
        # Basic scoring
        quality_score = 0.3  # Low quality for fallback
        confidence_score = 0.2  # Low confidence for fallback
        
        return {
            'ai_answer': answer,
            'quality_score': quality_score,
            'confidence_score': confidence_score,
            'generation_time': 0.1,  # Very fast
            'llm_provider': 'fallback_rule_based',
            'generation_metadata': {
                'prompt': f"Query: {query}",
                'prompt_tokens': len(query.split()),
                'response_tokens': len(answer.split()),
                'model_used': 'fallback_rule_based',
                'api_call_successful': True,
                'fallback_reason': 'API_failures'
            }
        }
    
    def _generate_rule_based_answer(self, query: str, 
                                  ranked_passages: List[RankedPassage],
                                  filtered_triples: List[FilteredTriple]) -> str:
        """Generate rule-based answer"""
        # Extract key information from passages and triples
        if not ranked_passages and not filtered_triples:
            return "Không có đủ thông tin để trả lời câu hỏi."
        
        # Simple pattern matching
        query_lower = query.lower()
        
        # Location queries
        if any(word in query_lower for word in ['nằm ở', 'ở đâu', 'vị trí', 'khu vực']):
            # Look for location information in triples
            for triple in filtered_triples:
                if any(loc_word in triple.predicate.lower() for loc_word in ['nằm', 'ở', 'thuộc']):
                    return f"{triple.subject} nằm ở {triple.object}."
        
        # What questions
        if query_lower.startswith('gì') or 'là gì' in query_lower:
            if ranked_passages:
                # Return first sentence from top passage
                first_passage = ranked_passages[0].original_text
                sentences = first_passage.split('.')
                if sentences:
                    return sentences[0].strip() + '.'
        
        # Default response
        if ranked_passages:
            return f"Dựa trên thông tin có sẵn: {ranked_passages[0].original_text[:100]}..."
        elif filtered_triples:
            first_triple = filtered_triples[0]
            return f"{first_triple.subject} {first_triple.predicate} {first_triple.object}."
        
        return "Không thể tạo câu trả lời từ thông tin đã cung cấp."

class AnswerGenerator:
    """Main answer generation orchestrator with fallback mechanism"""
    
    def __init__(self, config: Optional[AnswerGeneratorConfig] = None):
        self.config = config or AnswerGeneratorConfig()
        self._initialize_providers()
        self._initialize_cache()
    
    def _initialize_providers(self):
        """Initialize LLM providers"""
        self.providers = {}
        
        try:
            # Initialize primary provider (GPT-3.5)
            if self.config.primary_llm == LLMProvider.GPT3_5:
                self.providers['primary'] = GPTAnswerGenerator(self.config)
            elif self.config.primary_llm == LLMProvider.QWEN:
                self.providers['primary'] = QwenAnswerGenerator(self.config)
            
            logger.info(f"✅ Primary provider initialized: {self.config.primary_llm.value}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize primary provider: {str(e)}")
        
        try:
            # Initialize backup provider (Qwen)
            if self.config.backup_llm == LLMProvider.QWEN:
                self.providers['backup'] = QwenAnswerGenerator(self.config)
            elif self.config.backup_llm == LLMProvider.GPT3_5:
                self.providers['backup'] = GPTAnswerGenerator(self.config)
            
            logger.info(f"✅ Backup provider initialized: {self.config.backup_llm.value}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize backup provider: {str(e)}")
        
        # Always initialize fallback
        self.providers['fallback'] = FallbackAnswerGenerator(self.config)
        logger.info("✅ Fallback provider initialized")
        
        if not self.providers:
            raise RuntimeError("❌ No LLM providers could be initialized")
    
    def _initialize_cache(self):
        """Initialize answer cache"""
        self.cache = {}
        if self.config.enable_caching:
            logger.info("💾 Initialized answer cache")
    
    def generate_answer(self, query: str,
                       ranked_passages: List[RankedPassage],
                       filtered_triples: List[FilteredTriple],
                       expanded_context: Optional[ExpandedContext] = None) -> AnswerResult:
        """Generate answer with fallback mechanism"""
        try:
            logger.info(f"🎯 Starting answer generation for query: {query}")
            logger.info(f"📚 Input: {len(ranked_passages)} passages, {len(filtered_triples)} triples")
            
            # Check cache
            cache_key = self._generate_cache_key(query, ranked_passages, filtered_triples)
            if self.config.enable_caching and cache_key in self.cache:
                logger.info(f"💾 Cache hit! Retrieved answer for key: {cache_key[:50]}...")
                return self.cache[cache_key]
            else:
                logger.info("🔍 Cache miss - proceeding with generation")
            
            # Try providers in order: primary -> backup -> fallback
            result = None
            provider_used = None
            
            # Try primary provider first
            if 'primary' in self.providers:
                try:
                    logger.info(f"🚀 Attempting answer generation with primary provider: {self.config.primary_llm.value}")
                    result = self.providers['primary'].generate_answer(
                        query, ranked_passages, filtered_triples, expanded_context)
                    provider_used = 'primary'
                    logger.info(f"✅ Primary provider succeeded")
                except Exception as e:
                    logger.warning(f"⚠️ Primary provider failed: {str(e)}")
            
            # Try backup provider if primary failed
            if result is None and 'backup' in self.providers:
                try:
                    logger.info(f"🔄 Attempting answer generation with backup provider: {self.config.backup_llm.value}")
                    result = self.providers['backup'].generate_answer(
                        query, ranked_passages, filtered_triples, expanded_context)
                    provider_used = 'backup'
                    logger.info(f"✅ Backup provider succeeded")
                except Exception as e:
                    logger.error(f"❌ Backup provider also failed: {str(e)}")
            
            # Try fallback if all else failed
            if result is None and 'fallback' in self.providers:
                try:
                    logger.info("🆘 Using fallback provider")
                    result = self.providers['fallback'].generate_answer(
                        query, ranked_passages, filtered_triples, expanded_context)
                    provider_used = 'fallback'
                    logger.info("✅ Fallback provider succeeded")
                except Exception as e:
                    logger.error(f"❌ Even fallback provider failed: {str(e)}")
            
            if result is None:
                raise RuntimeError("❌ All LLM providers failed to generate answer")
            
            # Create answer result
            answer_result = AnswerResult(
                ai_answer=result['ai_answer'],
                query=query,
                quality_score=result['quality_score'],
                quality_level=self._determine_quality_level(result['quality_score']),
                confidence_score=result['confidence_score'],
                supporting_passages=[p.passage_id for p in ranked_passages[:5]],
                supporting_triples=[t.triple_id for t in filtered_triples[:10]],
                generation_time=result['generation_time'],
                llm_provider=result['llm_provider'],
                generation_metadata={
                    **result['generation_metadata'],
                    'provider_used': provider_used,
                    'cache_hit': False,
                    'supporting_passages_count': len(ranked_passages),
                    'supporting_triples_count': len(filtered_triples)
                }
            )
            
            logger.info(f"📊 Answer generation metrics:")
            logger.info(f"   - Quality score: {answer_result.quality_score:.3f}")
            logger.info(f"   - Quality level: {answer_result.quality_level.value}")
            logger.info(f"   - Confidence score: {answer_result.confidence_score:.3f}")
            logger.info(f"   - Generation time: {answer_result.generation_time:.2f}s")
            logger.info(f"   - Provider used: {provider_used}")
            logger.info(f"   - Supporting passages: {len(answer_result.supporting_passages)}")
            logger.info(f"   - Supporting triples: {len(answer_result.supporting_triples)}")
            
            # Validate answer quality
            if not answer_result.is_acceptable(self.config.min_quality_score):
                logger.warning(f"⚠️ Generated answer quality ({answer_result.quality_score:.3f}) below threshold ({self.config.min_quality_score})")
            
            # Cache result
            if self.config.enable_caching:
                self.cache[cache_key] = answer_result
                logger.info(f"💾 Cached answer with key: {cache_key[:50]}...")
            
            logger.info(f"✅ Answer generated successfully - Quality: {answer_result.quality_score:.3f}, Confidence: {answer_result.confidence_score:.3f}")
            return answer_result
            
        except Exception as e:
            logger.error(f"❌ Error in answer generation: {str(e)}")
            raise
    
    def _determine_quality_level(self, quality_score: float) -> AnswerQualityLevel:
        """Determine quality level from score"""
        if quality_score >= 0.8:
            return AnswerQualityLevel.EXCELLENT
        elif quality_score >= 0.6:
            return AnswerQualityLevel.GOOD
        elif quality_score >= 0.4:
            return AnswerQualityLevel.FAIR
        else:
            return AnswerQualityLevel.POOR
    
    def _generate_cache_key(self, query: str,
                          ranked_passages: List[RankedPassage],
                          filtered_triples: List[FilteredTriple]) -> str:
        """Generate cache key using hash"""
        passage_ids = sorted([p.passage_id for p in ranked_passages[:5]])
        triple_ids = sorted([t.triple_id for t in filtered_triples[:10]])
        
        cache_input = f"{query}|{','.join(passage_ids)}|{','.join(triple_ids)}"
        cache_key = hashlib.md5(cache_input.encode()).hexdigest()
        
        return cache_key
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'cache_enabled': self.config.enable_caching,
            'cache_size': len(self.cache),
            'cache_keys': list(self.cache.keys()) if len(self.cache) < 10 else list(self.cache.keys())[:10]
        }
    
    def clear_cache(self):
        """Clear answer cache"""
        cache_size = len(self.cache)
        self.cache.clear()
        logger.info(f"🧹 Cleared cache: {cache_size} entries removed")
    
    def close(self):
        """Clean up resources"""
        self.clear_cache()
        logger.info("🧹 Cleaned up answer generation resources")

def create_default_config() -> AnswerGeneratorConfig:
    """Create default answer generation configuration with GPT-3.5 as primary"""
    return AnswerGeneratorConfig(
        primary_llm=LLMProvider.GPT3_5,  # CHANGED: GPT-3.5 as primary
        backup_llm=LLMProvider.QWEN,     # CHANGED: Qwen as backup
        temperature=0.01,
        max_tokens=1000,
        enable_caching=True
    )

def quick_generate_answer(query: str,
                         ranked_passages: List[RankedPassage],
                         filtered_triples: List[FilteredTriple],
                         expanded_context: Optional[ExpandedContext] = None) -> AnswerResult:
    """Quick answer generation with default settings"""
    generator = AnswerGenerator(create_default_config())
    try:
        result = generator.generate_answer(query, ranked_passages, 
                                         filtered_triples, expanded_context)
        return result
    finally:
        generator.close()

def test_answer_generation():
    """Test answer generation with mock data"""
    # Create mock data
    mock_passages = [
        RankedPassage(
            passage_id="p1",
            original_text="Táo là một loại trái cây rất tốt cho sức khỏe. Táo chứa nhiều vitamin C và chất xơ.",
            hybrid_retrieval_score=0.8,
            support_score=0.7,
            final_score=0.75,
            rank=1,
            supporting_triples_count=2,
            supporting_triples=["t1", "t2"],
            score_breakdown={'bm25': 0.6, 'embedding': 0.9},
            ranking_metadata={'method': 'hybrid'}
        )
    ]
    
    mock_triples = [
        FilteredTriple(
            triple_id="t1",
            subject="Táo",
            predicate="chứa",
            object="vitamin C",
            original_text="Táo chứa vitamin C",
            query_relevance_score=0.8,
            relevance_level="highly_relevant",
            confidence_score=0.9,
            llm_explanation="Relevant triple about apple nutrition",
            source_passage_id="p1",
            original_hybrid_retrieval_score=0.8,
            filtering_metadata={'filter_method': 'llm'}
        )
    ]
    
    # Test answer generation
    query = "Táo có những lợi ích gì cho sức khỏe?"
    
    try:
        result = quick_generate_answer(query, mock_passages, mock_triples)
        
        print("="*60)
        print("🧪 ANSWER GENERATION TEST RESULTS")
        print("="*60)
        print(f"Query: {query}")
        print(f"Generated Answer: {result.ai_answer}")
        print(f"Quality Score: {result.quality_score:.3f}")
        print(f"Quality Level: {result.quality_level.value}")
        print(f"Confidence Score: {result.confidence_score:.3f}")
        print(f"Generation Time: {result.generation_time:.2f}s")
        print(f"LLM Provider: {result.llm_provider}")
        print(f"Supporting Passages: {len(result.supporting_passages)}")
        print(f"Supporting Triples: {len(result.supporting_triples)}")
        print("="*60)
        
        # Test quality assessment
        if result.is_acceptable():
            print("✅ Answer quality is acceptable")
        else:
            print("❌ Answer quality below threshold")
            
        return result
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return None

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Starting Answer Generation Module Test...")
    test_answer_generation()
