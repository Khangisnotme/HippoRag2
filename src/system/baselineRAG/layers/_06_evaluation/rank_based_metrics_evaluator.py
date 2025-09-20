# """
# rank_based_metrics_evaluator.py

# Module đánh giá hiệu quả retrieval sử dụng các chỉ số dựa trên thứ hạng.
# Bao gồm: MRR (Mean Reciprocal Rank), MAP (Mean Average Precision), nDCG@K

# Input:
# - Câu hỏi/truy vấn  
# - Danh sách tài liệu được retrieve theo thứ tự ranking
# - Danh sách tài liệu liên quan với điểm relevance (ground truth)
# - Giá trị K cho nDCG@K

# Output:
# - MRR: Trung bình nghịch đảo thứ hạng của kết quả đầu tiên đúng
# - MAP: Trung bình của Average Precision cho tất cả truy vấn
# - nDCG@K: Normalized Discounted Cumulative Gain tại K
# - DCG@K: Discounted Cumulative Gain tại K
# """

# from typing import List, Dict, Any, Tuple, Optional
# import numpy as np
# import math
# from dataclasses import dataclass

# @dataclass
# class RankedRetrievalResult:
#     """Lưu trữ kết quả retrieval có thứ hạng cho một truy vấn."""
#     query_id: str
#     retrieved_docs: List[str]  # ID tài liệu theo thứ tự ranking (cao -> thấp)
#     relevance_scores: Dict[str, float]  # {doc_id: relevance_score}
#     k_value: int = 10

# class RankBasedMetricsEvaluator:
#     """
#     Đánh giá hệ thống retrieval sử dụng các chỉ số dựa trên thứ hạng.
    
#     Các chỉ số được tính toán:
#     1. MRR (Mean Reciprocal Rank): 1/|Q| * Σ(1/rank_i)
#     2. MAP (Mean Average Precision): 1/|Q| * Σ(AP_q)  
#     3. nDCG@K: DCG@K / IDCG@K
#     4. DCG@K: Σ(rel_i / log2(i+1)) với i từ 1 đến K
    
#     Trong đó:
#     - rank_i: Thứ hạng của tài liệu liên quan đầu tiên cho truy vấn i
#     - AP_q: Average Precision cho truy vấn q
#     - rel_i: Điểm relevance của tài liệu tại vị trí i
#     - IDCG: Ideal DCG (DCG tối đa có thể đạt được)
#     """
    
#     def __init__(self, relevance_threshold: float = 1.0):
#         """
#         Khởi tạo evaluator.
        
#         Args:
#             relevance_threshold: Ngưỡng để coi tài liệu là "liên quan" (cho MRR, MAP)
#         """
#         self.relevance_threshold = relevance_threshold
    
#     def calculate_mrr_single_query(
#         self,
#         retrieved_docs: List[str],
#         relevance_scores: Dict[str, float],
#         query_id: str = "query_1"
#     ) -> Dict[str, Any]:
#         """
#         Tính MRR cho một truy vấn đơn lẻ.
        
#         Args:
#             retrieved_docs: Danh sách tài liệu theo thứ tự ranking
#             relevance_scores: Dict điểm relevance {doc_id: score}
#             query_id: ID truy vấn
            
#         Returns:
#             Dict chứa thông tin MRR cho truy vấn này
#         """
#         # Tìm tài liệu liên quan đầu tiên
#         first_relevant_rank = None
        
#         for rank, doc_id in enumerate(retrieved_docs, 1):
#             if doc_id in relevance_scores and relevance_scores[doc_id] >= self.relevance_threshold:
#                 first_relevant_rank = rank
#                 break
        
#         # Tính reciprocal rank
#         reciprocal_rank = 1.0 / first_relevant_rank if first_relevant_rank else 0.0
        
#         return {
#             "query_id": query_id,
#             "first_relevant_rank": first_relevant_rank,
#             "reciprocal_rank": reciprocal_rank,
#             "has_relevant_result": first_relevant_rank is not None
#         }
    
#     def calculate_average_precision_single_query(
#         self,
#         retrieved_docs: List[str],
#         relevance_scores: Dict[str, float],
#         query_id: str = "query_1"
#     ) -> Dict[str, Any]:
#         """
#         Tính Average Precision cho một truy vấn đơn lẻ.
        
#         AP = (1/R) * Σ(Precision@k * rel_k)
#         Trong đó R là tổng số tài liệu liên quan
        
#         Args:
#             retrieved_docs: Danh sách tài liệu theo thứ tự ranking
#             relevance_scores: Dict điểm relevance
#             query_id: ID truy vấn
            
#         Returns:
#             Dict chứa thông tin AP cho truy vấn này
#         """
#         relevant_docs = [doc for doc, score in relevance_scores.items() 
#                         if score >= self.relevance_threshold]
        
