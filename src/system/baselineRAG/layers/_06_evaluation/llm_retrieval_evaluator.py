# """
# llm_retrieval_evaluator.py

# Module đánh giá hiệu quả retrieval sử dụng LLM làm trọng tài.
# Đánh giá ngữ cảnh, độ liên quan và chất lượng tài liệu một cách tự nhiên.

# Input:
# - Câu hỏi/truy vấn gốc
# - Danh sách tài liệu được retrieve
# - Prompt đánh giá tùy chỉnh (optional)
# - Model LLM sử dụng

# Output:  
# - Context Relevance Score: Điểm liên quan ngữ cảnh (0-100)
# - Context Quality Score: Điểm chất lượng nội dung (0-100)
# - Coverage Score: Điểm bao phủ thông tin (0-100)
# - Coherence Score: Điểm nhất quán giữa các tài liệu (0-100)
# - Overall Score: Điểm tổng thể
# - Detailed Feedback: Phản hồi chi tiết từ LLM
# """

# from typing import List, Dict, Any, Optional
# from langchain_core.documents import Document
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
# from dotenv import load_dotenv
# import re
# import json
# from dataclasses import dataclass

# # Load environment variables
# load_dotenv()

# @dataclass
# class LLMRetrievalResult:
#     """Lưu trữ kết quả đánh giá LLM cho một truy vấn."""
#     query_id: str
#     query_text: str
#     retrieved_docs: List[Document]
#     context_relevance: float = 0.0
#     context_quality: float = 0.0
#     coverage_score: float = 0.0
#     coherence_score: float = 0.0
#     overall_score: float = 0.0
#     detailed_feedback: str = ""

# # Prompt mặc định cho đánh giá LLM
# DEFAULT_LLM_EVALUATION_PROMPT = """Bạn là chuyên gia đánh giá chất lượng hệ thống retrieval trong RAG.
# Nhiệm vụ của bạn là đánh giá mức độ phù hợp của các tài liệu được tìm kiếm với câu hỏi đưa ra.

# Hãy đánh giá theo 4 tiêu chí sau và cho điểm từ 0-100:

# 1. CONTEXT RELEVANCE (Độ liên quan ngữ cảnh):
#    - Mức độ liên quan trực tiếp của các tài liệu với câu hỏi
#    - Tài liệu có chứa thông tin cần thiết để trả lời câu hỏi không?
   
# 2. CONTEXT QUALITY (Chất lượng nội dung):
#    - Độ chính xác, đầy đủ và cập nhật của thông tin
#    - Nguồn thông tin có đáng tin cậy không?
   
# 3. COVERAGE (Độ bao phủ):
#    - Các tài liệu có bao phủ đầy đủ các khía cạnh của câu hỏi không?
#    - Có thiếu thông tin quan trọng nào không?
   
# 4. COHERENCE (Tính nhất quán):
#    - Các tài liệu có nhất quán với nhau không?
#    - Có mâu thuẫn hoặc trùng lặp thông tin không?

# ĐỊNH DẠNG PHẢN HỒI:
# ```json
# {
#     "context_relevance": <điểm 0-100>,
#     "context_quality": <điểm 0-100>, 
#     "coverage_score": <điểm 0-100>,
#     "coherence_score": <điểm 0-100>,
#     "overall_score": <điểm trung bình>,
#     "detailed_analysis": {
#         "relevant_docs": ["doc_index_1", "doc_index_2", ...],
#         "irrelevant_docs": ["doc_index_3", ...],
#         "missing_information": ["thông tin thiếu 1", "thông tin thiếu 2", ...],
#         "contradictions": ["mâu thuẫn 1", "mâu thuẫn 2", ...],
#         "strengths": ["điểm mạnh 1", "điểm mạnh 2", ...],
#         "weaknesses": ["điểm yếu 1", "điểm yếu 2", ...]
#     },
#     "recommendations": ["khuyến nghị 1", "khuyến nghị 2", ...]
# }
# ```"""

# class LLMRetrievalEvaluator:
#     """
#     Đánh giá hệ thống retrieval sử dụng LLM làm trọng tài.
    
