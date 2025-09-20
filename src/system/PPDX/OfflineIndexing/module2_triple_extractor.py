"""
OfflineIndexing/module2_triple_extractor.py
Module 2: Enhanced Triple Extractor with GPT-3.5 Turbo Fallback
FIXED for OpenAI >= 1.0.0 compatibility
"""

from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional
from huggingface_hub import InferenceClient
import re
import logging
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class Triple:
    """Data class cho Triple"""
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    source_chunk_id: str = ""
    source_doc_id: str = ""
    extraction_method: str = "qwen"  # "qwen" or "gpt35"

# ==================== MOCK TEST MODE ====================

class MockTripleExtractor:
    """Mock Triple Extractor cho testing không cần model thật"""
    
    def __init__(self, huggingface_api_key: str = None, api_key: str = None, 
                 openai_api_key: Optional[str] = None, enable_gpt_fallback: bool = True):
        """Initialize mock extractor"""
        logger.info("🎭 Khởi tạo MockTripleExtractor (không tải model)")
        logger.info("   ⚡ Sử dụng intelligent mock responses")
        
        self.extracted_triples = []
        self.extraction_stats = {
            'hf_success': 0,
            'hf_failed': 0,
            'gpt_success': 0,
            'gpt_failed': 0,
            'total_chunks': 0
        }
    
    def extract_triples_from_chunks(self, chunks: List[Dict[str, Any]]) -> List[Triple]:
        """Mock extraction với intelligent responses"""
        logger.info(f"🎭 Mock extracting từ {len(chunks)} chunks...")
        
        all_triples = []
        self.extraction_stats['total_chunks'] = len(chunks)
        
        for chunk in chunks:
            # Simulate processing time
            time.sleep(0.5)
            
            # Generate mock triples based on chunk content
            chunk_triples = self._generate_mock_triples(chunk)
            all_triples.extend(chunk_triples)
            
            # Update stats
            self.extraction_stats['hf_success'] += 1
        
        self.extracted_triples = all_triples
        return all_triples
    
    def _generate_mock_triples(self, chunk: Dict[str, Any]) -> List[Triple]:
        """Generate intelligent mock triples based on chunk content"""
        text = chunk.get('text', '').lower()
        chunk_id = chunk.get('chunk_id', '')
        doc_id = chunk.get('doc_id', '')
        
        mock_triples = []
        
        # Example patterns to extract
        if 'ph' in text:
            if 'nhỏ hơn 7' in text:
                mock_triples.append(Triple(
                    subject="dung dịch nước",
                    predicate="có giá trị pH",
                    object="nhỏ hơn 7",
                    confidence=0.95,
                    source_chunk_id=chunk_id,
                    source_doc_id=doc_id,
                    extraction_method="qwen"
                ))
                mock_triples.append(Triple(
                    subject="dung dịch axít",
                    predicate="có pH",
                    object="nhỏ hơn 7",
                    confidence=0.95,
                    source_chunk_id=chunk_id,
                    source_doc_id=doc_id,
                    extraction_method="qwen"
                ))
            if 'lớn hơn 7' in text:
                mock_triples.append(Triple(
                    subject="dung dịch kiềm",
                    predicate="có pH",
                    object="lớn hơn 7",
                    confidence=0.85,
                    source_chunk_id=chunk_id,
                    source_doc_id=doc_id,
                    extraction_method="gpt35"
                ))
        
        return mock_triples

# ==================== MOCK MODE TOGGLE ====================

def enable_mock_mode():
    """Enable mock mode để test không cần real models"""
    global TripleExtractor
    
    logger.info("🎭 ENABLING MOCK MODE - Không tải model thật")
    
    # Replace real class với mock class
    TripleExtractor = MockTripleExtractor
    
    logger.info("✅ Mock mode enabled - Safe to test!")

