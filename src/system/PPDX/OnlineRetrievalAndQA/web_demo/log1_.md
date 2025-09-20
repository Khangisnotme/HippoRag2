(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OnlineRetrievalAndQA\web_demo> python .\app_ppdx.py
✅ Real PPDX modules loaded successfully
🚀 Starting PPDX Web Demo (Simple Real Integration)...
📡 Server will be available at: http://localhost:8000
INFO:     Started server process [10732]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     ('127.0.0.1', 49375) - "WebSocket /ws/process" 403
INFO:     connection rejected (403 Forbidden)
INFO:     connection closed
🔄 First request - initializing PPDX...
🔄 Initializing PPDX pipeline...
2025-07-02 14:50:14,997 - module2_triple_filter - INFO - 🔑 Đã tải cấu hình API keys từ environment
2025-07-02 14:50:14,997 - module2_triple_filter - INFO -    📊 HuggingFace API: ✅ Có
2025-07-02 14:50:14,998 - module2_triple_filter - INFO -    🤖 OpenAI API: ✅ Có
2025-07-02 14:50:14,998 - retrieval_pipeline_orchestrator - INFO - 🚀 Khởi tạo RetrievalPipelineOrchestrator...
2025-07-02 14:50:14,999 - retrieval_pipeline_orchestrator - INFO -    🔧 Context expansion: Tắt
2025-07-02 14:50:14,999 - retrieval_pipeline_orchestrator - INFO -    📊 Output format: evaluation
2025-07-02 14:50:14,999 - retrieval_pipeline_orchestrator - INFO -    📋 Max final passages: 5
2025-07-02 14:50:15,000 - retrieval_pipeline_orchestrator - INFO - 🔧 Đang khởi tạo các modules...
2025-07-02 14:50:15,000 - retrieval_pipeline_orchestrator - INFO -    📊 Khởi tạo Module 1 - Dual Retrieval...
2025-07-02 14:50:15,000 - module1_dual_retrieval - INFO - 🚀 Đang khởi tạo DualRetriever...
2025-07-02 14:50:15,000 - module1_dual_retrieval - INFO - ⚙️ Cấu hình: BM25(0.3) + Embedding(0.7)
2025-07-02 14:50:15,001 - module1_dual_retrieval - INFO - 🗃️ Đang kết nối đến Neo4j: bolt://localhost:7687
2025-07-02 14:50:15,123 - module1_dual_retrieval - INFO - ✅ Kết nối Neo4j thành công
2025-07-02 14:50:15,123 - module1_dual_retrieval - INFO - 🔤 Khởi tạo BM25Retriever thành công
2025-07-02 14:50:15,124 - module1_dual_retrieval - INFO - 🧠 Khởi tạo EmbeddingRetriever thành công
2025-07-02 14:50:15,124 - module1_dual_retrieval - INFO - 🎭 Khởi tạo HybridScorer với trọng số: BM25=0.3, Embedding=0.7
2025-07-02 14:50:15,125 - module1_dual_retrieval - INFO - ✅ DualRetriever đã được khởi tạo thành công
2025-07-02 14:50:15,125 - retrieval_pipeline_orchestrator - INFO -    🤖 Khởi tạo Module 2 - LLM Triple Filter...
2025-07-02 14:50:15,125 - module2_triple_filter - INFO - 🚀 Khởi tạo LLMTripleFilter system...
2025-07-02 14:50:15,126 - module2_triple_filter - INFO -    🧠 Primary LLM: qwen2.5-7b-instruct
2025-07-02 14:50:15,126 - module2_triple_filter - INFO -    🔄 Backup LLM: gpt-3.5-turbo
2025-07-02 14:50:15,126 - module2_triple_filter - INFO -    📊 Strategy: moderate
2025-07-02 14:50:15,127 - module2_triple_filter - INFO -    🎯 Threshold: 0.3
2025-07-02 14:50:15,127 - module2_triple_filter - INFO -    🧠 Khởi tạo Qwen primary filter...
2025-07-02 14:50:15,127 - module2_triple_filter - INFO - 🧠 Khởi tạo QwenTripleFilter với HuggingFace Inference API...
2025-07-02 14:50:15,128 - module2_triple_filter - INFO -    💾 Caching: Bật
2025-07-02 14:50:15,128 - module2_triple_filter - INFO -    🌡️ Temperature: 0.1
2025-07-02 14:50:15,128 - module2_triple_filter - INFO -    📏 Max tokens: 800
2025-07-02 14:50:15,129 - module2_triple_filter - INFO -    🔄 Khởi tạo GPT-3.5 backup filter...
2025-07-02 14:50:15,129 - module2_triple_filter - INFO - 🤖 Khởi tạo GPTTripleFilter...
2025-07-02 14:50:15,130 - module2_triple_filter - INFO -    💾 Caching: Bật
2025-07-02 14:50:15,130 - module2_triple_filter - INFO -    🌡️ Temperature: 0.1
2025-07-02 14:50:15,130 - module2_triple_filter - INFO -    📏 Max tokens: 800
2025-07-02 14:50:15,131 - module2_triple_filter - INFO - ✅ OpenAI client đã sẵn sàng
2025-07-02 14:50:15,131 - module2_triple_filter - INFO - ✅ LLM providers đã được khởi tạo thành công
2025-07-02 14:50:15,131 - retrieval_pipeline_orchestrator - INFO -    🏆 Khởi tạo Module 3 - Passage Ranker...
2025-07-02 14:50:15,131 - module3_passage_ranker - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-07-02 14:50:15,132 - module3_passage_ranker - INFO -    🧮 Method: weighted_relevance
2025-07-02 14:50:15,132 - module3_passage_ranker - INFO -    🎯 Relevance threshold: 0.3
2025-07-02 14:50:15,132 - module3_passage_ranker - INFO - 🏆 Khởi tạo PassageRanker...
2025-07-02 14:50:15,133 - module3_passage_ranker - INFO -    📊 Strategy: hybrid_balanced
2025-07-02 14:50:15,133 - module3_passage_ranker - INFO -    🧮 Support method: weighted_relevance
2025-07-02 14:50:15,133 - module3_passage_ranker - INFO -    📝 Max output: 10
2025-07-02 14:50:15,134 - module3_passage_ranker - INFO -    ⚖️ Score normalization: Bật
2025-07-02 14:50:15,135 - retrieval_pipeline_orchestrator - INFO - ✅ Tất cả modules đã được khởi tạo thành công
2025-07-02 14:50:15,135 - module5_answer_generator - INFO - 🔑 Loaded API keys from environment
2025-07-02 14:50:15,135 - module5_answer_generator - INFO -    📊 HuggingFace API: ✅ Available
2025-07-02 14:50:15,135 - module5_answer_generator - INFO -    🤖 OpenAI API: ✅ Available
2025-07-02 14:50:15,135 - module5_answer_generator - INFO - 🤖 Initialized OpenAI client for answer generation
2025-07-02 14:50:15,135 - module5_answer_generator - INFO - ✅ Primary provider initialized: gpt-3.5-turbo
2025-07-02 14:50:15,135 - module5_answer_generator - INFO - 🤖 Initialized Qwen model for answer generation
2025-07-02 14:50:15,135 - module5_answer_generator - INFO -    📊 Model configuration: temperature=0.01, max_tokens=1000, top_p=0.9
2025-07-02 14:50:15,135 - module5_answer_generator - INFO - ✅ Backup provider initialized: qwen2.5-7b-instruct
2025-07-02 14:50:15,135 - module5_answer_generator.FallbackAnswerGenerator - INFO - ✅ Fallback Answer Generator initialized
2025-07-02 14:50:15,135 - module5_answer_generator - INFO - ✅ Fallback provider initialized
2025-07-02 14:50:15,135 - module5_answer_generator - INFO - 💾 Initialized answer cache
✅ Real PPDX pipeline initialized successfully
🔍 Processing with real PPDX: What are the benefits of regular exercise for ment...
2025-07-02 14:50:15,135 - run_retrieval_and_qa_pipeline - INFO - 🔍 Processing detailed query: WEB_1751442615135
2025-07-02 14:50:15,135 - run_retrieval_and_qa_pipeline - INFO - 📝 Query: 'What are the benefits of regular exercise for mental health?'
2025-07-02 14:50:15,135 - run_retrieval_and_qa_pipeline - INFO - 📊 Module 1: Dual Retrieval...
2025-07-02 14:50:15,135 - module1_dual_retrieval - INFO - ============================================================
2025-07-02 14:50:15,135 - module1_dual_retrieval - INFO - 🚀 BẮT ĐẦU TRUY XUẤT KÉP (DUAL RETRIEVAL)
2025-07-02 14:50:15,135 - module1_dual_retrieval - INFO - ============================================================
2025-07-02 14:50:15,135 - module1_dual_retrieval - INFO - 📝 Query: 'What are the benefits of regular exercise for mental health?'
2025-07-02 14:50:15,135 - module1_dual_retrieval - INFO - 🎯 Mục tiêu: 5 passages + 10 triples
2025-07-02 14:50:15,135 - module1_dual_retrieval - INFO -
🔍 GIAI ĐOẠN 1: TRUY XUẤT PASSAGES
2025-07-02 14:50:15,135 - module1_dual_retrieval - INFO - ----------------------------------------
2025-07-02 14:50:15,140 - module1_dual_retrieval - INFO - 🔧 Bắt đầu khởi tạo indices cho hệ thống truy xuất...
2025-07-02 14:50:15,140 - module1_dual_retrieval - INFO - 📥 Bước 1/4: Tải dữ liệu từ Neo4j...
2025-07-02 14:50:15,140 - module1_dual_retrieval - INFO - 📖 Đang truy vấn tất cả passages từ Neo4j...
2025-07-02 14:50:15,782 - module1_dual_retrieval - INFO - ✅ Đã truy xuất 3000 passages từ Neo4j
2025-07-02 14:50:15,783 - module1_dual_retrieval - INFO - 📊 Thống kê passages: tổng ký tự=1,487,836, trung bình=495.9 ký tự/passage
2025-07-02 14:50:15,783 - module1_dual_retrieval - INFO - 🔗 Đang truy vấn tất cả triples từ Neo4j...
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownPropertyKeyWarning} {category: UNRECOGNIZED} {title: The provided property key is not in the database} {description: One of the property names in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing property name is: original_subject)} {position: line: 5, column: 22, offset: 242} for query: '\n            MATCH (s:Phrase)-[r:RELATION]->(o:Phrase)\n            RETURN s.text as subject, r.predicate as predicate, o.text as object,\n                   
r.confidence as confidence, r.source_chunk as source_passage_id,\n                   r.original_subject as original_subject, r.original_object as original_object\n            ORDER BY r.confidence DESC\n            \n            '
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownPropertyKeyWarning} {category: UNRECOGNIZED} {title: The provided property key is not in the database} {description: One of the property names in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing property name is: original_object)} {position: line: 5, column: 62, offset: 282} for query: '\n            MATCH (s:Phrase)-[r:RELATION]->(o:Phrase)\n            RETURN s.text as subject, r.predicate as predicate, o.text as object,\n                   r.confidence as confidence, r.source_chunk as source_passage_id,\n                   r.original_subject as original_subject, r.original_object as original_object\n            ORDER BY r.confidence DESC\n            \n            '
2025-07-02 14:50:17,654 - module1_dual_retrieval - INFO - ✅ Đã truy xuất 20662 triples từ Neo4j
2025-07-02 14:50:17,654 - module1_dual_retrieval - INFO - 📊 Thống kê triples:
2025-07-02 14:50:17,654 - module1_dual_retrieval - INFO -    - Confidence trung bình: 0.850
2025-07-02 14:50:17,654 - module1_dual_retrieval - INFO -    - Triples confidence cao (≥0.8): 20662/20662
2025-07-02 14:50:17,654 - module1_dual_retrieval - INFO -    - Số predicates unique: 4319
2025-07-02 14:50:17,654 - module1_dual_retrieval - INFO - 🔍 Bước 2/4: Xây dựng indices BM25...
2025-07-02 14:50:17,664 - module1_dual_retrieval - INFO - 🔍 Bắt đầu xây dựng chỉ mục BM25 cho 3000 passages...
2025-07-02 14:50:17,679 - module1_dual_retrieval - INFO -    📝 Đã xử lý 100/3000 passages
2025-07-02 14:50:17,684 - module1_dual_retrieval - INFO -    📝 Đã xử lý 200/3000 passages
2025-07-02 14:50:17,700 - module1_dual_retrieval - INFO -    📝 Đã xử lý 300/3000 passages
2025-07-02 14:50:17,715 - module1_dual_retrieval - INFO -    📝 Đã xử lý 400/3000 passages
2025-07-02 14:50:17,731 - module1_dual_retrieval - INFO -    📝 Đã xử lý 500/3000 passages
2025-07-02 14:50:17,731 - module1_dual_retrieval - INFO -    📝 Đã xử lý 600/3000 passages
2025-07-02 14:50:17,748 - module1_dual_retrieval - INFO -    📝 Đã xử lý 700/3000 passages
2025-07-02 14:50:17,763 - module1_dual_retrieval - INFO -    📝 Đã xử lý 800/3000 passages
2025-07-02 14:50:17,769 - module1_dual_retrieval - INFO -    📝 Đã xử lý 900/3000 passages
2025-07-02 14:50:17,790 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1000/3000 passages
2025-07-02 14:50:17,803 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1100/3000 passages
2025-07-02 14:50:17,817 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1200/3000 passages
2025-07-02 14:50:17,831 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1300/3000 passages
2025-07-02 14:50:17,831 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1400/3000 passages
2025-07-02 14:50:17,864 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1500/3000 passages
2025-07-02 14:50:17,875 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1600/3000 passages
2025-07-02 14:50:17,887 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1700/3000 passages
2025-07-02 14:50:17,900 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1800/3000 passages
2025-07-02 14:50:17,908 - module1_dual_retrieval - INFO -    📝 Đã xử lý 1900/3000 passages
2025-07-02 14:50:17,917 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2000/3000 passages
2025-07-02 14:50:17,922 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2100/3000 passages
2025-07-02 14:50:17,931 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2200/3000 passages
2025-07-02 14:50:17,956 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2300/3000 passages
2025-07-02 14:50:17,974 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2400/3000 passages
2025-07-02 14:50:17,990 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2500/3000 passages
2025-07-02 14:50:18,001 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2600/3000 passages
2025-07-02 14:50:18,009 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2700/3000 passages
2025-07-02 14:50:18,021 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2800/3000 passages
2025-07-02 14:50:18,031 - module1_dual_retrieval - INFO -    📝 Đã xử lý 2900/3000 passages
2025-07-02 14:50:18,040 - module1_dual_retrieval - INFO -    📝 Đã xử lý 3000/3000 passages
2025-07-02 14:50:18,040 - module1_dual_retrieval - INFO - 🔨 Đang xây dựng chỉ mục BM25 cho passages...
2025-07-02 14:50:18,131 - module1_dual_retrieval - INFO - ✅ Hoàn thành xây dựng chỉ mục BM25 với k1=1.2, b=0.75
2025-07-02 14:50:18,132 - module1_dual_retrieval - INFO - 🔗 Bắt đầu xây dựng chỉ mục BM25 cho 20662 triples...
2025-07-02 14:50:18,138 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 500/20662 triples
2025-07-02 14:50:18,147 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 1000/20662 triples
2025-07-02 14:50:18,154 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 1500/20662 triples
2025-07-02 14:50:18,161 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 2000/20662 triples
2025-07-02 14:50:18,169 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 2500/20662 triples
2025-07-02 14:50:18,177 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 3000/20662 triples
2025-07-02 14:50:18,186 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 3500/20662 triples
2025-07-02 14:50:18,192 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 4000/20662 triples
2025-07-02 14:50:18,199 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 4500/20662 triples
2025-07-02 14:50:18,201 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 5000/20662 triples
2025-07-02 14:50:18,213 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 5500/20662 triples
2025-07-02 14:50:18,217 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 6000/20662 triples
2025-07-02 14:50:18,227 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 6500/20662 triples
2025-07-02 14:50:18,234 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 7000/20662 triples
2025-07-02 14:50:18,239 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 7500/20662 triples
2025-07-02 14:50:18,248 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 8000/20662 triples
2025-07-02 14:50:18,256 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 8500/20662 triples
2025-07-02 14:50:18,257 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 9000/20662 triples
2025-07-02 14:50:18,269 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 9500/20662 triples
2025-07-02 14:50:18,269 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 10000/20662 triples
2025-07-02 14:50:18,283 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 10500/20662 triples
2025-07-02 14:50:18,284 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 11000/20662 triples
2025-07-02 14:50:18,297 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 11500/20662 triples
2025-07-02 14:50:18,302 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 12000/20662 triples
2025-07-02 14:50:18,312 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 12500/20662 triples
2025-07-02 14:50:18,318 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 13000/20662 triples
2025-07-02 14:50:18,323 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 13500/20662 triples
2025-07-02 14:50:18,458 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 14000/20662 triples
2025-07-02 14:50:18,466 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 14500/20662 triples
2025-07-02 14:50:18,473 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 15000/20662 triples
2025-07-02 14:50:18,480 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 15500/20662 triples
2025-07-02 14:50:18,483 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 16000/20662 triples
2025-07-02 14:50:18,493 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 16500/20662 triples
2025-07-02 14:50:18,501 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 17000/20662 triples
2025-07-02 14:50:18,509 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 17500/20662 triples
2025-07-02 14:50:18,518 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 18000/20662 triples
2025-07-02 14:50:18,526 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 18500/20662 triples
2025-07-02 14:50:18,534 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 19000/20662 triples
2025-07-02 14:50:18,540 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 19500/20662 triples
2025-07-02 14:50:18,547 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 20000/20662 triples
2025-07-02 14:50:18,550 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 20500/20662 triples
2025-07-02 14:50:18,558 - module1_dual_retrieval - INFO -    🔗 Đã xử lý 20662/20662 triples
2025-07-02 14:50:18,558 - module1_dual_retrieval - INFO - 🔨 Đang xây dựng chỉ mục BM25 cho triples...
2025-07-02 14:50:18,616 - module1_dual_retrieval - INFO - ✅ Hoàn thành xây dựng chỉ mục BM25 cho triples
2025-07-02 14:50:18,633 - module1_dual_retrieval - INFO - 🧠 Bước 3/4: Tạo embeddings...
2025-07-02 14:50:18,633 - module1_dual_retrieval - INFO - 🧠 Bắt đầu tạo embeddings cho 3000 passages...
2025-07-02 14:50:18,634 - module1_dual_retrieval - INFO - 📥 Đang tải model embedding: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
2025-07-02 14:50:18,634 - module1_dual_retrieval - INFO - 🖥️ Sử dụng thiết bị: cpu
modules.json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 229/229 [00:00<?, ?B/s]
D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\.venv\Lib\site-packages\huggingface_hub\file_download.py:143: UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in C:\Users\User\.cache\huggingface\hub\models--sentence-transformers--paraphrase-multilingual-mpnet-base-v2. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations. 
To support symlinks on Windows, you either need to activate Developer Mode or to run Python as an administrator. In order to activate developer mode, see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development
  warnings.warn(message)
