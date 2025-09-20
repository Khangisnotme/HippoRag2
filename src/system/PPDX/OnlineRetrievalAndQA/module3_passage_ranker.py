"""
OnlineRetrievalAndQA/module3_passage_ranker.py
Module 3: Passage Ranking based on Filtered Triples (Xếp hạng Passage dựa trên Triple đã lọc)
Sử dụng filtered triples từ Module 2 để tính support score và re-rank passages từ Module 1

Mô tả chi tiết:
    Module này nhận raw passages từ Module 1 và filtered triples từ Module 2, 
    sau đó tính toán support score cho mỗi passage dựa trên số lượng filtered triples
    mà passage đó hỗ trợ, cuối cùng combine với retrieval score để tạo final ranking.

Kiến trúc chính:
    - PassageRankerConfig: Cấu hình ranking parameters
    - SupportScoreCalculator: Tính toán support score dựa trên triples
    - PassageRanker: Core ranking logic với multiple scoring methods
    - RankedPassage: Output data structure với comprehensive scoring
    - RankingResult: Container cho toàn bộ kết quả ranking

Workflow:
    Raw Passages + Filtered Triples → Support Score Calculation → Hybrid Ranking → Ranked Passages
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple, Set
import logging
import time
import json
from dataclasses import dataclass, asdict
from enum import Enum
import math
from collections import Counter, defaultdict
import datetime

# Shared utilities
from utils.utils_shared_general import (
    setup_logger,
    log_performance,
    validate_query,
    clean_text,
    save_json,
    load_json,
    merge_scores,
    PerformanceStats
)

# Module imports
from module1_dual_retrieval import RetrievedItem, RetrievalResult
from module2_triple_filter import FilteredTriple, FilteringResult, RelevanceLevel

# Setup logger with file output
log_file = Path("outputs/log/module3_passage_ranker_{}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
logger = setup_logger(__name__, log_file=log_file)

# ==================== ENUMS AND CONSTANTS ====================

class RankingStrategy(Enum):
    """
    Các chiến lược ranking khác nhau
    
    Định nghĩa cách thức combine retrieval score với support score:
    - RETRIEVAL_ONLY: Chỉ dùng retrieval score (baseline)
    - SUPPORT_ONLY: Chỉ dùng support score từ triples  
    - HYBRID_BALANCED: Cân bằng 50-50 giữa retrieval và support
    - HYBRID_RETRIEVAL_FOCUSED: Thiên về retrieval score (70-30)
    - HYBRID_SUPPORT_FOCUSED: Thiên về support score (30-70)
    - ADAPTIVE: Tự động điều chỉnh weights dựa trên data quality
    """
    RETRIEVAL_ONLY = "retrieval_only"
    SUPPORT_ONLY = "support_only"
    HYBRID_BALANCED = "hybrid_balanced"
    HYBRID_RETRIEVAL_FOCUSED = "hybrid_retrieval_focused"
    HYBRID_SUPPORT_FOCUSED = "hybrid_support_focused"
    ADAPTIVE = "adaptive"

    def get_weights(self) -> Tuple[float, float]:
        """
        Lấy weights cho (hybrid_retrieval_score, support_score)
        
        Returns:
            Tuple[float, float]: (alpha_retrieval, alpha_support)
        """
        weights = {
            RankingStrategy.RETRIEVAL_ONLY: (1.0, 0.0),
            RankingStrategy.SUPPORT_ONLY: (0.0, 1.0),
            RankingStrategy.HYBRID_BALANCED: (0.5, 0.5),
            RankingStrategy.HYBRID_RETRIEVAL_FOCUSED: (0.7, 0.3),
            RankingStrategy.HYBRID_SUPPORT_FOCUSED: (0.3, 0.7),
            RankingStrategy.ADAPTIVE: (0.6, 0.4)  # Default, sẽ được điều chỉnh
        }
        return weights[self]

class SupportCalculationMethod(Enum):
    """
    Các phương pháp tính support score
    
    Định nghĩa cách tính support score từ filtered triples:
    - COUNT_BASED: Đếm số lượng triples hỗ trợ passage
    - WEIGHTED_RELEVANCE: Tính theo trọng số relevance score của triples
    - QUALITY_WEIGHTED: Tính theo quality score (relevance + confidence)
    - LOG_SCALED: Áp dụng log scaling để giảm impact của outliers
    """
    COUNT_BASED = "count_based"
    WEIGHTED_RELEVANCE = "weighted_relevance"
    QUALITY_WEIGHTED = "quality_weighted"
    LOG_SCALED = "log_scaled"

# ==================== DATA CLASSES ====================

@dataclass
class PassageRankerConfig:
    """
    Cấu hình toàn diện cho hệ thống ranking passages
    
    Attributes:
        ranking_strategy (RankingStrategy): Chiến lược ranking chính
        support_calculation_method (SupportCalculationMethod): Phương pháp tính support score
        relevance_threshold (float): Ngưỡng relevance để tính support (0.0-1.0)
        max_passages_output (int): Số lượng passages tối đa trong output
        enable_score_normalization (bool): Có normalize scores không
        boost_factor_high_support (float): Hệ số boost cho passages có support cao
        penalty_factor_no_support (float): Hệ số penalty cho passages không có support
        enable_diversity_ranking (bool): Có áp dụng diversity ranking không
        diversity_threshold (float): Ngưỡng similarity để coi là duplicate (0.0-1.0)
        min_support_threshold (float): Support tối thiểu để không bị penalty
        adaptive_weight_adjustment (bool): Có tự động điều chỉnh weights không
    """
    # Core ranking parameters
    ranking_strategy: RankingStrategy = RankingStrategy.HYBRID_BALANCED
    support_calculation_method: SupportCalculationMethod = SupportCalculationMethod.WEIGHTED_RELEVANCE
    
    # Filtering and threshold parameters
    relevance_threshold: float = 0.3  # Chỉ count triples có relevance >= threshold
    max_passages_output: int = 10
    
    # Score processing parameters
    enable_score_normalization: bool = True
    boost_factor_high_support: float = 1.2  # Boost cho passages có nhiều support
    penalty_factor_no_support: float = 0.8  # Penalty cho passages không có support
    
    # Diversity parameters
    enable_diversity_ranking: bool = False  # Advanced feature
    diversity_threshold: float = 0.85  # Similarity threshold cho diversity
    
    # Advanced parameters
    min_support_threshold: float = 0.1  # Minimum support để avoid penalty
    adaptive_weight_adjustment: bool = True  # Auto-adjust weights based on data

@dataclass
class RankedPassage:
    """
    Passage đã được ranked với comprehensive scoring information
    
    Attributes:
        passage_id (str): ID unique của passage
        original_text (str): Nội dung gốc của passage
        hybrid_retrieval_score (float): Điểm từ Module 1 (hybrid score)
        support_score (float): Điểm support từ triples (0.0-1.0)
        final_score (float): Điểm cuối cùng sau khi combine
        rank (int): Thứ hạng final (1, 2, 3, ...)
        supporting_triples_count (int): Số lượng triples hỗ trợ passage này
        supporting_triples (List[str]): Danh sách IDs của supporting triples
        score_breakdown (Dict): Chi tiết breakdown các scores
        ranking_metadata (Dict): Metadata về quá trình ranking
    """
    passage_id: str
    original_text: str
    hybrid_retrieval_score: float
    support_score: float
    final_score: float
    rank: int
    supporting_triples_count: int
    supporting_triples: List[str]
    score_breakdown: Dict[str, float]
    ranking_metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi RankedPassage object thành dictionary
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        return asdict(self)
    
    def get_support_ratio(self) -> float:
        """
        Tính tỷ lệ support so với retrieval score
        
        Returns:
            float: Support ratio (support_score / hybrid_retrieval_score)
        """
        if self.hybrid_retrieval_score == 0:
            return float('inf') if self.support_score > 0 else 0
        return self.support_score / self.hybrid_retrieval_score
    
    def has_strong_support(self, threshold: int = 2) -> bool:
        """
        Kiểm tra passage có support mạnh không
        
        Args:
            threshold (int): Ngưỡng số triples để coi là strong support
            
        Returns:
            bool: True nếu có strong support
        """
        return self.supporting_triples_count >= threshold
    
    def get_summary(self) -> str:
        """
        Tạo summary ngắn gọn về ranked passage
        
        Returns:
            str: Summary string
        """
        return (f"Rank {self.rank}: {self.passage_id} | "
                f"Final: {self.final_score:.3f} "
                f"(Ret: {self.hybrid_retrieval_score:.3f}, Sup: {self.support_score:.3f}) | "
                f"Triples: {self.supporting_triples_count}")

@dataclass
class RankingResult:
    """
    Kết quả hoàn chỉnh của quá trình ranking với comprehensive statistics
    
    Attributes:
        ranked_passages (List[RankedPassage]): Passages đã được ranked
        original_passage_count (int): Số lượng passages ban đầu
        final_passage_count (int): Số lượng passages sau ranking
        ranking_time (float): Thời gian thực hiện ranking (giây)
        query (str): Query gốc
        statistics (Dict): Thống kê chi tiết về quá trình ranking
        ranking_config (PassageRankerConfig): Config được sử dụng
    """
    ranked_passages: List[RankedPassage]
    original_passage_count: int
    final_passage_count: int
    ranking_time: float
    query: str
    statistics: Dict[str, Any]
    ranking_config: PassageRankerConfig
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi RankingResult thành dictionary
        
        Returns:
            Dict[str, Any]: Dictionary representation
        """
        result = asdict(self)
        result['ranking_config'] = asdict(self.ranking_config)
        result['ranking_config']['ranking_strategy'] = self.ranking_config.ranking_strategy.value
        result['ranking_config']['support_calculation_method'] = self.ranking_config.support_calculation_method.value
        return result
    
    def save_to_file(self, filepath: Path):
        """
        Lưu kết quả ranking vào file JSON
        
        Args:
            filepath (Path): Đường dẫn file
        """
        save_json(self.to_dict(), filepath, indent=2)
        logger.info(f"💾 Đã lưu kết quả ranking vào file: {filepath}")
        logger.info(f"   📊 Passages: {self.original_passage_count} → {self.final_passage_count}")
        logger.info(f"   ⏱️ Thời gian: {self.ranking_time:.2f} giây")
    
    def get_ranking_efficiency(self) -> float:
        """
        Tính hiệu suất ranking
        
        Returns:
            float: Efficiency ratio
        """
        if self.original_passage_count == 0:
            return 0.0
        return self.final_passage_count / self.original_passage_count
    
    def get_support_distribution(self) -> Dict[str, int]:
        """
        Thống kê phân bố support levels
        
        Returns:
            Dict[str, int]: Support distribution
        """
        distribution = {
            'no_support': 0,
            'low_support': 0,    # 1-2 triples
            'medium_support': 0, # 3-5 triples
            'high_support': 0    # 6+ triples
        }
        
        for passage in self.ranked_passages:
            count = passage.supporting_triples_count
            if count == 0:
                distribution['no_support'] += 1
            elif count <= 2:
                distribution['low_support'] += 1
            elif count <= 5:
                distribution['medium_support'] += 1
            else:
                distribution['high_support'] += 1
        
        return distribution

