"""
OnlineRetrievalAndQA/module1_dual_retrieval.py
Module 1: Dual/Hybrid Retrieval (Truy xuất Kép/Lai)
Triển khai tìm kiếm lai BM25 + Embedding cho passages và triples

Mô tả chi tiết:
    Module này thực hiện truy xuất kép kết hợp phương pháp từ khóa (BM25) và 
    phương pháp ngữ nghĩa (Embedding) để tìm kiếm passages và triples liên quan 
    nhất với query của người dùng.

Kiến trúc chính:
    - BM25Retriever: Tìm kiếm dựa trên từ khóa
    - EmbeddingRetriever: Tìm kiếm dựa trên ngữ nghĩa
    - HybridScorer: Kết hợp điểm số từ hai phương pháp
    - Neo4jDataAccess: Truy cập dữ liệu từ Knowledge Graph
    - DualRetriever: Orchestrator chính cho toàn bộ quá trình

Workflow:
    Query → BM25 Search + Embedding Search → Score Combination → Ranked Results
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging
import time
import uuid
from dataclasses import dataclass
import numpy as np
import datetime

# Neo4j connection
from neo4j import GraphDatabase

# Text processing và search
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Shared utilities
from utils.utils_shared_general import (
    setup_logger,
    log_performance,
    validate_query,
    clean_text,
    extract_keywords,
    merge_scores,
    save_json,
    PerformanceStats
)

# Setup logger with file output
log_file = Path("outputs/log/module1_dual_retrieval_{}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
logger = setup_logger(__name__, log_file=log_file)

# ==================== DATA CLASSES ====================

@dataclass
class RetrievalConfig:
    """
    Cấu hình cho hệ thống truy xuất kép
    
    Attributes:
        bm25_k1 (float): Tham số k1 cho BM25 (kiểm soát tần suất từ)
        bm25_b (float): Tham số b cho BM25 (kiểm soát độ dài văn bản)
        embedding_model (str): Tên model embedding để sử dụng
        embedding_device (str): Thiết bị tính toán (cpu/cuda)
        alpha_bm25 (float): Trọng số cho điểm BM25 (0.0-1.0)
        alpha_embedding (float): Trọng số cho điểm embedding (0.0-1.0)
        max_passages (int): Số lượng tối đa passages có thể xử lý
        max_triples (int): Số lượng tối đa triples có thể xử lý
        batch_size (int): Kích thước batch cho xử lý embedding
        timeout (int): Thời gian timeout cho các thao tác (giây)
    """
    # Tham số BM25
    bm25_k1: float = 1.2
    bm25_b: float = 0.75
    
    # Tham số Embedding
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    embedding_device: str = "cpu"
    
    # Kết hợp điểm số lai
    alpha_bm25: float = 0.3      # Trọng số cho điểm BM25
    alpha_embedding: float = 0.7  # Trọng số cho điểm embedding
    
    # Giới hạn truy xuất
    max_passages: int = 10   # Ban đầu để 100. Đây là con số tối đa của Passage Raw (sau khi đã Hybrid: BM25 và Embedding)
    max_triples: int = 10   # Ban đầu để 200. Đây là con số tối đa của Triples Raw (sau khi đã Hybrid: BM25 và Embedding)
    
    # Tối ưu hiệu suất
    batch_size: int = 32
    timeout: int = 60

@dataclass
class RetrievedItem:
    """
    Lớp dữ liệu đại diện cho một item đã được truy xuất
    
    Attributes:
        item_id (str): Định danh duy nhất của item
        item_type (str): Loại item ('passage' hoặc 'triple')
        text (str): Nội dung văn bản của item
        bm25_score (float): Điểm số BM25 (0.0-1.0)
        embedding_score (float): Điểm số embedding (0.0-1.0)
        hybrid_score (float): Điểm số kết hợp cuối cùng (0.0-1.0)
        metadata (Dict): Thông tin metadata bổ sung
    """
    item_id: str
    item_type: str  # 'passage' hoặc 'triple'
    text: str
    bm25_score: float
    embedding_score: float
    hybrid_score: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi object thành dictionary
        
        Returns:
            Dict[str, Any]: Dictionary representation của object
        """
        return {
            'item_id': self.item_id,
            'item_type': self.item_type,
            'text': self.text,
            'bm25_score': self.bm25_score,
            'embedding_score': self.embedding_score,
            'hybrid_score': self.hybrid_score,
            'metadata': self.metadata
        }

