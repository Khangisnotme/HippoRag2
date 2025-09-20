"""
OnlineRetrievalAndQA/run_retrieval_pipeline.py - PLAN OVERVIEW
Xử lý file Excel questions và thêm detailed results từ các modules

PLAN STRUCTURE:
===============

1. INPUT/OUTPUT:
   - Input: questions.xlsx (cột 'question')
   - Output: questions_results.xlsx (+ nhiều cột mới)

2. COLUMNS SẼ ĐƯỢC THÊM:
   
   Module 1 - Dual Retrieval:
   - module1_top_passages: JSON [{id, score, text_preview}, ...]
   - module1_top_triples: JSON [{subject, predicate, object, score}, ...]
   - module1_stats: JSON {bm25_avg, embedding_avg, hybrid_avg}
   
   Module 2 - Triple Filtering:
   - module2_filtered_triples: JSON [{triple_id, relevance_score, level}, ...]
   - module2_stats: JSON {original_count, filtered_count, avg_relevance}
   
   Module 3 - Passage Ranking:
   - module3_ranked_passages: JSON [{passage_id, final_score, support_score}, ...]
   - module3_stats: JSON {reranking_changes, support_distribution}
   
   Module 4 - Context Expansion:
   - module4_expanded_contexts: JSON [{context_id, relevance_score, path}, ...]
   
   Final Results:
   - final_passages: JSON top passages với final scores
   - final_processing_time: float seconds
   - final_pipeline_stats: JSON overall statistics

3. CODE STRUCTURE:

class DetailedPipelineProcessor:
    - Extends RetrievalPipelineOrchestrator
    - Captures detailed outputs từ mỗi module
    - Extract functions cho từng module

def main():
    - Load Excel file
    - Initialize processor
    - Process each question
    - Add detailed columns
    - Save enhanced Excel

4. USAGE:
   python run_retrieval_pipeline.py --input questions.xlsx --output results.xlsx --top_k 10

5. FEATURES:
   ✅ Excel input/output
   ✅ Detailed module info capture
   ✅ JSON format for complex data
   ✅ Error handling per question
   ✅ Progress tracking
   ✅ Configurable parameters
   ✅ Excel formatting với colors
"""