config_sentence_transformers.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 122/122 [00:00<?, ?B/s]
README.md: 3.90kB [00:00, ?B/s]
sentence_bert_config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████| 53.0/53.0 [00:00<?, ?B/s]
config.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 723/723 [00:00<?, ?B/s]
model.safetensors: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████| 1.11G/1.11G [00:20<00:00, 54.4MB/s]
tokenizer_config.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 402/402 [00:00<?, ?B/s]
sentencepiece.bpe.model: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████| 5.07M/5.07M [00:01<00:00, 3.64MB/s]
tokenizer.json: 9.08MB [00:00, 136MB/s]
special_tokens_map.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 239/239 [00:00<?, ?B/s]



----




# Ask question: 


```bash
🔍 Processing with real PPDX: Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thí...
2025-07-02 15:17:51,433 - run_retrieval_and_qa_pipeline - INFO - 🔍 Processing detailed query: WEB_1751444271433
2025-07-02 15:17:51,433 - run_retrieval_and_qa_pipeline - INFO - 📝 Query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào'
2025-07-02 15:17:51,434 - run_retrieval_and_qa_pipeline - INFO - 📊 Module 1: Dual Retrieval...
2025-07-02 15:17:51,434 - module1_dual_retrieval - INFO - ============================================================
2025-07-02 15:17:51,434 - module1_dual_retrieval - INFO - 🚀 BẮT ĐẦU TRUY XUẤT KÉP (DUAL RETRIEVAL)
2025-07-02 15:17:51,434 - module1_dual_retrieval - INFO - ============================================================
2025-07-02 15:17:51,435 - module1_dual_retrieval - INFO - 📝 Query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào'
2025-07-02 15:17:51,435 - module1_dual_retrieval - INFO - 🎯 Mục tiêu: 5 passages + 10 triples
2025-07-02 15:17:51,435 - module1_dual_retrieval - INFO -
🔍 GIAI ĐOẠN 1: TRUY XUẤT PASSAGES
2025-07-02 15:17:51,436 - module1_dual_retrieval - INFO - ----------------------------------------
2025-07-02 15:17:51,436 - module1_dual_retrieval - INFO - ℹ️ Indices đã được khởi tạo trước đó, bỏ qua...
2025-07-02 15:17:51,436 - module1_dual_retrieval - INFO - 🔍 Bắt đầu truy xuất top-5 passages...
2025-07-02 15:17:51,437 - module1_dual_retrieval - INFO - 📝 Query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào'
2025-07-02 15:17:51,437 - module1_dual_retrieval - INFO - 🔤 Thực hiện tìm kiếm BM25...
2025-07-02 15:17:51,438 - module1_dual_retrieval - INFO - 🔍 Tìm kiếm BM25 passages với query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thí...'
2025-07-02 15:17:51,438 - module1_dual_retrieval - INFO - 📝 Query tokens: ['núi', 'lang', 'biang', 'ở', 'lạc', 'dương', 'lâm', 'đồng', 'được', 'giải', 'thích', 'bằng', 'huyền', 'thoại', 'nào']
2025-07-02 15:17:51,456 - module1_dual_retrieval - INFO - 🎯 BM25 passages: tìm thấy 15/15 kết quả có điểm > 0
2025-07-02 15:17:51,457 - module1_dual_retrieval - INFO - 🧠 Thực hiện tìm kiếm Embedding...
2025-07-02 15:17:51,457 - module1_dual_retrieval - INFO - 🧠 Tìm kiếm embedding passages với query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thí...'
2025-07-02 15:17:51,516 - module1_dual_retrieval - INFO - 🔍 Đã tạo embedding cho query. Shape: (1, 768)
2025-07-02 15:17:51,534 - module1_dual_retrieval - INFO - 🎯 Embedding passages: 15/15 kết quả có điểm > 0.5
2025-07-02 15:17:51,535 - module1_dual_retrieval - INFO - 📊 Điểm cao nhất: 0.774, thấp nhất: 0.635
2025-07-02 15:17:51,535 - module1_dual_retrieval - INFO - 🎭 Kết hợp điểm số lai...
2025-07-02 15:17:51,535 - module1_dual_retrieval - INFO - 🎭 Bắt đầu kết hợp điểm số: 15 BM25 + 15 embedding
2025-07-02 15:17:51,536 - module1_dual_retrieval - INFO - 📊 Normalized scores - BM25: min=0.000, max=1.000
2025-07-02 15:17:51,536 - module1_dual_retrieval - INFO - 📊 Normalized scores - Embedding: min=0.000, max=1.000
2025-07-02 15:17:51,537 - module1_dual_retrieval - INFO - 🔀 Đang kết hợp điểm cho 27 items unique...
2025-07-02 15:17:51,537 - module1_dual_retrieval - INFO - 🏆 Điểm lai: cao nhất=0.966, thấp nhất=0.000
2025-07-02 15:17:51,539 - module1_dual_retrieval - INFO - 📈 Nguồn điểm: cả hai=3, chỉ BM25=10, chỉ embedding=11
2025-07-02 15:17:51,539 - module1_dual_retrieval - INFO - ✅ Hoàn thành kết hợp điểm, trả về 5/5 kết quả
2025-07-02 15:17:51,539 - module1_dual_retrieval - INFO - 📦 Tạo objects kết quả...
2025-07-02 15:17:51,540 - module1_dual_retrieval - INFO -    1. passage_chunk_Cao nguyên Lâm Viên_17_0 - Điểm: 0.966 (BM25: 0.885, Emb: 1.000)
2025-07-02 15:17:51,540 - module1_dual_retrieval - INFO -    2. passage_chunk_Cao nguyên Lâm Viên_710_0 - Điểm: 0.966 (BM25: 0.885, Emb: 1.000)
2025-07-02 15:17:51,541 - module1_dual_retrieval - INFO -    3. passage_chunk_Khu dự trữ sinh quyển Langbiang_14_0 - Điểm: 0.809 (BM25: 1.000, Emb: 0.728)
2025-07-02 15:17:51,541 - module1_dual_retrieval - INFO -    4. passage_chunk_Đỉnh Langbiang_19_0 - Điểm: 0.267 (BM25: 0.891, Emb: 0.000)
2025-07-02 15:17:51,541 - module1_dual_retrieval - INFO -    5. passage_chunk_Tây Ninh_1560_0 - Điểm: 0.202 (BM25: 0.000, Emb: 0.289)
2025-07-02 15:17:51,542 - module1_dual_retrieval - INFO - ✅ Hoàn thành truy xuất 5 passages
2025-07-02 15:17:51,542 - module1_dual_retrieval - INFO -
🔗 GIAI ĐOẠN 2: TRUY XUẤT TRIPLES
2025-07-02 15:17:51,543 - module1_dual_retrieval - INFO - ----------------------------------------
2025-07-02 15:17:51,543 - module1_dual_retrieval - INFO - ℹ️ Indices đã được khởi tạo trước đó, bỏ qua...
2025-07-02 15:17:51,543 - module1_dual_retrieval - INFO - 🔗 Bắt đầu truy xuất top-10 triples...
2025-07-02 15:17:51,544 - module1_dual_retrieval - INFO - 📝 Query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào'
2025-07-02 15:17:51,545 - module1_dual_retrieval - INFO - 🔤 Thực hiện tìm kiếm BM25 cho triples...
2025-07-02 15:17:51,545 - module1_dual_retrieval - INFO - 🔗 Tìm kiếm BM25 triples với query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thí...'
2025-07-02 15:17:51,636 - module1_dual_retrieval - INFO - 🎯 BM25 triples: tìm thấy 30/30 kết quả có điểm > 0
2025-07-02 15:17:51,636 - module1_dual_retrieval - INFO - 🧠 Thực hiện tìm kiếm Embedding cho triples...
2025-07-02 15:17:51,637 - module1_dual_retrieval - INFO - 🔗 Tìm kiếm embedding triples với query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thí...'
2025-07-02 15:17:51,812 - module1_dual_retrieval - INFO - 🎯 Embedding triples: 30/30 kết quả có điểm > 0.3
2025-07-02 15:17:51,813 - module1_dual_retrieval - INFO - 📊 Điểm cao nhất: 0.761, thấp nhất: 0.663
2025-07-02 15:17:51,814 - module1_dual_retrieval - INFO - 🎭 Kết hợp điểm số lai cho triples...
2025-07-02 15:17:51,814 - module1_dual_retrieval - INFO - 🎭 Bắt đầu kết hợp điểm số: 30 BM25 + 30 embedding
2025-07-02 15:17:51,814 - module1_dual_retrieval - INFO - 📊 Normalized scores - BM25: min=0.000, max=1.000
2025-07-02 15:17:51,815 - module1_dual_retrieval - INFO - 📊 Normalized scores - Embedding: min=0.000, max=1.000
2025-07-02 15:17:51,815 - module1_dual_retrieval - INFO - 🔀 Đang kết hợp điểm cho 58 items unique...
2025-07-02 15:17:51,816 - module1_dual_retrieval - INFO - 🏆 Điểm lai: cao nhất=0.853, thấp nhất=0.000
2025-07-02 15:17:51,816 - module1_dual_retrieval - INFO - 📈 Nguồn điểm: cả hai=2, chỉ BM25=27, chỉ embedding=26
2025-07-02 15:17:51,817 - module1_dual_retrieval - INFO - ✅ Hoàn thành kết hợp điểm, trả về 10/10 kết quả
2025-07-02 15:17:51,817 - module1_dual_retrieval - INFO - 📦 Tạo objects kết quả triples...
2025-07-02 15:17:51,818 - module1_dual_retrieval - INFO -    1. (caonnguyen lam vien → has mountain peaks → lang biang) - Điểm: 0.853
2025-07-02 15:17:51,818 - module1_dual_retrieval - INFO -    2. (núi đôi quản bạ → thuộc → tỉnh hà giang) - Điểm: 0.598
2025-07-02 15:17:51,819 - module1_dual_retrieval - INFO -    3. (xã quảng thọ → part of → huyện quảng điền) - Điểm: 0.412
2025-07-02 15:17:51,819 - module1_dual_retrieval - INFO -    4. (xuân thu → is part of → chinese history) - Điểm: 0.336
2025-07-02 15:17:51,820 - module1_dual_retrieval - INFO -    5. (phổ đà sơn → is called → núi chùa cao) - Điểm: 0.325
2025-07-02 15:17:51,821 - module1_dual_retrieval - INFO -    6. (phổ đà sơn → is called → núi chùa cao) - Điểm: 0.325
2025-07-02 15:17:51,821 - module1_dual_retrieval - INFO -    7. (phổ đà sơn → is called → núi chùa cao) - Điểm: 0.325
2025-07-02 15:17:51,822 - module1_dual_retrieval - INFO -    8. (phổ đà sơn → is called → núi chùa cao) - Điểm: 0.325
2025-07-02 15:17:51,822 - module1_dual_retrieval - INFO -    9. (lang biang → named after → chàng k’lang và nàng h'biang) - Điểm: 0.300
2025-07-02 15:17:51,823 - module1_dual_retrieval - INFO -    10. (caonnguyen lam vien → is also known as → cao nguyên lang biang) - Điểm: 0.270
2025-07-02 15:17:51,823 - module1_dual_retrieval - INFO - ✅ Hoàn thành truy xuất 10 triples
2025-07-02 15:17:51,824 - module1_dual_retrieval - INFO -
📊 BIÊN SOẠN THỐNG KÊ
2025-07-02 15:17:51,824 - module1_dual_retrieval - INFO - ----------------------------------------
2025-07-02 15:17:51,825 - module1_dual_retrieval - INFO - ============================================================
2025-07-02 15:17:51,825 - module1_dual_retrieval - INFO - 🎉 HOÀN THÀNH TRUY XUẤT KÉP
2025-07-02 15:17:51,826 - module1_dual_retrieval - INFO - ============================================================
2025-07-02 15:17:51,826 - module1_dual_retrieval - INFO - ⏱️ Tổng thời gian: 0.39 giây
2025-07-02 15:17:51,826 - module1_dual_retrieval - INFO - 📖 Passages tìm được: 5/5
2025-07-02 15:17:51,827 - module1_dual_retrieval - INFO - 🔗 Triples tìm được: 10/10
2025-07-02 15:17:51,827 - module1_dual_retrieval - INFO - 📊 Hiệu suất: 38.6 items/giây
2025-07-02 15:17:51,828 - module1_dual_retrieval - INFO - 📈 Điểm trung bình passages: 0.642
2025-07-02 15:17:51,828 - module1_dual_retrieval - INFO - 📈 Điểm trung bình triples: 0.407
2025-07-02 15:17:51,829 - module1_dual_retrieval - INFO - ============================================================
2025-07-02 15:17:51,829 - run_retrieval_and_qa_pipeline - INFO - 🤖 Module 2: Triple Filtering...
2025-07-02 15:17:51,830 - module2_triple_filter - INFO - ============================================================
2025-07-02 15:17:51,830 - module2_triple_filter - INFO - 🤖 BẮT ĐẦU LLM TRIPLE FILTERING
2025-07-02 15:17:51,831 - module2_triple_filter - INFO - ============================================================
2025-07-02 15:17:51,831 - module2_triple_filter - INFO - 📝 Query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào'
2025-07-02 15:17:51,832 - module2_triple_filter - INFO - 📊 Raw triples: 10
2025-07-02 15:17:51,832 - module2_triple_filter - INFO - 🎯 Target threshold: 0.3
2025-07-02 15:17:51,832 - module2_triple_filter - INFO -
🔄 PROCESSING TRIPLES IN BATCHES
2025-07-02 15:17:51,833 - module2_triple_filter - INFO - ----------------------------------------
2025-07-02 15:17:51,834 - module2_triple_filter - INFO - 📦 Batch 1/2: triples 1-8
2025-07-02 15:17:51,834 - module2_triple_filter - INFO -    🧠 Sử dụng qwen2.5-7b-instruct primary filter...
2025-07-02 15:17:51,834 - module2_triple_filter - INFO - 🧠 Bắt đầu filtering 8 triples với Qwen API...
2025-07-02 15:17:51,835 - module2_triple_filter - INFO - 📝 Tạo filtering prompt cho 8 triples...
2025-07-02 15:17:51,835 - module2_triple_filter - INFO -    📏 Prompt length: 3899 characters
2025-07-02 15:17:51,836 - module2_triple_filter - INFO -    🔤 Estimated tokens: ~974
2025-07-02 15:17:51,836 - module2_triple_filter - INFO -    🔄 Đang gửi request đến HuggingFace Inference API (chat completion)...
2025-07-02 15:17:51,837 - module2_triple_filter - ERROR - ❌ Lỗi trong Qwen API filtering: Provider 'featherless-ai' not supported. Available values: 'auto' or any provider from ['black-forest-labs', 'cerebras', 'cohere', 'fal-ai', 'fireworks-ai', 'hf-inference', 'hyperbolic', 'nebius', 'novita', 'nscale', 'openai', 'replicate', 'sambanova', 'together'].Passing 'auto' (default value) will automatically select the first provider available for the model, sorted by the user's order in https://hf.co/settings/inference-providers.
2025-07-02 15:17:51,838 - module2_triple_filter - ERROR - Chi tiết lỗi:
Traceback (most recent call last):
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OnlineRetrievalAndQA\module2_triple_filter.py", line 291, in filter_triples_batch
    completion = self.client.chat.completions.create(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\.venv\Lib\site-packages\huggingface_hub\inference\_client.py", line 887, in chat_completion    
    provider_helper = get_provider_helper(
                      ^^^^^^^^^^^^^^^^^^^^
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\.venv\Lib\site-packages\huggingface_hub\inference\_providers\__init__.py", line 181, in get_provider_helper
    raise ValueError(
ValueError: Provider 'featherless-ai' not supported. Available values: 'auto' or any provider from ['black-forest-labs', 'cerebras', 'cohere', 'fal-ai', 'fireworks-ai', 'hf-inference', 'hyperbolic', 'nebius', 'novita', 'nscale', 'openai', 'replicate', 'sambanova', 'together'].Passing 'auto' (default value) will automatically select the first provider available for the model, sorted by the user's order in https://hf.co/settings/inference-providers.
2025-07-02 15:17:51,841 - module2_triple_filter - WARNING - 🔄 Tạo fallback evaluations (reason: qwen_api_error: Provider 'featherless-ai' not supported. Available values: 'auto' or any provider from ['black-forest-labs', 'cerebras', 'cohere', 'fal-ai', 'fireworks-ai', 'hf-inference', 'hyperbolic', 'nebius', 'novita', 'nscale', 'openai', 'replicate', 'sambanova', 'together'].Passing 'auto' (default value) will automatically select the first provider available for the model, sorted by the user's order in https://hf.co/settings/inference-providers.)...
2025-07-02 15:17:51,842 - module2_triple_filter - WARNING -    📊 Tạo 8 fallback evaluations với moderate relevance
2025-07-02 15:17:51,842 - module2_triple_filter - INFO -    📊 Evaluation quality: 1.00 (8/8 valid)
2025-07-02 15:17:51,842 - module2_triple_filter - INFO -    ✅ Primary LLM filtering thành công
2025-07-02 15:17:51,843 - module2_triple_filter - INFO -    ✅ Hoàn thành batch 1, evaluations: 8
2025-07-02 15:17:51,844 - module2_triple_filter - INFO - 📦 Batch 2/2: triples 9-10
2025-07-02 15:17:51,844 - module2_triple_filter - INFO -    🧠 Sử dụng qwen2.5-7b-instruct primary filter...
2025-07-02 15:17:51,845 - module2_triple_filter - INFO - 🧠 Bắt đầu filtering 2 triples với Qwen API...
2025-07-02 15:17:51,845 - module2_triple_filter - INFO - 📝 Tạo filtering prompt cho 2 triples...
2025-07-02 15:17:51,845 - module2_triple_filter - INFO -    📏 Prompt length: 2761 characters
2025-07-02 15:17:51,846 - module2_triple_filter - INFO -    🔤 Estimated tokens: ~690
2025-07-02 15:17:51,846 - module2_triple_filter - INFO -    🔄 Đang gửi request đến HuggingFace Inference API (chat completion)...
2025-07-02 15:17:51,846 - module2_triple_filter - ERROR - ❌ Lỗi trong Qwen API filtering: Provider 'featherless-ai' not supported. Available values: 'auto' or any provider from ['black-forest-labs', 'cerebras', 'cohere', 'fal-ai', 'fireworks-ai', 'hf-inference', 'hyperbolic', 'nebius', 'novita', 'nscale', 'openai', 'replicate', 'sambanova', 'together'].Passing 'auto' (default value) will automatically select the first provider available for the model, sorted by the user's order in https://hf.co/settings/inference-providers.
2025-07-02 15:17:51,847 - module2_triple_filter - ERROR - Chi tiết lỗi:
Traceback (most recent call last):
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OnlineRetrievalAndQA\module2_triple_filter.py", line 291, in filter_triples_batch
    completion = self.client.chat.completions.create(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\.venv\Lib\site-packages\huggingface_hub\inference\_client.py", line 887, in chat_completion    
    provider_helper = get_provider_helper(
                      ^^^^^^^^^^^^^^^^^^^^
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\.venv\Lib\site-packages\huggingface_hub\inference\_providers\__init__.py", line 181, in get_provider_helper
    raise ValueError(
ValueError: Provider 'featherless-ai' not supported. Available values: 'auto' or any provider from ['black-forest-labs', 'cerebras', 'cohere', 'fal-ai', 'fireworks-ai', 'hf-inference', 'hyperbolic', 'nebius', 'novita', 'nscale', 'openai', 'replicate', 'sambanova', 'together'].Passing 'auto' (default value) will automatically select the first provider available for the model, sorted by the user's order in https://hf.co/settings/inference-providers.
2025-07-02 15:17:51,849 - module2_triple_filter - WARNING - 🔄 Tạo fallback evaluations (reason: qwen_api_error: Provider 'featherless-ai' not supported. Available values: 'auto' or any provider from ['black-forest-labs', 'cerebras', 'cohere', 'fal-ai', 'fireworks-ai', 'hf-inference', 'hyperbolic', 'nebius', 'novita', 'nscale', 'openai', 'replicate', 'sambanova', 'together'].Passing 'auto' (default value) will automatically select the first provider available for the model, sorted by the user's order in https://hf.co/settings/inference-providers.)...
2025-07-02 15:17:51,850 - module2_triple_filter - WARNING -    📊 Tạo 2 fallback evaluations với moderate relevance
2025-07-02 15:17:51,851 - module2_triple_filter - INFO -    📊 Evaluation quality: 1.00 (2/2 valid)
2025-07-02 15:17:51,851 - module2_triple_filter - INFO -    ✅ Primary LLM filtering thành công
2025-07-02 15:17:51,851 - module2_triple_filter - INFO -    ✅ Hoàn thành batch 2, evaluations: 2
2025-07-02 15:17:51,851 - module2_triple_filter - INFO -
🔧 CONVERTING TO FILTERED TRIPLES
2025-07-02 15:17:51,853 - module2_triple_filter - INFO - ----------------------------------------
2025-07-02 15:17:51,854 - module2_triple_filter - INFO - 🔧 Converting 10 evaluations thành FilteredTriple objects...
2025-07-02 15:17:51,854 - module2_triple_filter - INFO -    📦 Converted 10/10 triples
2025-07-02 15:17:51,855 - module2_triple_filter - INFO - ✅ Hoàn thành conversion: 10 FilteredTriple objects
2025-07-02 15:17:51,855 - module2_triple_filter - INFO -
🎯 APPLYING FILTERING STRATEGY
2025-07-02 15:17:51,856 - module2_triple_filter - INFO - ----------------------------------------
2025-07-02 15:17:51,856 - module2_triple_filter - INFO - 🎯 Áp dụng filtering strategy: moderate
2025-07-02 15:17:51,856 - module2_triple_filter - INFO -    🎯 Fixed threshold: 0.300
2025-07-02 15:17:51,857 - module2_triple_filter - INFO -    📊 highly_relevant: 0 triples
2025-07-02 15:17:51,857 - module2_triple_filter - INFO -    📊 moderately_relevant: 10 triples
2025-07-02 15:17:51,858 - module2_triple_filter - INFO -    📊 slightly_relevant: 0 triples
2025-07-02 15:17:51,858 - module2_triple_filter - INFO -    📊 not_relevant: 0 triples
2025-07-02 15:17:51,859 - module2_triple_filter - INFO - ✅ Filtering strategy applied: 10 → 10 triples
2025-07-02 15:17:51,860 - module2_triple_filter - INFO - 📊 Tạo filtering statistics...
2025-07-02 15:17:51,860 - module2_triple_filter - INFO - ============================================================
2025-07-02 15:17:51,861 - module2_triple_filter - INFO - 🎉 LLM TRIPLE FILTERING HOÀN THÀNH
2025-07-02 15:17:51,861 - module2_triple_filter - INFO - ============================================================
2025-07-02 15:17:51,861 - module2_triple_filter - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-07-02 15:17:51,862 - module2_triple_filter - INFO -    📝 Query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào'
2025-07-02 15:17:51,862 - module2_triple_filter - INFO -    ⏱️ Thời gian xử lý: 0.03 giây
2025-07-02 15:17:51,863 - module2_triple_filter - INFO -    📈 Triples: 10 → 10
2025-07-02 15:17:51,863 - module2_triple_filter - INFO -    📊 Tỷ lệ giữ lại: 100.00%
2025-07-02 15:17:51,863 - module2_triple_filter - INFO -
📊 PHÂN BỐ RELEVANCE:
2025-07-02 15:17:51,864 - module2_triple_filter - INFO -    highly_relevant: 0 triples (0.0%) - Rất liên quan - Trả lời trực tiếp câu hỏi
2025-07-02 15:17:51,865 - module2_triple_filter - INFO -    moderately_relevant: 10 triples (100.0%) - Liên quan vừa phải - Cung cấp context hữu ích
2025-07-02 15:17:51,865 - module2_triple_filter - INFO -    slightly_relevant: 0 triples (0.0%) - Ít liên quan - Thông tin phụ trợ
2025-07-02 15:17:51,866 - module2_triple_filter - INFO -    not_relevant: 0 triples (0.0%) - Không liên quan - Thông tin nhiễu
2025-07-02 15:17:51,866 - module2_triple_filter - INFO -
🏆 TOP 5 FILTERED TRIPLES:
2025-07-02 15:17:51,867 - module2_triple_filter - INFO -    1. (caonnguyen lam vien → has mountain peaks → lang biang) | Relevance: 0.556 | Level: moderately_relevant | Quality: 0.644
2025-07-02 15:17:51,868 - module2_triple_filter - INFO -       💭 Explanation: Đánh giá fallback do qwen_api_error: Provider 'featherless-ai' not supported. Available values: 'aut...
2025-07-02 15:17:51,868 - module2_triple_filter - INFO -    2. (núi đôi quản bạ → thuộc → tỉnh hà giang) | Relevance: 0.480 | Level: moderately_relevant | Quality: 0.591
2025-07-02 15:17:51,869 - module2_triple_filter - INFO -       💭 Explanation: Đánh giá fallback do qwen_api_error: Provider 'featherless-ai' not supported. Available values: 'aut...
2025-07-02 15:17:51,869 - module2_triple_filter - INFO -    3. (xã quảng thọ → part of → huyện quảng điền) | Relevance: 0.424 | Level: moderately_relevant | Quality: 0.551
2025-07-02 15:17:51,870 - module2_triple_filter - INFO -       💭 Explanation: Đánh giá fallback do qwen_api_error: Provider 'featherless-ai' not supported. Available values: 'aut...
2025-07-02 15:17:51,871 - module2_triple_filter - INFO -    4. (xuân thu → is part of → chinese history) | Relevance: 0.401 | Level: moderately_relevant | Quality: 0.536
2025-07-02 15:17:51,871 - module2_triple_filter - INFO -       💭 Explanation: Đánh giá fallback do qwen_api_error: Provider 'featherless-ai' not supported. Available values: 'aut...
2025-07-02 15:17:51,872 - module2_triple_filter - INFO -    5. (phổ đà sơn → is called → núi chùa cao) | Relevance: 0.397 | Level: moderately_relevant | Quality: 0.533  
2025-07-02 15:17:51,872 - module2_triple_filter - INFO -       💭 Explanation: Đánh giá fallback do qwen_api_error: Provider 'featherless-ai' not supported. Available values: 'aut...
2025-07-02 15:17:51,873 - module2_triple_filter - INFO -
⚡ PERFORMANCE METRICS:
2025-07-02 15:17:51,874 - module2_triple_filter - INFO -    🏃 Triples/giây: 359.0
2025-07-02 15:17:51,874 - module2_triple_filter - INFO -    ⏱️ Avg time/triple: 0.003s
2025-07-02 15:17:51,874 - module2_triple_filter - INFO -
✅ KHÔNG CÓ LỖI TRONG QUÁ TRÌNH FILTERING
2025-07-02 15:17:51,875 - module2_triple_filter - INFO - ============================================================
2025-07-02 15:17:51,876 - run_retrieval_and_qa_pipeline - INFO - 🔄 Standardizing triple passage IDs...
2025-07-02 15:17:51,876 - run_retrieval_and_qa_pipeline - INFO - Standardizing triple source_passage_ids from 'chunk_' to 'passage_chunk_'...
2025-07-02 15:17:51,877 - run_retrieval_and_qa_pipeline - INFO - Finished standardizing 10 triples.
2025-07-02 15:17:51,877 - run_retrieval_and_qa_pipeline - INFO - 🏆 Module 3: Passage Ranking...
2025-07-02 15:17:51,877 - module3_passage_ranker - INFO - ============================================================
2025-07-02 15:17:51,878 - module3_passage_ranker - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-07-02 15:17:51,878 - module3_passage_ranker - INFO - ============================================================
2025-07-02 15:17:51,879 - module3_passage_ranker - INFO - 📝 Query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào'
2025-07-02 15:17:51,879 - module3_passage_ranker - INFO - 📄 Raw passages: 5
2025-07-02 15:17:51,880 - module3_passage_ranker - INFO - 🔗 Filtered triples: 10
2025-07-02 15:17:51,880 - module3_passage_ranker - INFO - 🎯 Strategy: hybrid_balanced
2025-07-02 15:17:51,880 - module3_passage_ranker - INFO -
📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):
2025-07-02 15:17:51,881 - module3_passage_ranker - INFO - ------------------------------------------------------------
2025-07-02 15:17:51,881 - module3_passage_ranker - INFO -    1. ID: passage_chunk_Cao nguyên Lâm Viên_17_0
2025-07-02 15:17:51,882 - module3_passage_ranker - INFO -       Text: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao nguyên Lạng Bương, cao...
2025-07-02 15:17:51,882 - module3_passage_ranker - INFO -       Scores: BM25=0.885, Embed=1.000, Hybrid=0.966
2025-07-02 15:17:51,883 - module3_passage_ranker - INFO -       Metadata: {'title': 'Cao nguyên Lâm Viên', 'doc_id': 'Cao nguyên Lâm Viên_17', 'text_length': 1139, 'rank': 1}
2025-07-02 15:17:51,883 - module3_passage_ranker - INFO -    2. ID: passage_chunk_Cao nguyên Lâm Viên_710_0
2025-07-02 15:17:51,883 - module3_passage_ranker - INFO -       Text: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao nguyên Lạng Bương, cao...
2025-07-02 15:17:51,884 - module3_passage_ranker - INFO -       Scores: BM25=0.885, Embed=1.000, Hybrid=0.966
2025-07-02 15:17:51,884 - module3_passage_ranker - INFO -       Metadata: {'title': 'Cao nguyên Lâm Viên', 'doc_id': 'Cao nguyên Lâm Viên_710', 'text_length': 1139, 'rank': 2}
2025-07-02 15:17:51,885 - module3_passage_ranker - INFO -    3. ID: passage_chunk_Khu dự trữ sinh quyển Langbiang_14_0
2025-07-02 15:17:51,885 - module3_passage_ranker - INFO -       Text: Khu dự trữ sinh quyển thế giới Langbiang có diện tích 275.439 ha, nằm ở phía bắc tỉnh Lâm Đồng, thuộ...
2025-07-02 15:17:51,886 - module3_passage_ranker - INFO -       Scores: BM25=1.000, Embed=0.728, Hybrid=0.809
2025-07-02 15:17:51,886 - module3_passage_ranker - INFO -       Metadata: {'title': 'Khu dự trữ sinh quyển Langbiang', 'doc_id': 'Khu dự trữ sinh quyển Langbiang_14', 'text_length': 310, 'rank': 3}
2025-07-02 15:17:51,887 - module3_passage_ranker - INFO -    4. ID: passage_chunk_Tây Ninh_1560_0
2025-07-02 15:17:51,887 - module3_passage_ranker - INFO -       Text: Tây Ninh nổi tiếng với những phong cảnh thiên nhiên hùng vĩ . Núi Bà Đen cao 986m là ngọn núi cao nh...
2025-07-02 15:17:51,888 - module3_passage_ranker - INFO -       Scores: BM25=0.000, Embed=0.289, Hybrid=0.202
2025-07-02 15:17:51,888 - module3_passage_ranker - INFO -       Metadata: {'title': 'Tây Ninh', 'doc_id': 'Tây Ninh_1560', 'text_length': 264, 'rank': 5}
2025-07-02 15:17:51,888 - module3_passage_ranker - INFO -    5. ID: passage_chunk_Đỉnh Langbiang_19_0
2025-07-02 15:17:51,889 - module3_passage_ranker - INFO -       Text: Câu chuyện tình của chàng K’lang (người Lát, một nhánh của dân tộc K’Ho) và người con gái tên H'bian...
2025-07-02 15:17:51,889 - module3_passage_ranker - INFO -       Scores: BM25=0.891, Embed=0.000, Hybrid=0.267
2025-07-02 15:17:51,890 - module3_passage_ranker - INFO -       Metadata: {'title': 'Đỉnh Langbiang', 'doc_id': 'Đỉnh Langbiang_19', 'text_length': 1355, 'rank': 4}     
2025-07-02 15:17:51,890 - module3_passage_ranker - INFO -
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-07-02 15:17:51,891 - module3_passage_ranker - INFO - ----------------------------------------
2025-07-02 15:17:51,891 - module3_passage_ranker - INFO - 🔗 Đang xây dựng support mapping cho 10 filtered triples...
2025-07-02 15:17:51,892 - module3_passage_ranker - INFO - ✅ Support mapping completed:
2025-07-02 15:17:51,892 - module3_passage_ranker - INFO -    📊 Relevant triples: 10/10
2025-07-02 15:17:51,892 - module3_passage_ranker - INFO -    📄 Passages with support: 10
2025-07-02 15:17:51,893 - module3_passage_ranker - INFO -    🏆 Top supported passages:
2025-07-02 15:17:51,893 - module3_passage_ranker - INFO -       1. passage_chunk_Cao nguyên Lâm Viên_710_0: 1 triples
2025-07-02 15:17:51,893 - module3_passage_ranker - INFO -       2. passage_chunk_Núi Đôi Quản Bạ_1564_0: 1 triples
2025-07-02 15:17:51,894 - module3_passage_ranker - INFO -       3. passage_chunk_Tố Hữu_2755_0: 1 triples
2025-07-02 15:17:51,894 - module3_passage_ranker - INFO -
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-07-02 15:17:51,895 - module3_passage_ranker - INFO - ----------------------------------------
2025-07-02 15:17:51,895 - module3_passage_ranker - INFO - 🧮 Đang tính scores cho 5 passages...
2025-07-02 15:17:51,895 - module3_passage_ranker - INFO -    📊 Processed 5/5 passages
2025-07-02 15:17:51,896 - module3_passage_ranker - INFO - 📈 Score distributions:
2025-07-02 15:17:51,896 - module3_passage_ranker - INFO -    📊 Retrieval scores: min=0.202, max=0.966, avg=0.642
2025-07-02 15:17:51,896 - module3_passage_ranker - INFO -    🔗 Support scores: min=0.000, max=0.449, avg=0.222
2025-07-02 15:17:51,897 - module3_passage_ranker - INFO -    📄 Support levels: no=2, low=0, medium=3, high=0
2025-07-02 15:17:51,898 - module3_passage_ranker - INFO - ✅ Hoàn thành tính scores cho 5 passages
2025-07-02 15:17:51,898 - module3_passage_ranker - INFO -
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-07-02 15:17:51,898 - module3_passage_ranker - INFO - ----------------------------------------
2025-07-02 15:17:51,899 - module3_passage_ranker - INFO - 🏆 Áp dụng ranking strategy: hybrid_balanced
2025-07-02 15:17:51,899 - module3_passage_ranker - INFO -    ⚖️ Fixed weights: retrieval=0.50, support=0.50
2025-07-02 15:17:51,900 - module3_passage_ranker - INFO -    📊 Scores đã được normalized
2025-07-02 15:17:51,900 - module3_passage_ranker - INFO - ✅ Final scores calculated và sorted
2025-07-02 15:17:51,900 - module3_passage_ranker - INFO -    🏆 Top passage: passage_chunk_Cao nguyên Lâm Viên_710_0 với score 0.725
2025-07-02 15:17:51,901 - module3_passage_ranker - INFO -
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-07-02 15:17:51,901 - module3_passage_ranker - INFO - ----------------------------------------
2025-07-02 15:17:51,902 - module3_passage_ranker - INFO - 🔧 Áp dụng final processing...
2025-07-02 15:17:51,902 - module3_passage_ranker - INFO -    📊 Limited output: 5 → 5 passages
2025-07-02 15:17:51,902 - module3_passage_ranker - INFO - ✅ Final processing hoàn thành: 5 ranked passages
2025-07-02 15:17:51,903 - module3_passage_ranker - INFO -
🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):
2025-07-02 15:17:51,903 - module3_passage_ranker - INFO - ------------------------------------------------------------
2025-07-02 15:17:51,903 - module3_passage_ranker - INFO -    Giải thích thứ tự mới:
2025-07-02 15:17:51,904 - module3_passage_ranker - INFO -    1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
2025-07-02 15:17:51,904 - module3_passage_ranker - INFO -    2. Support score được tính từ số lượng và chất lượng của supporting triples
2025-07-02 15:17:51,904 - module3_passage_ranker - INFO -    3. Passages có nhiều supporting triples sẽ được boost lên
2025-07-02 15:17:51,905 - module3_passage_ranker - INFO -    4. Passages không có support sẽ bị penalty
2025-07-02 15:17:51,905 - module3_passage_ranker - INFO - ------------------------------------------------------------
2025-07-02 15:17:51,905 - module3_passage_ranker - INFO -    Rank 1. ID: passage_chunk_Cao nguyên Lâm Viên_710_0
2025-07-02 15:17:51,906 - module3_passage_ranker - INFO -       Text: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao nguyên Lạng Bương, cao...
2025-07-02 15:17:51,906 - module3_passage_ranker - INFO -       Scores:
2025-07-02 15:17:51,906 - module3_passage_ranker - INFO -          - Final score: 0.725
2025-07-02 15:17:51,907 - module3_passage_ranker - INFO -          - Retrieval score: 1.000
2025-07-02 15:17:51,907 - module3_passage_ranker - INFO -          - Support score: 0.449
2025-07-02 15:17:51,909 - module3_passage_ranker - INFO -       Supporting triples: 1
2025-07-02 15:17:51,911 - module3_passage_ranker - INFO -       Triple IDs: triple_f37e7e98...
2025-07-02 15:17:51,911 - module3_passage_ranker - INFO -       Score breakdown: {'bm25_score': 0.8854028245254033, 'embedding_score': 1.0, 'hybrid_score': 0.9656208473576209, 'support_score': 0.4490931754064624, 'support_count': 1, 'normalized_retrieval': 1.0, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.7245465877032312, 'final_score_after_modifiers': 0.7245465877032312}
2025-07-02 15:17:51,912 - module3_passage_ranker - INFO -    Rank 2. ID: passage_chunk_Cao nguyên Lâm Viên_17_0
2025-07-02 15:17:51,912 - module3_passage_ranker - INFO -       Text: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao nguyên Lạng Bương, cao...
2025-07-02 15:17:51,913 - module3_passage_ranker - INFO -       Scores:
2025-07-02 15:17:51,914 - module3_passage_ranker - INFO -          - Final score: 0.663
2025-07-02 15:17:51,915 - module3_passage_ranker - INFO -          - Retrieval score: 1.000
2025-07-02 15:17:51,915 - module3_passage_ranker - INFO -          - Support score: 0.327
2025-07-02 15:17:51,916 - module3_passage_ranker - INFO -       Supporting triples: 1
2025-07-02 15:17:51,916 - module3_passage_ranker - INFO -       Triple IDs: triple_ad3485fb...
2025-07-02 15:17:51,917 - module3_passage_ranker - INFO -       Score breakdown: {'bm25_score': 0.8854028245254033, 'embedding_score': 1.0, 'hybrid_score': 0.9656208473576209, 'support_score': 0.32675236081739867, 'support_count': 1, 'normalized_retrieval': 1.0, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.6633761804086993, 'final_score_after_modifiers': 0.6633761804086993}
2025-07-02 15:17:51,917 - module3_passage_ranker - INFO -    Rank 3. ID: passage_chunk_Khu dự trữ sinh quyển Langbiang_14_0
2025-07-02 15:17:51,917 - module3_passage_ranker - INFO -       Text: Khu dự trữ sinh quyển thế giới Langbiang có diện tích 275.439 ha, nằm ở phía bắc tỉnh Lâm Đồng, thuộ...
2025-07-02 15:17:51,919 - module3_passage_ranker - INFO -       Scores:
2025-07-02 15:17:51,919 - module3_passage_ranker - INFO -          - Final score: 0.318
2025-07-02 15:17:51,919 - module3_passage_ranker - INFO -          - Retrieval score: 0.795
2025-07-02 15:17:51,920 - module3_passage_ranker - INFO -          - Support score: 0.000
2025-07-02 15:17:51,920 - module3_passage_ranker - INFO -       Supporting triples: 0
2025-07-02 15:17:51,921 - module3_passage_ranker - INFO -       Score breakdown: {'bm25_score': 1.0, 'embedding_score': 0.7276962202294861, 'hybrid_score': 0.8093873541606402, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.7953907544856289, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.39769537724281445, 'final_score_after_modifiers': 0.3181563017942516}
2025-07-02 15:17:51,921 - module3_passage_ranker - INFO -    Rank 4. ID: passage_chunk_Đỉnh Langbiang_19_0
2025-07-02 15:17:51,922 - module3_passage_ranker - INFO -       Text: Câu chuyện tình của chàng K’lang (người Lát, một nhánh của dân tộc K’Ho) và người con gái tên H'bian...
2025-07-02 15:17:51,922 - module3_passage_ranker - INFO -       Scores:
2025-07-02 15:17:51,923 - module3_passage_ranker - INFO -          - Final score: 0.209
2025-07-02 15:17:51,923 - module3_passage_ranker - INFO -          - Retrieval score: 0.085
2025-07-02 15:17:51,924 - module3_passage_ranker - INFO -          - Support score: 0.333
2025-07-02 15:17:51,925 - module3_passage_ranker - INFO -       Supporting triples: 1
2025-07-02 15:17:51,925 - module3_passage_ranker - INFO -       Triple IDs: triple_1d924646...
2025-07-02 15:17:51,925 - module3_passage_ranker - INFO -       Score breakdown: {'bm25_score': 0.8910113196816708, 'embedding_score': 0.0, 'hybrid_score': 0.26730339590450125, 'support_score': 0.33299999999999996, 'support_count': 1, 'normalized_retrieval': 0.08545726049155113, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.20922863024577554, 'final_score_after_modifiers': 0.20922863024577554}
2025-07-02 15:17:51,926 - module3_passage_ranker - INFO -    Rank 5. ID: passage_chunk_Tây Ninh_1560_0
2025-07-02 15:17:51,926 - module3_passage_ranker - INFO -       Text: Tây Ninh nổi tiếng với những phong cảnh thiên nhiên hùng vĩ . Núi Bà Đen cao 986m là ngọn núi cao nh...
2025-07-02 15:17:51,927 - module3_passage_ranker - INFO -       Scores:
2025-07-02 15:17:51,927 - module3_passage_ranker - INFO -          - Final score: 0.000
2025-07-02 15:17:51,927 - module3_passage_ranker - INFO -          - Retrieval score: 0.000
2025-07-02 15:17:51,928 - module3_passage_ranker - INFO -          - Support score: 0.000
2025-07-02 15:17:51,928 - module3_passage_ranker - INFO -       Supporting triples: 0
2025-07-02 15:17:51,928 - module3_passage_ranker - INFO -       Score breakdown: {'bm25_score': 0.0, 'embedding_score': 0.2886439866661157, 'hybrid_score': 0.20205079066628095, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.0, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.0, 'final_score_after_modifiers': 0.0}
2025-07-02 15:17:51,929 - module3_passage_ranker - INFO -
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-07-02 15:17:51,930 - module3_passage_ranker - INFO - ----------------------------------------
2025-07-02 15:17:51,930 - module3_passage_ranker - INFO - 📈 Tạo ranking statistics...
2025-07-02 15:17:51,930 - module3_passage_ranker - INFO - ============================================================
2025-07-02 15:17:51,931 - module3_passage_ranker - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-07-02 15:17:51,931 - module3_passage_ranker - INFO - ============================================================
2025-07-02 15:17:51,931 - module3_passage_ranker - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-07-02 15:17:51,932 - module3_passage_ranker - INFO -    📝 Query: 'Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào'
2025-07-02 15:17:51,932 - module3_passage_ranker - INFO -    ⏱️ Thời gian xử lý: 0.04 giây
2025-07-02 15:17:51,932 - module3_passage_ranker - INFO -    📄 Passages: 5 → 5
2025-07-02 15:17:51,933 - module3_passage_ranker - INFO -    📈 Efficiency: 100.00%
2025-07-02 15:17:51,933 - module3_passage_ranker - INFO -
🏆 TOP 5 RANKED PASSAGES:
2025-07-02 15:17:51,934 - module3_passage_ranker - INFO -    1. Rank 1: passage_chunk_Cao nguyên Lâm Viên_710_0 | Final: 0.725 (Ret: 1.000, Sup: 0.449) | Triples: 1     
2025-07-02 15:17:51,934 - module3_passage_ranker - INFO -       📝 Text: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao ng...
2025-07-02 15:17:51,934 - module3_passage_ranker - INFO -    2. Rank 2: passage_chunk_Cao nguyên Lâm Viên_17_0 | Final: 0.663 (Ret: 1.000, Sup: 0.327) | Triples: 1      
2025-07-02 15:17:51,935 - module3_passage_ranker - INFO -       📝 Text: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao ng...
2025-07-02 15:17:51,935 - module3_passage_ranker - INFO -    3. Rank 3: passage_chunk_Khu dự trữ sinh quyển Langbiang_14_0 | Final: 0.318 (Ret: 0.795, Sup: 0.000) | Triples: 0
2025-07-02 15:17:51,936 - module3_passage_ranker - INFO -       📝 Text: Khu dự trữ sinh quyển thế giới Langbiang có diện tích 275.439 ha, nằm ở phía bắc...
2025-07-02 15:17:51,936 - module3_passage_ranker - INFO -    4. Rank 4: passage_chunk_Đỉnh Langbiang_19_0 | Final: 0.209 (Ret: 0.085, Sup: 0.333) | Triples: 1
2025-07-02 15:17:51,937 - module3_passage_ranker - INFO -       📝 Text: Câu chuyện tình của chàng K’lang (người Lát, một nhánh của dân tộc K’Ho) và ngườ...
2025-07-02 15:17:51,937 - module3_passage_ranker - INFO -    5. Rank 5: passage_chunk_Tây Ninh_1560_0 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-07-02 15:17:51,938 - module3_passage_ranker - INFO -       📝 Text: Tây Ninh nổi tiếng với những phong cảnh thiên nhiên hùng vĩ . Núi Bà Đen cao 986...
2025-07-02 15:17:51,938 - module3_passage_ranker - INFO -
📊 PHÂN BỐ SUPPORT:
2025-07-02 15:17:51,939 - module3_passage_ranker - INFO -    no_support: 2 passages (40.0%)
2025-07-02 15:17:51,939 - module3_passage_ranker - INFO -    low_support: 3 passages (60.0%)
2025-07-02 15:17:51,940 - module3_passage_ranker - INFO -    medium_support: 0 passages (0.0%)
2025-07-02 15:17:51,940 - module3_passage_ranker - INFO -    high_support: 0 passages (0.0%)
2025-07-02 15:17:51,941 - module3_passage_ranker - INFO - 
🔄 THAY ĐỔI RANKING:
2025-07-02 15:17:51,941 - module3_passage_ranker - INFO -    ⬆️ Moved up: 1
2025-07-02 15:17:51,942 - module3_passage_ranker - INFO -    ⬇️ Moved down: 1
2025-07-02 15:17:51,942 - module3_passage_ranker - INFO -    ➡️ Unchanged: 3
2025-07-02 15:17:51,942 - module3_passage_ranker - INFO -    📈 Max improvement: 1 positions
2025-07-02 15:17:51,942 - module3_passage_ranker - INFO -    📉 Max decline: 1 positions
2025-07-02 15:17:51,944 - module3_passage_ranker - INFO -
⚡ PERFORMANCE:
2025-07-02 15:17:51,944 - module3_passage_ranker - INFO -    🏃 Passages/giây: 125.8
2025-07-02 15:17:51,945 - module3_passage_ranker - INFO -    ⏱️ Avg time/passage: 0.008s
2025-07-02 15:17:51,945 - module3_passage_ranker - INFO - ============================================================
2025-07-02 15:17:51,946 - run_retrieval_and_qa_pipeline - INFO - 💬 Module 5: Answer Generation...
2025-07-02 15:17:51,946 - module5_answer_generator - INFO - 🎯 Starting answer generation for query: Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào
2025-07-02 15:17:51,947 - module5_answer_generator - INFO - 📚 Input: 5 passages, 10 triples
2025-07-02 15:17:51,947 - module5_answer_generator - INFO - 🔍 Cache miss - proceeding with generation
2025-07-02 15:17:51,948 - module5_answer_generator - INFO - 🚀 Attempting answer generation with primary provider: gpt-3.5-turbo

================================================================================
🤖 PROMPT SENT TO GPT MODEL:
================================================================================
Dựa trên thông tin sau, hãy suy nghĩ chi tiết bên trong (think step by step) nhưng chỉ xuất phần Answer ngắn gọn.

Câu hỏi: Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào

Đoạn văn liên quan:
Đoạn 1: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao nguyên Lạng Bương, cao nguyên Đà Lạt, bình sơn Đà Lạt) là một cao nguyên thuộc Tây Nguyên, Việt Nam (được khám phá bởi nhà thám hiểm-bác sĩ Alexandre Yersin) với độ cao trung bình khoảng 1.500 m (4.920 ft) so với mực nước biển. Phía nam cao nguyên có thành phố Đà Lạt. Phía đông và đông nam dốc xuống thung lũng sông Đa Nhim, tây nam hạ đột ngột xuống cao nguyên Di Linh. Diện tích khoảng 1.080 km². Địa hình đồi núi trập trùng độ dốc dao động 8-10°. Tại đây có các đỉnh núi cao như Bi Doup (2.287 m), Lang Biang (hay Chư Cang Ca, 2.167 m), Hòn Giao (2.010 m). Nước sông trên cao nguyên chảy chậm; những chỗ bị chặn lại toả rộng thành hồ như hồ Xuân Hương, hồ Than Thở, hồ Đa Thiện, hồ Đan Kia (Suối Vàng), thác Cam Ly. Rìa cao nguyên có các thác lớn như Pren (Prenn), Gù Gà, Ankrôet, thác Voi. Phong cảnh đẹp, khí hậu trong lành phù hợp cho trồng rau và hoa quả ôn đới quanh năm, có rừng thông ba lá và thông năm lá diện tích lớn. Cao nguyên này chỉ chiếm khoảng 30% diện tích của toàn tỉnh Lâm Đồng, nằm trên các huyện Lạc Dương, Đam Rông và thành phố Đà Lạt.
Đoạn 2: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao nguyên Lạng Bương, cao nguyên Đà Lạt, bình sơn Đà Lạt) là một cao nguyên thuộc Tây Nguyên, Việt Nam (được khám phá bởi nhà thám hiểm-bác sĩ Alexandre Yersin) với độ cao trung bình khoảng 1.500 m (4.920 ft) so với mực nước biển. Phía nam cao nguyên có thành phố Đà Lạt. Phía đông và đông nam dốc xuống thung lũng sông Đa Nhim, tây nam hạ đột ngột xuống cao nguyên Di Linh. Diện tích khoảng 1.080 km². Địa hình đồi núi trập trùng độ dốc dao động 8-10°. Tại đây có các đỉnh núi cao như Bi Doup (2.287 m), Lang Biang (hay Chư Cang Ca, 2.167 m), Hòn Giao (2.010 m). Nước sông trên cao nguyên chảy chậm; những chỗ bị chặn lại toả rộng thành hồ như hồ Xuân Hương, hồ Than Thở, hồ Đa Thiện, hồ Đan Kia (Suối Vàng), thác Cam Ly. Rìa cao nguyên có các thác lớn như Pren (Prenn), Gù Gà, Ankrôet, thác Voi. Phong cảnh đẹp, khí hậu trong lành phù hợp cho trồng rau và hoa quả ôn đới quanh năm, có rừng thông ba lá và thông năm lá diện tích lớn. Cao nguyên này chỉ chiếm khoảng 30% diện tích của toàn tỉnh Lâm Đồng, nằm trên các huyện Lạc Dương, Đam Rông và thành phố Đà Lạt.
Đoạn 3: Khu dự trữ sinh quyển thế giới Langbiang có diện tích 275.439 ha, nằm ở phía bắc tỉnh Lâm Đồng, thuộc khu vực nam Tây Nguyên, Việt Nam và được đặt tên theo ngọn núi Langbiang, nơi có câu chuyện tình lãng mạn giữa chàng Lang và nàng Biang của người K’Ho - cư dân thiểu số bản địa đã sinh sống ở đây bao đời nay.
Đoạn 4: Câu chuyện tình của chàng K’lang (người Lát, một nhánh của dân tộc K’Ho) và người con gái tên H'biang (người Chil, một nhánh khác của dân tộc K’Ho) đã làm xúc động bao du khách khi đặt chân đến đây. Nhà K’lang và H'biang đều ở dưới chân núi, họ tình cờ gặp nhau trong một lần lên rừng hái quả. H'biang gặp nạn và chàng K’lang đã dũng cảm cứu nàng thoát khỏi đàn sói hung dữ. Một lần gặp gỡ nhưng cả hai đã cảm mến, rồi họ đem lòng yêu nhau. Nhưng do lời nguyền giữa 2 tộc người mà H'biang không thể lấy K’lang làm chồng. Vượt qua tục lệ khắt khe và lễ giáo, hai người vẫn quyết tâm đến với nhau. Họ trở thành chồng vợ rồi bỏ đến một nơi trên đỉnh núi để sinh sống. Khi H'biang bị bệnh, K’lang tìm mọi cách chữa trị nhưng không khỏi. Chàng đành quay về báo cho buôn làng để tìm cách cứu nàng. Kết thúc câu chuyện, H'biang bị chết do nàng đỡ mũi tên có tẩm thuốc độc của buôn làng nhắm bắn K’lang. Đau buồn khôn xiết, K’lang đã khóc rất nhiều, nước mắt chàng tuôn thành suối lớn, ngày nay gọi là Đạ Nhim (suối khóc). Sau cái chết của hai người, cha Biang rất hối hận, đứng ra thống nhất các bộ tộc thành một dân tộc có tên là K’Ho. Từ đó các đôi nam nữ trong làng dễ dàng đến với nhau. Ngọn núi cao ở làng La Ngư Thượng, nơi chàng K’lang và nàng H'biang chết được đặt lên là Lang Biang - tên ghép của đôi trai gái, để tưởng nhớ hai người và tình yêu của họ.
Đoạn 5: Tây Ninh nổi tiếng với những phong cảnh thiên nhiên hùng vĩ . Núi Bà Đen cao 986m là ngọn núi cao nhất miền Nam Việt Nam và là nơi có nhiều truyền thuyết nổi tiếng , ở đây có một bảo tàng được xây dựng trong động Kim Quang và một ngôi chùa cùng tên rất nổi tiếng .

Các thông tin quan trọng (triples):
1. caonnguyen lam vien has mountain peaks lang biang
2. núi đôi quản bạ thuộc tỉnh hà giang
3. xã quảng thọ part of huyện quảng điền
4. xuân thu is part of chinese history
5. phổ đà sơn is called núi chùa cao
6. phổ đà sơn is called núi chùa cao
7. phổ đà sơn is called núi chùa cao
8. phổ đà sơn is called núi chùa cao
9. lang biang named after chàng k’lang và nàng h'biang
10. caonnguyen lam vien is also known as cao nguyên lang biang


### Answer (chỉ ghi kết quả, không giải thích, tối đa 7 từ hoặc 1 con số (có thể kèm đơn vị))

================================================================================

2025-07-02 15:17:51,954 - module5_answer_generator - INFO -
================================================================================
2025-07-02 15:17:51,955 - module5_answer_generator - INFO - 🤖 PROMPT SENT TO GPT MODEL:
2025-07-02 15:17:51,955 - module5_answer_generator - INFO - ================================================================================
2025-07-02 15:17:51,956 - module5_answer_generator - INFO - 📝 Prompt length: 5042 characters
2025-07-02 15:17:51,957 - module5_answer_generator - INFO - 📊 Prompt word count: 1071 words
2025-07-02 15:17:51,957 - module5_answer_generator - INFO - ----------------------------------------
2025-07-02 15:17:51,958 - module5_answer_generator - INFO - PROMPT CONTENT:
2025-07-02 15:17:51,958 - module5_answer_generator - INFO - ----------------------------------------
2025-07-02 15:17:51,958 - module5_answer_generator - INFO - Dựa trên thông tin sau, hãy suy nghĩ chi tiết bên trong (think step by step) nhưng chỉ xuất phần Answer ngắn gọn.
2025-07-02 15:17:51,959 - module5_answer_generator - INFO -
2025-07-02 15:17:51,959 - module5_answer_generator - INFO - Câu hỏi: Núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào
2025-07-02 15:17:51,959 - module5_answer_generator - INFO -
2025-07-02 15:17:51,960 - module5_answer_generator - INFO - Đoạn văn liên quan:
2025-07-02 15:17:51,960 - module5_answer_generator - INFO - Đoạn 1: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao nguyên Lạng Bương, cao nguyên Đà Lạt, bình sơn Đà Lạt) là một cao nguyên thuộc Tây Nguyên, Việt Nam (được khám phá bởi nhà thám hiểm-bác sĩ Alexandre Yersin) với độ cao trung bình khoảng 1.500 m (4.920 ft) so với mực nước biển. Phía nam cao nguyên có thành phố Đà Lạt. Phía đông và đông nam dốc xuống thung lũng sông Đa Nhim, tây nam hạ đột ngột xuống cao nguyên Di Linh. Diện tích khoảng 1.080 km². Địa hình đồi núi trập trùng độ dốc dao động 8-10°. Tại đây có các đỉnh núi cao như Bi Doup (2.287 m), Lang Biang (hay Chư Cang Ca, 2.167 m), Hòn Giao (2.010 m). Nước sông trên cao nguyên chảy chậm; những chỗ bị chặn lại toả rộng thành hồ như hồ Xuân Hương, hồ Than Thở, hồ Đa Thiện, hồ Đan Kia (Suối Vàng), thác Cam Ly. Rìa cao nguyên có các thác lớn như Pren (Prenn), Gù Gà, Ankrôet, thác Voi. Phong cảnh đẹp, khí hậu trong lành phù hợp cho trồng rau và hoa quả ôn đới quanh năm, có rừng thông ba lá và thông năm lá diện tích lớn. Cao nguyên này chỉ chiếm khoảng 30% diện tích của toàn tỉnh Lâm Đồng, nằm trên các huyện Lạc Dương, Đam Rông và thành phố Đà Lạt.
2025-07-02 15:17:51,961 - module5_answer_generator - INFO - Đoạn 2: Cao nguyên Lâm Viên (còn gọi cao nguyên Lang Biang, cao nguyên Lang Bian, cao nguyên Lạng Bương, cao nguyên Đà Lạt, bình sơn Đà Lạt) là một cao nguyên thuộc Tây Nguyên, Việt Nam (được khám phá bởi nhà thám hiểm-bác sĩ Alexandre Yersin) với độ cao trung bình khoảng 1.500 m (4.920 ft) so với mực nước biển. Phía nam cao nguyên có thành phố Đà Lạt. Phía đông và đông nam dốc xuống thung lũng sông Đa Nhim, tây nam hạ đột ngột xuống cao nguyên Di Linh. Diện tích khoảng 1.080 km². Địa hình đồi núi trập trùng độ dốc dao động 8-10°. Tại đây có các đỉnh núi cao như Bi Doup (2.287 m), Lang Biang (hay Chư Cang Ca, 2.167 m), Hòn Giao (2.010 m). Nước sông trên cao nguyên chảy chậm; những chỗ bị chặn lại toả rộng thành hồ như hồ Xuân Hương, hồ Than Thở, hồ Đa Thiện, hồ Đan Kia (Suối Vàng), thác Cam Ly. Rìa cao nguyên có các thác lớn như Pren (Prenn), Gù Gà, Ankrôet, thác Voi. Phong cảnh đẹp, khí hậu trong lành phù hợp cho trồng rau và hoa quả ôn đới quanh năm, có rừng thông ba lá và thông năm lá diện tích lớn. Cao nguyên này chỉ chiếm khoảng 30% diện tích của toàn tỉnh Lâm Đồng, nằm trên các huyện Lạc Dương, Đam Rông và thành phố Đà Lạt.
2025-07-02 15:17:51,962 - module5_answer_generator - INFO - Đoạn 3: Khu dự trữ sinh quyển thế giới Langbiang có diện tích 275.439 ha, nằm ở phía bắc tỉnh Lâm Đồng, thuộc khu vực nam Tây Nguyên, Việt Nam và được đặt tên theo ngọn núi Langbiang, nơi có câu chuyện tình lãng mạn giữa chàng Lang và nàng Biang của người K’Ho - cư dân thiểu số bản địa đã sinh sống ở đây bao đời nay.
2025-07-02 15:17:51,962 - module5_answer_generator - INFO - Đoạn 4: Câu chuyện tình của chàng K’lang (người Lát, một nhánh của dân tộc K’Ho) và người con gái tên H'biang (người Chil, một nhánh khác của dân tộc K’Ho) đã làm xúc động bao du khách khi đặt chân đến đây. Nhà K’lang và H'biang đều ở dưới chân núi, họ tình cờ gặp nhau trong một lần lên rừng hái quả. H'biang gặp nạn và chàng K’lang đã dũng cảm cứu nàng thoát khỏi đàn sói hung dữ. Một lần gặp gỡ nhưng cả hai đã cảm mến, rồi họ đem lòng yêu nhau. Nhưng do lời nguyền giữa 2 tộc người mà H'biang không thể lấy K’lang làm chồng. Vượt qua tục lệ khắt khe và lễ giáo, hai người vẫn quyết tâm đến với nhau. Họ trở thành chồng vợ rồi bỏ đến một nơi trên đỉnh núi để sinh sống. Khi H'biang bị bệnh, K’lang tìm mọi cách chữa trị nhưng không khỏi. Chàng đành quay về báo cho buôn làng để tìm cách cứu nàng. Kết thúc câu chuyện, H'biang bị chết do nàng đỡ mũi tên có tẩm thuốc độc của buôn làng nhắm bắn K’lang. Đau buồn khôn xiết, K’lang đã khóc rất nhiều, nước mắt chàng tuôn thành suối lớn, ngày nay gọi là Đạ Nhim (suối khóc). Sau cái chết của hai người, cha Biang rất hối hận, đứng ra thống nhất các bộ tộc thành một dân tộc có tên là K’Ho. Từ đó các đôi nam nữ trong làng dễ dàng đến với nhau. Ngọn núi cao ở làng La Ngư Thượng, nơi chàng K’lang và nàng H'biang chết được đặt lên là Lang Biang - tên ghép của đôi trai gái, để tưởng nhớ hai người và tình yêu của họ.
2025-07-02 15:17:51,963 - module5_answer_generator - INFO - Đoạn 5: Tây Ninh nổi tiếng với những phong cảnh thiên nhiên hùng vĩ . Núi Bà Đen cao 986m là ngọn núi cao nhất miền Nam Việt Nam và là nơi có nhiều truyền thuyết nổi tiếng , ở đây có một bảo tàng được xây dựng trong động Kim Quang và một ngôi chùa cùng tên rất nổi tiếng .      
2025-07-02 15:17:51,964 - module5_answer_generator - INFO -
2025-07-02 15:17:51,964 - module5_answer_generator - INFO - Các thông tin quan trọng (triples):
2025-07-02 15:17:51,965 - module5_answer_generator - INFO - 1. caonnguyen lam vien has mountain peaks lang biang
2025-07-02 15:17:51,965 - module5_answer_generator - INFO - 2. núi đôi quản bạ thuộc tỉnh hà giang
2025-07-02 15:17:51,965 - module5_answer_generator - INFO - 3. xã quảng thọ part of huyện quảng điền
2025-07-02 15:17:51,966 - module5_answer_generator - INFO - 4. xuân thu is part of chinese history
2025-07-02 15:17:51,966 - module5_answer_generator - INFO - 5. phổ đà sơn is called núi chùa cao
2025-07-02 15:17:51,966 - module5_answer_generator - INFO - 6. phổ đà sơn is called núi chùa cao
2025-07-02 15:17:51,967 - module5_answer_generator - INFO - 7. phổ đà sơn is called núi chùa cao
2025-07-02 15:17:51,967 - module5_answer_generator - INFO - 8. phổ đà sơn is called núi chùa cao
2025-07-02 15:17:51,967 - module5_answer_generator - INFO - 9. lang biang named after chàng k’lang và nàng h'biang
2025-07-02 15:17:51,968 - module5_answer_generator - INFO - 10. caonnguyen lam vien is also known as cao nguyên lang biang
2025-07-02 15:17:51,968 - module5_answer_generator - INFO -
2025-07-02 15:17:51,968 - module5_answer_generator - INFO -
2025-07-02 15:17:51,969 - module5_answer_generator - INFO - ### Answer (chỉ ghi kết quả, không giải thích, tối đa 7 từ hoặc 1 con số (có thể kèm đơn vị))
2025-07-02 15:17:51,969 - module5_answer_generator - INFO -
2025-07-02 15:17:51,969 - module5_answer_generator - INFO - ================================================================================

2025-07-02 15:17:52,938 - module5_answer_generator - INFO - 🤖 Initialized Qwen model for answer generation
2025-07-02 15:17:52,939 - module5_answer_generator - INFO -    📊 Model configuration: temperature=0.01, max_tokens=1000, top_p=0.9
2025-07-02 15:17:52,939 - module5_answer_generator - INFO - 📏 Length score: +0.2 (length: 5 words)
2025-07-02 15:17:52,940 - module5_answer_generator - INFO - 🎯 Relevance score: +0.00 (overlap: 0/15 words)
2025-07-02 15:17:52,940 - module5_answer_generator - INFO - 📝 Structure score: +0.1 (complete sentence)
2025-07-02 15:17:52,941 - module5_answer_generator - INFO - 🇻🇳 Vietnamese text score: +0.1 (contains Vietnamese characters)
2025-07-02 15:17:52,941 - module5_answer_generator - INFO - ✨ Content quality score: +0.1 (no generic phrases)
2025-07-02 15:17:52,942 - module5_answer_generator - INFO - 📊 Final quality score: 0.50
2025-07-02 15:17:52,942 - module5_answer_generator - INFO - 📚 Passage support confidence: +0.23 (avg score: 0.57)
2025-07-02 15:17:52,943 - module5_answer_generator - INFO - 🔍 Triple support confidence: +0.14 (avg relevance: 0.45)
2025-07-02 15:17:52,943 - module5_answer_generator - INFO - 🔗 Evidence consistency: +0.1 (total evidence: 15)
2025-07-02 15:17:52,944 - module5_answer_generator - INFO - 📊 Final confidence score: 0.46
2025-07-02 15:17:52,945 - module5_answer_generator - INFO - ✅ Primary provider succeeded
2025-07-02 15:17:52,945 - module5_answer_generator - INFO - 📊 Answer generation metrics:
2025-07-02 15:17:52,946 - module5_answer_generator - INFO -    - Quality score: 0.500
2025-07-02 15:17:52,946 - module5_answer_generator - INFO -    - Quality level: fair
2025-07-02 15:17:52,946 - module5_answer_generator - INFO -    - Confidence score: 0.463
2025-07-02 15:17:52,947 - module5_answer_generator - INFO -    - Generation time: 0.99s
2025-07-02 15:17:52,947 - module5_answer_generator - INFO -    - Provider used: primary
2025-07-02 15:17:52,948 - module5_answer_generator - INFO -    - Supporting passages: 5
2025-07-02 15:17:52,948 - module5_answer_generator - INFO -    - Supporting triples: 10
2025-07-02 15:17:52,949 - module5_answer_generator - INFO - 💾 Cached answer with key: 67746b3e40d411a5035dde4905a18b5e...
2025-07-02 15:17:52,949 - module5_answer_generator - INFO - ✅ Answer generated successfully - Quality: 0.500, Confidence: 0.463
2025-07-02 15:17:52,950 - run_retrieval_and_qa_pipeline - INFO - ✅ Query WEB_1751444271433 processed successfully in 1.52s
✅ Real PPDX processing completed in 1.52s
INFO:     127.0.0.1:50840 - "POST /api/process HTTP/1.1" 200 OK

```