@dataclass
class RetrievalResult:
    """
    Container chứa kết quả truy xuất hoàn chỉnh
    
    Attributes:
        raw_passages (List[RetrievedItem]): Danh sách passages đã truy xuất
        raw_triples (List[RetrievedItem]): Danh sách triples đã truy xuất
        query (str): Truy vấn gốc của người dùng
        retrieval_time (float): Thời gian thực hiện truy xuất (giây)
        statistics (Dict): Thống kê chi tiết về quá trình truy xuất
    """
    raw_passages: List[RetrievedItem]
    raw_triples: List[RetrievedItem]
    query: str
    retrieval_time: float
    statistics: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi kết quả thành dictionary để lưu trữ
        
        Returns:
            Dict[str, Any]: Dictionary representation của kết quả
        """
        return {
            'raw_passages': [item.to_dict() for item in self.raw_passages],
            'raw_triples': [item.to_dict() for item in self.raw_triples],
            'query': self.query,
            'retrieval_time': self.retrieval_time,
            'statistics': self.statistics
        }
    
    def save_to_file(self, filepath: Path):
        """
        Lưu kết quả truy xuất vào file JSON
        
        Args:
            filepath (Path): Đường dẫn file để lưu
        """
        save_json(self.to_dict(), filepath)
        logger.info(f"✅ Đã lưu kết quả truy xuất vào file: {filepath}")

# ==================== BM25 RETRIEVER ====================

class BM25Retriever:
    """
    Hệ thống truy xuất dựa trên BM25 cho việc khớp từ khóa
    
    BM25 (Best Matching 25) là thuật toán xếp hạng tài liệu dựa trên
    tần suất từ khóa và độ dài tài liệu. Đây là phương pháp cổ điển
    nhưng hiệu quả cho tìm kiếm từ khóa chính xác.
    """
    
    def __init__(self, config: RetrievalConfig):
        """
        Khởi tạo BM25Retriever
        
        Args:
            config (RetrievalConfig): Cấu hình hệ thống truy xuất
        """
        self.config = config
        self.bm25_passages = None
        self.bm25_triples = None
        self.passage_corpus = []
        self.triple_corpus = []
        self.passage_metadata = []
        self.triple_metadata = []
        logger.info("🔤 Khởi tạo BM25Retriever thành công")
        
    def build_passage_index(self, passages: List[Dict[str, Any]]):
        """
        Xây dựng chỉ mục BM25 cho passages
        
        Quá trình này bao gồm:
        1. Làm sạch và tokenize văn bản
        2. Tạo corpus cho BM25
        3. Lưu trữ metadata
        4. Xây dựng chỉ mục BM25
        
        Args:
            passages (List[Dict]): Danh sách passage objects từ Neo4j
        """
        logger.info(f"🔍 Bắt đầu xây dựng chỉ mục BM25 cho {len(passages)} passages...")
        start_time = time.time()
        
        self.passage_corpus = []
        self.passage_metadata = []
        
        for i, passage in enumerate(passages, 1):
            # Trích xuất và làm sạch văn bản
            text = passage.get('text', '')
            cleaned_text = clean_text(text)
            
            # Tokenize cho BM25 (chia thành từ)
            tokens = cleaned_text.lower().split()
            self.passage_corpus.append(tokens)
            
            # Lưu trữ metadata
            metadata = {
                'passage_id': passage.get('id', ''),
                'title': passage.get('title', ''),
                'doc_id': passage.get('doc_id', ''),
                'original_text': text,
                'text_length': len(text),
                'token_count': len(tokens)
            }
            self.passage_metadata.append(metadata)
            
            if i % 100 == 0 or i == len(passages):
                logger.info(f"   📝 Đã xử lý {i}/{len(passages)} passages")
        
        # Xây dựng chỉ mục BM25
        if self.passage_corpus:
            logger.info("🔨 Đang xây dựng chỉ mục BM25 cho passages...")
            self.bm25_passages = BM25Okapi(
                self.passage_corpus,
                k1=self.config.bm25_k1,
                b=self.config.bm25_b
            )
            logger.info(f"✅ Hoàn thành xây dựng chỉ mục BM25 với k1={self.config.bm25_k1}, b={self.config.bm25_b}")
        
        end_time = time.time()
        log_performance("Xây dựng chỉ mục BM25 cho passages", start_time, end_time, 
                       {"passages": len(passages), "total_tokens": sum(len(tokens) for tokens in self.passage_corpus)})
    
    def build_triple_index(self, triples: List[Dict[str, Any]]):
        """
        Xây dựng chỉ mục BM25 cho triples
        
        Quá trình tương tự passages nhưng có cách tạo văn bản đặc biệt:
        - Kết hợp subject + predicate + object thành một chuỗi
        - Tạo representation có thể tìm kiếm được
        
        Args:
            triples (List[Dict]): Danh sách triple objects từ Neo4j
        """
        logger.info(f"🔗 Bắt đầu xây dựng chỉ mục BM25 cho {len(triples)} triples...")
        start_time = time.time()
        
        self.triple_corpus = []
        self.triple_metadata = []
        
        for i, triple in enumerate(triples, 1):
            # Tạo representation văn bản cho triple
            subject = triple.get('subject', '')
            predicate = triple.get('predicate', '')
            obj = triple.get('object', '')
            
            # Tạo văn bản có thể tìm kiếm
            triple_text = f"{subject} {predicate} {obj}"
            cleaned_text = clean_text(triple_text)
            
            # Tokenize cho BM25
            tokens = cleaned_text.lower().split()
            self.triple_corpus.append(tokens)
            
            # Lưu trữ metadata
            metadata = {
                'subject': subject,
                'predicate': predicate,
                'object': obj,
                'triple_text': triple_text,
                'source_passage_id': triple.get('source_passage_id', ''),
                'confidence': triple.get('confidence', 1.0),
                'token_count': len(tokens)
            }
            self.triple_metadata.append(metadata)
            
            if i % 500 == 0 or i == len(triples):
                logger.info(f"   🔗 Đã xử lý {i}/{len(triples)} triples")
        
        # Xây dựng chỉ mục BM25
        if self.triple_corpus:
            logger.info("🔨 Đang xây dựng chỉ mục BM25 cho triples...")
            self.bm25_triples = BM25Okapi(
                self.triple_corpus,
                k1=self.config.bm25_k1,
                b=self.config.bm25_b
            )
            logger.info(f"✅ Hoàn thành xây dựng chỉ mục BM25 cho triples")
        
        end_time = time.time()
        log_performance("Xây dựng chỉ mục BM25 cho triples", start_time, end_time, 
                       {"triples": len(triples), "total_tokens": sum(len(tokens) for tokens in self.triple_corpus)})
    
    def search_passages(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Tìm kiếm passages sử dụng BM25
        
        Args:
            query (str): Truy vấn tìm kiếm
            top_k (int): Số lượng kết quả hàng đầu
            
        Returns:
            List[Tuple[int, float]]: Danh sách (index, score) của kết quả
        """
        if not self.bm25_passages or not query:
            logger.warning("⚠️ Chỉ mục BM25 cho passages chưa được khởi tạo hoặc query rỗng")
            return []
        
        logger.info(f"🔍 Tìm kiếm BM25 passages với query: '{query[:50]}{'...' if len(query) > 50 else ''}'")
        
        # Tokenize query
        query_tokens = clean_text(query).lower().split()
        logger.info(f"📝 Query tokens: {query_tokens}")
        
        # Lấy điểm BM25
        scores = self.bm25_passages.get_scores(query_tokens)
        
        # Lấy top-k indices và scores
        top_indices = np.argsort(scores)[::-1][:top_k]
        top_scores = scores[top_indices]
        
        # Log kết quả
        non_zero_scores = [(idx, score) for idx, score in zip(top_indices, top_scores) if score > 0]
        logger.info(f"🎯 BM25 passages: tìm thấy {len(non_zero_scores)}/{top_k} kết quả có điểm > 0")
        
        return [(int(idx), float(score)) for idx, score in zip(top_indices, top_scores)]
    
    def search_triples(self, query: str, top_n: int = 10) -> List[Tuple[int, float]]:
        """
        Tìm kiếm triples sử dụng BM25
        
        Args:
            query (str): Truy vấn tìm kiếm
            top_n (int): Số lượng kết quả hàng đầu
            
        Returns:
            List[Tuple[int, float]]: Danh sách (index, score) của kết quả
        """
        if not self.bm25_triples or not query:
            logger.warning("⚠️ Chỉ mục BM25 cho triples chưa được khởi tạo hoặc query rỗng")
            return []
        
        logger.info(f"🔗 Tìm kiếm BM25 triples với query: '{query[:50]}{'...' if len(query) > 50 else ''}'")
        
        # Tokenize query
        query_tokens = clean_text(query).lower().split()
        
        # Lấy điểm BM25
        scores = self.bm25_triples.get_scores(query_tokens)
        
        # Lấy top-n indices và scores
        top_indices = np.argsort(scores)[::-1][:top_n]
        top_scores = scores[top_indices]
        
        # Log kết quả
        non_zero_scores = [(idx, score) for idx, score in zip(top_indices, top_scores) if score > 0]
        logger.info(f"🎯 BM25 triples: tìm thấy {len(non_zero_scores)}/{top_n} kết quả có điểm > 0")
        
        return [(int(idx), float(score)) for idx, score in zip(top_indices, top_scores)]

# ==================== EMBEDDING RETRIEVER ====================

