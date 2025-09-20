# docs_implement2.3_Claude_.md: 1. Ko còn nhiều time và các lần thử Cursor, Manus thất bại quá -> mình đã chạy Claude Opus rồi nhưng tạm bỏ -> qua genspark trước vì tỉ lệ thành công ở nó siêu cao. 

```python
"""
Module 1: Dual Retrieval (Truy xuất Kép)
Implements hybrid retrieval using both sparse (BM25) and dense (embedding) methods
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging
import time
import numpy as np
from dataclasses import dataclass
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import json

logger = logging.getLogger(__name__)

@dataclass
class RetrievalResult:
    """
    Container for dual retrieval results.
    
    Attributes:
        raw_passages: Retrieved passages with metadata
        raw_triples: Retrieved triples with metadata
        retrieval_time: Time taken for retrieval
        method_scores: Scores from different retrieval methods
    """
    raw_passages: List[Dict[str, Any]]
    raw_triples: List[Dict[str, Any]]
    retrieval_time: float
    method_scores: Dict[str, Any]
    
    def get_top_passages(self, n: int) -> List[Dict[str, Any]]:
        """Get top N passages by hybrid score."""
        return sorted(self.raw_passages, 
                     key=lambda x: x.get('hybrid_score', 0), 
                     reverse=True)[:n]
    
    def get_top_triples(self, n: int) -> List[Dict[str, Any]]:
        """Get top N triples by score."""
        return sorted(self.raw_triples, 
                     key=lambda x: x.get('score', 0), 
                     reverse=True)[:n]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'raw_passages': self.raw_passages,
            'raw_triples': self.raw_triples,
            'retrieval_time': self.retrieval_time,
            'method_scores': self.method_scores,
            'passage_count': len(self.raw_passages),
            'triple_count': len(self.raw_triples)
        }

class DualRetriever:
    """
    Hybrid retrieval system combining BM25 and embedding-based methods.
    """
    
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                 alpha: float = 0.5):
        """
        Initialize dual retriever.
        
        Args:
            neo4j_uri: Neo4j database URI
            neo4j_user: Database username
            neo4j_password: Database password
            embedding_model_name: Name of sentence transformer model
            alpha: Weight for BM25 vs embedding scores (0-1)
        """
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.alpha = alpha
        
        # Initialize BM25 components
        self.bm25_passages = None
        self.bm25_triples = None
        self.passage_corpus = []
        self.triple_corpus = []
        
        # Cache for embeddings
        self.passage_embeddings = None
        self.triple_embeddings = None
        
        # Performance tracking
        self.retrieval_stats = {
            'total_queries': 0,
            'avg_retrieval_time': 0,
            'bm25_time': 0,
            'embedding_time': 0
        }
        
        logger.info(f"Initialized DualRetriever with model: {embedding_model_name}")
        
    def initialize_indices(self):
        """Initialize BM25 and embedding indices from Neo4j data."""
        start_time = time.time()
        
        with self.neo4j_driver.session() as session:
            # Load passages
            passages_query = """
            MATCH (p:Passage)
            RETURN p.id as id, p.text as text, p.title as title, 
                   p.embedding as embedding
            """
            passages = session.run(passages_query).data()
            
            # Load triples
            triples_query = """
            MATCH (s:Phrase)-[r:RELATION]->(o:Phrase)
            RETURN s.text as subject, r.type as predicate, o.text as object,
                   s.id as subject_id, o.id as object_id, r.id as relation_id
            """
            triples = session.run(triples_query).data()
        
        # Build passage corpus
        self.passage_corpus = []
        self.passage_metadata = []
        passage_texts = []
        
        for p in passages:
            text = f"{p.get('title', '')} {p['text']}"
            self.passage_corpus.append(text.lower().split())
            self.passage_metadata.append({
                'id': p['id'],
                'text': p['text'],
                'title': p.get('title', ''),
                'embedding': p.get('embedding')
            })
            passage_texts.append(text)
        
        # Build triple corpus
        self.triple_corpus = []
        self.triple_metadata = []
        triple_texts = []
        
        for t in triples:
            text = f"{t['subject']} {t['predicate']} {t['object']}"
            self.triple_corpus.append(text.lower().split())
            self.triple_metadata.append({
                'subject': t['subject'],
                'predicate': t['predicate'],
                'object': t['object'],
                'subject_id': t['subject_id'],
                'object_id': t['object_id'],
                'relation_id': t['relation_id']
            })
            triple_texts.append(text)
        
        # Initialize BM25
        self.bm25_passages = BM25Okapi(self.passage_corpus)
        self.bm25_triples = BM25Okapi(self.triple_corpus)
        
        # Generate embeddings if not stored
        if not passages[0].get('embedding'):
            logger.info("Generating passage embeddings...")
            self.passage_embeddings = self.embedding_model.encode(
                passage_texts, 
                convert_to_tensor=True,
                show_progress_bar=True
            )
        else:
            # Load from stored embeddings
            self.passage_embeddings = np.array([p['embedding'] for p in passages])
        
        # Generate triple embeddings
        logger.info("Generating triple embeddings...")
        self.triple_embeddings = self.embedding_model.encode(
            triple_texts,
            convert_to_tensor=True,
            show_progress_bar=True
        )
        
        init_time = time.time() - start_time
        logger.info(f"Initialized indices in {init_time:.2f}s")
        logger.info(f"Loaded {len(self.passage_corpus)} passages and {len(self.triple_corpus)} triples")
        
    def retrieve(self, query: str, top_k: int = 20, top_n: int = 50) -> RetrievalResult:
        """
        Perform dual retrieval for passages and triples.
        
        Args:
            query: User query
            top_k: Number of passages to retrieve
            top_n: Number of triples to retrieve
            
        Returns:
            RetrievalResult containing passages and triples
        """
        start_time = time.time()
        self.retrieval_stats['total_queries'] += 1
        
        # Tokenize query for BM25
        query_tokens = query.lower().split()
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(
            query, 
            convert_to_tensor=True
        )
        
        # Retrieve passages
        passages = self._retrieve_passages(query_tokens, query_embedding, top_k)
        
        # Retrieve triples
        triples = self._retrieve_triples(query_tokens, query_embedding, top_n)
        
        retrieval_time = time.time() - start_time
        
        # Update stats
        self.retrieval_stats['avg_retrieval_time'] = (
            (self.retrieval_stats['avg_retrieval_time'] * 
             (self.retrieval_stats['total_queries'] - 1) + retrieval_time) / 
            self.retrieval_stats['total_queries']
        )
        
        method_scores = {
            'bm25_passage_scores': [p['bm25_score'] for p in passages],
            'embedding_passage_scores': [p['embedding_score'] for p in passages],
            'bm25_triple_scores': [t['bm25_score'] for t in triples],
            'embedding_triple_scores': [t['embedding_score'] for t in triples]
        }
        
        return RetrievalResult(
            raw_passages=passages,
            raw_triples=triples,
            retrieval_time=retrieval_time,
            method_scores=method_scores
        )
    
    def _retrieve_passages(self, query_tokens: List[str], 
                          query_embedding: np.ndarray, 
                          top_k: int) -> List[Dict[str, Any]]:
        """Retrieve passages using hybrid approach."""
        # BM25 retrieval
        bm25_start = time.time()
        bm25_scores = self.bm25_passages.get_scores(query_tokens)
        self.retrieval_stats['bm25_time'] += time.time() - bm25_start
        
        # Embedding similarity
        emb_start = time.time()
        embedding_scores = np.dot(self.passage_embeddings, query_embedding)
        self.retrieval_stats['embedding_time'] += time.time() - emb_start
        
        # Normalize scores
        bm25_scores_norm = self._normalize_scores(bm25_scores)
        embedding_scores_norm = self._normalize_scores(embedding_scores)
        
        # Hybrid scores
        hybrid_scores = (self.alpha * bm25_scores_norm + 
                        (1 - self.alpha) * embedding_scores_norm)
        
        # Get top-k indices
        top_indices = np.argsort(hybrid_scores)[::-1][:top_k]
        
        # Build result list
        passages = []
        for idx in top_indices:
            passage = self.passage_metadata[idx].copy()
            passage['bm25_score'] = float(bm25_scores[idx])
            passage['embedding_score'] = float(embedding_scores[idx])
            passage['hybrid_score'] = float(hybrid_scores[idx])
            passage['rank'] = len(passages) + 1
            passages.append(passage)
        
        return passages
    
    def _retrieve_triples(self, query_tokens: List[str], 
                         query_embedding: np.ndarray, 
                         top_n: int) -> List[Dict[str, Any]]:
        """Retrieve triples using hybrid approach."""
        # BM25 retrieval
        bm25_scores = self.bm25_triples.get_scores(query_tokens)
        
        # Embedding similarity
        embedding_scores = np.dot(self.triple_embeddings, query_embedding)
        
        # Normalize scores
        bm25_scores_norm = self._normalize_scores(bm25_scores)
        embedding_scores_norm = self._normalize_scores(embedding_scores)
        
        # Hybrid scores
        hybrid_scores = (self.alpha * bm25_scores_norm + 
                        (1 - self.alpha) * embedding_scores_norm)
        
        # Get top-n indices
        top_indices = np.argsort(hybrid_scores)[::-1][:top_n]
        
        # Build result list
        triples = []
        for idx in top_indices:
            triple = self.triple_metadata[idx].copy()
            triple['bm25_score'] = float(bm25_scores[idx])
            triple['embedding_score'] = float(embedding_scores[idx])
            triple['score'] = float(hybrid_scores[idx])
            triple['rank'] = len(triples) + 1
            triples.append(triple)
        
        return triples
    
    def _normalize_scores(self, scores: np.ndarray) -> np.ndarray:
        """Normalize scores to [0, 1] range."""
        if scores.max() == scores.min():
            return np.zeros_like(scores)
        return (scores - scores.min()) / (scores.max() - scores.min())
    
    def batch_retrieve(self, queries: List[str], top_k: int = 20, 
                      top_n: int = 50) -> List[RetrievalResult]:
        """Batch retrieval for multiple queries."""
        results = []
        for query in queries:
            results.append(self.retrieve(query, top_k, top_n))
        return results
    
    def get_retrieval_statistics(self) -> Dict[str, Any]:
        """Get retrieval performance statistics."""
        return {
            'total_queries': self.retrieval_stats['total_queries'],
            'avg_retrieval_time': self.retrieval_stats['avg_retrieval_time'],
            'avg_bm25_time': self.retrieval_stats['bm25_time'] / max(1, self.retrieval_stats['total_queries']),
            'avg_embedding_time': self.retrieval_stats['embedding_time'] / max(1, self.retrieval_stats['total_queries']),
            'corpus_size': {
                'passages': len(self.passage_corpus),
                'triples': len(self.triple_corpus)
            },
            'alpha_parameter': self.alpha
        }
    
    def close(self):
        """Close database connection."""
        self.neo4j_driver.close()
        logger.info("Closed Neo4j connection")
```

