"""
non_rank_metrics_evaluator.py

Module đánh giá hiệu quả retrieval sử dụng các chỉ số không dựa trên thứ hạng.
Bao gồm: Accuracy, Precision, Recall@K, F1-Score, Hit Rate@K

Input: 
- Câu hỏi/truy vấn
- Danh sách tài liệu được retrieve
- Danh sách tài liệu liên quan thực tế (ground truth)
- Giá trị K cho Recall@K và Hit Rate@K

Output:
- Accuracy: Tỷ lệ dự đoán đúng tổng thể
  Công thức: Accuracy = (TP + TN) / (TP + TN + FP + FN)
  Trong đó:
  + TP (True Positive): Số tài liệu liên quan được retrieve đúng
  + TN (True Negative): Số tài liệu không liên quan không được retrieve  
  (Tính được khi biết tổng số tài liệu trong corpus)
  + FP (False Positive): Số tài liệu không liên quan được retrieve
  + FN (False Negative): Số tài liệu liên quan không được retrieve

- Precision: Tỷ lệ tài liệu liên quan trong kết quả retrieve
  Công thức: Precision = TP / (TP + FP)
  Ý nghĩa: Trong số các tài liệu được retrieve, bao nhiêu phần trăm là liên quan

- Recall@K: Tỷ lệ tài liệu liên quan được tìm thấy trong top-K
  Công thức: Recall@K = TP / (TP + FN) = |Relevant ∩ Retrieved@K| / |Relevant|
  Trong đó:
  + Retrieved@K: Tập hợp K tài liệu đầu tiên được retrieve
  + Relevant: Tập hợp tất cả tài liệu liên quan thực tế

- F1-Score: Điểm cân bằng giữa Precision và Recall
  Công thức: F1 = 2 * (Precision * Recall) / (Precision + Recall)
  Ý nghĩa: Trung bình điều hòa của Precision và Recall

- Hit Rate@K: Tỷ lệ truy vấn có ít nhất 1 tài liệu liên quan trong top-K
  Công thức: Hit Rate@K = Số truy vấn có ít nhất 1 hit trong top-K / Tổng số truy vấn
  Trong đó:
  + Hit: Truy vấn có ít nhất một tài liệu liên quan trong top-K kết quả
"""

from typing import List, Dict, Any, Set, Tuple
from langchain_core.documents import Document
import numpy as np
from dataclasses import dataclass

@dataclass
class RetrievalResult:
    """Lưu trữ kết quả đánh giá retrieval cho một truy vấn."""
    query_id: str
    retrieved_docs: List[str]  # ID của các tài liệu được retrieve
    relevant_docs: List[str]   # ID của các tài liệu liên quan (ground truth)
    k_value: int = 10