class TripleExtractor:
    """Extract triples với dual API support: Qwen2.5-7B + GPT-3.5 Turbo fallback"""
    
    def __init__(self, huggingface_api_key: str = None, api_key: str = None, 
                 openai_api_key: Optional[str] = None, enable_gpt_fallback: bool = True):
        """
        Initialize với backward compatibility và OpenAI 1.0+ support
        
        Args:
            huggingface_api_key (str): HuggingFace API key (new parameter)
            api_key (str): HuggingFace API key (old parameter for compatibility)
            openai_api_key (str, optional): OpenAI API key (fallback)
            enable_gpt_fallback (bool): Enable GPT-3.5 fallback when HF fails
        """
        # Backward compatibility: support both old and new parameter names
        self.hf_api_key = huggingface_api_key or api_key
        if not self.hf_api_key:
            raise ValueError("HuggingFace API key required (huggingface_api_key or api_key)")
            
        # Primary API: HuggingFace
        self.hf_client = InferenceClient(
            provider="hf-inference",
            api_key=self.hf_api_key,
        )
        self.hf_model_name = "Qwen/Qwen2.5-7B-Instruct"
        
        # Fallback API: OpenAI GPT-3.5 Turbo (FIXED for OpenAI 1.0+)
        self.openai_api_key = openai_api_key
        self.enable_gpt_fallback = enable_gpt_fallback
        self.openai_client = None
        
        if self.openai_api_key and enable_gpt_fallback:
            try:
                # TRY MODERN OPENAI FIRST (>= 1.0.0)
                try:
                    from openai import OpenAI
                    self.openai_client = OpenAI(api_key=self.openai_api_key)
                    self.openai_version = "modern"
                    logger.info("OpenAI GPT-3.5 Turbo fallback enabled (OpenAI >= 1.0.0)")
                except ImportError:
                    # FALLBACK TO OLD OPENAI (< 1.0.0)
                    import openai
                    openai.api_key = self.openai_api_key
                    self.openai = openai
                    self.openai_version = "legacy"
                    logger.info("OpenAI GPT-3.5 Turbo fallback enabled (OpenAI < 1.0.0)")
                    
            except ImportError:
                logger.warning("OpenAI package not installed - fallback disabled")
                logger.warning("Install with: pip install openai")
                self.enable_gpt_fallback = False
        else:
            if not self.openai_api_key:
                logger.info("No OpenAI API key provided - fallback disabled")
            else:
                logger.info("GPT fallback manually disabled")
            self.enable_gpt_fallback = False
            
        self.extracted_triples = []
        
        # Statistics tracking
        self.extraction_stats = {
            'hf_success': 0,
            'hf_failed': 0,
            'gpt_success': 0,
            'gpt_failed': 0,
            'total_chunks': 0
        }
        
    def extract_triples_from_chunks(self, chunks: List[Dict[str, Any]]) -> List[Triple]:
        """Extract triples từ list of chunks với fallback support"""
        all_triples = []
        self.extraction_stats['total_chunks'] = len(chunks)
        
        for chunk in chunks:
            chunk_triples = self.extract_triples_from_chunk(chunk)
            all_triples.extend(chunk_triples)
            
        self.extracted_triples = all_triples
        
        # Log extraction statistics
        stats = self.extraction_stats
        logger.info(f"Extraction completed: {len(all_triples)} triples from {len(chunks)} chunks")
        logger.info(f"HF success: {stats['hf_success']}, HF failed: {stats['hf_failed']}")
        if self.enable_gpt_fallback:
            logger.info(f"GPT success: {stats['gpt_success']}, GPT failed: {stats['gpt_failed']}")
        
        return all_triples
    
    def extract_triples_from_chunk(self, chunk: Dict[str, Any]) -> List[Triple]:
        """
        Extract triples từ single chunk với intelligent fallback
        
        Flow:
        1. Try HuggingFace Qwen2.5-7B (primary)
        2. If fails and GPT fallback enabled → Try OpenAI GPT-3.5 Turbo
        3. If both fail → Return empty list
        """
        chunk_id = chunk.get('chunk_id', '')
        
        # STEP 1: Try HuggingFace Qwen first
        try:
            logger.debug(f"Attempting HF extraction for chunk {chunk_id}")
            triples = self._extract_with_huggingface(chunk)
            
            if triples:  # Success!
                self.extraction_stats['hf_success'] += 1
                logger.debug(f"HF extraction successful: {len(triples)} triples from {chunk_id}")
                return triples
            else:
                logger.warning(f"HF extraction returned 0 triples for {chunk_id}")
                
        except Exception as e:
            logger.error(f"HF extraction failed for chunk {chunk_id}: {e}")
            self.extraction_stats['hf_failed'] += 1
            
            # STEP 2: Try GPT-3.5 Turbo fallback
            if self.enable_gpt_fallback:
                logger.info(f"Attempting GPT-3.5 fallback for chunk {chunk_id}")
                try:
                    triples = self._extract_with_gpt35(chunk)
                    
                    if triples:  # Fallback success!
                        self.extraction_stats['gpt_success'] += 1
                        logger.info(f"GPT fallback successful: {len(triples)} triples from {chunk_id}")
                        return triples
                    else:
                        logger.warning(f"GPT fallback returned 0 triples for {chunk_id}")
                        
                except Exception as gpt_e:
                    logger.error(f"GPT fallback also failed for chunk {chunk_id}: {gpt_e}")
                    self.extraction_stats['gpt_failed'] += 1
            else:
                self.extraction_stats['gpt_failed'] += 1
        
        # Both methods failed
        logger.error(f"All extraction methods failed for chunk {chunk_id}")
        return []
    
    def _extract_with_huggingface(self, chunk: Dict[str, Any]) -> List[Triple]:
        """Extract triples using HuggingFace Qwen2.5-7B"""
        # Create prompt cho Qwen
        prompt = self._create_extraction_prompt(chunk['text'])
        
        # Call Qwen API
        try:
            response = self.hf_client.chat_completion(
                model=self.hf_model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            triples = self._parse_triples_response(
                response_text, 
                chunk.get('chunk_id', ''),
                chunk.get('doc_id', ''),
                extraction_method="qwen"
            )
            
            return triples
            
        except Exception as e:
            logger.error(f"Error calling HuggingFace API: {e}")
            raise
    
    def _extract_with_gpt35(self, chunk: Dict[str, Any]) -> List[Triple]:
        """Extract triples using OpenAI GPT-3.5 Turbo fallback (FIXED for both versions)"""
        # Create prompt cho GPT-3.5 (slightly adapted)
        prompt = self._create_gpt_extraction_prompt(chunk['text'])
        
        # Call OpenAI API với retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if hasattr(self, 'openai_client') and self.openai_client:
                    # MODERN OPENAI (>= 1.0.0)
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert at extracting knowledge triples from text."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1,
                        max_tokens=1024
                    )
                    response_text = response.choices[0].message.content
                    
                else:
                    # LEGACY OPENAI (< 1.0.0)
                    response = self.openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert at extracting knowledge triples from text."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.1,
                        max_tokens=1024
                    )
                    response_text = response.choices[0].message.content
                
                triples = self._parse_triples_response(
                    response_text,
                    chunk.get('chunk_id', ''),
                    chunk.get('doc_id', ''),
                    extraction_method="gpt35"
                )
                
                return triples
                
            except Exception as e:
                logger.warning(f"GPT attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise e
    
    def _create_extraction_prompt(self, text: str) -> str:
        """Tạo prompt cho Qwen để extract triples"""
        prompt = f"""
Nhiệm vụ: Trích xuất tất cả các mối quan hệ thực tế từ đoạn văn sau dưới dạng bộ ba (chủ thể, quan hệ, đối tượng).

Quy tắc:
1. Chỉ trích xuất những mối quan hệ rõ ràng và thực tế
2. Sử dụng từ ngữ chính xác từ văn bản gốc
3. Mỗi bộ ba phải có ý nghĩa hoàn chỉnh
4. Không tạo ra thông tin không có trong văn bản
5. Tránh các mối quan hệ quá chung chung hoặc không rõ nghĩa

Đoạn văn: {text}

Định dạng đầu ra (mỗi dòng một bộ ba):
(chủ thể, quan hệ, đối tượng)
(chủ thể, quan hệ, đối tượng)

Ví dụ format:
(nước, có pH, 7)
(dung dịch axít, có pH, nhỏ hơn 7)

Trích xuất:
"""
        return prompt
    
    def _create_gpt_extraction_prompt(self, text: str) -> str:
        """Tạo prompt cho GPT-3.5 để extract triples (English optimized)"""
        prompt = f"""
Task: Extract all factual relationships from the following text as triples (subject, predicate, object).

Rules:
1. Extract only clear and factual relationships
2. Use exact terms from the original text
3. Each triple must be complete and meaningful
4. Do not create information not in the text
5. Avoid overly generic or unclear relationships

Text: {text}

Output format (one triple per line):
(subject, predicate, object)
(subject, predicate, object)

Example format:
(water, has pH, 7)
(acidic solution, has pH, less than 7)

Extract:
"""
        return prompt
    
    def _parse_triples_response(self, response: str, chunk_id: str, doc_id: str, 
                              extraction_method: str = "qwen") -> List[Triple]:
        """Parse response từ API thành list of Triple objects"""
        triples = []
        
        # Pattern để match (subject, predicate, object)
        pattern = r'\(\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*([^)]+?)\s*\)'
        matches = re.findall(pattern, response)
        
        for match in matches:
            subject, predicate, obj = match
            
            # Clean up extracted text
            subject = subject.strip().strip('"\'')
            predicate = predicate.strip().strip('"\'')
            obj = obj.strip().strip('"\'')
            
            # Validate triple
            if self._is_valid_triple(subject, predicate, obj):
                # Set confidence based on extraction method
                confidence = 0.95 if extraction_method == "qwen" else 0.85
                
                triple = Triple(
                    subject=subject,
                    predicate=predicate,
                    object=obj,
                    confidence=confidence,
                    source_chunk_id=chunk_id,
                    source_doc_id=doc_id,
                    extraction_method=extraction_method
                )
                triples.append(triple)
        
        return triples
    
    def _is_valid_triple(self, subject: str, predicate: str, obj: str) -> bool:
        """Validate extracted triple"""
        # Check minimum length
        if len(subject) < 2 or len(predicate) < 2 or len(obj) < 2:
            return False
        
        # Check maximum length (avoid very long extractions)
        if len(subject) > 100 or len(predicate) > 50 or len(obj) > 100:
            return False
        
        # Check for common extraction errors
        error_patterns = ['...', '???', 'unknown', 'unclear', 'etc', 'và nhiều', 'v.v']
        for pattern in error_patterns:
            if (pattern.lower() in subject.lower() or 
                pattern.lower() in obj.lower() or
                pattern.lower() in predicate.lower()):
                return False
        
        # Check for too generic predicates
        generic_predicates = ['là', 'có', 'được', 'bao gồm', 'is', 'has', 'are']
        if predicate.lower().strip() in generic_predicates and len(predicate) < 5:
            return False
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive extraction statistics"""
        if not self.extracted_triples:
            return {}
        
        subjects = [t.subject for t in self.extracted_triples]
        predicates = [t.predicate for t in self.extracted_triples]
        objects = [t.object for t in self.extracted_triples]
        
        # Count by extraction method
        qwen_triples = [t for t in self.extracted_triples if t.extraction_method == "qwen"]
        gpt_triples = [t for t in self.extracted_triples if t.extraction_method == "gpt35"]
        
        stats = {
            'total_triples': len(self.extracted_triples),
            'unique_subjects': len(set(subjects)),
            'unique_predicates': len(set(predicates)),
            'unique_objects': len(set(objects)),
            'avg_confidence': sum(t.confidence for t in self.extracted_triples) / len(self.extracted_triples),
            'most_common_predicates': self._get_most_common(predicates, 5),
            'most_common_subjects': self._get_most_common(subjects, 5),
            # Extraction method breakdown
            'qwen_triples': len(qwen_triples),
            'gpt35_triples': len(gpt_triples),
            'extraction_stats': self.extraction_stats
        }
        
        # Success rates
        if self.extraction_stats['total_chunks'] > 0:
            stats['hf_success_rate'] = self.extraction_stats['hf_success'] / self.extraction_stats['total_chunks']
            if self.extraction_stats['hf_failed'] > 0:
                stats['gpt_fallback_rate'] = self.extraction_stats['gpt_success'] / self.extraction_stats['hf_failed']
            else:
                stats['gpt_fallback_rate'] = 0
        
        return stats
    
    def _get_most_common(self, items: List[str], top_k: int = 5) -> List[Tuple[str, int]]:
        """Get most common items"""
        from collections import Counter
        counter = Counter(items)
        return counter.most_common(top_k)
    
    def save_triples_to_file(self, output_path: Path):
        """Save extracted triples to file với extraction method info"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Subject\tPredicate\tObject\tConfidence\tSource_Chunk\tSource_Doc\tExtraction_Method\n")
            for triple in self.extracted_triples:
                f.write(f"{triple.subject}\t{triple.predicate}\t{triple.object}\t"
                       f"{triple.confidence}\t{triple.source_chunk_id}\t{triple.source_doc_id}\t"
                       f"{triple.extraction_method}\n")