class EmbeddingRetriever:
    """
    Hệ thống truy xuất dựa trên Embedding cho tương tự ngữ nghĩa
    
    Sử dụng sentence transformers để tạo vector representations
    của văn bản và tính toán cosine similarity cho việc tìm kiếm
    ngữ nghĩa.
    """
    
    def __init__(self, config: RetrievalConfig):
        """
        Khởi tạo EmbeddingRetriever
        
        Args:
            config (RetrievalConfig): Cấu hình hệ thống truy xuất
        """
        self.config = config
        self.model = None
        self.passage_embeddings = None
        self.triple_embeddings = None
        self.passage_texts = []
        self.triple_texts = []
        self.passage_metadata = []
        self.triple_metadata = []
        logger.info("🧠 Khởi tạo EmbeddingRetriever thành công")
        
    def load_model(self):
        """
        Tải model sentence transformer
        
        Chỉ tải một lần và sử dụng lại để tối ưu hiệu suất
        """
        if self.model is None:
            logger.info(f"📥 Đang tải model embedding: {self.config.embedding_model}")
            logger.info(f"🖥️ Sử dụng thiết bị: {self.config.embedding_device}")
            start_time = time.time()
            
            self.model = SentenceTransformer(
                self.config.embedding_model,
                device=self.config.embedding_device
            )
            
            end_time = time.time()
            log_performance("Tải model embedding", start_time, end_time)
            logger.info("✅ Model embedding đã sẵn sàng")
    
    def build_passage_embeddings(self, passages: List[Dict[str, Any]]):
        """
        Xây dựng embeddings cho passages
        
        Quá trình:
        1. Tải model nếu chưa có
        2. Chuẩn bị văn bản và metadata
        3. Tạo embeddings theo batch
        4. Lưu trữ kết quả
        
        Args:
            passages (List[Dict]): Danh sách passage objects
        """
        logger.info(f"🧠 Bắt đầu tạo embeddings cho {len(passages)} passages...")
        start_time = time.time()
        
        self.load_model()
        
        self.passage_texts = []
        self.passage_metadata = []
        
        for i, passage in enumerate(passages, 1):
            text = passage.get('text', '')
            self.passage_texts.append(text)
            
            # Lưu metadata (giống như BM25)
            metadata = {
                'passage_id': passage.get('id', ''),
                'title': passage.get('title', ''),
                'doc_id': passage.get('doc_id', ''),
                'original_text': text,
                'text_length': len(text)
            }
            self.passage_metadata.append(metadata)
            
            if i % 100 == 0 or i == len(passages):
                logger.info(f"   📝 Đã chuẩn bị {i}/{len(passages)} passages cho embedding")
        
        # Tạo embeddings
        if self.passage_texts:
            logger.info(f"🔄 Đang tạo embeddings với batch_size={self.config.batch_size}...")
            self.passage_embeddings = self.model.encode(
                self.passage_texts,
                show_progress_bar=True,
                batch_size=self.config.batch_size
            )
            logger.info(f"✅ Hoàn thành tạo embeddings cho passages. Shape: {self.passage_embeddings.shape}")
        
        end_time = time.time()
        log_performance("Tạo passage embeddings", start_time, end_time,
                       {"passages": len(passages), "embedding_dim": self.passage_embeddings.shape[1] if self.passage_embeddings is not None else 0})
    
    def build_triple_embeddings(self, triples: List[Dict[str, Any]]):
        """
        Xây dựng embeddings cho triples
        
        Args:
            triples (List[Dict]): Danh sách triple objects
        """
        logger.info(f"🔗 Bắt đầu tạo embeddings cho {len(triples)} triples...")
        start_time = time.time()
        
        self.load_model()
        
        self.triple_texts = []
        self.triple_metadata = []
        
        for i, triple in enumerate(triples, 1):
            # Tạo văn bản triple (giống BM25)
            subject = triple.get('subject', '')
            predicate = triple.get('predicate', '')
            obj = triple.get('object', '')
            
            triple_text = f"{subject} {predicate} {obj}"
            self.triple_texts.append(triple_text)
            
            # Lưu metadata (giống BM25)
            metadata = {
                'subject': subject,
                'predicate': predicate,
                'object': obj,
                'triple_text': triple_text,
                'source_passage_id': triple.get('source_passage_id', ''),
                'confidence': triple.get('confidence', 1.0)
            }
            self.triple_metadata.append(metadata)
            
            if i % 500 == 0 or i == len(triples):
                logger.info(f"   🔗 Đã chuẩn bị {i}/{len(triples)} triples cho embedding")
        
        # Tạo embeddings
        if self.triple_texts:
            logger.info(f"🔄 Đang tạo embeddings cho triples...")
            self.triple_embeddings = self.model.encode(
                self.triple_texts,
                show_progress_bar=True,
                batch_size=self.config.batch_size
            )
            logger.info(f"✅ Hoàn thành tạo embeddings cho triples. Shape: {self.triple_embeddings.shape}")
        
        end_time = time.time()
        log_performance("Tạo triple embeddings", start_time, end_time,
                       {"triples": len(triples), "embedding_dim": self.triple_embeddings.shape[1] if self.triple_embeddings is not None else 0})
    
    def search_passages(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Tìm kiếm passages sử dụng embedding similarity
        
        Args:
            query (str): Truy vấn tìm kiếm
            top_k (int): Số lượng kết quả hàng đầu
            
        Returns:
            List[Tuple[int, float]]: Danh sách (index, score) của kết quả
        """
        if self.passage_embeddings is None or not query:
            logger.warning("⚠️ Embeddings cho passages chưa được tạo hoặc query rỗng")
            return []
        
        logger.info(f"🧠 Tìm kiếm embedding passages với query: '{query[:50]}{'...' if len(query) > 50 else ''}'")
        
        self.load_model()
        
        # Encode query
        query_embedding = self.model.encode([query])
        logger.info(f"🔍 Đã tạo embedding cho query. Shape: {query_embedding.shape}")
        
        # Tính similarities
        similarities = cosine_similarity(query_embedding, self.passage_embeddings)[0]
        
        # Lấy top-k indices và scores
        top_indices = np.argsort(similarities)[::-1][:top_k]
        top_scores = similarities[top_indices]
        
        # Log kết quả
        high_scores = [(idx, score) for idx, score in zip(top_indices, top_scores) if score > 0.5]
        logger.info(f"🎯 Embedding passages: {len(high_scores)}/{top_k} kết quả có điểm > 0.5")
        logger.info(f"📊 Điểm cao nhất: {top_scores[0]:.3f}, thấp nhất: {top_scores[-1]:.3f}")
        
        return [(int(idx), float(score)) for idx, score in zip(top_indices, top_scores)]
    
    def search_triples(self, query: str, top_n: int = 50) -> List[Tuple[int, float]]:
        """
        Tìm kiếm triples sử dụng embedding similarity
        
        Args:
            query (str): Truy vấn tìm kiếm
            top_n (int): Số lượng kết quả hàng đầu
            
        Returns:
            List[Tuple[int, float]]: Danh sách (index, score) của kết quả
        """
        if self.triple_embeddings is None or not query:
            logger.warning("⚠️ Embeddings cho triples chưa được tạo hoặc query rỗng")
            return []
        
        logger.info(f"🔗 Tìm kiếm embedding triples với query: '{query[:50]}{'...' if len(query) > 50 else ''}'")
        
        self.load_model()
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Tính similarities
        similarities = cosine_similarity(query_embedding, self.triple_embeddings)[0]
        
        # Lấy top-n indices và scores
        top_indices = np.argsort(similarities)[::-1][:top_n]
        top_scores = similarities[top_indices]
        
        # Log kết quả
        high_scores = [(idx, score) for idx, score in zip(top_indices, top_scores) if score > 0.3]
        logger.info(f"🎯 Embedding triples: {len(high_scores)}/{top_n} kết quả có điểm > 0.3")
        logger.info(f"📊 Điểm cao nhất: {top_scores[0]:.3f}, thấp nhất: {top_scores[-1]:.3f}")
        
        return [(int(idx), float(score)) for idx, score in zip(top_indices, top_scores)]

# ==================== HYBRID SCORER ====================

class HybridScorer:
    """
    Kết hợp điểm số BM25 và embedding để tạo điểm số lai
    
    Sử dụng weighted combination với normalization để đảm bảo
    công bằng giữa hai phương pháp scoring khác nhau.
    """
    
    def __init__(self, config: RetrievalConfig):
        """
        Khởi tạo HybridScorer
        
        Args:
            config (RetrievalConfig): Cấu hình với trọng số alpha
        """
        self.config = config
        logger.info(f"🎭 Khởi tạo HybridScorer với trọng số: BM25={config.alpha_bm25}, Embedding={config.alpha_embedding}")
    
    def combine_scores(self, bm25_results: List[Tuple[int, float]], 
                      embedding_results: List[Tuple[int, float]],
                      max_results: int) -> List[Tuple[int, float, float, float]]:
        """
        Kết hợp điểm số BM25 và embedding
        
        Quá trình:
        1. Normalize điểm số về khoảng [0, 1]
        2. Tạo dictionaries để tra cứu điểm
        3. Tính điểm lai cho tất cả items
        4. Sắp xếp theo điểm lai giảm dần
        
        Args:
            bm25_results (List[Tuple]): Kết quả BM25 (index, score)
            embedding_results (List[Tuple]): Kết quả embedding (index, score)
            max_results (int): Số lượng kết quả tối đa
            
        Returns:
            List[Tuple[int, float, float, float]]: (index, bm25_score, embedding_score, hybrid_score)
        """
        logger.info(f"🎭 Bắt đầu kết hợp điểm số: {len(bm25_results)} BM25 + {len(embedding_results)} embedding")
        # Normalize điểm số về [0, 1] range
        bm25_scores = self._normalize_scores([score for _, score in bm25_results])
        embedding_scores = self._normalize_scores([score for _, score in embedding_results])
        
        logger.info(f"📊 Normalized scores - BM25: min={min(bm25_scores) if bm25_scores else 0:.3f}, max={max(bm25_scores) if bm25_scores else 0:.3f}")
        logger.info(f"📊 Normalized scores - Embedding: min={min(embedding_scores) if embedding_scores else 0:.3f}, max={max(embedding_scores) if embedding_scores else 0:.3f}")
        
        # Tạo dictionaries để tra cứu điểm
        bm25_dict = {idx: norm_score for (idx, _), norm_score in zip(bm25_results, bm25_scores)}
        embedding_dict = {idx: norm_score for (idx, _), norm_score in zip(embedding_results, embedding_scores)}
        
        # Kết hợp điểm số
        all_indices = set(bm25_dict.keys()) | set(embedding_dict.keys())
        combined_results = []
        
        logger.info(f"🔀 Đang kết hợp điểm cho {len(all_indices)} items unique...")
        
        for idx in all_indices:
            bm25_score = bm25_dict.get(idx, 0.0)
            embedding_score = embedding_dict.get(idx, 0.0)
            
            # Tính điểm lai
            hybrid_score = (
                self.config.alpha_bm25 * bm25_score + 
                self.config.alpha_embedding * embedding_score
            )
            
            combined_results.append((idx, bm25_score, embedding_score, hybrid_score))
        
        # Sắp xếp theo điểm lai giảm dần
        combined_results.sort(key=lambda x: x[3], reverse=True)
        
        # Log thống kê
        if combined_results:
            top_hybrid = combined_results[0][3]
            bottom_hybrid = combined_results[-1][3]
            logger.info(f"🏆 Điểm lai: cao nhất={top_hybrid:.3f}, thấp nhất={bottom_hybrid:.3f}")
            
            # Thống kê nguồn điểm
            both_sources = sum(1 for _, bm25, emb, _ in combined_results if bm25 > 0 and emb > 0)
            only_bm25 = sum(1 for _, bm25, emb, _ in combined_results if bm25 > 0 and emb == 0)
            only_embedding = sum(1 for _, bm25, emb, _ in combined_results if bm25 == 0 and emb > 0)
            
            logger.info(f"📈 Nguồn điểm: cả hai={both_sources}, chỉ BM25={only_bm25}, chỉ embedding={only_embedding}")
        
        final_results = combined_results[:max_results]
        logger.info(f"✅ Hoàn thành kết hợp điểm, trả về {len(final_results)}/{max_results} kết quả")
        
        return final_results
    
    def _normalize_scores(self, scores: List[float]) -> List[float]:
        """
        Chuẩn hóa điểm số về khoảng [0, 1]
        
        Args:
            scores (List[float]): Danh sách điểm số gốc
            
        Returns:
            List[float]: Danh sách điểm số đã chuẩn hóa
        """
        if not scores:
            return []
        
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            # Tất cả điểm bằng nhau
            return [1.0] * len(scores)
        
        # Min-max normalization
        normalized = [(score - min_score) / (max_score - min_score) for score in scores]
        return normalized

# ==================== NEO4J DATA ACCESS ====================

class Neo4jDataAccess:
    """
    Truy cập dữ liệu từ Neo4j database
    
    Lớp này chịu trách nhiệm kết nối và truy vấn Knowledge Graph
    để lấy passages và triples cho hệ thống truy xuất.
    """
    
    def __init__(self, uri: str, user: str, password: str):
        """
        Khởi tạo kết nối Neo4j
        
        Args:
            uri (str): URI của Neo4j database
            user (str): Tên đăng nhập
            password (str): Mật khẩu
        """
        logger.info(f"🗃️ Đang kết nối đến Neo4j: {uri}")
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("✅ Kết nối Neo4j thành công")
        except Exception as e:
            logger.error(f"❌ Lỗi kết nối Neo4j: {e}")
            raise
        
    def close(self):
        """Đóng kết nối database"""
        if self.driver:
            self.driver.close()
            logger.info("🔐 Đã đóng kết nối Neo4j")
    
    def get_all_passages(self) -> List[Dict[str, Any]]:
        """
        Lấy tất cả passage nodes từ Neo4j
        
        Returns:
            List[Dict[str, Any]]: Danh sách passages với metadata
        """
        logger.info("📖 Đang truy vấn tất cả passages từ Neo4j...")
        
        with self.driver.session() as session:
            query = """
            MATCH (p:Passage)
            RETURN p.id as id, p.text as text, p.title as title, 
                   p.doc_id as doc_id, p.chunk_id as chunk_id,
                   p.text_length as text_length
            ORDER BY p.id
            """
            
            result = session.run(query)
            passages = []
            
            for record in result:
                passage = {
                    'id': record['id'] or '',
                    'text': record['text'] or '',
                    'title': record['title'] or '',
                    'doc_id': record['doc_id'] or '',
                    'chunk_id': record['chunk_id'] or '',
                    'text_length': record['text_length'] or len(record['text'] or '')
                }
                passages.append(passage)
            
            logger.info(f"✅ Đã truy xuất {len(passages)} passages từ Neo4j")
            
            if passages:
                # Thống kê
                total_chars = sum(len(p['text']) for p in passages)
                avg_length = total_chars / len(passages)
                logger.info(f"📊 Thống kê passages: tổng ký tự={total_chars:,}, trung bình={avg_length:.1f} ký tự/passage")
            
            return passages
    
    def get_all_triples(self) -> List[Dict[str, Any]]:
        """
        Lấy tất cả relation triples từ Neo4j
        
        Returns:
            List[Dict[str, Any]]: Danh sách triples với metadata
        """
        logger.info("🔗 Đang truy vấn tất cả triples từ Neo4j...")
        
        with self.driver.session() as session:
            query = """
            MATCH (s:Phrase)-[r:RELATION]->(o:Phrase)
            RETURN s.text as subject, r.predicate as predicate, o.text as object,
                   r.confidence as confidence, r.source_chunk as source_passage_id,
                   r.original_subject as original_subject, r.original_object as original_object
            ORDER BY r.confidence DESC
            
            """
            
            result = session.run(query)
            triples = []
            
            for record in result:
                triple = {
                    'subject': record['subject'] or '',
                    'predicate': record['predicate'] or '',
                    'object': record['object'] or '',
                    'confidence': record['confidence'] or 1.0,
                    'source_passage_id': record['source_passage_id'] or '',
                    'original_subject': record['original_subject'] or record['subject'] or '',
                    'original_object': record['original_object'] or record['object'] or ''
                }
                triples.append(triple)
            
            logger.info(f"✅ Đã truy xuất {len(triples)} triples từ Neo4j")
            
            if triples:
                # Thống kê
                confidence_scores = [t['confidence'] for t in triples]
                avg_confidence = sum(confidence_scores) / len(confidence_scores)
                high_confidence = sum(1 for c in confidence_scores if c >= 0.8)
                
                predicates = [t['predicate'] for t in triples]
                unique_predicates = len(set(predicates))
                
                logger.info(f"📊 Thống kê triples:")
                logger.info(f"   - Confidence trung bình: {avg_confidence:.3f}")
                logger.info(f"   - Triples confidence cao (≥0.8): {high_confidence}/{len(triples)}")
                logger.info(f"   - Số predicates unique: {unique_predicates}")
            
            return triples

# ==================== MAIN DUAL RETRIEVER ====================

class DualRetriever:
    """
    Lớp chính cho hệ thống truy xuất kép kết hợp BM25 và embedding-based search
    
    Đây là orchestrator chính điều phối toàn bộ quá trình truy xuất:
    1. Kết nối Neo4j và tải dữ liệu
    2. Xây dựng indices BM25 và embedding
    3. Thực hiện tìm kiếm lai
    4. Kết hợp và xếp hạng kết quả
    """
    
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 config: Optional[RetrievalConfig] = None):
        """
        Khởi tạo DualRetriever
        
        Args:
            neo4j_uri (str): URI Neo4j database
            neo4j_user (str): Tên đăng nhập Neo4j
            neo4j_password (str): Mật khẩu Neo4j
            config (Optional[RetrievalConfig]): Cấu hình truy xuất
        """
        logger.info("🚀 Đang khởi tạo DualRetriever...")
        
        self.config = config or RetrievalConfig()
        logger.info(f"⚙️ Cấu hình: BM25({self.config.alpha_bm25}) + Embedding({self.config.alpha_embedding})")
        
        # Khởi tạo các components
        self.neo4j_access = Neo4jDataAccess(neo4j_uri, neo4j_user, neo4j_password)
        self.bm25_retriever = BM25Retriever(self.config)
        self.embedding_retriever = EmbeddingRetriever(self.config)
        self.hybrid_scorer = HybridScorer(self.config)
        
        # Lưu trữ dữ liệu
        self.passages_data = []
        self.triples_data = []
        self.is_initialized = False
        
        logger.info("✅ DualRetriever đã được khởi tạo thành công")
    
    def initialize_indices(self):
        """
        Tải dữ liệu từ Neo4j và xây dựng search indices
        
        Quá trình này chỉ chạy một lần và bao gồm:
        1. Tải passages và triples từ Neo4j
        2. Xây dựng indices BM25
        3. Tạo embeddings
        4. Chuẩn bị cho tìm kiếm
        """
        if self.is_initialized:
            logger.info("ℹ️ Indices đã được khởi tạo trước đó, bỏ qua...")
            return
        
        logger.info("🔧 Bắt đầu khởi tạo indices cho hệ thống truy xuất...")
        start_time = time.time()
        
        # Bước 1: Tải dữ liệu từ Neo4j
        logger.info("📥 Bước 1/4: Tải dữ liệu từ Neo4j...")
        self.passages_data = self.neo4j_access.get_all_passages()
        self.triples_data = self.neo4j_access.get_all_triples()
        
        if not self.passages_data:
            logger.warning("⚠️ Không tìm thấy passages nào trong database!")
        if not self.triples_data:
            logger.warning("⚠️ Không tìm thấy triples nào trong database!")
        
        # Bước 2: Xây dựng indices BM25
        logger.info("🔍 Bước 2/4: Xây dựng indices BM25...")
        self.bm25_retriever.build_passage_index(self.passages_data)
        self.bm25_retriever.build_triple_index(self.triples_data)
        
        # Bước 3: Tạo embeddings
        logger.info("🧠 Bước 3/4: Tạo embeddings...")
        self.embedding_retriever.build_passage_embeddings(self.passages_data)
        self.embedding_retriever.build_triple_embeddings(self.triples_data)
        
        # Bước 4: Hoàn thành
        logger.info("✅ Bước 4/4: Hoàn thành khởi tạo...")
        self.is_initialized = True
        
        end_time = time.time()
        log_performance("Khởi tạo toàn bộ indices", start_time, end_time, {
            "passages": len(self.passages_data),
            "triples": len(self.triples_data),
            "total_items": len(self.passages_data) + len(self.triples_data)
        })
        
        logger.info("🎉 Hệ thống truy xuất đã sẵn sàng!")
    
    def retrieve_passages(self, query: str, top_k: int = 20) -> List[RetrievedItem]:
        """
        Truy xuất top-k passages liên quan nhất sử dụng phương pháp lai
        
        Args:
            query (str): Truy vấn của người dùng
            top_k (int): Số lượng passages cần truy xuất
            
        Returns:
            List[RetrievedItem]: Danh sách passages đã truy xuất với điểm số
        """
        if not validate_query(query):
            logger.error(f"❌ Query không hợp lệ: '{query}'")
            return []
        
        self.initialize_indices()
        
        logger.info(f"🔍 Bắt đầu truy xuất top-{top_k} passages...")
        logger.info(f"📝 Query: '{query}'")
        start_time = time.time()
        
        # Tìm kiếm BM25
        logger.info("🔤 Thực hiện tìm kiếm BM25...")
        bm25_results = self.bm25_retriever.search_passages(query, min(top_k * 3, 100))
        
        # Tìm kiếm Embedding
        logger.info("🧠 Thực hiện tìm kiếm Embedding...")
        embedding_results = self.embedding_retriever.search_passages(query, min(top_k * 3, 100))
        
        # Kết hợp điểm số
        logger.info("🎭 Kết hợp điểm số lai...")
        combined_results = self.hybrid_scorer.combine_scores(
            bm25_results, embedding_results, top_k
        )
        
        # Tạo RetrievedItem objects
        logger.info("📦 Tạo objects kết quả...")
        retrieved_passages = []
        for i, (idx, bm25_score, embedding_score, hybrid_score) in enumerate(combined_results, 1):
            if idx < len(self.passages_data):
                passage_data = self.passages_data[idx]
                passage_metadata = self.bm25_retriever.passage_metadata[idx]
                
                retrieved_item = RetrievedItem(
                    item_id=passage_metadata['passage_id'],
                    item_type='passage',
                    text=passage_metadata['original_text'],
                    bm25_score=bm25_score,
                    embedding_score=embedding_score,
                    hybrid_score=hybrid_score,
                    metadata={
                        'title': passage_metadata['title'],
                        'doc_id': passage_metadata['doc_id'],
                        'text_length': passage_metadata['text_length'],
                        'rank': i
                    }
                )
                retrieved_passages.append(retrieved_item)
                
                logger.info(f"   {i}. {retrieved_item.item_id} - Điểm: {hybrid_score:.3f} (BM25: {bm25_score:.3f}, Emb: {embedding_score:.3f})")
        
        end_time = time.time()
        log_performance("Truy xuất passages", start_time, end_time, {
            "query_length": len(query),
            "results_found": len(retrieved_passages),
            "requested": top_k
        })
        
        logger.info(f"✅ Hoàn thành truy xuất {len(retrieved_passages)} passages")
        return retrieved_passages
    
    def retrieve_triples(self, query: str, top_n: int = 10) -> List[RetrievedItem]:
        """
        Truy xuất top-n triples liên quan nhất sử dụng phương pháp lai
        
        Args:
            query (str): Truy vấn của người dùng
            top_n (int): Số lượng triples cần truy xuất
            
        Returns:
            List[RetrievedItem]: Danh sách triples đã truy xuất với điểm số
        """
        if not validate_query(query):
            logger.error(f"❌ Query không hợp lệ: '{query}'")
            return []
        
        self.initialize_indices()
        
        logger.info(f"🔗 Bắt đầu truy xuất top-{top_n} triples...")
        logger.info(f"📝 Query: '{query}'")
        start_time = time.time()
        
        # Tìm kiếm BM25
        logger.info("🔤 Thực hiện tìm kiếm BM25 cho triples...")
        bm25_results = self.bm25_retriever.search_triples(query, min(top_n * 3, 200))
        
        # Tìm kiếm Embedding
        logger.info("🧠 Thực hiện tìm kiếm Embedding cho triples...")
        embedding_results = self.embedding_retriever.search_triples(query, min(top_n * 3, 200))
        
        # Kết hợp điểm số
        logger.info("🎭 Kết hợp điểm số lai cho triples...")
        combined_results = self.hybrid_scorer.combine_scores(
            bm25_results, embedding_results, top_n
        )
        
        # Tạo RetrievedItem objects
        logger.info("📦 Tạo objects kết quả triples...")
        retrieved_triples = []
        for i, (idx, bm25_score, embedding_score, hybrid_score) in enumerate(combined_results, 1):
            if idx < len(self.triples_data):
                triple_data = self.triples_data[idx]
                triple_metadata = self.bm25_retriever.triple_metadata[idx]
                
                # Tạo unique triple ID
                triple_id = f"triple_{uuid.uuid4().hex[:8]}"
                
                retrieved_item = RetrievedItem(
                    item_id=triple_id,
                    item_type='triple',
                    text=triple_metadata['triple_text'],
                    bm25_score=bm25_score,
                    embedding_score=embedding_score,
                    hybrid_score=hybrid_score,
                    metadata={
                        'subject': triple_metadata['subject'],
                        'predicate': triple_metadata['predicate'],
                        'object': triple_metadata['object'],
                        'source_passage_id': triple_metadata['source_passage_id'],
                        'confidence': triple_metadata['confidence'],
                        'rank': i
                    }
                )
                retrieved_triples.append(retrieved_item)
                
                logger.info(f"   {i}. ({triple_metadata['subject']} → {triple_metadata['predicate']} → {triple_metadata['object']}) - Điểm: {hybrid_score:.3f}")
        
        end_time = time.time()
        log_performance("Truy xuất triples", start_time, end_time, {
            "query_length": len(query),
            "results_found": len(retrieved_triples),
            "requested": top_n
        })
        
        logger.info(f"✅ Hoàn thành truy xuất {len(retrieved_triples)} triples")
        return retrieved_triples
    
    def retrieve_dual(self, query: str, top_k_passages: int = 10, 
                     top_n_triples: int = 10) -> RetrievalResult:
        """
        Thực hiện truy xuất kép cho cả passages và triples
        
        Args:
            query (str): Truy vấn của người dùng
            top_k_passages (int): Số lượng passages cần truy xuất
            top_n_triples (int): Số lượng triples cần truy xuất
            
        Returns:
            RetrievalResult: Kết quả truy xuất kép hoàn chỉnh
        """
        logger.info("=" * 60)
        logger.info("🚀 BẮT ĐẦU TRUY XUẤT KÉP (DUAL RETRIEVAL)")
        logger.info("=" * 60)
        logger.info(f"📝 Query: '{query}'")
        logger.info(f"🎯 Mục tiêu: {top_k_passages} passages + {top_n_triples} triples")
        
        start_time = time.time()
        
        # Truy xuất passages
        logger.info("\n🔍 GIAI ĐOẠN 1: TRUY XUẤT PASSAGES")
        logger.info("-" * 40)
        raw_passages = self.retrieve_passages(query, top_k_passages)
        
        # Truy xuất triples
        logger.info("\n🔗 GIAI ĐOẠN 2: TRUY XUẤT TRIPLES")
        logger.info("-" * 40)
        raw_triples = self.retrieve_triples(query, top_n_triples)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Biên soạn thống kê
        logger.info("\n📊 BIÊN SOẠN THỐNG KÊ")
        logger.info("-" * 40)
        
        statistics = {
            'passages_retrieved': len(raw_passages),
            'triples_retrieved': len(raw_triples),
            'total_passages_in_db': len(self.passages_data),
            'total_triples_in_db': len(self.triples_data),
            'query_info': {
                'original_query': query,
                'query_length': len(query),
                'query_words': len(query.split()),
                'extracted_keywords': extract_keywords(query)
            },
            'retrieval_config': {
                'alpha_bm25': self.config.alpha_bm25,
                'alpha_embedding': self.config.alpha_embedding,
                'embedding_model': self.config.embedding_model,
                'bm25_k1': self.config.bm25_k1,
                'bm25_b': self.config.bm25_b
            },
            'performance': {
                'total_time_seconds': total_time,
                'passages_per_second': len(raw_passages) / total_time if total_time > 0 else 0,
                'triples_per_second': len(raw_triples) / total_time if total_time > 0 else 0
            }
        }
        
        # Tạo kết quả
        result = RetrievalResult(
            raw_passages=raw_passages,
            raw_triples=raw_triples,
            query=query,
            retrieval_time=total_time,
            statistics=statistics
        )
        
        # Log tổng kết
        logger.info("=" * 60)
        logger.info("🎉 HOÀN THÀNH TRUY XUẤT KÉP")
        logger.info("=" * 60)
        logger.info(f"⏱️ Tổng thời gian: {total_time:.2f} giây")
        logger.info(f"📖 Passages tìm được: {len(raw_passages)}/{top_k_passages}")
        logger.info(f"🔗 Triples tìm được: {len(raw_triples)}/{top_n_triples}")
        logger.info(f"📊 Hiệu suất: {(len(raw_passages) + len(raw_triples)) / total_time:.1f} items/giây")
        
        if raw_passages:
            avg_passage_score = sum(p.hybrid_score for p in raw_passages) / len(raw_passages)
            logger.info(f"📈 Điểm trung bình passages: {avg_passage_score:.3f}")
            
        if raw_triples:
            avg_triple_score = sum(t.hybrid_score for t in raw_triples) / len(raw_triples)
            logger.info(f"📈 Điểm trung bình triples: {avg_triple_score:.3f}")
        
        logger.info("=" * 60)
        
        return result
    
    def get_retrieval_statistics(self) -> Dict[str, Any]:
        """
        Lấy thống kê toàn diện về hệ thống truy xuất
        
        Returns:
            Dict[str, Any]: Thống kê chi tiết về trạng thái hệ thống
        """
        if not self.is_initialized:
            return {
                "status": "chưa_khởi_tạo",
                "message": "Hệ thống chưa được khởi tạo. Gọi initialize_indices() trước."
            }
        
        return {
            'status': 'đã_khởi_tạo',
            'data_info': {
                'total_passages': len(self.passages_data),
                'total_triples': len(self.triples_data),
                'total_items': len(self.passages_data) + len(self.triples_data)
            },
            'config_info': {
                'bm25_parameters': {
                    'k1': self.config.bm25_k1,
                    'b': self.config.bm25_b
                },
                'hybrid_weights': {
                    'alpha_bm25': self.config.alpha_bm25,
                    'alpha_embedding': self.config.alpha_embedding
                },
                'embedding_info': {
                    'model': self.config.embedding_model,
                    'device': self.config.embedding_device,
                    'batch_size': self.config.batch_size
                }
            },
            'indices_status': {
                'bm25_passages': self.bm25_retriever.bm25_passages is not None,
                'bm25_triples': self.bm25_retriever.bm25_triples is not None,
                'embedding_passages': self.embedding_retriever.passage_embeddings is not None,
                'embedding_triples': self.embedding_retriever.triple_embeddings is not None
            },
            'capabilities': {
                'can_search_passages': all([
                    self.bm25_retriever.bm25_passages is not None,
                    self.embedding_retriever.passage_embeddings is not None
                ]),
                'can_search_triples': all([
                    self.bm25_retriever.bm25_triples is not None,
                    self.embedding_retriever.triple_embeddings is not None
                ])
            }
        }
    
    def close(self):
        """Đóng kết nối Neo4j và giải phóng tài nguyên"""
        logger.info("🔐 Đang đóng DualRetriever...")
        self.neo4j_access.close()
        
        # Clear large data structures
        self.passages_data.clear()
        self.triples_data.clear()
        
        logger.info("✅ DualRetriever đã được đóng và giải phóng tài nguyên")

# ==================== TEST FUNCTIONS ====================

def test_dual_retrieval():
    """Test đầy đủ chức năng dual retrieval"""
    print("🧪 BẮT ĐẦU TEST DUAL RETRIEVAL")
    print("=" * 50)
    
    # Cấu hình kết nối Neo4j
    neo4j_uri = "bolt://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "graphrag123"
    
    try:
        # Khởi tạo retriever
        print("⚙️ Khởi tạo cấu hình...")
        config = RetrievalConfig(
            alpha_bm25=0.3,
            alpha_embedding=0.7
        )
        
        print("🚀 Khởi tạo DualRetriever...")
        retriever = DualRetriever(neo4j_uri, neo4j_user, neo4j_password, config)
        
        # Test query
        test_query = "Lợi ích của táo cho sức khỏe"
        
        print(f"\n📝 Testing với query: '{test_query}'")
        print("-" * 50)
        
        # Test dual retrieval
        print("🔍 Thực hiện dual retrieval...")
        result = retriever.retrieve_dual(
            query=test_query,
            top_k_passages=10,
            top_n_triples=10
        )
        
        print(f"\n📊 KẾT QUẢ DUAL RETRIEVAL:")
        print("=" * 50)
        print(f"⏱️ Thời gian thực hiện: {result.retrieval_time:.2f} giây")
        print(f"📖 Số passages tìm được: {len(result.raw_passages)}")
        print(f"🔗 Số triples tìm được: {len(result.raw_triples)}")
        
        # Hiển thị top passages
        print(f"\n🏆 TOP PASSAGES:")
        print("-" * 50)
        for i, passage in enumerate(result.raw_passages[:3], 1):
            print(f"{i}. ID: {passage.item_id}")
            print(f"   📊 Điểm số: Lai={passage.hybrid_score:.3f} (BM25={passage.bm25_score:.3f}, Embedding={passage.embedding_score:.3f})")
            print(f"   📝 Nội dung: {passage.text[:100]}...")
            print(f"   📋 Metadata: {passage.metadata.get('title', 'N/A')} | Độ dài: {passage.metadata.get('text_length', 0)} ký tự")
            print()
        
        # Hiển thị top triples
        print(f"🏆 TOP TRIPLES:")
        print("-" * 50)
        for i, triple in enumerate(result.raw_triples[:5], 1):
            print(f"{i}. 🔗 Triple: {triple.metadata['subject']} → {triple.metadata['predicate']} → {triple.metadata['object']}")
            print(f"   📊 Điểm số: Lai={triple.hybrid_score:.3f} (BM25={triple.bm25_score:.3f}, Embedding={triple.embedding_score:.3f})")
            print(f"   🎯 Confidence: {triple.metadata.get('confidence', 'N/A')}")
            print(f"   📍 Nguồn: {triple.metadata.get('source_passage_id', 'N/A')}")
            print()
        
        # Lấy và hiển thị thống kê
        stats = retriever.get_retrieval_statistics()
        print(f"📈 THỐNG KÊ HỆ THỐNG:")
        print("-" * 50)
        print(f"📊 Trạng thái: {stats['status']}")
        print(f"📖 Tổng passages trong DB: {stats['data_info']['total_passages']}")
        print(f"🔗 Tổng triples trong DB: {stats['data_info']['total_triples']}")
        print(f"🎭 Trọng số BM25: {stats['config_info']['hybrid_weights']['alpha_bm25']}")
        print(f"🧠 Trọng số Embedding: {stats['config_info']['hybrid_weights']['alpha_embedding']}")
        print(f"🔧 Model embedding: {stats['config_info']['embedding_info']['model']}")
        
        print(f"\n🔧 TRẠNG THÁI INDICES:")
        indices_status = stats['indices_status']
        for index_name, status in indices_status.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {index_name}: {'Sẵn sàng' if status else 'Chưa khởi tạo'}")
        
        print(f"\n🎯 KHẢ NĂNG HỆ THỐNG:")
        capabilities = stats['capabilities']
        for capability, status in capabilities.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {capability}: {'Có thể' if status else 'Không thể'}")
        
        # Test chức năng lưu file
        output_path = Path("outputs/test_retrieval_result_detailed.json")
        result.save_to_file(output_path)
        print(f"\n💾 Kết quả đã được lưu vào: {output_path}")
        
        # Hiển thị thống kê chi tiết từ kết quả
        result_stats = result.statistics
        print(f"\n📊 THỐNG KÊ TRUY XUẤT CHI TIẾT:")
        print("-" * 50)
        print(f"🔍 Query gốc: '{result_stats['query_info']['original_query']}'")
        print(f"📏 Độ dài query: {result_stats['query_info']['query_length']} ký tự")
        print(f"🔤 Số từ trong query: {result_stats['query_info']['query_words']}")
        print(f"🏷️ Keywords trích xuất: {result_stats['query_info']['extracted_keywords']}")
        print(f"⚡ Hiệu suất: {result_stats['performance']['passages_per_second']:.1f} passages/giây, {result_stats['performance']['triples_per_second']:.1f} triples/giây")
        
        # Đóng retriever
        retriever.close()
        
        print("\n🎉 TEST DUAL RETRIEVAL HOÀN THÀNH THÀNH CÔNG!")
        print("=" * 50)
        return result
        
    except Exception as e:
        print(f"\n❌ TEST THẤT BẠI: {e}")
        logger.exception("Chi tiết lỗi dual retrieval test:")
        return None

def test_individual_components():
    """Test các components riêng lẻ với mock data"""
    print("🧪 BẮT ĐẦU TEST CÁC COMPONENTS RIÊNG LẺ")
    print("=" * 50)
    
    # Test cấu hình
    config = RetrievalConfig()
    print(f"⚙️ Cấu hình test:")
    print(f"   🔤 Trọng số BM25: {config.alpha_bm25}")
    print(f"   🧠 Trọng số Embedding: {config.alpha_embedding}")
    print(f"   📊 Model embedding: {config.embedding_model}")
    
    # Test BM25 retriever với mock data
    print(f"\n🔤 Test BM25Retriever...")
    bm25_retriever = BM25Retriever(config)
    
    # Mock passages cho test
    mock_passages = [
        {
            "id": "passage_1", 
            "text": "Táo là loại trái cây giàu vitamin C và chất xơ, rất tốt cho sức khỏe", 
            "title": "Lợi ích của táo", 
            "doc_id": "doc_health_01"
        },
        {
            "id": "passage_2", 
            "text": "Cam chứa nhiều chất xơ và vitamin C, giúp tăng cường hệ miễn dịch và hỗ trợ tiêu hóa", 
            "title": "Giá trị dinh dưỡng của cam", 
            "doc_id": "doc_health_02"
        },
        {
            "id": "passage_3", 
            "text": "Chuối cung cấp kali và năng lượng nhanh, thích hợp cho người tập thể thao", 
            "title": "Chuối và thể thao", 
            "doc_id": "doc_health_03"
        }
    ]
    
    print(f"📝 Xây dựng BM25 index với {len(mock_passages)} mock passages...")
    bm25_retriever.build_passage_index(mock_passages)
    
    # Test tìm kiếm BM25
    test_queries = ["táo vitamin sức khỏe", "cam chất xơ", "chuối năng lượng"]
    
    for query in test_queries:
        print(f"\n🔍 Test BM25 với query: '{query}'")
        bm25_results = bm25_retriever.search_passages(query, top_k=10)
        print(f"   📊 Kết quả BM25: {bm25_results}")
        
        # Hiển thị chi tiết kết quả
        for idx, score in bm25_results:
            if idx < len(mock_passages):
                passage = mock_passages[idx]
                print(f"   {idx+1}. Điểm: {score:.3f} - {passage['title']}: {passage['text'][:50]}...")
    
    # Test hybrid scorer
    print(f"\n🎭 Test HybridScorer...")
    hybrid_scorer = HybridScorer(config)
    
    # Mock results cho test
    mock_bm25_results = [(0, 0.8), (1, 0.6), (2, 0.3)]
    mock_embedding_results = [(0, 0.9), (1, 0.7), (2, 0.4)]
    
    print(f"🔤 Mock BM25 results: {mock_bm25_results}")
    print(f"🧠 Mock Embedding results: {mock_embedding_results}")
    
    combined = hybrid_scorer.combine_scores(mock_bm25_results, mock_embedding_results, 3)
    print(f"🎭 Kết quả kết hợp: {combined}")
    
    # Hiển thị breakdown chi tiết
    print(f"\n📊 Chi tiết điểm số:")
    for i, (idx, bm25_score, emb_score, hybrid_score) in enumerate(combined, 1):
        print(f"   {i}. Index {idx}: BM25={bm25_score:.3f}, Embedding={emb_score:.3f}, Lai={hybrid_score:.3f}")
    
    print(f"\n✅ Test components riêng lẻ hoàn thành!")

def test_query_processing():
    """Test xử lý query và validation"""
    print("\n🔍 TEST XỬ LÝ QUERY")
    print("-" * 30)
    
    test_queries = [
        "Lợi ích của táo cho sức khỏe",           # Valid Vietnamese
        "What are the benefits of apples?",       # Valid English  
        "táo + cam = gì?",                        # Valid with symbols
        "a",                                      # Too short
        "",                                       # Empty
        "x" * 1001,                              # Too long
        "123456789",                             # Only numbers
        "Táo đỏ tốt hơn táo xanh không?"         # Valid question
    ]
    
    print("📝 Test validation cho các queries:")
    for i, query in enumerate(test_queries, 1):
        is_valid = validate_query(query)
        status = "✅ Hợp lệ" if is_valid else "❌ Không hợp lệ"
        display_query = f"'{query[:50]}...'" if len(query) > 50 else f"'{query}'"
        print(f"   {i}. {display_query} → {status}")
        
        if is_valid:
            keywords = extract_keywords(query)
            clean_text_result = clean_text(query)
            print(f"      🏷️ Keywords: {keywords}")
            print(f"      🧹 Cleaned: '{clean_text_result}'")

if __name__ == "__main__":
    print("🚀 BẮT ĐẦU CHẠY TẤT CẢ TESTS CHO MODULE 1")
    print("=" * 60)
    
    # Test 1: Query processing
    test_query_processing()
    
    print("\n" + "=" * 60)
    
    # Test 2: Individual components
    test_individual_components()
    
    print("\n" + "=" * 60)
    
    # Test 3: Full dual retrieval (yêu cầu Neo4j)
    print("⚠️ LƯU Ý: Test tiếp theo yêu cầu Neo4j đang chạy")
    input("Nhấn Enter để tiếp tục với full dual retrieval test...")
    
    test_dual_retrieval()
    
    print("\n🎉 HOÀN THÀNH TẤT CẢ TESTS CHO MODULE 1!")
    print("=" * 60)