## 2. 

```python 
"""
Module 2: LLM-based Triple Filtering (Lọc Triple bằng LLM)
Sử dụng Large Language Models để lọc và chọn triples liên quan nhất
Hỗ trợ Qwen2.5-7B với GPT-3.5-Turbo backup
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import time
import json
import re
from dataclasses import dataclass
import openai
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)

@dataclass
class FilteredTripleResult:
    """
    Container cho kết quả filtered triple với metadata.
    """
    filtered_triples: List[Dict]
    original_count: int
    filtered_count: int
    filtering_time: float
    llm_model_used: str
    backup_used: bool = False
    
    def get_top_triples(self, n: int) -> List[Dict]:
        """Lấy top N filtered triples theo điểm liên quan."""
        return sorted(self.filtered_triples, 
                     key=lambda x: x.get('llm_relevance_score', 0), 
                     reverse=True)[:n]
    
    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi sang định dạng dictionary."""
        return {
            'filtered_triples': self.filtered_triples,
            'original_count': self.original_count,
            'filtered_count': self.filtered_count,
            'filtering_time': self.filtering_time,
            'llm_model_used': self.llm_model_used,
            'backup_used': self.backup_used,
            'filter_ratio': self.filtered_count / max(1, self.original_count)
        }
    
    def save_to_file(self, filepath: Path):
        """Lưu kết quả vào file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

class TripleFilter:
    """
    Hệ thống lọc triple dựa trên LLM để chọn các fact liên quan nhất cho query.
    """
    
    def __init__(self, primary_model: str = "Qwen/Qwen2.5-7B-Instruct", 
                 backup_model: str = "gpt-3.5-turbo",
                 primary_provider: str = "huggingface",
                 backup_provider: str = "openai",
                 hf_token: Optional[str] = None,
                 openai_api_key: Optional[str] = None):
        """
        Khởi tạo TripleFilter với cấu hình LLM primary và backup.
        """
        self.primary_model = primary_model
        self.backup_model = backup_model
        self.use_backup_on_failure = True
        
        # Initialize HuggingFace client
        self.hf_client = InferenceClient(
            model=primary_model,
            token=hf_token
        )
        
        # Initialize OpenAI client
        if openai_api_key:
            openai.api_key = openai_api_key
        
        # Filtering parameters
        self.max_triples_to_filter = 100  # Limit for API calls
        self.temperature = 0.3  # Lower temperature for consistent filtering
        
        # Statistics tracking
        self.filter_stats = {
            'total_queries': 0,
            'hf_success': 0,
            'hf_failures': 0,
            'gpt_success': 0,
            'gpt_failures': 0,
            'avg_filter_time': 0
        }
        
        logger.info(f"Initialized TripleFilter with primary: {primary_model}, backup: {backup_model}")
    
    def filter_triples(self, query: str, raw_triples: List[Dict[str, Any]], 
                      target_count: int = 15) -> FilteredTripleResult:
        """
        Lọc raw triples sử dụng LLM để chọn các fact liên quan nhất.
        """
        start_time = time.time()
        self.filter_stats['total_queries'] += 1
        
        # Limit triples if too many
        if len(raw_triples) > self.max_triples_to_filter:
            # Take top triples by score
            raw_triples = sorted(raw_triples, 
                               key=lambda x: x.get('score', 0), 
                               reverse=True)[:self.max_triples_to_filter]
        
        # Try primary LLM first
        filtered_result = self._filter_with_primary_llm(query, raw_triples, target_count)
        
        # Fallback to backup if needed
        if filtered_result is None and self.use_backup_on_failure:
            logger.warning("Primary LLM failed, falling back to GPT-3.5")
            filtered_result = self._filter_with_backup_llm(query, raw_triples, target_count)
            model_used = self.backup_model
            backup_used = True
        else:
            model_used = self.primary_model
            backup_used = False
        
        # If both failed, return top triples by original score
        if filtered_result is None:
            logger.error("Both LLMs failed, returning top triples by score")
            filtered_result = raw_triples[:target_count]
            for i, triple in enumerate(filtered_result):
                triple['llm_relevance_score'] = 1.0 - (i / target_count)
                triple['llm_reasoning'] = "Fallback: selected by retrieval score"
                triple['filter_rank'] = i + 1
            model_used = "fallback"
            backup_used = False
        
        filtering_time = time.time() - start_time
        
        # Update statistics
        self.filter_stats['avg_filter_time'] = (
            (self.filter_stats['avg_filter_time'] * 
             (self.filter_stats['total_queries'] - 1) + filtering_time) / 
            self.filter_stats['total_queries']
        )
        
        return FilteredTripleResult(
            filtered_triples=filtered_result,
            original_count=len(raw_triples),
            filtered_count=len(filtered_result),
            filtering_time=filtering_time,
            llm_model_used=model_used,
            backup_used=backup_used
        )
    
    def _filter_with_primary_llm(self, query: str, raw_triples: List[Dict], 
                                target_count: int) -> Optional[List[Dict[str, Any]]]:
        """Thử lọc với Qwen2.5-7B trước."""
        try:
            prompt = self._prepare_filter_prompt(query, raw_triples, target_count, "qwen")
            
            response = self.hf_client.text_generation(
                prompt=prompt,
                temperature=self.temperature,
                max_new_tokens=1500,
                return_full_text=False
            )
            
            filtered_triples = self._parse_llm_response(response, raw_triples, "qwen2.5")
            self.filter_stats['hf_success'] += 1
            
            return filtered_triples
            
        except Exception as e:
            logger.error(f"HuggingFace API error: {str(e)}")
            self.filter_stats['hf_failures'] += 1
            return None
    
    def _filter_with_backup_llm(self, query: str, raw_triples: List[Dict], 
                               target_count: int) -> List[Dict[str, Any]]:
        """Fallback sang GPT-3.5-Turbo khi Qwen fail."""
        try:
            prompt = self._prepare_filter_prompt(query, raw_triples, target_count, "gpt")
            
            response = openai.ChatCompletion.create(
                model=self.backup_model,
                messages=[
                    {"role": "system", "content": "You are an expert at identifying relevant facts for answering questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=1500
            )
            
            response_text = response.choices[0].message.content
            filtered_triples = self._parse_llm_response(response_text, raw_triples, "gpt-3.5")
            self.filter_stats['gpt_success'] += 1
            
            return filtered_triples
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            self.filter_stats['gpt_failures'] += 1
            return None
    
    def _prepare_filter_prompt(self, query: str, raw_triples: List[Dict], 
                              target_count: int, model_type: str = "qwen") -> str:
        """Chuẩn bị prompt cho LLM triple filtering."""
        # Format triples for prompt
        triple_list = []
        for i, triple in enumerate(raw_triples):
            triple_str = f"{i+1}. ({triple['subject']}, {triple['predicate']}, {triple['object']})"
            triple_list.append(triple_str)
        
        triples_text = "\n".join(triple_list)
        
        prompt = f"""Given the following query and list of facts (triples), select the {target_count} most relevant facts that would help answer the query.

Query: {query}

Facts:
{triples_text}

Instructions:
1. Select exactly {target_count} facts that are most relevant to answering the query
2. For each selected fact, provide:
   - The fact number (1-{len(raw_triples)})
   - A relevance score (0.0-1.0)
   - A brief explanation of why it's relevant

Format your response as:
SELECTED_FACTS:
[number]: [score] - [reason]
[number]: [score] - [reason]
...

Be concise and focus on direct relevance to the query."""
        
        return prompt
    
    def _parse_llm_response(self, llm_response: str, 
                           original_triples: List[Dict],
                           model_used: str) -> List[Dict[str, Any]]:
        """Parse response từ LLM và map về original triple objects."""
        filtered_triples = []
        
        # Extract selected facts section
        if "SELECTED_FACTS:" in llm_response:
            facts_section = llm_response.split("SELECTED_FACTS:")[1].strip()
        else:
            facts_section = llm_response
        
        # Parse each line
        lines = facts_section.strip().split('\n')
        rank = 1
        
        for line in lines:
            # Pattern: [number]: [score] - [reason]
            match = re.match(r'(\d+):\s*([\d.]+)\s*-\s*(.+)', line.strip())
            if match:
                idx = int(match.group(1)) - 1  # Convert to 0-based index
                score = float(match.group(2))
                reason = match.group(3).strip()
                
                if 0 <= idx < len(original_triples):
                    triple = original_triples[idx].copy()
                    triple['llm_relevance_score'] = score
                    triple['llm_reasoning'] = reason
                    triple['filter_rank'] = rank
                    triple['llm_model_used'] = model_used
                    filtered_triples.append(triple)
                    rank += 1
        
        # If parsing failed, try simpler pattern
        if not filtered_triples:
            for line in lines:
                match = re.match(r'(\d+)', line.strip())
                if match:
                    idx = int(match.group(1)) - 1
                    if 0 <= idx < len(original_triples):
                        triple = original_triples[idx].copy()
                        triple['llm_relevance_score'] = 1.0 - (len(filtered_triples) * 0.05)
                        triple['llm_reasoning'] = "Selected by LLM"
                        triple['filter_rank'] = len(filtered_triples) + 1
                        triple['llm_model_used'] = model_used
                        filtered_triples.append(triple)
        
        return filtered_triples
    
    def batch_filter_triples(self, queries: List[str], 
                           raw_triples_list: List[List[Dict]], 
                           target_count: int = 15) -> List[FilteredTripleResult]:
        """Lọc triples cho nhiều queries trong batch để tăng hiệu quả."""
        results = []
        for query, raw_triples in zip(queries, raw_triples_list):
            result = self.filter_triples(query, raw_triples, target_count)
            results.append(result)
        return results
    
    def get_filtering_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về quá trình filtering."""
        total = self.filter_stats['total_queries']
        if total == 0:
            return self.filter_stats
        
        return {
            'total_queries': total,
            'hf_success_rate': self.filter_stats['hf_success'] / total,
            'hf_failure_rate': self.filter_stats['hf_failures'] / total,
            'gpt_success_rate': self.filter_stats['gpt_success'] / total,
            'gpt_failure_rate': self.filter_stats['gpt_failures'] / total,
            'avg_filter_time': self.filter_stats['avg_filter_time'],
            'primary_model': self.primary_model,
            'backup_model': self.backup_model
        }
```