class NonRankMetricsEvaluator:
    """
    Đánh giá hệ thống retrieval sử dụng các chỉ số không dựa trên thứ hạng.
    
    Các chỉ số được tính toán:
    1. Accuracy: (TP + TN) / (TP + TN + FP + FN)
    2. Precision: TP / (TP + FP) = số đúng / tổng dự đoán
    3. Recall@K: TP/ (TP + FN) = |Relevant ∩ Retrieved@K| / |Relevant| = số đúng / tổng đúng
    4. F1-Score: 2 * (Precision * Recall) / (Precision + Recall)
    5. Hit Rate@K: Số truy vấn có ít nhất 1 hit trong top-K / Tổng số truy vấn
    
    Trong đó:
    - TP: True Positive (tài liệu liên quan được retrieve)
    - TN: True Negative (tài liệu không liên quan không được retrieve)
    - FP: False Positive (tài liệu không liên quan được retrieve)
    - FN: False Negative (tài liệu liên quan không được retrieve)
    - Hit: Truy vấn có ít nhất một tài liệu liên quan trong top-K
    """
    
    def __init__(self, total_docs_in_corpus: int = None):
        """
        Khởi tạo evaluator.
        
        Args:
            total_docs_in_corpus: Tổng số tài liệu trong corpus (cần để tính Accuracy)
        """
        self.total_docs = total_docs_in_corpus
    
    def evaluate_single_query(
        self, 
        retrieved_docs: List[str], 
        relevant_docs: List[str],
        k: int = 10,
        query_id: str = "query_1"
    ) -> Dict[str, float]:
        """
        Đánh giá retrieval cho một truy vấn đơn lẻ.
        
        Args:
            retrieved_docs: Danh sách ID tài liệu được retrieve (theo thứ tự relevance)
            relevant_docs: Danh sách ID tài liệu liên quan thực tế
            k: Số lượng tài liệu top-K để tính Recall@K và Hit Rate@K
            query_id: ID của truy vấn
            
        Returns:
            Dict chứa các chỉ số đánh giá
        """
        # Chuyển về set để tính toán dễ dàng
        retrieved_set = set(retrieved_docs[:k])  # Chỉ lấy top-K
        relevant_set = set(relevant_docs)
        
        # Tính các thành phần cơ bản
        tp = len(retrieved_set & relevant_set)  # True Positive
        fp = len(retrieved_set - relevant_set)  # False Positive  
        fn = len(relevant_set - retrieved_set)  # False Negative
        
        # Tính Precision
        precision = tp / len(retrieved_set) if len(retrieved_set) > 0 else 0.0
        
        # Tính Recall@K
        recall_at_k = tp / len(relevant_set) if len(relevant_set) > 0 else 0.0
        
        # Tính F1-Score
        f1_score = (2 * precision * recall_at_k) / (precision + recall_at_k) if (precision + recall_at_k) > 0 else 0.0
        
        # Tính Hit Rate@K (cho truy vấn đơn lẻ: 1 nếu có ít nhất 1 hit, 0 nếu không)
        hit_rate_single = 1.0 if tp > 0 else 0.0
        
        # Tính Accuracy (nếu biết tổng số tài liệu trong corpus)
        accuracy = None
        if self.total_docs:
            tn = self.total_docs - len(relevant_set) - fp  # True Negative
            accuracy = (tp + tn) / self.total_docs if self.total_docs > 0 else 0.0
        
        return {
            "query_id": query_id,
            "precision": precision,
            "recall_at_k": recall_at_k,
            "f1_score": f1_score,
            "hit_rate_single": hit_rate_single,  # 1 hoặc 0 cho truy vấn này
            "accuracy": accuracy,
            "true_positive": tp,
            "false_positive": fp,
            "false_negative": fn,
            "retrieved_count": len(retrieved_set),
            "relevant_count": len(relevant_set),
            "k_value": k,
            "has_hit": tp > 0  # Boolean: có hit hay không
        }
    
    def evaluate_multiple_queries(
        self, 
        retrieval_results: List[RetrievalResult]
    ) -> Dict[str, Any]:
        """
        Đánh giá retrieval cho nhiều truy vấn và tính trung bình.
        
        Args:
            retrieval_results: Danh sách kết quả retrieval cho các truy vấn
            
        Returns:
            Dict chứa các chỉ số trung bình và chi tiết cho từng truy vấn
        """
        individual_results = []
        
        # Đánh giá từng truy vấn
        for result in retrieval_results:
            eval_result = self.evaluate_single_query(
                retrieved_docs=result.retrieved_docs,
                relevant_docs=result.relevant_docs,
                k=result.k_value,
                query_id=result.query_id
            )
            individual_results.append(eval_result)
        
        # Tính các chỉ số trung bình
        avg_metrics = self._calculate_average_metrics(individual_results)
        
        # Tính Hit Rate@K cho tập truy vấn
        hit_rate_at_k = self._calculate_hit_rate(individual_results)
        avg_metrics["hit_rate_at_k"] = hit_rate_at_k
        
        return {
            "average_metrics": avg_metrics,
            "individual_results": individual_results,
            "total_queries": len(retrieval_results),
            "queries_with_hits": sum(1 for r in individual_results if r["has_hit"]),
            "evaluation_summary": self._generate_summary(avg_metrics)
        }
    
    def _calculate_hit_rate(self, results: List[Dict]) -> float:
        """
        Tính Hit Rate@K cho tập truy vấn.
        
        Hit Rate@K = Số truy vấn có ít nhất 1 tài liệu liên quan trong top-K / Tổng số truy vấn
        
        Args:
            results: Danh sách kết quả đánh giá cho từng truy vấn
            
        Returns:
            Hit Rate@K (0.0 - 1.0)
        """
        if not results:
            return 0.0
        
        queries_with_hits = sum(1 for result in results if result["has_hit"])
        total_queries = len(results)
        
        return queries_with_hits / total_queries
    
    def _calculate_average_metrics(self, results: List[Dict]) -> Dict[str, float]:
        """Tính toán các chỉ số trung bình từ kết quả của nhiều truy vấn."""
        if not results:
            return {}
        
        # Tính trung bình cho các chỉ số chính
        avg_precision = np.mean([r["precision"] for r in results])
        avg_recall = np.mean([r["recall_at_k"] for r in results])
        avg_f1 = np.mean([r["f1_score"] for r in results])
        
        # Tính trung bình accuracy (nếu có)
        accuracies = [r["accuracy"] for r in results if r["accuracy"] is not None]
        avg_accuracy = np.mean(accuracies) if accuracies else None
        
        # Tính các thống kê bổ sung
        total_tp = sum(r["true_positive"] for r in results)
        total_fp = sum(r["false_positive"] for r in results)
        total_fn = sum(r["false_negative"] for r in results)
        
        # Macro-averaged metrics (trung bình đơn giản)
        macro_metrics = {
            "macro_precision": avg_precision,
            "macro_recall": avg_recall,
            "macro_f1": avg_f1,
            "macro_accuracy": avg_accuracy
        }
        
        # Micro-averaged metrics (tính trên tổng TP, FP, FN)
        micro_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
        micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
        micro_f1 = (2 * micro_precision * micro_recall) / (micro_precision + micro_recall) if (micro_precision + micro_recall) > 0 else 0.0
        
        micro_metrics = {
            "micro_precision": micro_precision,
            "micro_recall": micro_recall,
            "micro_f1": micro_f1
        }
        
        return {**macro_metrics, **micro_metrics}
    
    def _generate_summary(self, metrics: Dict[str, float]) -> str:
        """Tạo báo cáo tóm tắt kết quả đánh giá."""
        summary = "=== BÁO CÁO ĐÁNH GIÁ NON-RANK METRICS ===\n\n"
        
        # Add corpus information
        if self.total_docs:
            summary += "📚 THÔNG TIN CORPUS:\n"
            summary += f"  • Tổng số tài liệu unique: {self.total_docs}\n"
            summary += "  • Cách tính: Lấy union của tất cả document IDs từ retrieved_docs và supporting_facts\n\n"
        
        # Add explanation of averaging methods
        summary += "📊 PHƯƠNG PHÁP TÍNH TRUNG BÌNH:\n"
        summary += "  • MACRO-AVERAGED: Tính trung bình đơn giản của các metrics từ từng truy vấn.\n"
        summary += "    - Ưu điểm: Mỗi truy vấn có trọng số bằng nhau\n"
        summary += "    - Phù hợp khi: Các truy vấn có tầm quan trọng như nhau\n"
        summary += "    - Ví dụ: Có 3 truy vấn với Precision lần lượt là 0.8, 0.6, 0.4\n"
        summary += "      MACRO Precision = (0.8 + 0.6 + 0.4) / 3 = 0.6\n\n"
        
        summary += "  • MICRO-AVERAGED: Tính metrics trên tổng số TP, FP, FN của tất cả truy vấn.\n"
        summary += "    - Ưu điểm: Phản ánh hiệu suất tổng thể trên toàn bộ dữ liệu\n"
        summary += "    - Phù hợp khi: Cần đánh giá hiệu suất trên tập dữ liệu lớn\n"
        summary += "    - Ví dụ:\n"
        summary += "      + Truy vấn 1: TP=2, FP=1, FN=1\n"
        summary += "      + Truy vấn 2: TP=3, FP=2, FN=0\n"
        summary += "      + Truy vấn 3: TP=1, FP=1, FN=2\n"
        summary += "      Tổng: TP=6, FP=4, FN=3\n"
        summary += "      MICRO Precision = 6/(6+4) = 0.6\n\n"
        
        summary += "  Sự khác biệt chính:\n"
        summary += "  - MACRO: Mỗi truy vấn có trọng số bằng nhau, không quan tâm số lượng tài liệu\n"
        summary += "  - MICRO: Các truy vấn có nhiều tài liệu sẽ có ảnh hưởng lớn hơn đến kết quả cuối cùng\n\n"
        
        summary += "📊 MACRO-AVERAGED METRICS:\n"
        summary += f"  • Precision: {metrics.get('macro_precision', 0):.3f}\n"
        summary += f"  • Recall@K: {metrics.get('macro_recall', 0):.3f}\n"
        summary += f"  • F1-Score: {metrics.get('macro_f1', 0):.3f}\n"
        summary += f"  • Hit Rate@K: {metrics.get('hit_rate_at_k', 0):.3f}\n"
        
        if metrics.get('macro_accuracy') is not None:
            summary += f"  • Accuracy: {metrics['macro_accuracy']:.3f}\n"
        
        summary += "\n📈 MICRO-AVERAGED METRICS:\n"
        summary += f"  • Precision: {metrics.get('micro_precision', 0):.3f}\n"
        summary += f"  • Recall@K: {metrics.get('micro_recall', 0):.3f}\n"
        summary += f"  • F1-Score: {metrics.get('micro_f1', 0):.3f}\n"
        
        # Đánh giá chất lượng
        hit_rate = metrics.get('hit_rate_at_k', 0)
        precision = metrics.get('macro_precision', 0)
        recall = metrics.get('macro_recall', 0)
        
        summary += "\n🎯 ĐÁNH GIÁ CHẤT LƯỢNG:\n"
        
        if hit_rate >= 0.8:
            summary += "  • Hit Rate: XUẤT SẮC (≥80% truy vấn có kết quả liên quan)\n"
        elif hit_rate >= 0.6:
            summary += "  • Hit Rate: TỐT (60-80% truy vấn có kết quả liên quan)\n"
        elif hit_rate >= 0.4:
            summary += "  • Hit Rate: TRUNG BÌNH (40-60% truy vấn có kết quả liên quan)\n"
        else:
            summary += "  • Hit Rate: CẦN CẢI THIỆN (<40% truy vấn có kết quả liên quan)\n"
        
        if precision >= 0.7:
            summary += "  • Precision: CAO (ít nhiễu trong kết quả)\n"
        elif precision >= 0.5:
            summary += "  • Precision: TRUNG BÌNH\n"
        else:
            summary += "  • Precision: THẤP (nhiều kết quả không liên quan)\n"
        
        if recall >= 0.7:
            summary += "  • Recall: CAO (tìm được nhiều tài liệu liên quan)\n"
        elif recall >= 0.5:
            summary += "  • Recall: TRUNG BÌNH\n"
        else:
            summary += "  • Recall: THẤP (bỏ sót nhiều tài liệu liên quan)\n"
        
        return summary