#     Ưu điểm:
#     - Đánh giá ngữ cảnh sâu sắc
#     - Hiểu được ý nghĩa semantic của câu hỏi và tài liệu
#     - Phát hiện thông tin thiếu và mâu thuẫn
#     - Đưa ra khuyến nghị cải thiện
    
#     Nhược điểm:
#     - Chậm hơn các phương pháp truyền thống
#     - Chi phí cao hơn
#     - Có thể không nhất quán giữa các lần đánh giá
#     """
    
#     def __init__(
#         self,
#         model_name: str = "gpt-4o-mini",
#         temperature: float = 0.1,
#         evaluation_prompt: str = DEFAULT_LLM_EVALUATION_PROMPT,
#         max_retries: int = 3
#     ):
#         """
#         Khởi tạo LLM evaluator.
        
#         Args:
#             model_name: Tên model LLM sử dụng
#             temperature: Độ sáng tạo (thấp để đánh giá nhất quán)
#             evaluation_prompt: Prompt hướng dẫn đánh giá
#             max_retries: Số lần thử lại khi parse JSON thất bại
#         """
#         self.llm = ChatOpenAI(
#             model_name=model_name,
#             temperature=temperature
#         )
        
#         self.eval_prompt = ChatPromptTemplate.from_messages([
#             ("system", evaluation_prompt),
#             ("human", """TRUY VẤN: {query}

# CÁC TÀI LIỆU ĐƯỢC TÌM KIẾM:
# {documents}

# Hãy đánh giá chất lượng retrieval theo định dạng JSON đã yêu cầu:""")
#         ])
        
#         self.chain = (
#             {
#                 "query": RunnablePassthrough(),
#                 "documents": RunnablePassthrough()
#             }
#             | self.eval_prompt
#             | self.llm
#             | StrOutputParser()
#         )
        
#         self.max_retries = max_retries
    
#     def evaluate_single_query(
#         self,
#         query: str,
#         documents: List[Document],
#         query_id: str = "query_1"
#     ) -> LLMRetrievalResult:
#         """
#         Đánh giá retrieval cho một truy vấn đơn lẻ sử dụng LLM.
        
#         Args:
#             query: Câu hỏi/truy vấn gốc
#             documents: Danh sách tài liệu được retrieve
#             query_id: ID của truy vấn
            
#         Returns:
#             LLMRetrievalResult chứa kết quả đánh giá chi tiết
#         """
#         if not documents:
#             return LLMRetrievalResult(
#                 query_id=query_id,
#                 query_text=query,
#                 retrieved_docs=[],
#                 detailed_feedback="Không có tài liệu nào được tìm kiếm."
#             )
        
#         # Format documents cho LLM
#         doc_text = self._format_documents_for_llm(documents)
        
#         # Gọi LLM để đánh giá
#         for attempt in range(self.max_retries):
#             try:
#                 evaluation_text = self.chain.invoke({
#                     "query": query,
#                     "documents": doc_text
#                 })
                
#                 # Parse kết quả JSON
#                 evaluation_data = self._parse_llm_response(evaluation_text)
                
#                 # Tạo kết quả đánh giá
#                 result = LLMRetrievalResult(
#                     query_id=query_id,
#                     query_text=query,
#                     retrieved_docs=documents,
#                     context_relevance=evaluation_data.get("context_relevance", 0.0),
#                     context_quality=evaluation_data.get("context_quality", 0.0),
#                     coverage_score=evaluation_data.get("coverage_score", 0.0),
#                     coherence_score=evaluation_data.get("coherence_score", 0.0),
#                     overall_score=evaluation_data.get("overall_score", 0.0),
#                     detailed_feedback=json.dumps(evaluation_data, ensure_ascii=False, indent=2)
#                 )
                
#                 return result
                
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt == self.max_retries - 1:
#                     # Fallback: tạo kết quả với điểm 0 và thông báo lỗi
#                     return LLMRetrievalResult(
#                         query_id=query_id,
#                         query_text=query,
#                         retrieved_docs=documents,
#                         detailed_feedback=f"LLM evaluation failed after {self.max_retries} attempts: {str(e)}"
#                     )
        
