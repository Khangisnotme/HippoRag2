# 🚀 **OUTPUT CỦA run_retrieval_pipeline.py**

## 📊 **Output File JSON Format:**

### **🔥 Main Output Structure:**
```json
{
  "method": "proposed_hipporag",
  "total_queries": 5,
  "timestamp": "2025-05-31T10:30:45.123456",
  "results": [
    {
      "query_id": "Q001",
      "query": "Lợi ích của táo cho sức khỏe là gì?",
      "method": "proposed_hipporag",
      "top_passages": [
        {
          "passage_id": "passage_chunk_FOOD_0_0",
          "rank": 1,
          "score": 0.847,
          "text": "Táo là loại trái cây giàu vitamin C và chất xơ, rất tốt cho sức khỏe. Vitamin C giúp tăng cường hệ miễn dịch...",
          "metadata": {
            "hybrid_retrieval_score": 0.75,
            "support_score": 0.85,
            "supporting_triples_count": 3,
            "score_breakdown": {
              "bm25_score": 0.8,
              "embedding_score": 0.7,
              "hybrid_score": 0.75,
              "support_score": 0.85,
              "final_score_after_modifiers": 0.847
            }
          }
        },
        {
          "passage_id": "passage_chunk_HEALTH_2_0", 
          "rank": 2,
          "score": 0.723,
          "text": "Chất xơ trong táo giúp cải thiện tiêu hóa và kiểm soát cholesterol...",
          "metadata": {
            "hybrid_retrieval_score": 0.68,
            "support_score": 0.72,
            "supporting_triples_count": 2,
            "score_breakdown": {...}
          }
        },
        // ... up to 10 passages
      ],
      "processing_time": 12.47,
      "metadata": {
        "total_passages_retrieved": 20,
        "filtered_triples_count": 15,
        "final_passages_count": 10
      }
    },
    {
      "query_id": "Q002",
      "query": "Vitamin C có tác dụng gì đối với hệ miễn dịch?",
      // ... similar structure
    }
    // ... more queries
  ]
}
```

---

## 📋 **Console Output Example:**

### **🖥️ Terminal Display:**
```bash
(.venv) PS> python run_retrieval_pipeline.py --queries sample_queries.json --output results.json

🚀 Running multiple queries mode...
📄 Loading queries from: sample_queries.json
📋 Loaded 5 queries
🔧 Đang khởi tạo các modules...
   📊 Khởi tạo Module 1 - Dual Retrieval...
   🤖 Khởi tạo Module 2 - LLM Triple Filter...
   🏆 Khởi tạo Module 3 - Passage Ranker...
✅ Tất cả modules đã được khởi tạo thành công

📊 PROCESSING QUERY 1/5: Q001
================================================================================
🚀 BẮT ĐẦU RETRIEVAL PIPELINE
================================================================================
📝 Query ID: Q001
📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'

📊 MODULE 1: DUAL RETRIEVAL
------------------------------------------------------------
🔧 Bắt đầu khởi tạo indices cho hệ thống truy xuất...
📥 Bước 1/4: Tải dữ liệu từ Neo4j...
✅ Đã truy xuất 10 passages từ Neo4j
✅ Đã truy xuất 87 triples từ Neo4j
🔍 Bước 2/4: Xây dựng indices BM25...
🧠 Bước 3/4: Tạo embeddings...
✅ Module 1 hoàn thành trong 8.23s

🤖 MODULE 2: LLM TRIPLE FILTERING
------------------------------------------------------------
🤖 Bắt đầu filtering 50 triples với Qwen...
📦 Batch 1/7: triples 1-8
   ✅ Hoàn thành batch 1, evaluations: 8
✅ Module 2 hoàn thành trong 3.15s

🏆 MODULE 3: PASSAGE RANKING
------------------------------------------------------------
📊 Bắt đầu xây dựng support mapping cho 15 filtered triples...
🧮 Đang tính scores cho 20 passages...
🏆 Áp dụng ranking strategy: hybrid_balanced
✅ Module 3 hoàn thành trong 1.09s

================================================================================
🎉 RETRIEVAL PIPELINE HOÀN THÀNH
================================================================================
📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
⏱️ Tổng thời gian: 12.47s
📊 Top passages: 10

📈 THỜI GIAN TỪNG MODULE:
   dual_retrieval: 8.23s (66.0%)
   triple_filtering: 3.15s (25.2%)
   passage_ranking: 1.09s (8.7%)

🏆 TOP 3 PASSAGES:
   1. passage_chunk_FOOD_0_0: 0.847
      📝 Táo là loại trái cây giàu vitamin C và chất xơ, rất tốt cho sức khỏe...
   2. passage_chunk_HEALTH_2_0: 0.723
      📝 Chất xơ trong táo giúp cải thiện tiêu hóa và kiểm soát cholesterol...
   3. passage_chunk_NUTRITION_1_0: 0.689
      📝 Vitamin C có vai trò quan trọng trong việc tăng cường hệ miễn dịch...

✅ Query Q001 hoàn thành

📊 PROCESSING QUERY 2/5: Q002
// ... similar output for other queries

🎉 Batch processing completed!
   📊 Queries processed: 5
   ⏱️ Total time: 58.34s
   📈 Average time per query: 11.67s
   💾 Results saved to: results.json

============================================================
📊 RETRIEVAL RESULTS SUMMARY
============================================================
📋 Total queries processed: 5
🔧 Method: proposed_hipporag
⏱️ Average processing time: 11.67s per query

🏆 TOP 3 SAMPLE RESULTS:

1. Query: Lợi ích của táo cho sức khỏe là gì?...
   Query ID: Q001
   Top passages found: 10
   Processing time: 12.47s
     1. passage_chunk_FOOD_0_0: 0.847
        Táo là loại trái cây giàu vitamin C và chất xơ, rất tốt cho sức khỏe...
     2. passage_chunk_HEALTH_2_0: 0.723
        Chất xơ trong táo giúp cải thiện tiêu hóa và kiểm soát cholesterol...

2. Query: Vitamin C có tác dụng gì đối với hệ miễn dịch?...
   Query ID: Q002
   Top passages found: 10
   Processing time: 10.92s
     1. passage_chunk_VITAMIN_0_0: 0.891
        Vitamin C đóng vai trò quan trọng trong việc tăng cường hệ miễn dịch...
     2. passage_chunk_HEALTH_3_0: 0.756
        Hệ miễn dịch mạnh giúp cơ thể chống lại bệnh tật hiệu quả...

💾 Full results available in output file
============================================================

✅ Pipeline completed successfully!
💾 Results saved to: results.json
📊 Ready for evaluation against baseline RAG!
```

