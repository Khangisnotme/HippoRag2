"""
README.md - Tài liệu hướng dẫn cho OnlineRetrievalAndQA
"""

# OnlineRetrievalAndQA 
- Đọc hiểu 5 module của pha Online để hiểu code (đặc biệt là các ví dụ trong 5 module)
- Cách chạy các file xem ở các file .sh 

---

## Cấu trúc thư mục 


### Code pha Offline: 
```bash
   │
│   └── 📁 OfflineIndexing/
│       ├── 📋 offline_indexing_requirements.txt
│       │
│       ├── 📄 module1_chunking.py
│       ├── 🧠 module2_triple_extractor.py  
│       ├── 🔗 module3_synonym_detector.py
│       ├── 🏗️ module4_graph_builder.py
│       ├── 🎯 pipeline_orchestrator.py
│       ├── 🚀 run_offline_pipeline.py
│       │
│       ├── 📁 utils/
│       │   ├── 🔧 utils_general.py
│       │   ├── 📊 utils_excel_documents.py
│       │   └── 🗃️ utils_neo4j.py
│       │
│       └── 📁 test/
│           ├── 📊 test_data.py
│           ├── 🧪 test_offline_pipeline.py
│           └── 🔍 test_query_functions.py
│
└── 📁 OnlineRetrievalAndQA
```

### Cấu trúc OnlineRetrievalAndQA (Updated Utils Structure)

```bash
📁 OnlineRetrievalAndQA/                      # 🌐 ONLINE PHASE
├── 📋 online_requirements.txt                # Dependencies for online phase
│
├── 🔍 module1_dual_retrieval.py              # Bước 1: Dual/Hybrid Retrieval
├── 🤖 module2_triple_filter.py               # Bước 2: LLM Triple Filtering  
├── 📊 module3_passage_ranker.py              # Bước 3: Triple-based Passage Ranking
├── 🎯 module4_context_expander.py            # Bước 4: 1-hop Context Expansion (Optional)
├── 🗣️ module5_answer_generator.py            # Bước 5: Final Answer Generation
│
├── 🎯 (retrieval_pipeline_orchestrator)  online_pipeline_orchestrator.py        # Pipeline Logic Coordinator (Core orchestration)

----   retrieval_and_qa_pipeline_orchestrator.py  (file này ko dùng đến - nên đã comment ẩn đi)│

├── 🔍 run_retrieval_pipeline.py              # Run Retrieval Only (Steps 1-3/4)
│                                             # Args: --enable_expansion True/False
├── 🌐 run_retrieval_and_qa_pipeline.py       # Run Full Pipeline (Steps 1-5)
│                                             # Args: --enable_expansion True/False
│
├── 📁 utils/                                 # 🔧 UTILS FLATTENED BY MODULE
│   ├── 🔧 utils_shared_general.py            # General shared utilities
│
└── 📁 test/    # ko cần nữa luôn 
├── 📖 README.md
├── 📚 docs/
│   ├── 🚀 quickstart.md
│   └── 🔧 api_reference.md
├── 📁 outputs/
│   ├── 📁 retrieval_results/
│   └── 📁 final_answers/
├── .env.example
```


#### Phương pháp đề xuất (tóm tắt như sau)
```bash
1. Pha offline (y nguyên HippoRAG2)
2. Pha online: 


Luồng xử lý 5 bước - Giai đoạn Online Retrieval & QA:

1. Truy xuất Kép/Lai (Dual/Hybrid Retrieval) : mục đích tận dụng Hybrid Search
Input: Truy vấn người dùng
Xử lý: Truy xuất song song từ 2 nguồn bằng BM25 + Embedding:
Passages: Lấy Top-K passages (50-100) → Raw Passages
Triples: Lấy Top-N triples (20-50) → Raw Triples
Output: Raw Passages + Raw Triples

2. Lọc Triple bằng LLM - mục đích: giữ lại triples phù hợp với truy vấn ban đầu
Input: Raw Triples + truy vấn gốc
Xử lý: LLM (Qwen2.5-7B) đánh giá và chọn facts cốt lõi nhất
Output: Filtered Triples (Top-M, khoảng 10-20 triple chất lượng cao)

3. Xếp hạng lại Passages dựa trên Triples - mục đích lọc bỏ passages nhiễu bằng cách tính score của nó với các triples
Input: Raw Passages + Filtered Triples
Xử lý:
Tính điểm hỗ trợ: đếm số triple mà mỗi passage hỗ trợ
Kết hợp điểm: Score_final = α × Score_retriever + (1-α) × Score_support
Chọn Top-P passages có điểm cao nhất
Output: Final Passages (5-10 passages tốt nhất)

Score_retriever (Điểm truy xuất ban đầu)
Điểm số từ Module 1 (kết hợp BM25 + Embedding)
Phản ánh độ liên quan ngữ nghĩa với truy vấn
Giá trị: thường từ 0-1

Score_support (Điểm hỗ trợ triple)
Đếm số lượng Filtered Triples mà passage đó hỗ trợ
Kiểm tra: passage có chứa cả subject và object của triple không?
Giá trị: số nguyên (0, 1, 2, 3...)

Score_final (Điểm cuối cùng)
Score_final = α × Score_retriever + (1-α) × Score_support

Tham số α (alpha):
α = 0.7-0.8: Ưu tiên độ liên quan ngữ nghĩa
α = 0.5: Cân bằng giữa liên quan và hỗ trợ facts
α < 0.5: Ưu tiên passages được facts hỗ trợ mạnh

Ví dụ nhanh:
Passage A: Score_retriever = 0.85, hỗ trợ 3 triples
Với α = 0.7: Score_final = 0.7×0.85 + 0.3×3 = 1.495
Passage này sẽ được ưu tiên cao vì vừa liên quan vừa được facts xác thực

4. Mở rộng Ngữ cảnh (Tùy chọn) - Mở rộng 1 hop cho Filted Triples (thay vì lan truyền rộng như PPR) 
Input: Filtered Triples
Xử lý: Tìm kiếm 1-hop trên KG để lấy thêm thông tin liên quan
Output: Expanded Context

5. Tạo Câu trả lời
Input: Truy vấn + Final Passages + Filtered Triples + Expanded Context
Xử lý:
Định dạng thành prompt có cấu trúc
Đưa vào LLM mạnh (GPT-3.5-turbo, Qwen2.5-7B-Instruction) để tạo câu trả lời
Output: Câu trả lời cuối cùng cho người dùng

Đánh giá tổng quan: Mục đích chính là cải thiện vấn đề Retrieve nhờ vào:
Kết hợp ưu điểm của cả passages (ngữ cảnh phong phú) và triples (facts chính xác) => Bổ sung thông tin.
Lọc Triples => Sau đó dùng Filtered Triples để lọc Passages => Bỏ thông tin dư thừa.
Sử dụng filtered triples lan truyền 1 - hop sang các Phrase Nodes khác => Bổ sung thông tin.
```