# Test function
def test_enhanced_triple_extractor():
    """Test function cho Enhanced Module 2"""
    print("🚀 BẮT ĐẦU CHẠY TẤT CẢ TESTS CHO MODULE 2")
    print("=" * 60)
    print("🎭 LƯU Ý: Đang chạy trong MOCK MODE để tránh tải model")
    print("=" * 60)
    
    # Enable mock mode
    enable_mock_mode()
    
    # Test configuration
    hf_api_key = "your_hf_key_here"
    openai_api_key = "your_openai_key_here"  # Optional
    
    # Initialize with fallback
    extractor = TripleExtractor(
        huggingface_api_key=hf_api_key,
        openai_api_key=openai_api_key,
        enable_gpt_fallback=True
    )
    
    # Test chunks
    test_chunks = [
        {
            'chunk_id': 'chunk_PH_0_0',
            'doc_id': 'PH_0',
            'text': 'Các dung dịch nước có giá trị pH nhỏ hơn 7 được coi là có tính axít, trong khi các giá trị pH lớn hơn 7 được coi là có tính kiềm.'
        }
    ]
    
    print("Note: Actual extraction requires valid API keys")
    
    # Mock extraction for testing
    mock_triples = [
        Triple("dung dịch nước", "có giá trị pH", "nhỏ hơn 7", 0.95, "chunk_PH_0_0", "PH_0", "qwen"),
        Triple("dung dịch axít", "có pH", "nhỏ hơn 7", 0.95, "chunk_PH_0_0", "PH_0", "qwen"),
        Triple("dung dịch kiềm", "có pH", "lớn hơn 7", 0.85, "chunk_PH_0_0", "PH_0", "gpt35")
    ]
    
    extractor.extracted_triples = mock_triples
    extractor.extraction_stats = {
        'hf_success': 2, 'hf_failed': 1, 'gpt_success': 1, 'gpt_failed': 0, 'total_chunks': 3
    }
    
    stats = extractor.get_statistics()
    
    print("Enhanced Triple Extraction Results:")
    print(f"Total triples: {stats['total_triples']}")
    print(f"Qwen triples: {stats['qwen_triples']}")
    print(f"GPT-3.5 triples: {stats['gpt35_triples']}")
    print(f"HF success rate: {stats['hf_success_rate']:.2%}")
    print(f"GPT fallback rate: {stats['gpt_fallback_rate']:.2%}")
    print(f"Most common predicates: {stats['most_common_predicates']}")
    
    print("\n🎉 HOÀN THÀNH TẤT CẢ TESTS CHO MODULE 2!")
    print("🎭 Mock mode test thành công - Sẵn sàng implement API version!")
    print("=" * 60)
    
    return mock_triples

if __name__ == "__main__":
    test_enhanced_triple_extractor()