#         return result
    
#     def evaluate_multiple_queries(
#         self,
#         queries_and_docs: List[tuple[str, List[Document], str]]
#     ) -> Dict[str, Any]:
#         """
#         Đánh giá nhiều truy vấn sử dụng LLM.
        
#         Args:
#             queries_and_docs: List of (query, documents, query_id)
            
#         Returns:
#             Dict chứa kết quả đánh giá tổng hợp
#         """
#         individual_results = []
        
#         # Đánh giá từng truy vấn
#         for query, docs, query_id in queries_and_docs:
#             print(f"Đang đánh giá query: {query_id}...")
#             result = self.evaluate_single_query(query, docs, query_id)
#             individual_results.append(result)
        
#         # Tính các chỉ số trung bình
#         avg_metrics = self._calculate_average_metrics(individual_results)
        
#         return {
#             "average_metrics": avg_metrics,
#             "individual_results": individual_results,
#             "total_queries": len(queries_and_docs),
#             "evaluation_summary": self._generate_summary(avg_metrics, individual_results)
#         }
    
#     def _format_documents_for_llm(self, documents: List[Document]) -> str:
#         """Format tài liệu thành text cho LLM đánh giá."""
#         doc_text = ""
#         for i, doc in enumerate(documents, 1):
#             doc_text += f"--- TÀI LIỆU {i} ---\n"
#             doc_text += f"Nội dung: {doc.page_content[:1000]}...\n"  # Giới hạn độ dài
#             if doc.metadata:
#                 doc_text += f"Metadata: {doc.metadata}\n"
#             doc_text += "\n"
#         return doc_text
    
#     def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
#         """Parse phản hồi JSON từ LLM."""
#         # Tìm JSON block trong response
#         json_pattern = r'```json\s*(.*?)\s*```'
#         json_match = re.search(json_pattern, response_text, re.DOTALL)
        
#         if json_match:
#             json_str = json_match.group(1)
#         else:
#             # Thử parse toàn bộ response như JSON
#             json_str = response_text.strip()
        
#         try:
#             evaluation_data = json.loads(json_str)
            
#             # Validate và đảm bảo có đủ các trường cần thiết
#             required_fields = ["context_relevance", "context_quality", "coverage_score", "coherence_score"]
#             for field in required_fields:
#                 if field not in evaluation_data:
#                     evaluation_data[field] = 0.0
            
#             # Tính overall_score nếu chưa có
#             if "overall_score" not in evaluation_data:
#                 scores = [evaluation_data[field] for field in required_fields]
#                 evaluation_data["overall_score"] = sum(scores) / len(scores)
            
#             return evaluation_data
            
#         except json.JSONDecodeError as e:
#             raise ValueError(f"Failed to parse LLM response as JSON: {e}\nResponse: {response_text}")
    
#     def _calculate_average_metrics(self, results: List[LLMRetrievalResult]) -> Dict[str, float]:
#         """Tính toán các chỉ số trung bình từ kết quả LLM."""
#         if not results:
#             return {}
        
#         # Tính trung bình các điểm số
#         avg_context_relevance = sum(r.context_relevance for r in results) / len(results)
#         avg_context_quality = sum(r.context_quality for r in results) / len(results)
#         avg_coverage = sum(r.coverage_score for r in results) / len(results)
#         avg_coherence = sum(r.coherence_score for r in results) / len(results)
#         avg_overall = sum(r.overall_score for r in results) / len(results)
        
#         # Thống kê bổ sung
#         successful_evaluations = sum(1 for r in results if r.overall_score > 0)
        
#         return {
#             "avg_context_relevance": avg_context_relevance,
#             "avg_context_quality": avg_context_quality,
#             "avg_coverage_score": avg_coverage,
#             "avg_coherence_score": avg_coherence,
#             "avg_overall_score": avg_overall,
#             "successful_evaluations": successful_evaluations,
#             "success_rate": successful_evaluations / len(results) * 100
#         }
    
