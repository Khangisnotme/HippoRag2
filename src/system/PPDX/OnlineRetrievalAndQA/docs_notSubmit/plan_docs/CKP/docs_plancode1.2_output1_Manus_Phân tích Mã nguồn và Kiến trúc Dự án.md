# Phân tích Mã nguồn và Kiến trúc Dự án

## 1. Tóm tắt Quy trình Offline và Online (Dựa trên pasted_content.txt)

### Pha Offline (Xây dựng Bộ nhớ - Tương tự HippoRAG2)

1.  **Phân đoạn Tài liệu (Module 1):** Chia tài liệu gốc thành các đoạn (passages) có ý nghĩa logic, sử dụng LLM (Qwen2.5-7B) để nhận diện ranh giới dựa trên ngữ nghĩa thay vì quy tắc cứng.
2.  **Trích xuất Triple (Module 2 - OpenIE by LLM):** Sử dụng LLM (Qwen2.5-7B) để trích xuất các bộ ba thông tin (subject, relation, object) từ mỗi passage, tạo thành kiến thức có cấu trúc.
3.  **Phát hiện Từ đồng nghĩa (Module 3 - Synonym Detection):** Sử dụng mô hình embedding (paraphrase-multilingual-mpnet-base-v2) để tính toán độ tương đồng giữa các cụm từ (phrase) đã trích xuất (subject/object). Nếu độ tương đồng vượt ngưỡng (ví dụ: 0.85), tạo cạnh `Synonym Edge` giữa các `Phrase Node` tương ứng.
4.  **Xây dựng Đồ thị Tri thức (Module 4 - Graph Builder):** Tích hợp tất cả thông tin vào Neo4j:
    *   Tạo `Passage Node` cho mỗi đoạn văn gốc.
    *   Tạo `Phrase Node` cho mỗi subject và object từ các triple.
    *   Tạo `Relation Edge` (có hướng) giữa các `Phrase Node` để biểu diễn triple.
    *   Tạo `Synonym Edge` (vô hướng) giữa các `Phrase Node` đồng nghĩa.
    *   Tạo `Contain Edge` (có hướng) từ `Passage Node` đến các `Phrase Node` mà nó chứa.

### Pha Online (Truy xuất và Hỏi đáp - Đề xuất mới)

1.  **Truy xuất Kép/Lai (Dual/Hybrid Retrieval):**
    *   Input: Truy vấn người dùng.
    *   Xử lý: Dùng BM25 + Embedding để truy xuất song song:
        *   Top-K passages (50-100) -> `Raw Passages`.
        *   Top-N triples (20-50) -> `Raw Triples`.
2.  **Lọc Triple bằng LLM:**
    *   Input: `Raw Triples` + Truy vấn gốc.
    *   Xử lý: Dùng LLM (Qwen2.5-7B) để chọn lọc, giữ lại các facts cốt lõi, phù hợp nhất với truy vấn.
    *   Output: `Filtered Triples` (Top-M, khoảng 10-20).
3.  **Xếp hạng lại Passages dựa trên Triples:**
    *   Input: `Raw Passages` + `Filtered Triples`.
    *   Xử lý:
        *   Tính điểm hỗ trợ (`Score_support`): Đếm số `Filtered Triples` mà mỗi passage hỗ trợ (chứa cả subject và object).
        *   Kết hợp điểm: `Score_final = α * Score_retriever + (1-α) * Score_support` (với `Score_retriever` là điểm từ bước 1, α là trọng số).
        *   Chọn Top-P passages có `Score_final` cao nhất.
    *   Output: `Final Passages` (5-10 passages tốt nhất).
4.  **Mở rộng Ngữ cảnh (Tùy chọn):**
    *   Input: `Filtered Triples`.
    *   Xử lý: Thực hiện tìm kiếm 1-hop trên KG từ các `Filtered Triples` để lấy thêm thông tin liên quan (thay vì lan truyền rộng như PPR).
    *   Output: `Expanded Context`.
5.  **Tạo Câu trả lời:**
    *   Input: Truy vấn + `Final Passages` + `Filtered Triples` + `Expanded Context`.
    *   Xử lý: Định dạng thành prompt cấu trúc, đưa vào LLM (Qwen2.5-7B) để sinh câu trả lời.
    *   Output: Câu trả lời cuối cùng.

**Mục tiêu chính của pha Online đề xuất:** Cải thiện Retrieval bằng cách kết hợp ngữ cảnh (passages) và facts (triples), lọc nhiễu thông qua triple filtering và passage re-ranking, và mở rộng thông tin có kiểm soát (1-hop) thay vì lan truyền rộng.

## 2. Phân tích Mã nguồn Python Pha Offline

*   **`module1_chunking.py`:**
    *   **Chức năng:** Thực hiện việc chia tài liệu thành các chunks. Hiện tại, triển khai rất đơn giản: mỗi document đầu vào (giả định là một paragraph từ Excel) được coi là một chunk duy nhất (`chunking_method: 'keep_as_paragraph'`).
    *   **Input:** List các dictionary, mỗi dict đại diện cho một document (`doc_id`, `title`, `text`, `metadata`).
    *   **Output:** List các dictionary, mỗi dict đại diện cho một chunk (`chunk_id`, `doc_id`, `text`, `metadata`...). Lưu kết quả vào `self.processed_chunks`.
    *   **Vai trò:** Chuẩn bị dữ liệu đầu vào cho các bước sau dưới dạng các đơn vị văn bản (chunks).