---

## 🎯 **Output Files Generated:**

### **📁 File Structure:**
```
outputs/
├── retrieval_results.json          # Main results file
├── log/
│   ├── pipeline_20250531_103045.log  # Detailed logs
│   └── module*_*.log                  # Module-specific logs
└── intermediate/ (nếu enabled)
    ├── query_Q001_result.json        # Per-query detailed results
    ├── query_Q002_result.json
    └── ...
```

---

## 📊 **Key Metrics trong Output:**

### **🔥 Performance Metrics:**
```json
{
  "processing_time": 12.47,           // Total time per query
  "module_breakdown": {
    "dual_retrieval": 8.23,           // Module 1 time
    "triple_filtering": 3.15,         // Module 2 time  
    "passage_ranking": 1.09           // Module 3 time
  },
  "data_flow": {
    "raw_passages": 20,               // Retrieved by Module 1
    "raw_triples": 50,                // Retrieved by Module 1
    "filtered_triples": 15,           // Filtered by Module 2
    "final_passages": 10              // Final ranked by Module 3
  }
}
```

### **🎯 Ready for Baseline Comparison:**
```python
# Extract for evaluation
proposed_rankings = ["passage_chunk_FOOD_0_0", "passage_chunk_HEALTH_2_0", ...]
baseline_rankings = ["passage_chunk_WATER_1_0", "passage_chunk_FOOD_0_0", ...]

# Calculate metrics
precision_at_3 = calculate_precision(proposed_rankings[:3], ground_truth)
recall_at_5 = calculate_recall(proposed_rankings[:5], ground_truth)
mrr = calculate_mrr(proposed_rankings, ground_truth)
```

### **🔥 Thông tin Complete để So sánh:**
- ✅ **Top-K ranked passages** với scores
- ✅ **Processing time breakdown** 
- ✅ **Rich metadata** cho analysis
- ✅ **Performance statistics**
- ✅ **Error tracking** (nếu có)

**🚀 Output này CHÍNH XÁC là những gì cần để so sánh với baseline RAG! 💪**


---



# Output: 

Hãy cùng phân tích log bạn đã cung cấp:

---

## Tóm tắt hoạt động