if __name__ == "__main__":
    """Test NonRankMetricsEvaluator với Hit Rate@K"""
    
    # Dữ liệu test mẫu
    test_results = [
        RetrievalResult(
            query_id="Q1",
            retrieved_docs=["doc1", "doc2", "doc3", "doc4", "doc5"],
            relevant_docs=["doc1", "doc3", "doc6"],  # doc6 không được retrieve
            k_value=5
        ),
        RetrievalResult(
            query_id="Q2", 
            retrieved_docs=["doc7", "doc8", "doc9", "doc10"],
            relevant_docs=["doc11", "doc12"],  # Không có tài liệu nào liên quan được retrieve
            k_value=5
        ),
        RetrievalResult(
            query_id="Q3",
            retrieved_docs=["doc13", "doc14", "doc15"],
            relevant_docs=["doc13", "doc14"],  # Tất cả đều được retrieve
            k_value=5
        )
    ]
    
    print("Testing NonRankMetricsEvaluator với Hit Rate@K...")
    
    try:
        # Khởi tạo evaluator với 100 tài liệu trong corpus
        evaluator = NonRankMetricsEvaluator(total_docs_in_corpus=100)
        
        # Đánh giá nhiều truy vấn
        results = evaluator.evaluate_multiple_queries(test_results)
        
        print("📊 KẾT QUẢ ĐÁNH GIÁ:")
        print(f"Tổng số truy vấn: {results['total_queries']}")
        print(f"Số truy vấn có hit: {results['queries_with_hits']}")
        print(f"Hit Rate@K: {results['average_metrics']['hit_rate_at_k']:.3f}")
        
        print("\n" + results['evaluation_summary'])
        
        print("\n📋 CHI TIẾT TỪNG TRUY VẤN:")
        for result in results['individual_results']:
            print(f"Query {result['query_id']}:")
            print(f"  - Precision: {result['precision']:.3f}")
            print(f"  - Recall@K: {result['recall_at_k']:.3f}")
            print(f"  - F1-Score: {result['f1_score']:.3f}")
            print(f"  - Has Hit: {'✅' if result['has_hit'] else '❌'}")
            print(f"  - TP/FP/FN: {result['true_positive']}/{result['false_positive']}/{result['false_negative']}")
            print()
            
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