*   **`module2_triple_extractor.py`:**
    *   **Chức năng:** Trích xuất các bộ ba (subject, predicate, object) từ nội dung text của các chunks. Sử dụng API HuggingFace với mô hình Qwen2.5-7B làm phương thức chính. Có cơ chế fallback sử dụng OpenAI GPT-3.5 Turbo nếu Qwen thất bại (nếu được kích hoạt và có API key). Tương thích với cả phiên bản OpenAI < 1.0 và >= 1.0.
    *   **Input:** List các chunk dictionaries.
    *   **Output:** List các đối tượng `Triple` (dataclass) chứa thông tin `subject`, `predicate`, `object`, `confidence`, `source_chunk_id`, `source_doc_id`, `extraction_method`.
    *   **Vai trò:** Chuyển đổi văn bản phi cấu trúc thành kiến thức có cấu trúc (triples).
*   **`module3_synonym_detector.py`:**
    *   **Chức năng:** Phát hiện các cụm từ (phrases) đồng nghĩa trong tập hợp các subject và object từ các triple đã trích xuất. Sử dụng mô hình Sentence Transformer (mặc định `paraphrase-multilingual-mpnet-base-v2`) để tạo embeddings cho các phrase, sau đó tính cosine similarity. Các cặp phrase có similarity vượt ngưỡng (`similarity_threshold`) được coi là đồng nghĩa.
    *   **Input:** List các đối tượng `Triple`.
    *   **Output:** List các đối tượng `SynonymPair` (dataclass) chứa `phrase1`, `phrase2`, `similarity_score`. Có thể tạo ra một `synonym_mapping` từ phrase về dạng chuẩn (canonical form) nhưng phiên bản hiện tại trong `pipeline_orchestrator.py` dường như không sử dụng mapping này, phù hợp với phong cách HippoRAG 2 giữ lại các biến thể.
    *   **Vai trò:** Xác định và liên kết các biểu diễn khác nhau của cùng một khái niệm, làm giàu ngữ nghĩa cho đồ thị.
*   **`module4_graph_builder.py`:**
    *   **Chức năng:** Xây dựng đồ thị tri thức trong Neo4j dựa trên chunks, triples, và synonym pairs. Tạo các `Passage Node`, `Phrase Node` (sử dụng text chuẩn hóa làm ID để dễ đọc, không dùng canonical mapping), `Relation Edge`, `Synonym Edge`, và `Contain Edge`. Tính toán và lưu trữ embeddings cho cả Passage và Phrase nodes.
    *   **Input:** List các chunk dictionaries, list các đối tượng `Triple`, list các đối tượng `SynonymPair`.
    *   **Output:** Xây dựng cấu trúc đồ thị trong cơ sở dữ liệu Neo4j. Trả về thống kê về số lượng node/edge đã tạo.
    *   **Vai trò:** Lưu trữ và tổ chức toàn bộ kiến thức đã xử lý thành một cấu trúc đồ thị liên kết, sẵn sàng cho truy vấn.
*   **`pipeline_orchestrator.py`:**
    *   **Chức năng:** Điều phối toàn bộ quy trình Offline. Gọi lần lượt các module: đọc dữ liệu Excel (`ExcelDocumentProcessor`), chunking (`ChunkProcessor`), trích xuất triple (`TripleExtractor` với fallback), phát hiện synonym (`SynonymDetector`), và xây dựng đồ thị (`GraphBuilder`). Quản lý luồng dữ liệu giữa các bước và thu thập thống kê.
    *   **Input:** Đường dẫn file Excel, các API keys, cấu hình Neo4j, các tham số (ngưỡng synonym, có xóa graph cũ không...).
    *   **Output:** Hoàn thành việc xây dựng đồ thị trong Neo4j. Trả về dictionary chứa thống kê chi tiết của toàn bộ pipeline.
    *   **Vai trò:** Đóng vai trò trung tâm, kết nối các module riêng lẻ thành một quy trình hoàn chỉnh.
*   **`run_offline_pipeline.py`:**
    *   **Chức năng:** Là điểm khởi chạy (entry point) cho toàn bộ pipeline Offline. Có nhiệm vụ thiết lập logging, lấy các cấu hình cần thiết (ví dụ: API keys, đường dẫn file input/output, cấu hình Neo4j) từ biến môi trường hoặc file config, khởi tạo `OfflinePipelineOrchestrator` và gọi phương thức `run_complete_pipeline`.
    *   **Input:** Các tham số cấu hình (qua command line, env vars, hoặc file config).
    *   **Output:** Thực thi pipeline và in ra kết quả tóm tắt.
    *   **Vai trò:** Cung cấp giao diện để người dùng chạy quy trình xử lý Offline.