Log này cho thấy quá trình khởi tạo và thực hiện truy xuất kép (Dual Retrieval) của một hệ thống. Hệ thống này kết hợp hai phương pháp tìm kiếm: **BM25** (thuật toán tìm kiếm dựa trên tần suất từ) và **Embedding** (tìm kiếm dựa trên ngữ nghĩa thông qua vector nhúng). Dữ liệu được truy xuất từ cơ sở dữ liệu đồ thị **Neo4j**.

---

## Chi tiết các bước

### 1. Khởi tạo DualRetriever
* **Thời gian:** 2025-05-31 12:35:13,087
* Hệ thống bắt đầu khởi tạo DualRetriever.
* Cấu hình của bộ truy xuất được đặt là **BM25 với trọng số 0.3** và **Embedding với trọng số 0.7**. Điều này có nghĩa là kết quả từ Embedding sẽ có ảnh hưởng lớn hơn đến điểm số cuối cùng.
* Kết nối đến cơ sở dữ liệu Neo4j tại `bolt://localhost:7687` đã thành công.
* Các bộ truy xuất **BM25Retriever** và **EmbeddingRetriever** được khởi tạo thành công.
* **HybridScorer** (bộ tính điểm kết hợp) được thiết lập với các trọng số đã định.
* Quá trình khởi tạo DualRetriever hoàn tất.

### 2. Bắt đầu truy xuất kép
* **Thời gian:** 2025-05-31 12:35:13,161
* Truy vấn được đưa ra là: **'Diego Maradona nhỏ tuổi hơn Rutherford B. Hayes phải không?'**
* Hệ thống đặt mục tiêu truy xuất: 100 passages và 200 triples.

### 3. Giai đoạn 1: Truy xuất Passages
* Hệ thống bắt đầu tải dữ liệu và xây dựng chỉ mục.
* Đã truy xuất **10 passages** từ Neo4j (thống kê: tổng 4,460 ký tự, trung bình 446 ký tự/passage).
* Đã truy xuất **87 triples** từ Neo4j (thống kê: độ tin cậy trung bình 0.932, 87/87 triples có độ tin cậy cao, 54 predicates độc nhất).
* Chỉ mục **BM25** được xây dựng cho cả 10 passages và 87 triples thành công.
* Embeddings được tạo cho cả passages và triples bằng cách sử dụng mô hình `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`. Thời gian tải mô hình khá nhanh (khoảng 5 giây).
* Quá trình khởi tạo indices hoàn tất.
* Hệ thống thực hiện tìm kiếm passages:
    * **BM25** tìm thấy 8 kết quả có điểm > 0.
    * **Embedding** tìm thấy 1 kết quả có điểm > 0.5 (điểm cao nhất 0.682).
* Điểm số từ BM25 và Embedding được kết hợp. Log chỉ ra rằng có 10 mục duy nhất được kết hợp điểm.
    * Điểm lai cao nhất là 0.985, thấp nhất là 0.000.
    * Có 8 kết quả có nguồn điểm từ cả BM25 và Embedding, 0 kết quả chỉ từ BM25, và 1 kết quả chỉ từ Embedding.
* **Top 10 passages được truy xuất:**
    1.  `passage_chunk_Diego Maradona_2_0` - Điểm: 0.985 (Rất liên quan)
    2.  `passage_chunk_Thảo My_6_0` - Điểm: 0.464
    3.  `passage_chunk_Diego Costa_1_0` - Điểm: 0.460
    4.  `passage_chunk_Danh sách Tổng thống Hoa Kỳ_3_0` - Điểm: 0.458 (Cũng liên quan đến Rutherford B. Hayes)
    5.  `passage_chunk_Isaac Hayes_7_0` - Điểm: 0.397
    6.  `passage_chunk_Ernest Rutherford_4_0` - Điểm: 0.331
    7.  `passage_chunk_PH_0_0` - Điểm: 0.299
    8.  `passage_chunk_Helen Hayes_5_0` - Điểm: 0.256
    9.  `passage_chunk_FOOD_0_0` - Điểm: 0.024
    10. `passage_chunk_WATER_0_0` - Điểm: 0.000

### 4. Giai đoạn 2: Truy xuất Triples
* Hệ thống sử dụng lại các indices đã khởi tạo.
* Hệ thống thực hiện tìm kiếm triples:
    * **BM25** tìm thấy 68 kết quả có điểm > 0.
    * **Embedding** tìm thấy 26 kết quả có điểm > 0.3 (điểm cao nhất 0.617).
* Điểm số từ BM25 và Embedding được kết hợp cho 87 triples.
    * Điểm lai cao nhất là 0.879, thấp nhất là 0.000.
    * Có 68 kết quả có nguồn điểm từ cả hai, 0 chỉ từ BM25, và 18 chỉ từ Embedding.