#     def _generate_summary(self, metrics: Dict[str, float], individual_results: List[LLMRetrievalResult]) -> str:
#         """Tạo báo cáo tóm tắt kết quả đánh giá LLM."""
#         summary = "=== BÁO CÁO ĐÁNH GIÁ LLM-BASED RETRIEVAL ===\n\n"
        
#         summary += "📊 CÁC CHỈ SỐ TRUNG BÌNH:\n"
#         summary += f"  • Context Relevance: {metrics.get('avg_context_relevance', 0):.1f}/100\n"
#         summary += f"  • Context Quality: {metrics.get('avg_context_quality', 0):.1f}/100\n"
#         summary += f"  • Coverage Score: {metrics.get('avg_coverage_score', 0):.1f}/100\n"
#         summary += f"  • Coherence Score: {metrics.get('avg_coherence_score', 0):.1f}/100\n"
#         summary += f"  • Overall Score: {metrics.get('avg_overall_score', 0):.1f}/100\n"
        
#         total_queries = len(individual_results)
#         successful = metrics.get('successful_evaluations', 0)
        
#         summary += f"\n📈 THỐNG KÊ ĐÁNH GIÁ:\n"
#         summary += f"  • Tổng số truy vấn: {total_queries}\n"
#         summary += f"  • Đánh giá thành công: {successful}/{total_queries}\n"
#         summary += f"  • Tỷ lệ thành công: {metrics.get('success_rate', 0):.1f}%\n"
        
#         # Phân tích chất lượng
#         overall_score = metrics.get('avg_overall_score', 0)
#         relevance_score = metrics.get('avg_context_relevance', 0)
#         quality_score = metrics.get('avg_context_quality', 0)
#         coverage_score = metrics.get('avg_coverage_score', 0)
#         coherence_score = metrics.get('avg_coherence_score', 0)
        
#         summary += "\n🎯 ĐÁNH GIÁ CHI TIẾT:\n"
        
#         if overall_score >= 80:
#             summary += "  • Chất lượng tổng thể: XUẤT SẮC\n"
#         elif overall_score >= 60:
#             summary += "  • Chất lượng tổng thể: TỐT\n"
#         elif overall_score >= 40:
#             summary += "  • Chất lượng tổng thể: TRUNG BÌNH\n"
#         else:
#             summary += "  • Chất lượng tổng thể: CẦN CẢI THIỆN\n"
        
#         # Phân tích từng khía cạnh
#         aspects = [
#             ("Context Relevance", relevance_score, "Độ liên quan ngữ cảnh"),
#             ("Context Quality", quality_score, "Chất lượng nội dung"),
#             ("Coverage", coverage_score, "Độ bao phủ thông tin"), 
#             ("Coherence", coherence_score, "Tính nhất quán")
#         ]
        
#         summary += "\n📋 PHÂN TÍCH TỪNG KHÍA CẠNH:\n"
#         for name, score, description in aspects:
#             if score >= 80:
#                 level = "XUẤT SẮC"
#             elif score >= 60:
#                 level = "TỐT"
#             elif score >= 40:
#                 level = "TRUNG BÌNH"
#             else:
#                 level = "YẾU"
#             summary += f"  • {description}: {score:.1f} ({level})\n"
        
#         # Khuyến nghị
#         summary += "\n💡 KHUYẾN NGHỊ:\n"
#         if relevance_score < 60:
#             summary += "  • Cải thiện thuật toán tìm kiếm để tăng độ liên quan\n"
#         if quality_score < 60:
#             summary += "  • Kiểm tra và nâng cao chất lượng nguồn dữ liệu\n"
#         if coverage_score < 60:
#             summary += "  • Mở rộng corpus để bao phủ đầy đủ hơn\n"
#         if coherence_score < 60:
#             summary += "  • Xử lý duplicate và loại bỏ thông tin mâu thuẫn\n"
        
#         return summary
    
#     def export_detailed_results(self, results: List[LLMRetrievalResult], output_file: str = "llm_evaluation_results.json"):
#         """
#         Xuất kết quả đánh giá chi tiết ra file JSON.
        