#         if not relevant_docs:
#             return {
#                 "query_id": query_id,
#                 "average_precision": 0.0,
#                 "relevant_docs_count": 0,
#                 "precision_at_k_values": []
#             }
        
#         precision_sum = 0.0
#         relevant_found = 0
#         precision_values = []
        
#         for k, doc_id in enumerate(retrieved_docs, 1):
#             if doc_id in relevance_scores and relevance_scores[doc_id] >= self.relevance_threshold:
#                 relevant_found += 1
#                 precision_at_k = relevant_found / k
#                 precision_sum += precision_at_k
#                 precision_values.append({
#                     "k": k,
#                     "doc_id": doc_id,
#                     "precision_at_k": precision_at_k
#                 })
        
#         average_precision = precision_sum / len(relevant_docs) if relevant_docs else 0.0
        
#         return {
#             "query_id": query_id,
#             "average_precision": average_precision,
#             "relevant_docs_count": len(relevant_docs),
#             "relevant_found": relevant_found,
#             "precision_at_k_values": precision_values
#         }
    
#     def calculate_dcg_at_k(
#         self,
#         retrieved_docs: List[str],
#         relevance_scores: Dict[str, float],
#         k: int = 10
#     ) -> float:
#         """
#         Tính DCG@K (Discounted Cumulative Gain).
        
#         DCG@K = Σ(rel_i / log2(i+1)) với i từ 1 đến K
        
#         Args:
#             retrieved_docs: Danh sách tài liệu theo thứ tự ranking
#             relevance_scores: Dict điểm relevance
#             k: Số lượng tài liệu top-K
            
#         Returns:
#             Giá trị DCG@K
#         """
#         dcg = 0.0
        
#         for i, doc_id in enumerate(retrieved_docs[:k], 1):
#             relevance = relevance_scores.get(doc_id, 0.0)
#             if relevance > 0:
#                 dcg += relevance / math.log2(i + 1)
        
#         return dcg
    
#     def calculate_ideal_dcg_at_k(
#         self,
#         relevance_scores: Dict[str, float],
#         k: int = 10
#     ) -> float:
#         """
#         Tính IDCG@K (Ideal DCG) - DCG tối đa có thể đạt được.
        
#         Args:
#             relevance_scores: Dict điểm relevance
#             k: Số lượng tài liệu top-K
            
#         Returns:
#             Giá trị IDCG@K
#         """
#         # Sắp xếp các điểm relevance theo thứ tự giảm dần
#         sorted_relevances = sorted(relevance_scores.values(), reverse=True)
        
#         idcg = 0.0
#         for i, relevance in enumerate(sorted_relevances[:k], 1):
#             if relevance > 0:
#                 idcg += relevance / math.log2(i + 1)
        
#         return idcg
    
#     def calculate_ndcg_single_query(
#         self,
#         retrieved_docs: List[str],
#         relevance_scores: Dict[str, float],
#         k: int = 10,
#         query_id: str = "query_1"
#     ) -> Dict[str, Any]:
#         """
#         Tính nDCG@K cho một truy vấn đơn lẻ.
        
#         nDCG@K = DCG@K / IDCG@K
        
#         Args:
#             retrieved_docs: Danh sách tài liệu theo thứ tự ranking
#             relevance_scores: Dict điểm relevance
#             k: Số lượng tài liệu top-K
#             query_id: ID truy vấn
            
#         Returns:
#             Dict chứa thông tin nDCG cho truy vấn này
#         """
#         dcg_k = self.calculate_dcg_at_k(retrieved_docs, relevance_scores, k)
#         idcg_k = self.calculate_ideal_dcg_at_k(relevance_scores, k)
        
#         ndcg_k = dcg_k / idcg_k if idcg_k > 0 else 0.0
        
#         return {
#             "query_id": query_id,
#             "dcg_at_k": dcg_k,
#             "idcg_at_k": idcg_k,
#             "ndcg_at_k": ndcg_k,
#             "k_value": k
#         }
    
#     def evaluate_single_query(
#         self,
#         retrieved_docs: List[str],
#         relevance_scores: Dict[str, float],
#         k: int = 10,
#         query_id: str = "query_1"
#     ) -> Dict[str, Any]:
#         """
#         Đánh giá đầy đủ cho một truy vấn đơn lẻ (tất cả các chỉ số rank-based).
        
#         Args:
#             retrieved_docs: Danh sách tài liệu theo thứ tự ranking
#             relevance_scores: Dict điểm relevance
#             k: Giá trị K cho nDCG@K
#             query_id: ID truy vấn
            
#         Returns:
#             Dict chứa tất cả các chỉ số đánh giá
#         """
#         # Tính MRR
#         mrr_result = self.calculate_mrr_single_query(retrieved_docs, relevance_scores, query_id)
        