# ==================== CORE COMPONENTS ====================

class SupportScoreCalculator:
    """
    Calculator cho support scores dựa trên filtered triples
    
    Class này implement các phương pháp khác nhau để tính support score
    cho passages dựa trên các filtered triples từ Module 2.
    """
    
    def __init__(self, config: PassageRankerConfig):
        """
        Khởi tạo SupportScoreCalculator
        
        Args:
            config (PassageRankerConfig): Cấu hình ranking
        """
        self.config = config
        self.passage_triple_mapping = defaultdict(list)  # passage_id -> [triple_ids]
        self.triple_lookup = {}  # triple_id -> FilteredTriple
        
        logger.info("📊 Khởi tạo SupportScoreCalculator...")
        logger.info(f"   🧮 Method: {config.support_calculation_method.value}")
        logger.info(f"   🎯 Relevance threshold: {config.relevance_threshold}")
    
    def build_support_mapping(self, filtered_triples: List[FilteredTriple]):
        """
        Xây dựng mapping giữa passages và supporting triples
        
        Args:
            filtered_triples (List[FilteredTriple]): Filtered triples từ Module 2
        """
        logger.info(f"🔗 Đang xây dựng support mapping cho {len(filtered_triples)} filtered triples...")
        
        # Clear previous mappings
        self.passage_triple_mapping.clear()
        self.triple_lookup.clear()
        
        relevant_triples_count = 0
        
        for triple in filtered_triples:
            # Store triple lookup
            self.triple_lookup[triple.triple_id] = triple
            
            # Only consider triples above relevance threshold
            if triple.query_relevance_score >= self.config.relevance_threshold:
                passage_id = triple.source_passage_id
                if passage_id:  # Ensure passage_id exists
                    self.passage_triple_mapping[passage_id].append(triple.triple_id)
                    relevant_triples_count += 1
        
        passages_with_support = len(self.passage_triple_mapping)
        logger.info(f"✅ Support mapping completed:")
        logger.info(f"   📊 Relevant triples: {relevant_triples_count}/{len(filtered_triples)}")
        logger.info(f"   📄 Passages with support: {passages_with_support}")
        
        # Log top supported passages
        if self.passage_triple_mapping:
            sorted_passages = sorted(
                self.passage_triple_mapping.items(), 
                key=lambda x: len(x[1]), 
                reverse=True
            )
            logger.info(f"   🏆 Top supported passages:")
            for i, (passage_id, triple_ids) in enumerate(sorted_passages[:3], 1):
                logger.info(f"      {i}. {passage_id}: {len(triple_ids)} triples")
    
    def calculate_support_score(self, passage_id: str) -> Tuple[float, int, List[str]]:
        """
        Tính support score cho một passage
        
        Args:
            passage_id (str): ID của passage
            
        Returns:
            Tuple[float, int, List[str]]: (support_score, count, supporting_triple_ids)
        """
        supporting_triple_ids = self.passage_triple_mapping.get(passage_id, [])
        
        if not supporting_triple_ids:
            return 0.0, 0, []
        
        # Get supporting triples
        supporting_triples = [
            self.triple_lookup[triple_id] 
            for triple_id in supporting_triple_ids 
            if triple_id in self.triple_lookup
        ]
        
        # Calculate score based on method
        if self.config.support_calculation_method == SupportCalculationMethod.COUNT_BASED:
            score = self._calculate_count_based_score(supporting_triples)
        elif self.config.support_calculation_method == SupportCalculationMethod.WEIGHTED_RELEVANCE:
            score = self._calculate_weighted_relevance_score(supporting_triples)
        elif self.config.support_calculation_method == SupportCalculationMethod.QUALITY_WEIGHTED:
            score = self._calculate_quality_weighted_score(supporting_triples)
        elif self.config.support_calculation_method == SupportCalculationMethod.LOG_SCALED:
            score = self._calculate_log_scaled_score(supporting_triples)
        else:
            score = self._calculate_weighted_relevance_score(supporting_triples)  # Default
        
        return score, len(supporting_triples), supporting_triple_ids
    
    def _calculate_count_based_score(self, supporting_triples: List[FilteredTriple]) -> float:
        """
        Tính support score dựa trên số lượng triples
        
        Args:
            supporting_triples (List[FilteredTriple]): Supporting triples
            
        Returns:
            float: Count-based support score
        """
        count = len(supporting_triples)
        # Normalize using log scaling to prevent very high scores
        if count == 0:
            return 0.0
        elif count == 1:
            return 0.3
        elif count == 2:
            return 0.5
        elif count <= 5:
            return 0.7
        else:
            return min(0.9, 0.7 + 0.05 * (count - 5))  # Cap at 0.9
    
    def _calculate_weighted_relevance_score(self, supporting_triples: List[FilteredTriple]) -> float:
        """
        Tính support score dựa trên tổng relevance scores
        
        Args:
            supporting_triples (List[FilteredTriple]): Supporting triples
            
        Returns:
            float: Weighted relevance support score
        """
        if not supporting_triples:
            return 0.0
        
        # Sum of all relevance scores
        total_relevance = sum(triple.query_relevance_score for triple in supporting_triples)
        
        # Average relevance
        avg_relevance = total_relevance / len(supporting_triples)
        
        # Apply count boost (more triples = higher score)
        count_boost = min(1.0, len(supporting_triples) / 5.0)  # Max boost at 5 triples
        
        # Combine average relevance with count boost
        final_score = (avg_relevance * 0.7) + (count_boost * 0.3)
        
        return min(final_score, 1.0)  # Cap at 1.0
    
    def _calculate_quality_weighted_score(self, supporting_triples: List[FilteredTriple]) -> float:
        """
        Tính support score dựa trên quality scores (relevance + confidence)
        
        Args:
            supporting_triples (List[FilteredTriple]): Supporting triples
            
        Returns:
            float: Quality weighted support score
        """
        if not supporting_triples:
            return 0.0
        
        quality_scores = [triple.get_quality_score() for triple in supporting_triples]
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        # Apply count boost
        count_boost = min(1.0, len(supporting_triples) / 5.0)
        
        # Combine quality with count
        final_score = (avg_quality * 0.8) + (count_boost * 0.2)
        
        return min(final_score, 1.0)
    
    def _calculate_log_scaled_score(self, supporting_triples: List[FilteredTriple]) -> float:
        """
        Tính support score với log scaling để handle outliers
        
        Args:
            supporting_triples (List[FilteredTriple]): Supporting triples
            
        Returns:
            float: Log scaled support score
        """
        if not supporting_triples:
            return 0.0
        
        # Base score from relevance
        total_relevance = sum(triple.query_relevance_score for triple in supporting_triples)
        
        # Log scaling to prevent extreme values
        log_scaled_count = math.log(len(supporting_triples) + 1) / math.log(6)  # Normalize to ~1.0 at 5 triples
        log_scaled_relevance = math.log(total_relevance + 1) / math.log(6)
        
        # Combine
        final_score = (log_scaled_relevance * 0.6) + (log_scaled_count * 0.4)
        
        return min(final_score, 1.0)
    
    def get_support_statistics(self) -> Dict[str, Any]:
        """
        Lấy thống kê về support mapping
        
        Returns:
            Dict[str, Any]: Support statistics
        """
        if not self.passage_triple_mapping:
            return {
                'total_passages_with_support': 0,
                'total_supporting_triples': 0,
                'avg_triples_per_passage': 0,
                'max_triples_per_passage': 0
            }
        
        triple_counts = [len(triple_ids) for triple_ids in self.passage_triple_mapping.values()]
        
        return {
            'total_passages_with_support': len(self.passage_triple_mapping),
            'total_supporting_triples': sum(triple_counts),
            'avg_triples_per_passage': sum(triple_counts) / len(triple_counts),
            'max_triples_per_passage': max(triple_counts),
            'min_triples_per_passage': min(triple_counts),
            'support_distribution': {
                '1_triple': sum(1 for count in triple_counts if count == 1),
                '2-3_triples': sum(1 for count in triple_counts if 2 <= count <= 3),
                '4-5_triples': sum(1 for count in triple_counts if 4 <= count <= 5),
                '6+_triples': sum(1 for count in triple_counts if count >= 6)
            }
        }