#         Args:
#             results: Danh sách kết quả đánh giá
#             output_file: Đường dẫn file output
#         """
#         export_data = []
        
#         for result in results:
#             export_data.append({
#                 "query_id": result.query_id,
#                 "query_text": result.query_text,
#                 "scores": {
#                     "context_relevance": result.context_relevance,
#                     "context_quality": result.context_quality,
#                     "coverage_score": result.coverage_score,
#                     "coherence_score": result.coherence_score,
#                     "overall_score": result.overall_score
#                 },
#                 "documents_count": len(result.retrieved_docs),
#                 "detailed_feedback": result.detailed_feedback
#             })
        
#         with open(output_file, 'w', encoding='utf-8') as f:
#             json.dump(export_data, f, ensure_ascii=False, indent=2)
        
#         print(f"Đã xuất kết quả chi tiết ra file: {output_file}")

# if __name__ == "__main__":
#     """Test LLMRetrievalEvaluator"""
    
#     # Dữ liệu test mẫu
#     test_queries_and_docs = [
#         (
#             "RAG là gì và hoạt động như thế nào?",
#             [
#                 Document(
#                     page_content="RAG (Retrieval-Augmented Generation) là phương pháp kết hợp việc tìm kiếm tài liệu liên quan với khả năng sinh text của mô hình ngôn ngữ. Hệ thống RAG hoạt động bằng cách đầu tiên tìm kiếm các tài liệu có liên quan đến câu hỏi, sau đó sử dụng thông tin này để sinh ra câu trả lời chính xác.",
#                     metadata={"source": "wiki_rag", "type": "definition"}
#                 ),
#                 Document(
#                     page_content="Hệ thống RAG gồm 2 thành phần chính: Retriever (bộ tìm kiếm) và Generator (bộ sinh text). Retriever sử dụng embedding để tìm tài liệu liên quan, sau đó Generator sử dụng LLM để tạo câu trả lời dựa trên ngữ cảnh được cung cấp.",
#                     metadata={"source": "technical_guide", "type": "explanation"}
#                 ),
#                 Document(
#                     page_content="Thời tiết hôm nay rất đẹp, nắng vàng và nhiệt độ khoảng 25 độ C. Dự báo sẽ có mưa rào vào chiều tối.",
#                     metadata={"source": "weather_report", "type": "irrelevant"}
#                 )
#             ],
#             "Q1"
#         ),
#         (
#             "Ưu điểm của hệ thống RAG so với LLM truyền thống?",
#             [
#                 Document(
#                     page_content="RAG giúp LLM truy cập thông tin cập nhật mà không cần retrain model. Điều này giúp giảm chi phí và thời gian đào tạo.",
#                     metadata={"source": "comparison_study", "type": "advantage"}
#                 )
#             ],
#             "Q2"
#         )
#     ]
    
#     print("Testing LLMRetrievalEvaluator...")
    
#     try:
#         evaluator = LLMRetrievalEvaluator(temperature=0.1)
        
#         # Đánh giá một truy vấn đơn lẻ
#         single_result = evaluator.evaluate_single_query(
#             query=test_queries_and_docs[0][0],
#             documents=test_queries_and_docs[0][1],
#             query_id=test_queries_and_docs[0][2]
#         )
        
#         print("📊 KẾT QUẢ ĐÁNH GIÁ ĐỢN LẺ:")
#         print(f"Query: {single_result.query_text}")
#         print(f"Context Relevance: {single_result.context_relevance}")
#         print(f"Context Quality: {single_result.context_quality}")
#         print(f"Coverage Score: {single_result.coverage_score}")
#         print(f"Coherence Score: {single_result.coherence_score}")
#         print(f"Overall Score: {single_result.overall_score}")
        
#         # Đánh giá nhiều truy vấn
#         results = evaluator.evaluate_multiple_queries(test_queries_and_docs)
        
#         print("\n" + results['evaluation_summary'])
        
#         # Xuất kết quả chi tiết
#         evaluator.export_detailed_results(results['individual_results'])
        
#     except Exception as e:
#         print(f"Test failed: {e}")
#         import traceback
#         traceback.print_exc()