*   **`utils/`:**
    *   **`utils_general.py`:** Chứa các hàm tiện ích chung như thiết lập logging, lưu kết quả...
    *   **`utils_excel_documents.py`:** Chuyên xử lý việc đọc và tiền xử lý dữ liệu từ file Excel đầu vào.
    *   **`utils_neo4j.py`:** Đóng gói các tương tác với Neo4j (kết nối, thực thi Cypher queries, tạo node/edge, thiết lập constraints/indexes). Giúp tách biệt logic nghiệp vụ khỏi chi tiết thao tác cơ sở dữ liệu.

## 3. Kiến trúc Mã nguồn Dự án (Pha Offline)

Dựa trên cấu trúc thư mục và các file được cung cấp:

```
│   └── 📁 OfflineIndexing/
│       ├── 📋 offline_indexing_requirements.txt  # Dependencies
│       │
│       ├── 📄 module1_chunking.py             # Module xử lý cụ thể
│       ├── 🧠 module2_triple_extractor.py     # Module xử lý cụ thể
│       ├── 🔗 module3_synonym_detector.py    # Module xử lý cụ thể
│       ├── 🏗️ module4_graph_builder.py       # Module xử lý cụ thể
│       │
│       ├── 🎯 pipeline_orchestrator.py       # Lớp điều phối pipeline
│       ├── 🚀 run_offline_pipeline.py         # Script chạy chính
│       │
│       ├── 📁 utils/                         # Thư mục chứa tiện ích
│       │   ├── 🔧 utils_general.py           # Tiện ích chung
│       │   ├── 📊 utils_excel_documents.py    # Tiện ích xử lý Excel
│       │   └── 🗃️ utils_neo4j.py             # Tiện ích tương tác Neo4j
│       │
│       └── 📁 test/                         # Thư mục chứa tests
│           ├── 📊 test_data.py              # Dữ liệu test
│           ├── 🧪 test_offline_pipeline.py   # Test pipeline tổng thể
│           └── 🔍 test_query_functions.py    # Test các hàm query (Neo4j?)
│
└── 📁 OnlineRetrievalAndQA                 # Thư mục cho pha Online (chưa có nội dung)
```

*   **Phân tách Rõ ràng:** Dự án được chia thành hai thư mục cấp cao tương ứng với hai pha chính: `OfflineIndexing` và `OnlineRetrievalAndQA`. Điều này giúp quản lý code dễ dàng.
*   **Modular Hóa (Offline):** Bên trong `OfflineIndexing`, các bước xử lý chính được tách thành các module riêng biệt (`module1_...`, `module2_...`, etc.). Mỗi module tập trung vào một nhiệm vụ cụ thể, giúp code dễ hiểu, dễ bảo trì và dễ thay thế.
*   **Lớp Điều phối:** `pipeline_orchestrator.py` đóng vai trò là tầng điều phối, gọi các module theo đúng thứ tự và quản lý luồng dữ liệu. Điều này tuân theo nguyên tắc Single Responsibility và giúp giảm sự phụ thuộc trực tiếp giữa các module xử lý.
*   **Điểm Khởi chạy:** `run_offline_pipeline.py` là điểm vào duy nhất để thực thi toàn bộ quy trình Offline, giúp việc triển khai và sử dụng đơn giản hơn.
*   **Tách biệt Tiện ích:** Các hàm tiện ích được gom vào thư mục `utils/` và phân loại rõ ràng (general, excel, neo4j). Điều này thúc đẩy tái sử dụng code và giữ cho các module chính tập trung vào logic nghiệp vụ.
*   **Tập trung vào Testing:** Sự hiện diện của thư mục `test/` cho thấy dự án có chú trọng đến việc kiểm thử, đảm bảo chất lượng code.
*   **Quản lý Dependencies:** `offline_indexing_requirements.txt` giúp quản lý các thư viện Python cần thiết cho pha Offline.

**Nhìn chung:** Kiến trúc pha Offline được tổ chức tốt, theo hướng module hóa, có sự phân tách rõ ràng giữa logic xử lý, điều phối, tiện ích và testing. Cấu trúc này dễ dàng mở rộng và bảo trì.

## 4. Mô tả Luồng Online (Dựa trên pasted_content.txt)

Luồng Online được mô tả chi tiết trong `pasted_content.txt` (xem lại Mục 1 ở trên). Tóm tắt các bước chính:

1.  **Hybrid Retrieval:** Nhận query, dùng BM25 + Embedding lấy top Passages và top Triples.
2.  **Triple Filtering:** Dùng LLM lọc Triples dựa trên query gốc.
3.  **Passage Re-ranking:** Tính điểm mới cho Passages dựa trên điểm retrieval ban đầu và số Filtered Triples mà passage đó hỗ trợ. Chọn top Passages theo điểm mới.
4.  **Context Expansion (Optional):** Mở rộng 1-hop trên KG từ Filtered Triples.
5.  **Answer Generation:** Dùng LLM mạnh tạo câu trả lời từ query, Final Passages, Filtered Triples, và Expanded Context.

*(Lưu ý: Phân tích này dựa trên các file text và cấu trúc thư mục bạn cung cấp. Chưa phân tích nội dung file PDF và các file utils chi tiết.)*