class PassageRanker:
    """
    Main class cho ranking passages dựa trên retrieval scores và support scores
    
    Class này implement logic chính để combine retrieval scores từ Module 1
    với support scores tính từ filtered triples của Module 2.
    """
    
    def __init__(self, config: Optional[PassageRankerConfig] = None):
        """
        Khởi tạo PassageRanker
        
        Args:
            config (Optional[PassageRankerConfig]): Cấu hình ranking
        """
        self.config = config or PassageRankerConfig()
        self.support_calculator = SupportScoreCalculator(self.config)
        
        logger.info("🏆 Khởi tạo PassageRanker...")
        logger.info(f"   📊 Strategy: {self.config.ranking_strategy.value}")
        logger.info(f"   🧮 Support method: {self.config.support_calculation_method.value}")
        logger.info(f"   📝 Max output: {self.config.max_passages_output}")
        logger.info(f"   ⚖️ Score normalization: {'Bật' if self.config.enable_score_normalization else 'Tắt'}")
    
    def rank_passages(self, raw_passages: List[RetrievedItem], 
                     filtered_triples: List[FilteredTriple],
                     query: str) -> RankingResult:
        """
        Main method để rank passages dựa trên retrieval scores và support scores
        
        Args:
            raw_passages (List[RetrievedItem]): Raw passages từ Module 1
            filtered_triples (List[FilteredTriple]): Filtered triples từ Module 2
            query (str): Query gốc
            
        Returns:
            RankingResult: Kết quả ranking hoàn chỉnh
        """
        logger.info("=" * 60)
        logger.info("🏆 BẮT ĐẦU PASSAGE RANKING")
        logger.info("=" * 60)
        logger.info(f"📝 Query: '{query}'")
        logger.info(f"📄 Raw passages: {len(raw_passages)}")
        logger.info(f"🔗 Filtered triples: {len(filtered_triples)}")
        logger.info(f"🎯 Strategy: {self.config.ranking_strategy.value}")
        
        # Log raw passages với thứ tự ban đầu
        logger.info("\n📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):")
        logger.info("-" * 60)
        # Sort raw passages by embedding score for clear comparison
        sorted_raw = sorted(raw_passages, key=lambda x: x.embedding_score, reverse=True)
        for i, passage in enumerate(sorted_raw, 1):
            logger.info(f"   {i}. ID: {passage.item_id}")
            logger.info(f"      Text: {passage.text[:100]}...")
            logger.info(f"      Scores: BM25={passage.bm25_score:.3f}, Embed={passage.embedding_score:.3f}, Hybrid={passage.hybrid_score:.3f}")
            logger.info(f"      Metadata: {passage.metadata}")
        
        start_time = time.time()
        
        # Validate inputs
        if not raw_passages:
            logger.warning("⚠️ Không có raw passages để rank")
            return self._create_empty_result(query, 0, "no_passages")
        
        if not validate_query(query):
            logger.error("❌ Invalid query")
            return self._create_empty_result(query, len(raw_passages), "invalid_query")
        
        # Step 1: Build support mapping
        logger.info(f"\n📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING")
        logger.info("-" * 40)
        self.support_calculator.build_support_mapping(filtered_triples)
        
        # Step 2: Calculate scores for all passages
        logger.info(f"\n🧮 BƯỚC 2: TÍNH TOÁN SCORES")
        logger.info("-" * 40)
        scored_passages = self._calculate_all_scores(raw_passages)
        
        # Step 3: Apply ranking strategy
        logger.info(f"\n🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY")
        logger.info("-" * 40)
        ranked_passages = self._apply_ranking_strategy(scored_passages, query)
        
        # Step 4: Apply final processing
        logger.info(f"\n🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG")
        logger.info("-" * 40)
        final_passages = self._apply_final_processing(ranked_passages)
        
        # Log final passages với thứ tự mới và giải thích
        logger.info("\n🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):")
        logger.info("-" * 60)
        logger.info("   Giải thích thứ tự mới:")
        logger.info("   1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)")
        logger.info("   2. Support score được tính từ số lượng và chất lượng của supporting triples")
        logger.info("   3. Passages có nhiều supporting triples sẽ được boost lên")
        logger.info("   4. Passages không có support sẽ bị penalty")
        logger.info("-" * 60)
        
        for passage in final_passages:
            logger.info(f"   Rank {passage.rank}. ID: {passage.passage_id}")
            logger.info(f"      Text: {passage.original_text[:100]}...")
            logger.info(f"      Scores:")
            logger.info(f"         - Final score: {passage.final_score:.3f}")
            logger.info(f"         - Retrieval score: {passage.hybrid_retrieval_score:.3f}")
            logger.info(f"         - Support score: {passage.support_score:.3f}")
            logger.info(f"      Supporting triples: {passage.supporting_triples_count}")
            if passage.supporting_triples:
                logger.info(f"      Triple IDs: {', '.join(passage.supporting_triples[:3])}...")
            logger.info(f"      Score breakdown: {passage.score_breakdown}")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Step 5: Create result với statistics
        logger.info(f"\n📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ")
        logger.info("-" * 40)
        statistics = self._create_ranking_statistics(
            raw_passages, final_passages, filtered_triples, total_time
        )
        
        result = RankingResult(
            ranked_passages=final_passages,
            original_passage_count=len(raw_passages),
            final_passage_count=len(final_passages),
            ranking_time=total_time,
            query=query,
            statistics=statistics,
            ranking_config=self.config
        )
        
        # Log final summary
        self._log_ranking_summary(result)
        
        return result
    
    def _calculate_all_scores(self, raw_passages: List[RetrievedItem]) -> List[Dict[str, Any]]:
        """
        Tính toán scores cho tất cả passages
        
        Args:
            raw_passages (List[RetrievedItem]): Raw passages
            
        Returns:
            List[Dict[str, Any]]: Scored passages với đầy đủ thông tin
        """
        logger.info(f"🧮 Đang tính scores cho {len(raw_passages)} passages...")
        
        scored_passages = []
        hybrid_retrieval_scores = []
        support_scores = []
        
        for i, passage in enumerate(raw_passages, 1):
            # Get retrieval score từ Module 1
            hybrid_retrieval_score = passage.hybrid_score
            hybrid_retrieval_scores.append(hybrid_retrieval_score)
            
            # Calculate support score
            support_score, support_count, supporting_triple_ids = \
                self.support_calculator.calculate_support_score(passage.item_id)
            support_scores.append(support_score)
            
            # Create scored passage info
            scored_passage = {
                'passage_id': passage.item_id,
                'original_text': passage.text,
                'hybrid_retrieval_score': hybrid_retrieval_score,
                'support_score': support_score,
                'supporting_triples_count': support_count,
                'supporting_triples': supporting_triple_ids,
                'original_passage': passage,
                'score_breakdown': {
                    'bm25_score': passage.bm25_score,
                    'embedding_score': passage.embedding_score,
                    'hybrid_score': passage.hybrid_score,
                    'support_score': support_score,
                    'support_count': support_count
                }
            }
            
            scored_passages.append(scored_passage)
            
            if i % 5 == 0 or i == len(raw_passages):
                logger.info(f"   📊 Processed {i}/{len(raw_passages)} passages")
        
        # Log score distributions
        if hybrid_retrieval_scores and support_scores:
            logger.info(f"📈 Score distributions:")
            logger.info(f"   📊 Retrieval scores: min={min(hybrid_retrieval_scores):.3f}, max={max(hybrid_retrieval_scores):.3f}, avg={sum(hybrid_retrieval_scores)/len(hybrid_retrieval_scores):.3f}")
            logger.info(f"   🔗 Support scores: min={min(support_scores):.3f}, max={max(support_scores):.3f}, avg={sum(support_scores)/len(support_scores):.3f}")
            
            # Count passages by support level
            no_support = sum(1 for score in support_scores if score == 0)
            low_support = sum(1 for score in support_scores if 0 < score <= 0.3)
            medium_support = sum(1 for score in support_scores if 0.3 < score <= 0.7)
            high_support = sum(1 for score in support_scores if score > 0.7)
            
            logger.info(f"   📄 Support levels: no={no_support}, low={low_support}, medium={medium_support}, high={high_support}")
        
        logger.info(f"✅ Hoàn thành tính scores cho {len(scored_passages)} passages")
        return scored_passages
    
    def _apply_ranking_strategy(self, scored_passages: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Áp dụng ranking strategy để tính final scores
        
        Args:
            scored_passages (List[Dict]): Passages với scores
            query (str): Query gốc
            
        Returns:
            List[Dict[str, Any]]: Passages với final scores
        """
        logger.info(f"🏆 Áp dụng ranking strategy: {self.config.ranking_strategy.value}")
        
        # Get weights based on strategy
        if self.config.ranking_strategy == RankingStrategy.ADAPTIVE:
            alpha_retrieval, alpha_support = self._calculate_adaptive_weights(scored_passages)
            logger.info(f"   🧠 Adaptive weights: retrieval={alpha_retrieval:.2f}, support={alpha_support:.2f}")
        else:
            alpha_retrieval, alpha_support = self.config.ranking_strategy.get_weights()
            logger.info(f"   ⚖️ Fixed weights: retrieval={alpha_retrieval:.2f}, support={alpha_support:.2f}")
        
        # Normalize scores if enabled
        if self.config.enable_score_normalization:
            scored_passages = self._normalize_scores(scored_passages)
            logger.info("   📊 Scores đã được normalized")
        
        # Calculate final scores
        for passage in scored_passages:
            hybrid_retrieval_score = passage['hybrid_retrieval_score']
            support_score = passage['support_score']
            
            # Base final score
            final_score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
            
            # Apply boost/penalty factors
            if support_score > 0.7:  # High support boost
                final_score *= self.config.boost_factor_high_support
                logger.debug(f"   🚀 Boost applied to {passage['passage_id']}: {final_score:.3f}")
            elif support_score < self.config.min_support_threshold:  # Low support penalty
                final_score *= self.config.penalty_factor_no_support
                logger.debug(f"   ⬇️ Penalty applied to {passage['passage_id']}: {final_score:.3f}")
            
            # Cap final score at 1.0
            final_score = min(final_score, 1.0)
            
            passage['final_score'] = final_score
            
            # Update score breakdown
            passage['score_breakdown'].update({
                'alpha_retrieval': alpha_retrieval,
                'alpha_support': alpha_support,
                'base_final_score': (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score),
                'final_score_after_modifiers': final_score
            })
        
        # Sort by final score descending
        scored_passages.sort(key=lambda x: x['final_score'], reverse=True)
        
        logger.info(f"✅ Final scores calculated và sorted")
        if scored_passages:
            top_passage = scored_passages[0]
            logger.info(f"   🏆 Top passage: {top_passage['passage_id']} với score {top_passage['final_score']:.3f}")
        
        return scored_passages
    
    def _calculate_adaptive_weights(self, scored_passages: List[Dict[str, Any]]) -> Tuple[float, float]:
        """
        Tính adaptive weights dựa trên chất lượng data
        
        Args:
            scored_passages (List[Dict]): Scored passages
            
        Returns:
            Tuple[float, float]: (alpha_retrieval, alpha_support)
        """
        hybrid_retrieval_scores = [p['hybrid_retrieval_score'] for p in scored_passages]
        support_scores = [p['support_score'] for p in scored_passages]
        
        # Calculate quality metrics
        retrieval_variance = self._calculate_variance(hybrid_retrieval_scores)
        support_variance = self._calculate_variance(support_scores)
        
        # Calculate support coverage (percentage of passages with support > 0)
        passages_with_support = sum(1 for score in support_scores if score > 0)
        support_coverage = passages_with_support / len(support_scores) if support_scores else 0
        
        logger.info(f"   📊 Adaptive metrics:")
        logger.info(f"      📈 Retrieval variance: {retrieval_variance:.3f}")
        logger.info(f"      🔗 Support variance: {support_variance:.3f}")
        logger.info(f"      📄 Support coverage: {support_coverage:.2%}")
        
        # Adaptive logic
        if support_coverage < 0.3:  # Low support coverage
            alpha_retrieval, alpha_support = 0.8, 0.2
            logger.info("   🎯 Low support coverage → Retrieval focused")
        elif support_coverage > 0.7 and support_variance > 0.1:  # High support with good variance
            alpha_retrieval, alpha_support = 0.4, 0.6
            logger.info("   🎯 High quality support → Support focused")
        else:  # Balanced case
            alpha_retrieval, alpha_support = 0.6, 0.4
            logger.info("   🎯 Balanced case → Moderate weights")
        
        return alpha_retrieval, alpha_support
    
    def _calculate_variance(self, scores: List[float]) -> float:
        """Tính variance của scores"""
        if len(scores) <= 1:
            return 0.0
        
        mean = sum(scores) / len(scores)
        variance = sum((score - mean) ** 2 for score in scores) / len(scores)
        return variance
    
    def _normalize_scores(self, scored_passages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize retrieval và support scores về [0, 1] range
        
        Args:
            scored_passages (List[Dict]): Passages với scores
            
        Returns:
            List[Dict[str, Any]]: Passages với normalized scores
        """
        hybrid_retrieval_scores = [p['hybrid_retrieval_score'] for p in scored_passages]
        support_scores = [p['support_score'] for p in scored_passages]
        
        # Normalize retrieval scores
        if hybrid_retrieval_scores:
            min_ret, max_ret = min(hybrid_retrieval_scores), max(hybrid_retrieval_scores)
            if max_ret > min_ret:
                for passage in scored_passages:
                    old_score = passage['hybrid_retrieval_score']
                    new_score = (old_score - min_ret) / (max_ret - min_ret)
                    passage['hybrid_retrieval_score'] = new_score
                    passage['score_breakdown']['normalized_retrieval'] = new_score
        
        # Normalize support scores (usually already in [0,1] but ensure it)
        if support_scores:
            max_sup = max(support_scores)
            if max_sup > 1.0:  # Only normalize if exceeds 1.0
                for passage in scored_passages:
                    old_score = passage['support_score']
                    new_score = old_score / max_sup
                    passage['support_score'] = new_score
                    passage['score_breakdown']['normalized_support'] = new_score
        
        return scored_passages
    
    def _apply_final_processing(self, ranked_passages: List[Dict[str, Any]]) -> List[RankedPassage]:
        """
        Áp dụng final processing và convert thành RankedPassage objects
        
        Args:
            ranked_passages (List[Dict]): Ranked passages
            
        Returns:
            List[RankedPassage]: Final ranked passages
        """
        logger.info(f"🔧 Áp dụng final processing...")
        
        # Apply max output limit
        limited_passages = ranked_passages[:self.config.max_passages_output]
        logger.info(f"   📊 Limited output: {len(ranked_passages)} → {len(limited_passages)} passages")
        
        # Apply diversity ranking if enabled
        if self.config.enable_diversity_ranking:
            limited_passages = self._apply_diversity_ranking(limited_passages)
            logger.info(f"   🌈 Diversity ranking applied")
        
        # Convert to RankedPassage objects
        final_passages = []
        for rank, passage_data in enumerate(limited_passages, 1):
            ranked_passage = RankedPassage(
                passage_id=passage_data['passage_id'],
                original_text=passage_data['original_text'],
                hybrid_retrieval_score=passage_data['hybrid_retrieval_score'],
                support_score=passage_data['support_score'],
                final_score=passage_data['final_score'],
                rank=rank,
                supporting_triples_count=passage_data['supporting_triples_count'],
                supporting_triples=passage_data['supporting_triples'],
                score_breakdown=passage_data['score_breakdown'],
                ranking_metadata={
                    'ranking_strategy': self.config.ranking_strategy.value,
                    'support_method': self.config.support_calculation_method.value,
                    'processing_timestamp': time.time(),
                    'original_rank_from_retrieval': None  # Could track original ranking
                }
            )
            final_passages.append(ranked_passage)
        
        logger.info(f"✅ Final processing hoàn thành: {len(final_passages)} ranked passages")
        return final_passages
    
    def _apply_diversity_ranking(self, passages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Áp dụng diversity ranking để tránh duplicate/similar passages
        
        Args:
            passages (List[Dict]): Ranked passages
            
        Returns:
            List[Dict[str, Any]]: Diversified passages
        """
        # Simple diversity implementation based on text similarity
        # Advanced version would use embedding similarity
        
        diversified = []
        seen_texts = set()
        
        for passage in passages:
            text = passage['original_text'].lower()
            
            # Simple duplicate detection based on first 100 characters
            text_signature = text[:100]
            
            is_duplicate = False
            for seen_sig in seen_texts:
                # Simple similarity check
                common_chars = len(set(text_signature) & set(seen_sig))
                similarity = common_chars / max(len(text_signature), len(seen_sig), 1)
                
                if similarity > self.config.diversity_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                diversified.append(passage)
                seen_texts.add(text_signature)
            else:
                logger.debug(f"   🔄 Filtered duplicate: {passage['passage_id']}")
        
        logger.info(f"   🌈 Diversity filtering: {len(passages)} → {len(diversified)}")
        return diversified
    
    def _create_ranking_statistics(self, raw_passages: List[RetrievedItem], 
                                  final_passages: List[RankedPassage],
                                  filtered_triples: List[FilteredTriple],
                                  processing_time: float) -> Dict[str, Any]:
        """
        Tạo comprehensive statistics cho ranking process
        
        Args:
            raw_passages (List[RetrievedItem]): Original passages
            final_passages (List[RankedPassage]): Final ranked passages
            filtered_triples (List[FilteredTriple]): Input triples
            processing_time (float): Total processing time
            
        Returns:
            Dict[str, Any]: Comprehensive statistics
        """
        logger.info("📈 Tạo ranking statistics...")
        
        # Basic counts
        original_count = len(raw_passages)
        final_count = len(final_passages)
        
        # Score statistics
        if final_passages:
            hybrid_retrieval_scores = [p.hybrid_retrieval_score for p in final_passages]
            support_scores = [p.support_score for p in final_passages]
            final_scores = [p.final_score for p in final_passages]
            
            score_stats = {
                'hybrid_retrieval_scores': {
                    'min': min(hybrid_retrieval_scores),
                    'max': max(hybrid_retrieval_scores),
                    'avg': sum(hybrid_retrieval_scores) / len(hybrid_retrieval_scores),
                    'median': sorted(hybrid_retrieval_scores)[len(hybrid_retrieval_scores) // 2]
                },
                'support_scores': {
                    'min': min(support_scores),
                    'max': max(support_scores),
                    'avg': sum(support_scores) / len(support_scores),
                    'median': sorted(support_scores)[len(support_scores) // 2]
                },
                'final_scores': {
                    'min': min(final_scores),
                    'max': max(final_scores),
                    'avg': sum(final_scores) / len(final_scores),
                    'median': sorted(final_scores)[len(final_scores) // 2]
                }
            }
        else:
            score_stats = {
                'hybrid_retrieval_scores': {'min': 0, 'max': 0, 'avg': 0, 'median': 0},
                'support_scores': {'min': 0, 'max': 0, 'avg': 0, 'median': 0},
                'final_scores': {'min': 0, 'max': 0, 'avg': 0, 'median': 0}
            }
        
        # Support statistics
        support_stats = self.support_calculator.get_support_statistics()
        
        # Ranking changes analysis
        ranking_changes = self._analyze_ranking_changes(raw_passages, final_passages)
        
        # Performance metrics
        performance_stats = {
            'total_time_seconds': processing_time,
            'passages_per_second': original_count / processing_time if processing_time > 0 else 0,
            'avg_time_per_passage': processing_time / original_count if original_count > 0 else 0
        }
        
        # Configuration info
        config_stats = {
            'ranking_strategy': self.config.ranking_strategy.value,
            'support_calculation_method': self.config.support_calculation_method.value,
            'relevance_threshold': self.config.relevance_threshold,
            'max_passages_output': self.config.max_passages_output,
            'score_normalization_enabled': self.config.enable_score_normalization,
            'diversity_ranking_enabled': self.config.enable_diversity_ranking
        }
        
        return {
            'processing_counts': {
                'original_passages': original_count,
                'final_passages': final_count,
                'filtered_triples_used': len(filtered_triples)
            },
            'score_statistics': score_stats,
            'support_statistics': support_stats,
            'ranking_changes': ranking_changes,
            'performance_metrics': performance_stats,
            'configuration': config_stats,
            'timestamp': time.time()
        }
    
    def _analyze_ranking_changes(self, raw_passages: List[RetrievedItem], 
                                final_passages: List[RankedPassage]) -> Dict[str, Any]:
        """
        Phân tích những thay đổi trong ranking so với original retrieval order
        
        Args:
            raw_passages (List[RetrievedItem]): Original passages (sorted by hybrid score)
            final_passages (List[RankedPassage]): Final ranked passages
            
        Returns:
            Dict[str, Any]: Ranking change analysis
        """
        # Create mapping from passage_id to original rank
        original_ranks = {passage.item_id: i + 1 for i, passage in enumerate(raw_passages)}
        
        # Calculate rank changes
        rank_changes = []
        significant_changes = 0
        
        for final_passage in final_passages:
            original_rank = original_ranks.get(final_passage.passage_id, len(raw_passages) + 1)
            final_rank = final_passage.rank
            
            rank_change = original_rank - final_rank  # Positive = moved up
            rank_changes.append(rank_change)
            
            if abs(rank_change) >= 3:  # Significant change threshold
                significant_changes += 1
        
        # Statistics
        if rank_changes:
            avg_rank_change = sum(rank_changes) / len(rank_changes)
            max_improvement = max(rank_changes)
            max_decline = min(rank_changes)
        else:
            avg_rank_change = max_improvement = max_decline = 0
        
        return {
            'total_rank_changes': len(rank_changes),
            'significant_changes': significant_changes,
            'avg_rank_change': avg_rank_change,
            'max_improvement': max_improvement,
            'max_decline': max_decline,
            'passages_moved_up': sum(1 for change in rank_changes if change > 0),
            'passages_moved_down': sum(1 for change in rank_changes if change < 0),
            'passages_unchanged': sum(1 for change in rank_changes if change == 0)
        }
    
    def _create_empty_result(self, query: str, original_count: int, reason: str) -> RankingResult:
        """
        Tạo empty RankingResult khi có lỗi
        
        Args:
            query (str): Original query
            original_count (int): Number of original passages
            reason (str): Reason for empty result
            
        Returns:
            RankingResult: Empty result với error info
        """
        logger.warning(f"🔄 Tạo empty ranking result (reason: {reason})")
        
        return RankingResult(
            ranked_passages=[],
            original_passage_count=original_count,
            final_passage_count=0,
            ranking_time=0.0,
            query=query,
            statistics={
                'error_info': {
                    'reason': reason,
                    'timestamp': time.time()
                }
            },
            ranking_config=self.config
        )
    
    def _log_ranking_summary(self, result: RankingResult):
        """
        Log comprehensive summary của ranking process
        
        Args:
            result (RankingResult): Final ranking result
        """
        logger.info("=" * 60)
        logger.info("🎉 PASSAGE RANKING HOÀN THÀNH")
        logger.info("=" * 60)
        
        # Basic metrics
        logger.info(f"📊 KẾT QUẢ TỔNG QUAN:")
        logger.info(f"   📝 Query: '{result.query}'")
        logger.info(f"   ⏱️ Thời gian xử lý: {result.ranking_time:.2f} giây")
        logger.info(f"   📄 Passages: {result.original_passage_count} → {result.final_passage_count}")
        logger.info(f"   📈 Efficiency: {result.get_ranking_efficiency():.2%}")
        
        # Top ranked passages
        if result.ranked_passages:
            logger.info(f"\n🏆 TOP 5 RANKED PASSAGES:")
            for i, passage in enumerate(result.ranked_passages[:5], 1):
                logger.info(f"   {i}. {passage.get_summary()}")
                logger.info(f"      📝 Text: {passage.original_text[:80]}...")
        
        # Support distribution
        support_dist = result.get_support_distribution()
        logger.info(f"\n📊 PHÂN BỐ SUPPORT:")
        for level, count in support_dist.items():
            percentage = (count / result.final_passage_count * 100) if result.final_passage_count > 0 else 0
            logger.info(f"   {level}: {count} passages ({percentage:.1f}%)")
        
        # Ranking changes
        stats = result.statistics
        if 'ranking_changes' in stats:
            changes = stats['ranking_changes']
            logger.info(f"\n🔄 THAY ĐỔI RANKING:")
            logger.info(f"   ⬆️ Moved up: {changes['passages_moved_up']}")
            logger.info(f"   ⬇️ Moved down: {changes['passages_moved_down']}")
            logger.info(f"   ➡️ Unchanged: {changes['passages_unchanged']}")
            logger.info(f"   📈 Max improvement: {changes['max_improvement']} positions")
            logger.info(f"   📉 Max decline: {abs(changes['max_decline'])} positions")
        
        # Performance metrics
        if 'performance_metrics' in stats:
            perf = stats['performance_metrics']
            logger.info(f"\n⚡ PERFORMANCE:")
            logger.info(f"   🏃 Passages/giây: {perf['passages_per_second']:.1f}")
            logger.info(f"   ⏱️ Avg time/passage: {perf['avg_time_per_passage']:.3f}s")
        
        logger.info("=" * 60)

# ==================== UTILITY FUNCTIONS ====================

def create_default_ranking_config() -> PassageRankerConfig:
    """
    Tạo cấu hình mặc định cho Passage Ranker
    
    Returns:
        PassageRankerConfig: Default configuration
    """
    logger.info("⚙️ Tạo default PassageRankerConfig...")
    
    config = PassageRankerConfig(
        ranking_strategy=RankingStrategy.HYBRID_BALANCED,
        support_calculation_method=SupportCalculationMethod.WEIGHTED_RELEVANCE,
        relevance_threshold=0.3,
        max_passages_output=10,
        enable_score_normalization=True,
        boost_factor_high_support=1.2,
        penalty_factor_no_support=0.8
    )
    
    logger.info("✅ Default ranking config đã được tạo")
    return config

def quick_rank_passages(raw_passages: List[RetrievedItem], 
                       filtered_triples: List[FilteredTriple],
                       query: str,
                       strategy: str = "hybrid_balanced") -> RankingResult:
    """
    Quick utility function để rank passages với cấu hình đơn giản
    
    Args:
        raw_passages (List[RetrievedItem]): Raw passages từ Module 1
        filtered_triples (List[FilteredTriple]): Filtered triples từ Module 2
        query (str): User query
        strategy (str): Ranking strategy
        
    Returns:
        RankingResult: Ranking result
    """
    logger.info(f"🚀 Quick ranking với strategy: {strategy}")
    
    # Create config based on strategy
    config = create_default_ranking_config()
    config.ranking_strategy = RankingStrategy(strategy)
    
    # Initialize ranker và process
    ranker = PassageRanker(config)
    result = ranker.rank_passages(raw_passages, filtered_triples, query)
    
    return result

# ==================== TEST FUNCTIONS ====================

def test_passage_ranking_with_mock_data():
    """Test Passage Ranking với mock data"""
    print("🧪 BẮT ĐẦU TEST PASSAGE RANKING")
    print("=" * 50)
    
    # Mock raw passages từ Module 1
    mock_passages = [
        RetrievedItem(
            item_id="passage_001",
            item_type="passage",
            text="Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ.",
            bm25_score=0.8,
            embedding_score=0.7,
            hybrid_score=0.75,
            metadata={'title': 'Lợi ích của táo', 'doc_id': 'health_001'}
        ),
        RetrievedItem(
            item_id="passage_002", 
            item_type="passage",
            text="Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật.",
            bm25_score=0.6,
            embedding_score=0.8,
            hybrid_score=0.7,
            metadata={'title': 'Vitamin C và miễn dịch', 'doc_id': 'health_002'}
        ),
        RetrievedItem(
            item_id="passage_003",
            item_type="passage", 
            text="Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol.",
            bm25_score=0.5,
            embedding_score=0.6,
            hybrid_score=0.55,
            metadata={'title': 'Chất xơ và tiêu hóa', 'doc_id': 'health_003'}
        ),
        RetrievedItem(
            item_id="passage_004",
            item_type="passage",
            text="Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ.",
            bm25_score=0.2,
            embedding_score=0.1, 
            hybrid_score=0.15,
            metadata={'title': 'Thời tiết', 'doc_id': 'weather_001'}
        )
    ]
    
    # Mock filtered triples từ Module 2
    mock_filtered_triples = [
        FilteredTriple(
            triple_id="triple_001",
            subject="táo",
            predicate="chứa",
            object="vitamin C",
            original_text="táo chứa vitamin C",
            query_relevance_score=0.9,
            relevance_level=RelevanceLevel.HIGHLY_RELEVANT,
            confidence_score=0.85,
            llm_explanation="Triple trả lời trực tiếp về thành phần dinh dưỡng của táo",
            source_passage_id="passage_001",
            original_hybrid_retrieval_score=0.75,
            filtering_metadata={}
        ),
        FilteredTriple(
            triple_id="triple_002",
            subject="vitamin C",
            predicate="tăng cường",
            object="hệ miễn dịch",
            original_text="vitamin C tăng cường hệ miễn dịch",
            query_relevance_score=0.8,
            relevance_level=RelevanceLevel.HIGHLY_RELEVANT,
            confidence_score=0.9,
            llm_explanation="Triple giải thích lợi ích sức khỏe của vitamin C",
            source_passage_id="passage_002",
            original_hybrid_retrieval_score=0.7,
            filtering_metadata={}
        ),
        FilteredTriple(
            triple_id="triple_003",
            subject="táo",
            predicate="chứa",
            object="chất xơ",
            original_text="táo chứa chất xơ",
            query_relevance_score=0.7,
            relevance_level=RelevanceLevel.MODERATELY_RELEVANT,
            confidence_score=0.8,
            llm_explanation="Triple cung cấp thông tin bổ sung về thành phần của táo",
            source_passage_id="passage_001",
            original_hybrid_retrieval_score=0.75,
            filtering_metadata={}
        ),
        FilteredTriple(
            triple_id="triple_004",
            subject="chất xơ",
            predicate="cải thiện",
            object="tiêu hóa",
            original_text="chất xơ cải thiện tiêu hóa",
            query_relevance_score=0.5,
            relevance_level=RelevanceLevel.MODERATELY_RELEVANT,
            confidence_score=0.75,
            llm_explanation="Triple liên quan gián tiếp đến lợi ích sức khỏe",
            source_passage_id="passage_003",
            original_hybrid_retrieval_score=0.55,
            filtering_metadata={}
        )
    ]
    
    test_query = "Lợi ích của táo cho sức khỏe là gì?"
    
    print(f"📝 Test query: '{test_query}'")
    print(f"📄 Mock passages: {len(mock_passages)}")
    print(f"🔗 Mock filtered triples: {len(mock_filtered_triples)}")
    
    try:
        # Test với different strategies
        strategies = ["hybrid_balanced", "hybrid_support_focused", "retrieval_only", "adaptive"]
        
        for strategy in strategies:
            print(f"\n🎯 Testing với strategy: {strategy}")
            print("-" * 40)
            
            result = quick_rank_passages(mock_passages, mock_filtered_triples, test_query, strategy)
            
            print(f"   📊 Kết quả: {result.original_passage_count} → {result.final_passage_count} passages")
            print(f"   ⏱️ Thời gian: {result.ranking_time:.2f}s")
            print(f"   📈 Efficiency: {result.get_ranking_efficiency():.2%}")
            
            # Show top ranked passages
            print(f"   🏆 Top 3 passages:")
            for i, passage in enumerate(result.ranked_passages[:3], 1):
                print(f"      {i}. {passage.get_summary()}")
                print(f"         📝 Text: {passage.original_text[:60]}...")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.exception("Chi tiết lỗi test:")

def test_individual_ranking_components():
    """Test các components riêng lẻ của ranking system"""
    print("\n🧪 TEST INDIVIDUAL RANKING COMPONENTS")
    print("=" * 50)
    
    # Test RankingStrategy enum
    print("🎯 Test RankingStrategy enum:")
    for strategy in RankingStrategy:
        alpha_ret, alpha_sup = strategy.get_weights()
        print(f"   {strategy.value}: retrieval={alpha_ret}, support={alpha_sup}")
    
    # Test SupportCalculationMethod enum
    print("\n🧮 Test SupportCalculationMethod enum:")
    for method in SupportCalculationMethod:
        print(f"   {method.value}")
    
    # Test PassageRankerConfig
    print("\n⚙️ Test PassageRankerConfig:")
    config = create_default_ranking_config()
    print(f"   Ranking strategy: {config.ranking_strategy.value}")
    print(f"   Support method: {config.support_calculation_method.value}")
    print(f"   Relevance threshold: {config.relevance_threshold}")
    print(f"   Max output: {config.max_passages_output}")
    print(f"   Score normalization: {config.enable_score_normalization}")
    
    # Test SupportScoreCalculator
    print("\n📊 Test SupportScoreCalculator:")
    calculator = SupportScoreCalculator(config)
    print(f"   Calculator initialized with method: {config.support_calculation_method.value}")
    
    # Test với mock triples
    mock_triples = [
        FilteredTriple(
            triple_id="test_triple_1",
            subject="táo",
            predicate="chứa", 
            object="vitamin C",
            original_text="táo chứa vitamin C",
            query_relevance_score=0.9,
            relevance_level=RelevanceLevel.HIGHLY_RELEVANT,
            confidence_score=0.85,
            llm_explanation="Test triple",
            source_passage_id="test_passage_1",
            original_hybrid_retrieval_score=0.75,
            filtering_metadata={}
        )
    ]
    
    calculator.build_support_mapping(mock_triples)
    support_score, count, triple_ids = calculator.calculate_support_score("test_passage_1")
    print(f"   Support score calculation: score={support_score:.3f}, count={count}, triples={triple_ids}")
    
    stats = calculator.get_support_statistics()
    print(f"   Support stats: {stats}")

def test_ranking_strategies():
    """Test các ranking strategies với mock data"""
    print("\n🏆 TEST RANKING STRATEGIES")
    print("=" * 40)
    
    # Create simple mock data
    mock_passages = [
        RetrievedItem(
            item_id="p1", item_type="passage", text="High retrieval, high support",
            bm25_score=0.9, embedding_score=0.8, hybrid_score=0.85,
            metadata={}
        ),
        RetrievedItem(
            item_id="p2", item_type="passage", text="High retrieval, no support", 
            bm25_score=0.8, embedding_score=0.7, hybrid_score=0.75,
            metadata={}
        ),
        RetrievedItem(
            item_id="p3", item_type="passage", text="Low retrieval, high support",
            bm25_score=0.3, embedding_score=0.4, hybrid_score=0.35,
            metadata={}
        )
    ]
    
    mock_triples = [
        FilteredTriple(
            triple_id="t1", subject="test", predicate="has", object="property",
            original_text="test", query_relevance_score=0.8,
            relevance_level=RelevanceLevel.HIGHLY_RELEVANT, confidence_score=0.9,
            llm_explanation="test", source_passage_id="p1",
            original_hybrid_retrieval_score=0.85, filtering_metadata={}
        ),
        FilteredTriple(
            triple_id="t2", subject="test", predicate="shows", object="benefit",
            original_text="test", query_relevance_score=0.7,
            relevance_level=RelevanceLevel.MODERATELY_RELEVANT, confidence_score=0.8,
            llm_explanation="test", source_passage_id="p3",
            original_hybrid_retrieval_score=0.35, filtering_metadata={}
        )
    ]
    
    strategies = [
        RankingStrategy.RETRIEVAL_ONLY,
        RankingStrategy.SUPPORT_ONLY, 
        RankingStrategy.HYBRID_BALANCED
    ]
    
    for strategy in strategies:
        print(f"\n   🎯 Strategy: {strategy.value}")
        config = PassageRankerConfig(ranking_strategy=strategy)
        ranker = PassageRanker(config)
        
        result = ranker.rank_passages(mock_passages, mock_triples, "test query")
        
        print(f"      Ranking results:")
        for passage in result.ranked_passages:
            print(f"         {passage.rank}. {passage.passage_id}: final={passage.final_score:.3f} "
                  f"(ret={passage.hybrid_retrieval_score:.3f}, sup={passage.support_score:.3f})")

if __name__ == "__main__":
    print("🚀 BẮT ĐẦU CHẠY TẤT CẢ TESTS CHO MODULE 3")
    print("=" * 60)
    
    # Test 1: Individual components
    test_individual_ranking_components()
    
    print("\n" + "=" * 60)
    
    # Test 2: Ranking strategies
    test_ranking_strategies()
    
    print("\n" + "=" * 60)
    
    # Test 3: Full ranking với mock data
    print("🎯 Test tiếp theo sử dụng comprehensive mock data")
    test_passage_ranking_with_mock_data()
    
    print("\n🎉 HOÀN THÀNH TẤT CẢ TESTS CHO MODULE 3!")
    print("=" * 60)