* **Top triples được truy xuất (chỉ liệt kê những cái liên quan trực tiếp đến câu hỏi):**
    * `(diego armando maradona → cơ động hơn → hầu hết các cầu thủ khác)` - Điểm: 0.879 (Rất cao, nhưng không trực tiếp trả lời câu hỏi tuổi tác)
    * `(tổng thống → phải có độ tuổi → 35 tuổi)` - Điểm: 0.575 (Liên quan đến tiêu chí tuổi của tổng thống)
    * `(diego da silva costa → sinh ngày → 7 tháng 10 năm 1988)` - Điểm: 0.338 (Là Diego Costa, không phải Maradona)
    * `(chảo my → đăng quang khi → mới 16 tuổi)` - Điểm: 0.291 (Không liên quan)

### 5. Biên soạn thống kê & Hoàn thành
* **Tổng thời gian:** 7.50 giây.
* **Passages tìm được:** 10/100 (10% mục tiêu).
* **Triples tìm được:** 87/200 (43.5% mục tiêu).
* **Hiệu suất:** 12.9 items/giây.
* **Điểm trung bình:** Passages: 0.367, Triples: 0.316.
* DualRetriever được đóng và giải phóng tài nguyên.

---

## Nhận xét và Phân tích

* **Hiệu suất:** Thời gian chạy 7.50 giây là chấp nhận được cho một truy vấn khởi tạo và tìm kiếm dữ liệu từ Neo4j. Hiệu suất 12.9 items/giây có vẻ hơi thấp nếu dataset lớn, nhưng đối với 10 passages và 87 triples thì không quá tệ.
* **Relevance của kết quả:**
    * Đối với câu hỏi về tuổi tác của Diego Maradona và Rutherford B. Hayes, hệ thống đã tìm thấy `passage_chunk_Diego Maradona_2_0` và `passage_chunk_Danh sách Tổng thống Hoa Kỳ_3_0` với điểm số khá cao, cho thấy khả năng thu thập thông tin liên quan đến cả hai nhân vật.
    * Tuy nhiên, trong các triples được truy xuất, không có triple nào trực tiếp so sánh tuổi của Diego Maradona và Rutherford B. Hayes hoặc cung cấp ngày sinh của cả hai nhân vật này để so sánh. Triple liên quan đến tuổi tác như `(tổng thống → phải có độ tuổi → 35 tuổi)` chỉ là một quy định chung chứ không phải thông tin cụ thể về Rutherford B. Hayes.
    * Nhiều triple liên quan đến "Diego Maradona" chỉ tập trung vào sự nghiệp bóng đá của ông (ví dụ: `cơ động hơn`, `chơi cho`, `được coi là`).
* **Trọng số:** Việc gán trọng số 0.7 cho Embedding và 0.3 cho BM25 có thể giúp hệ thống nắm bắt ngữ nghĩa tốt hơn, nhưng nếu thông tin cụ thể (như ngày sinh) không có sẵn trong các embeddings hoặc passages liên quan, thì kết quả sẽ không trực tiếp trả lời được câu hỏi "nhỏ tuổi hơn phải không?".
* **Dữ liệu thiếu:** Log cho thấy hệ thống đã tìm kiếm được các passage và triple, nhưng rõ ràng thông tin cụ thể về ngày sinh của Rutherford B. Hayes và Diego Maradona để so sánh trực tiếp không nằm trong top kết quả được hiển thị. Điều này có thể do:
    * Dữ liệu ngày sinh không tồn tại trong cơ sở dữ liệu Neo4j.
    * Thông tin ngày sinh tồn tại nhưng không được đánh điểm đủ cao hoặc không được biểu diễn dưới dạng triple mà hệ thống có thể dễ dàng truy xuất để so sánh trực tiếp.

---

## Kết luận

Hệ thống DualRetriever đã hoạt động thành công trong việc khởi tạo, kết nối với Neo4j và thực hiện truy xuất kép. Nó đã tìm thấy các passage và triple liên quan đến các thực thể được nhắc đến trong câu hỏi ("Diego Maradona" và "Tổng thống Hoa Kỳ"). Tuy nhiên, dựa trên các kết quả được hiển thị, hệ thống chưa tìm được thông tin cụ thể (như ngày sinh) để trực tiếp trả lời câu hỏi so sánh tuổi tác giữa Diego Maradona và Rutherford B. Hayes.

Bạn có muốn tôi thử tìm thông tin ngày sinh của Diego Maradona và Rutherford B. Hayes để bạn có thể so sánh không?