# 3. 
```python 
"""
Module 3: Triple-based Passage Ranking (Xếp hạng Passage dựa trên Triple)
Xếp hạng lại passages dựa trên mức độ hỗ trợ cho filtered triples
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging
import time
import numpy as np
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

logger = logging.getLogger(__name__)

@dataclass
class RankedPassageResult:
    """
    Container cho kết quả xếp hạng passage.
    """
    ranked_passages: List[Dict]
    ranking_method: str
    alpha_used: float
    ranking_time: float
    triple_coverage: float  # Percentage of triples covered by top passages
    
    def get_top_passages(self, n: int) -> List[Dict]:
        """Lấy top N passages đã xếp hạng."""
        return self.ranked_passages[:n]
    
    def get_ranking_summary(self) -> Dict[str, Any]:
        """Lấy tóm tắt kết quả xếp hạng."""
        return {
            'total_passages': len(self.ranked_passages),
            'ranking_method': self.ranking_method,
            'alpha_parameter': self.alpha_used,
            'ranking_time': self.ranking_time,
            'triple_coverage': self.triple_coverage,
            'avg_support_score': np.mean([p['triple_support_score'] 
                                         for p in self.ranked_passages])
        }
    
    def save_to_file(self, filepath: Path):
        """Lưu kết quả xếp hạng vào file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                'ranked_passages': self.ranked_passages,
                'summary': self.get_ranking_summary()
            }, f, ensure_ascii=False, indent=2)

class PassageRanker:
    """
    Hệ thống xếp hạng passage sử dụng filtered triples để đánh giá lại retrieved passages.
    """
    
    def __init__(self, alpha: float = 0.7, 
                 embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"):
        """
        Khởi tạo PassageRanker với trọng số kết hợp điểm.
        
        Args:
            alpha (float): Trọng số cho điểm retrieval gốc vs hỗ trợ triple
                         alpha=1.0: Chỉ điểm retrieval
                         alpha=0.0: Chỉ điểm hỗ trợ triple
                         alpha=0.7: Cân bằng (khuyến nghị)
            embedding_model_name: Model for semantic similarity
        """
        self.alpha = alpha
        self.embedding_model = SentenceTransformer(embedding_model_name)
        
        # Statistics tracking
        self.ranking_stats = {
            'total_rankings': 0,
            'avg_ranking_time': 0,
            'avg_triple_coverage': 0
        }
        
        logger.info(f"Initialized PassageRanker with alpha={alpha}")
    
    def rank_passages(self, raw_passages: List[Dict[str, Any]], 
                     filtered_triples: List[Dict[str, Any]], 
                     top_p: int = 10) -> RankedPassageResult:
        """
        Xếp hạng lại passages dựa trên mức độ hỗ trợ cho filtered triples.
        """
        start_time = time.time()
        self.ranking_stats['total_rankings'] += 1
        
        # Calculate triple support for each passage
        passage_scores = []
        for passage in raw_passages:
            support_result = self.calculate_passage_triple_support(passage, filtered_triples)
            
            # Combine scores
            original_score = passage.get('hybrid_score', 0.5)
            triple_support_score = support_result['total_support_score']
            final_score = self.alpha * original_score + (1 - self.alpha) * triple_support_score
            
            # Create scored passage
            scored_passage = passage.copy()
            scored_passage.update({
                'triple_support_score': triple_support_score,
                'original_hybrid_retrieval_score': original_score,
                'final_ranking_score': final_score,
                'supported_triples': support_result['supported_triples'],
                'support_details': support_result['support_breakdown']
            })
            passage_scores.append(scored_passage)
        
        # Sort by final score
        ranked_passages = sorted(passage_scores, 
                               key=lambda x: x['final_ranking_score'], 
                               reverse=True)[:top_p]
        
        # Add new ranks
        for i, passage in enumerate(ranked_passages):
            passage['new_rank'] = i + 1
            passage['rank_change'] = passage.get('rank', i+1) - (i + 1)
        
        # Calculate triple coverage in top passages
        covered_triples = set()
        for passage in ranked_passages:
            covered_triples.update(passage['supported_triples'])
        triple_coverage = len(covered_triples) / max(1, len(filtered_triples))
        
        ranking_time = time.time() - start_time
        
        # Update statistics
        self.ranking_stats['avg_ranking_time'] = (
            (self.ranking_stats['avg_ranking_time'] * 
             (self.ranking_stats['total_rankings'] - 1) + ranking_time) / 
            self.ranking_stats['total_rankings']
        )
        self.ranking_stats['avg_triple_coverage'] = (
            (self.ranking_stats['avg_triple_coverage'] * 
             (self.ranking_stats['total_rankings'] - 1) + triple_coverage) / 
            self.ranking_stats['total_rankings']
        )
        
        return RankedPassageResult(
            ranked_passages=ranked_passages,
            ranking_method="triple_support_hybrid",
            alpha_used=self.alpha,
            ranking_time=ranking_time,
            triple_coverage=triple_coverage
        )
    
    def calculate_passage_triple_support(self, passage: Dict[str, Any], 
                                       filtered_triples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Tính toán mức độ hỗ trợ tốt của một passage cho tập filtered triples.
        """
        passage_text = passage.get('text', '')
        passage_title = passage.get('title', '')
        full_text = f"{passage_title} {passage_text}".lower()
        
        # Generate passage embedding once
        passage_embedding = self.embedding_model.encode(full_text)
        
        supported_triples = []
        support_breakdown = []
        total_score = 0
        
        for triple in filtered_triples:
            # Calculate relevance using multiple methods
            relevance_score = self._calculate_triple_passage_relevance(
                triple, passage, passage_embedding
            )
            
            # Consider LLM-assigned relevance score if available
            llm_score = triple.get('llm_relevance_score', 1.0)
            weighted_score = relevance_score * llm_score
            
            if relevance_score > 0.3:  # Threshold for considering support
                supported_triples.append(triple.get('relation_id', str(triple)))
                support_breakdown.append({
                    'triple': f"{triple['subject']} - {triple['predicate']} - {triple['object']}",
                    'relevance_score': relevance_score,
                    'weighted_score': weighted_score
                })
                total_score += weighted_score
        
        # Normalize total score
        if filtered_triples:
            # Consider both coverage and strength
            coverage_ratio = len(supported_triples) / len(filtered_triples)
            avg_support_strength = total_score / max(1, len(supported_triples))
            total_support_score = 0.6 * coverage_ratio + 0.4 * avg_support_strength
        else:
            total_support_score = 0
        
        return {
            'total_support_score': min(1.0, total_support_score),
            'supported_triples': supported_triples,
            'support_breakdown': support_breakdown,
            'coverage_ratio': coverage_ratio if filtered_triples else 0
        }
    
    def _calculate_triple_passage_relevance(self, triple: Dict[str, Any], 
                                          passage: Dict[str, Any],
                                          passage_embedding: np.ndarray) -> float:
        """
        Tính điểm liên quan giữa một triple và passage đơn lẻ.
        Sử dụng nhiều phương pháp: co-occurrence, embedding similarity, v.v.
        """
        passage_text = passage.get('text', '').lower()
        passage_title = passage.get('title', '').lower()
        full_text = f"{passage_title} {passage_text}"
        
        # Method 1: Direct term matching
        subject = triple['subject'].lower()
        predicate = triple['predicate'].lower()
        object_term = triple['object'].lower()
        
        term_score = 0
        if subject in full_text:
            term_score += 0.4
        if object_term in full_text:
            term_score += 0.4
        if predicate in full_text:
            term_score += 0.2
        
        # Method 2: Semantic similarity
        triple_text = f"{triple['subject']} {triple['predicate']} {triple['object']}"
        triple_embedding = self.embedding_model.encode(triple_text)
        
        semantic_score = cosine_similarity(
            [passage_embedding], 
            [triple_embedding]
        )[0][0]
        
        # Method 3: Context window matching
        # Check if subject and object appear near each other
        context_score = 0
        if subject in full_text and object_term in full_text:
            subject_pos = full_text.find(subject)
            object_pos = full_text.find(object_term)
            distance = abs(subject_pos - object_pos)
            
            # Closer terms get higher scores
            if distance < 100:  # Within ~15 words
                context_score = 0.8
            elif distance < 200:  # Within ~30 words
                context_score = 0.5
            elif distance < 400:  # Within ~60 words
                context_score = 0.3
        
        # Combine scores with weights
        final_score = (
            0.3 * term_score +
            0.5 * semantic_score +
            0.2 * context_score
        )
        
        return final_score
    
    def batch_rank_passages(self, passage_lists: List[List[Dict]], 
                          triple_lists: List[List[Dict]], 
                          top_p: int = 10) -> List[RankedPassageResult]:
        """Xếp hạng passages cho nhiều queries trong batch."""
        results = []
        for passages, triples in zip(passage_lists, triple_lists):
            result = self.rank_passages(passages, triples, top_p)
            results.append(result)
        return results
    
    def get_ranking_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về quá trình ranking."""
        return {
            'total_rankings': self.ranking_stats['total_rankings'],
            'avg_ranking_time': self.ranking_stats['avg_ranking_time'],
            'avg_triple_coverage': self.ranking_stats['avg_triple_coverage'],
            'alpha_parameter': self.alpha,
            'ranking_method': 'triple_support_hybrid'
        }

```