#         # Tính AP
#         ap_result = self.calculate_average_precision_single_query(retrieved_docs, relevance_scores, query_id)
        
#         # Tính nDCG@K
#         ndcg_result = self.calculate_ndcg_single_query(retrieved_docs, relevance_scores, k, query_id)
        
#         return {
#             "query_id": query_id,
#             "mrr": mrr_result["reciprocal_rank"],
#             "average_precision": ap_result["average_precision"],
#             "ndcg_at_k": ndcg_result["ndcg_at_k"],
#             "dcg_at_k": ndcg_result["dcg_at_k"],
#             "idcg_at_k": ndcg_result["idcg_at_k"],
#             "first_relevant_rank": mrr_result["first_relevant_rank"],
#             "relevant_docs_count": ap_result["relevant_docs_count"],
#             "relevant_found": ap_result["relevant_found"],
#             "k_value": k,
#             "detailed_mrr": mrr_result,
#             "detailed_ap": ap_result,
#             "detailed_ndcg": ndcg_result
#         }
    
#     def evaluate_multiple_queries(
#         self,
#         ranked_results: List[RankedRetrievalResult]
#     ) -> Dict[str, Any]:
#         """
#         Đánh giá cho nhiều truy vấn và tính các chỉ số trung bình.
        
#         Args:
#             ranked_results: Danh sách kết quả retrieval có ranking
            
#         Returns:
#             Dict chứa các chỉ số trung bình và chi tiết
#         """
#         individual_results = []
        
#         # Đánh giá từng truy vấn
#         for result in ranked_results:
#             eval_result = self.evaluate_single_query(
#                 retrieved_docs=result.retrieved_docs,
#                 relevance_scores=result.relevance_scores,
#                 k=result.k_value,
#                 query_id=result.query_id
#             )
#             individual_results.append(eval_result)
        
#         # Tính các chỉ số trung bình
#         avg_metrics = self._calculate_average_metrics(individual_results)
        
#         return {
#             "average_metrics": avg_metrics,
#             "individual_results": individual_results,
#             "total_queries": len(ranked_results),
#             "evaluation_summary": self._generate_summary(avg_metrics, individual_results)
#         }
    
#     def _calculate_average_metrics(self, results: List[Dict]) -> Dict[str, float]:
#         """Tính toán các chỉ số trung bình."""
#         if not results:
#             return {}
        
#         # Tính Mean Reciprocal Rank
#         mrr_values = [r["mrr"] for r in results]
#         mean_mrr = np.mean(mrr_values)
        
#         # Tính Mean Average Precision  
#         map_values = [r["average_precision"] for r in results]
#         mean_ap = np.mean(map_values)
        
#         # Tính Mean nDCG@K
#         ndcg_values = [r["ndcg_at_k"] for r in results]
#         mean_ndcg = np.mean(ndcg_values)
        
#         # Tính Mean DCG@K
#         dcg_values = [r["dcg_at_k"] for r in results]
#         mean_dcg = np.mean(dcg_values)
        
#         return {
#             "mean_reciprocal_rank": mean_mrr,
#             "mean_average_precision": mean_ap,
#             "mean_ndcg_at_k": mean_ndcg,
#             "mean_dcg_at_k": mean_dcg,
#             "queries_with_relevant_results": sum(1 for r in results if r["first_relevant_rank"] is not None),
#             "average_first_relevant_rank": np.mean([r["first_relevant_rank"] for r in results if r["first_relevant_rank"] is not None]) if any(r["first_relevant_rank"] for r in results) else None
#         }
    
#     def _generate_summary(self, metrics: Dict[str, float], individual_results: List[Dict]) -> str:
#         """Tạo báo cáo tóm tắt kết quả đánh giá."""
#         summary = "=== BÁO CÁO ĐÁNH GIÁ RANK-BASED METRICS ===\n\n"
        
#         summary += "📊 CÁC CHỈ SỐ TRUNG BÌNH:\n"
#         summary += f"  • Mean Reciprocal Rank (MRR): {metrics.get('mean_reciprocal_rank', 0):.3f}\n"
#         summary += f"  • Mean Average Precision (MAP): {metrics.get('mean_average_precision', 0):.3f}\n"
#         summary += f"  • Mean nDCG@K: {metrics.get('mean_ndcg_at_k', 0):.3f}\n"
#         summary += f"  • Mean DCG@K: {metrics.get('mean_dcg_at_k', 0):.3f}\n"
        
#         total_queries = len(individual_results)
#         queries_with_results = metrics.get('queries_with_relevant_results', 0)
        
#         summary += f"\n📈 THỐNG KÊ TRUY VẤN:\n"
#         summary += f"  • Tổng số truy vấn: {total_queries}\n"
#         summary += f"  • Truy vấn có kết quả liên quan: {queries_with_results}/{total_queries}\n"
#         summary += f"  • Tỷ lệ thành công: {queries_with_results/total_queries*100:.1f}%\n"
        
#         if metrics.get('average_first_relevant_rank'):
#             summary += f"  • Vị trí trung bình của kết quả đầu tiên: {metrics['average_first_relevant_rank']:.1f}\n"
        
#         # Đánh giá chất lượng
#         mrr = metrics.get('mean_reciprocal_rank', 0)
#         map_score = metrics.get('mean_average_precision', 0)
#         ndcg = metrics.get('mean_ndcg_at_k', 0)
        
#         summary += "\n🎯 ĐÁNH GIÁ CHẤT LƯỢNG:\n"
        
#         if mrr >= 0.8:
#             summary += "  • MRR: XUẤT SẮC (kết quả liên quan thường ở vị trí cao)\n"
#         elif mrr >= 0.6:
#             summary += "  • MRR: TỐT (kết quả liên quan ở vị trí khá cao)\n"
#         elif mrr >= 0.4:
#             summary += "  • MRR: TRUNG BÌNH (kết quả liên quan ở vị trí trung bình)\n"
#         else:
#             summary += "  • MRR: CẦN CẢI THIỆN (kết quả liên quan ở vị trí thấp)\n"
        
#         if map_score >= 0.7:
#             summary += "  • MAP: CAO (precision tốt qua nhiều vị trí)\n"
#         elif map_score >= 0.5:
#             summary += "  • MAP: TRUNG BÌNH\n"
#         else:
#             summary += "  • MAP: THẤP (precision kém qua các vị trí)\n"
        
#         if ndcg >= 0.8:
#             summary += "  • nDCG@K: XUẤT SẮC (ranking rất tốt)\n"
#         elif ndcg >= 0.6:
#             summary += "  • nDCG@K: TỐT (ranking khá tốt)\n"
#         elif ndcg >= 0.4:
#             summary += "  • nDCG@K: TRUNG BÌNH (ranking cần cải thiện)\n"
#         else:
#             summary += "  • nDCG@K: THẤP (ranking kém)\n"
        
#         return summary

# if __name__ == "__main__":
#     """Test RankBasedMetricsEvaluator"""
    
#     # Dữ liệu test mẫu với điểm relevance
#     test_results = [
#         RankedRetrievalResult(
#             query_id="Q1",
#             retrieved_docs=["doc1", "doc2", "doc3", "doc4", "doc5"],
#             relevance_scores={"doc1": 3.0, "doc2": 0.0, "doc3": 2.0, "doc6": 3.0},  # doc6 không được retrieve
#             k_value=5
#         ),
#         RankedRetrievalResult(
#             query_id="Q2",
#             retrieved_docs=["doc7", "doc8", "doc9", "doc10"],
#             relevance_scores={"doc11": 2.0, "doc12": 1.0},  # Không có doc nào liên quan được retrieve
#             k_value=5
#         ),
#         RankedRetrievalResult(
#             query_id="Q3",
#             retrieved_docs=["doc13", "doc14", "doc15"],
#             relevance_scores={"doc13": 3.0, "doc14": 2.0, "doc15": 1.0},  # Tất cả đều được retrieve
#             k_value=5
#         )
#     ]
    
#     print("Testing RankBasedMetricsEvaluator...")
    
#     try:
#         evaluator = RankBasedMetricsEvaluator(relevance_threshold=1.0)
        
#         # Đánh giá nhiều truy vấn
#         results = evaluator.evaluate_multiple_queries(test_results)
        
#         print("📊 KẾT QUẢ ĐÁNH GIÁ:")
#         print(f"MRR: {results['average_metrics']['mean_reciprocal_rank']:.3f}")
#         print(f"MAP: {results['average_metrics']['mean_average_precision']:.3f}")
#         print(f"nDCG@K: {results['average_metrics']['mean_ndcg_at_k']:.3f}")
        
#         print("\n" + results['evaluation_summary'])
        
#         print("\n📋 CHI TIẾT TỪNG TRUY VẤN:")
#         for result in results['individual_results']:
#             print(f"Query {result['query_id']}:")
#             print(f"  - MRR: {result['mrr']:.3f}")
#             print(f"  - AP: {result['average_precision']:.3f}")
#             print(f"  - nDCG@{result['k_value']}: {result['ndcg_at_k']:.3f}")
#             print(f"  - Vị trí đầu tiên liên quan: {result['first_relevant_rank']}")
#             print()
            
#     except Exception as e:
#         print(f"Test failed: {e}")
#         import traceback
#         traceback.print_exc()
