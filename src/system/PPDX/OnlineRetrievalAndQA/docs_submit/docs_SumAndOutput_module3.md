# Summary module 3 

# 🎉 **MODULE 3 - PASSAGE RANKING SUMMARY**

## 📊 **Tổng quan Architecture Module 3:**

### **🏗️ Workflow chính:**
```
Raw Passages (Module 1) + Filtered Triples (Module 2) → Support Score Calculation → Hybrid Ranking → Ranked Passages
```

### **🔧 Core Components:**

#### **1️⃣ SupportScoreCalculator - Tính điểm hỗ trợ:**
```python
4 Phương pháp tính Support Score:
✅ COUNT_BASED: Đếm số lượng triples hỗ trợ
✅ WEIGHTED_RELEVANCE: Trọng số theo relevance score
✅ QUALITY_WEIGHTED: Kết hợp relevance + confidence
✅ LOG_SCALED: Log scaling để tránh outliers

Mapping System:
- passage_id → [supporting_triple_ids]
- Chỉ count triples có relevance >= threshold
- Statistics tracking cho performance monitoring
```

#### **2️⃣ PassageRanker - Main orchestrator:**
```python
6 Ranking Strategies:
✅ RETRIEVAL_ONLY: 100% retrieval score (baseline)
✅ SUPPORT_ONLY: 100% support score từ triples
✅ HYBRID_BALANCED: 50-50 giữa retrieval và support
✅ HYBRID_RETRIEVAL_FOCUSED: 70% retrieval, 30% support
✅ HYBRID_SUPPORT_FOCUSED: 30% retrieval, 70% support
✅ ADAPTIVE: Auto-adjust weights dựa trên data quality

Final Score = α_retrieval × hybrid_retrieval_score + α_support × support_score
```

#### **3️⃣ RankedPassage - Rich output structure:**
```python
Comprehensive Information:
- passage_id, original_text
- hybrid_retrieval_score, support_score, final_score
- rank, supporting_triples_count
- supporting_triples (list of IDs)
- score_breakdown (detailed calculation)
- ranking_metadata (traceability)
```

---

## 🎯 **Key Innovations:**

### **🔥 Multi-Strategy Ranking:**
```python
Strategy Selection dựa trên use case:
- High-precision: RETRIEVAL_ONLY hoặc HYBRID_RETRIEVAL_FOCUSED
- Knowledge-driven: SUPPORT_ONLY hoặc HYBRID_SUPPORT_FOCUSED
- Balanced: HYBRID_BALANCED
- Smart: ADAPTIVE (auto-adjust based on data quality)
```

### **⚡ Intelligent Support Scoring:**
```python
Support Score Logic:
1. Map triples → source passages
2. Filter triples theo relevance threshold (default 0.3)
3. Calculate score theo method được chọn:
   - Count: Simple counting với log scaling
   - Weighted: Average relevance × count boost
   - Quality: Combine relevance + confidence
   - Log: Log scaling để handle outliers
```

### **🧠 Adaptive Weight Calculation:**
```python
Auto-adjust weights dựa trên:
- Support coverage (% passages có support)
- Score variance (quality of discrimination)
- Data distribution patterns

Logic:
- Low support coverage → Thiên về retrieval
- High support quality → Thiên về support
- Balanced case → Moderate weights
```

---

## 📈 **Performance Characteristics:**

### **🚀 Processing Efficiency:**
```
Input: Raw passages + Filtered triples
Processing: Support mapping + Score calculation + Strategy application
Output: Ranked passages với comprehensive metadata
Typical time: ~0.1-0.5 seconds cho 10-20 passages
```

### **🎯 Quality Improvements:**
```
Ranking Quality Enhancements:
- Boost factor cho high support passages (default 1.2×)
- Penalty factor cho no support passages (default 0.8×)
- Score normalization để fair comparison
- Diversity ranking để tránh duplicates
```

### **📊 Rich Analytics:**
```
Comprehensive Statistics:
- Score distributions (retrieval, support, final)
- Support level breakdown (no/low/medium/high)
- Ranking change analysis (up/down/unchanged)
- Performance metrics (time, efficiency)
```

---

## 🔗 **Pipeline Integration:**

### **📋 Input Sources:**
```
Module 1: Raw passages với hybrid scores
Module 2: Filtered triples với relevance scores
Query: Original user query
```

### **📊 Output cho Module 5:**
```
RankedPassage objects với:
- Final ranking order
- Support evidence
- Score breakdowns
- Traceability metadata
```

### **🎯 Key Value:**
```
Intelligent Re-ranking:
- Passages có nhiều supporting triples → Rank cao hơn
- Passages không có support → Penalty
- Balance giữa retrieval quality và knowledge support
- Rich metadata cho answer generation
```

---

## 💪 **Production Features:**

### **🛡️ Robust Design:**
```python
✅ Multiple strategies cho different use cases
✅ Configurable parameters và thresholds
✅ Comprehensive error handling
✅ Rich logging và monitoring
✅ Graceful degradation khi no support
✅ Performance optimization
```

### **🧪 Testing Coverage:**
```python
✅ Individual component tests
✅ Strategy comparison tests
✅ Mock data comprehensive testing
✅ Edge case handling
✅ Performance benchmarking
```

---

## 🎭 **Module 3 Complete Summary:**

### **🏆 Core Achievement:**
**Intelligent passage re-ranking dựa trên knowledge graph support, cải thiện đáng kể quality của passages được đưa vào answer generation.**

### **📊 Technical Specs:**
```
Code lines: ~1,500+ lines
Classes: 4 main classes
Enums: 2 strategy enums
Strategies: 6 ranking approaches
Test suites: 3 comprehensive tests
Configuration options: 10+ parameters
```

### **🔥 Key Impact:**
```
🎯 Smart re-ranking - Passages có evidence được ưu tiên
⚡ Multiple strategies - Flexible theo use case
📈 Rich metadata - Complete traceability cho downstream
🧠 Adaptive logic - Auto-optimization dựa trên data
🛡️ Production ready - Robust error handling
```

---

## 🚀 **Ready for Module 5!**

### **📋 Perfect Setup cho Answer Generation:**
```
Module 3 Output → Module 5 Input:
- Top-ranked passages với evidence support
- Supporting triples clearly identified
- Score breakdowns cho confidence assessment
- Rich metadata cho citation generation
```

### **🎯 Current Pipeline Status:**
```
✅ Module 1: Dual Retrieval (Raw passages + triples)
✅ Module 2: LLM Triple Filtering (High-quality triples)
✅ Module 3: Passage Ranking (Evidence-supported passages)
✅ Module 4: Context Expansion (Additional context)
🔄 Module 5: Answer Generation (Final answer synthesis)
```

**🎉 Pipeline đã hoàn chỉnh 80%! Ready for final Module 5 - Answer Generation! 🚀**

**Bắt đầu Module 5 để complete toàn bộ Online Pipeline! 💪**

# Output module 3 

```bash
2025-05-31 07:40:27,275 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:40:27,275 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:40:27,277 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:40:27,278 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:40:27,278 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:40:27,279 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 1 filtered triples...
2025-05-31 07:40:27,279 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:40:27,279 - __main__ - INFO -    📊 Relevant triples: 1/1
2025-05-31 07:40:27,280 - __main__ - INFO -    📄 Passages with support: 1
2025-05-31 07:40:27,280 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:40:27,281 - __main__ - INFO -       1. test_passage_1: 1 triples
2025-05-31 07:40:27,282 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:40:27,282 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:40:27,282 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:40:27,283 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:40:27,283 - __main__ - INFO -    📊 Strategy: retrieval_only
2025-05-31 07:40:27,283 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:40:27,283 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:40:27,283 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:40:27,283 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,283 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:40:27,284 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,284 - __main__ - INFO - 📝 Query: 'test query'
2025-05-31 07:40:27,284 - __main__ - INFO - 📄 Raw passages: 3
2025-05-31 07:40:27,284 - __main__ - INFO - 🔗 Filtered triples: 2
2025-05-31 07:40:27,284 - __main__ - INFO - 🎯 Strategy: retrieval_only
2025-05-31 07:40:27,285 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:40:27,285 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,286 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 2 filtered triples...
2025-05-31 07:40:27,286 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:40:27,286 - __main__ - INFO -    📊 Relevant triples: 2/2
2025-05-31 07:40:27,286 - __main__ - INFO -    📄 Passages with support: 2
2025-05-31 07:40:27,287 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:40:27,287 - __main__ - INFO -       1. p1: 1 triples
2025-05-31 07:40:27,287 - __main__ - INFO -       2. p3: 1 triples
2025-05-31 07:40:27,287 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:40:27,287 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,287 - __main__ - INFO - 🧮 Đang tính scores cho 3 passages...
2025-05-31 07:40:27,288 - __main__ - INFO -    📊 Processed 3/3 passages
2025-05-31 07:40:27,288 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:40:27,288 - __main__ - INFO -    📊 Retrieval scores: min=0.350, max=0.850, avg=0.650
2025-05-31 07:40:27,288 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.620, avg=0.390
2025-05-31 07:40:27,289 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=2, high=0
2025-05-31 07:40:27,289 - __main__ - INFO - ✅ Hoàn thành tính scores cho 3 passages
2025-05-31 07:40:27,289 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:40:27,289 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,290 - __main__ - INFO - 🏆 Áp dụng ranking strategy: retrieval_only
2025-05-31 07:40:27,290 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=1.00, support=0.00
2025-05-31 07:40:27,290 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:40:27,290 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:40:27,291 - __main__ - INFO -    🏆 Top passage: p1 với score 1.000
2025-05-31 07:40:27,291 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:40:27,291 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,292 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:40:27,292 - __main__ - INFO -    📊 Limited output: 3 → 3 passages
2025-05-31 07:40:27,292 - __main__ - INFO - ✅ Final processing hoàn thành: 3 ranked passages
2025-05-31 07:40:27,292 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:40:27,292 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,292 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:40:27,293 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,293 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:40:27,293 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,293 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:40:27,293 - __main__ - INFO -    📝 Query: 'test query'
2025-05-31 07:40:27,293 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:40:27,293 - __main__ - INFO -    📄 Passages: 3 → 3
2025-05-31 07:40:27,294 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:40:27,294 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:40:27,294 - __main__ - INFO -    1. Rank 1: p1 | Final: 1.000 (Ret: 1.000, Sup: 0.620) | Triples: 1
2025-05-31 07:40:27,294 - __main__ - INFO -       📝 Text: High retrieval, high support...
2025-05-31 07:40:27,294 - __main__ - INFO -    2. Rank 2: p2 | Final: 0.640 (Ret: 0.800, Sup: 0.000) | Triples: 0
2025-05-31 07:40:27,294 - __main__ - INFO -       📝 Text: High retrieval, no support...
2025-05-31 07:40:27,295 - __main__ - INFO -    3. Rank 3: p3 | Final: 0.000 (Ret: 0.000, Sup: 0.550) | Triples: 1
2025-05-31 07:40:27,295 - __main__ - INFO -       📝 Text: Low retrieval, high support...
2025-05-31 07:40:27,295 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:40:27,295 - __main__ - INFO -    no_support: 1 passages (33.3%)
2025-05-31 07:40:27,295 - __main__ - INFO -    low_support: 2 passages (66.7%)
2025-05-31 07:40:27,295 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:40:27,295 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:40:27,296 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:40:27,296 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:40:27,296 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:40:27,296 - __main__ - INFO -    ➡️ Unchanged: 3
2025-05-31 07:40:27,297 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:40:27,297 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:40:27,297 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:40:27,297 - __main__ - INFO -    🏃 Passages/giây: 427.6
2025-05-31 07:40:27,298 - __main__ - INFO -    ⏱️ Avg time/passage: 0.002s
2025-05-31 07:40:27,298 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,299 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:40:27,299 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:40:27,299 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:40:27,300 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:40:27,300 - __main__ - INFO -    📊 Strategy: support_only
2025-05-31 07:40:27,300 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:40:27,300 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:40:27,300 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:40:27,300 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,301 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:40:27,301 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,301 - __main__ - INFO - 📝 Query: 'test query'
2025-05-31 07:40:27,301 - __main__ - INFO - 📄 Raw passages: 3
2025-05-31 07:40:27,302 - __main__ - INFO - 🔗 Filtered triples: 2
2025-05-31 07:40:27,302 - __main__ - INFO - 🎯 Strategy: support_only
2025-05-31 07:40:27,302 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:40:27,302 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,303 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 2 filtered triples...
2025-05-31 07:40:27,303 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:40:27,303 - __main__ - INFO -    📊 Relevant triples: 2/2
2025-05-31 07:40:27,303 - __main__ - INFO -    📄 Passages with support: 2
2025-05-31 07:40:27,303 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:40:27,304 - __main__ - INFO -       1. p1: 1 triples
2025-05-31 07:40:27,304 - __main__ - INFO -       2. p3: 1 triples
2025-05-31 07:40:27,304 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:40:27,304 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,304 - __main__ - INFO - 🧮 Đang tính scores cho 3 passages...
2025-05-31 07:40:27,304 - __main__ - INFO -    📊 Processed 3/3 passages
2025-05-31 07:40:27,305 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:40:27,305 - __main__ - INFO -    📊 Retrieval scores: min=0.350, max=0.850, avg=0.650
2025-05-31 07:40:27,305 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.620, avg=0.390
2025-05-31 07:40:27,305 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=2, high=0
2025-05-31 07:40:27,305 - __main__ - INFO - ✅ Hoàn thành tính scores cho 3 passages
2025-05-31 07:40:27,305 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:40:27,305 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,306 - __main__ - INFO - 🏆 Áp dụng ranking strategy: support_only
2025-05-31 07:40:27,306 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=0.00, support=1.00
2025-05-31 07:40:27,306 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:40:27,306 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:40:27,307 - __main__ - INFO -    🏆 Top passage: p1 với score 0.620
2025-05-31 07:40:27,307 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:40:27,308 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,308 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:40:27,308 - __main__ - INFO -    📊 Limited output: 3 → 3 passages
2025-05-31 07:40:27,308 - __main__ - INFO - ✅ Final processing hoàn thành: 3 ranked passages
2025-05-31 07:40:27,309 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:40:27,309 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,309 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:40:27,309 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,309 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:40:27,309 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,310 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:40:27,310 - __main__ - INFO -    📝 Query: 'test query'
2025-05-31 07:40:27,310 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:40:27,310 - __main__ - INFO -    📄 Passages: 3 → 3
2025-05-31 07:40:27,311 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:40:27,311 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:40:27,311 - __main__ - INFO -    1. Rank 1: p1 | Final: 0.620 (Ret: 1.000, Sup: 0.620) | Triples: 1
2025-05-31 07:40:27,312 - __main__ - INFO -       📝 Text: High retrieval, high support...
2025-05-31 07:40:27,312 - __main__ - INFO -    2. Rank 2: p3 | Final: 0.550 (Ret: 0.000, Sup: 0.550) | Triples: 1
2025-05-31 07:40:27,312 - __main__ - INFO -       📝 Text: Low retrieval, high support...
2025-05-31 07:40:27,313 - __main__ - INFO -    3. Rank 3: p2 | Final: 0.000 (Ret: 0.800, Sup: 0.000) | Triples: 0
2025-05-31 07:40:27,313 - __main__ - INFO -       📝 Text: High retrieval, no support...
2025-05-31 07:40:27,313 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:40:27,313 - __main__ - INFO -    no_support: 1 passages (33.3%)
2025-05-31 07:40:27,313 - __main__ - INFO -    low_support: 2 passages (66.7%)
2025-05-31 07:40:27,314 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:40:27,314 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:40:27,314 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:40:27,314 - __main__ - INFO -    ⬆️ Moved up: 1
2025-05-31 07:40:27,314 - __main__ - INFO -    ⬇️ Moved down: 1
2025-05-31 07:40:27,314 - __main__ - INFO -    ➡️ Unchanged: 1
2025-05-31 07:40:27,315 - __main__ - INFO -    📈 Max improvement: 1 positions
2025-05-31 07:40:27,315 - __main__ - INFO -    📉 Max decline: 1 positions
2025-05-31 07:40:27,315 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:40:27,315 - __main__ - INFO -    🏃 Passages/giây: 428.6
2025-05-31 07:40:27,315 - __main__ - INFO -    ⏱️ Avg time/passage: 0.002s
2025-05-31 07:40:27,316 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,316 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:40:27,317 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:40:27,317 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:40:27,317 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:40:27,317 - __main__ - INFO -    📊 Strategy: hybrid_balanced
2025-05-31 07:40:27,317 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:40:27,318 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:40:27,318 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:40:27,318 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,318 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:40:27,319 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,319 - __main__ - INFO - 📝 Query: 'test query'
2025-05-31 07:40:27,320 - __main__ - INFO - 📄 Raw passages: 3
2025-05-31 07:40:27,320 - __main__ - INFO - 🔗 Filtered triples: 2
2025-05-31 07:40:27,320 - __main__ - INFO - 🎯 Strategy: hybrid_balanced
2025-05-31 07:40:27,320 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:40:27,321 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,321 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 2 filtered triples...
2025-05-31 07:40:27,321 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:40:27,321 - __main__ - INFO -    📊 Relevant triples: 2/2
2025-05-31 07:40:27,321 - __main__ - INFO -    📄 Passages with support: 2
2025-05-31 07:40:27,322 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:40:27,322 - __main__ - INFO -       1. p1: 1 triples
2025-05-31 07:40:27,322 - __main__ - INFO -       2. p3: 1 triples
2025-05-31 07:40:27,322 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:40:27,323 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,323 - __main__ - INFO - 🧮 Đang tính scores cho 3 passages...
2025-05-31 07:40:27,323 - __main__ - INFO -    📊 Processed 3/3 passages
2025-05-31 07:40:27,323 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:40:27,323 - __main__ - INFO -    📊 Retrieval scores: min=0.350, max=0.850, avg=0.650
2025-05-31 07:40:27,324 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.620, avg=0.390
2025-05-31 07:40:27,324 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=2, high=0
2025-05-31 07:40:27,324 - __main__ - INFO - ✅ Hoàn thành tính scores cho 3 passages
2025-05-31 07:40:27,324 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:40:27,325 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,325 - __main__ - INFO - 🏆 Áp dụng ranking strategy: hybrid_balanced
2025-05-31 07:40:27,325 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=0.50, support=0.50
2025-05-31 07:40:27,325 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:40:27,326 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:40:27,326 - __main__ - INFO -    🏆 Top passage: p1 với score 0.810
2025-05-31 07:40:27,326 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:40:27,326 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,326 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:40:27,326 - __main__ - INFO -    📊 Limited output: 3 → 3 passages
2025-05-31 07:40:27,327 - __main__ - INFO - ✅ Final processing hoàn thành: 3 ranked passages
2025-05-31 07:40:27,327 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:40:27,327 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,327 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:40:27,327 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,328 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:40:27,328 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,328 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:40:27,328 - __main__ - INFO -    📝 Query: 'test query'
2025-05-31 07:40:27,328 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:40:27,329 - __main__ - INFO -    📄 Passages: 3 → 3
2025-05-31 07:40:27,329 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:40:27,329 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:40:27,329 - __main__ - INFO -    1. Rank 1: p1 | Final: 0.810 (Ret: 1.000, Sup: 0.620) | Triples: 1
2025-05-31 07:40:27,329 - __main__ - INFO -       📝 Text: High retrieval, high support...
2025-05-31 07:40:27,330 - __main__ - INFO -    2. Rank 2: p2 | Final: 0.320 (Ret: 0.800, Sup: 0.000) | Triples: 0
2025-05-31 07:40:27,330 - __main__ - INFO -       📝 Text: High retrieval, no support...
2025-05-31 07:40:27,330 - __main__ - INFO -    3. Rank 3: p3 | Final: 0.275 (Ret: 0.000, Sup: 0.550) | Triples: 1
2025-05-31 07:40:27,330 - __main__ - INFO -       📝 Text: Low retrieval, high support...
2025-05-31 07:40:27,330 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:40:27,330 - __main__ - INFO -    no_support: 1 passages (33.3%)
2025-05-31 07:40:27,331 - __main__ - INFO -    low_support: 2 passages (66.7%)
2025-05-31 07:40:27,331 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:40:27,331 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:40:27,331 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:40:27,331 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:40:27,331 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:40:27,331 - __main__ - INFO -    ➡️ Unchanged: 3
2025-05-31 07:40:27,332 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:40:27,332 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:40:27,332 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:40:27,332 - __main__ - INFO -    🏃 Passages/giây: 429.1
2025-05-31 07:40:27,332 - __main__ - INFO -    ⏱️ Avg time/passage: 0.002s
2025-05-31 07:40:27,332 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,334 - __main__ - INFO - 🚀 Quick ranking với strategy: hybrid_balanced
2025-05-31 07:40:27,334 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:40:27,334 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:40:27,335 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:40:27,335 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:40:27,335 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:40:27,335 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:40:27,336 - __main__ - INFO -    📊 Strategy: hybrid_balanced
2025-05-31 07:40:27,336 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:40:27,336 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:40:27,336 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:40:27,336 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,337 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:40:27,337 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,337 - __main__ - INFO - 📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:40:27,337 - __main__ - INFO - 📄 Raw passages: 4
2025-05-31 07:40:27,337 - __main__ - INFO - 🔗 Filtered triples: 4
2025-05-31 07:40:27,338 - __main__ - INFO - 🎯 Strategy: hybrid_balanced
2025-05-31 07:40:27,338 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:40:27,338 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,338 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 4 filtered triples...
2025-05-31 07:40:27,338 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:40:27,338 - __main__ - INFO -    📊 Relevant triples: 4/4
2025-05-31 07:40:27,339 - __main__ - INFO -    📄 Passages with support: 3
2025-05-31 07:40:27,339 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:40:27,339 - __main__ - INFO -       1. passage_001: 2 triples
2025-05-31 07:40:27,339 - __main__ - INFO -       2. passage_002: 1 triples
2025-05-31 07:40:27,339 - __main__ - INFO -       3. passage_003: 1 triples
2025-05-31 07:40:27,339 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:40:27,340 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,340 - __main__ - INFO - 🧮 Đang tính scores cho 4 passages...
2025-05-31 07:40:27,340 - __main__ - INFO -    📊 Processed 4/4 passages
2025-05-31 07:40:27,340 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:40:27,340 - __main__ - INFO -    📊 Retrieval scores: min=0.150, max=0.750, avg=0.537
2025-05-31 07:40:27,340 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.680, avg=0.427
2025-05-31 07:40:27,341 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=3, high=0
2025-05-31 07:40:27,341 - __main__ - INFO - ✅ Hoàn thành tính scores cho 4 passages
2025-05-31 07:40:27,341 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:40:27,341 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,341 - __main__ - INFO - 🏆 Áp dụng ranking strategy: hybrid_balanced
2025-05-31 07:40:27,342 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=0.50, support=0.50
2025-05-31 07:40:27,342 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:40:27,342 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:40:27,342 - __main__ - INFO -    🏆 Top passage: passage_001 với score 0.840
2025-05-31 07:40:27,342 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:40:27,342 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,342 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:40:27,342 - __main__ - INFO -    📊 Limited output: 4 → 4 passages
2025-05-31 07:40:27,344 - __main__ - INFO - ✅ Final processing hoàn thành: 4 ranked passages
2025-05-31 07:40:27,344 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:40:27,344 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,344 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:40:27,345 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,345 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:40:27,345 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,345 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:40:27,345 - __main__ - INFO -    📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:40:27,346 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:40:27,346 - __main__ - INFO -    📄 Passages: 4 → 4
2025-05-31 07:40:27,346 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:40:27,346 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:40:27,346 - __main__ - INFO -    1. Rank 1: passage_001 | Final: 0.840 (Ret: 1.000, Sup: 0.680) | Triples: 2
2025-05-31 07:40:27,346 - __main__ - INFO -       📝 Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:40:27,347 - __main__ - INFO -    2. Rank 2: passage_002 | Final: 0.768 (Ret: 0.917, Sup: 0.620) | Triples: 1
2025-05-31 07:40:27,347 - __main__ - INFO -       📝 Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:40:27,347 - __main__ - INFO -    3. Rank 3: passage_003 | Final: 0.538 (Ret: 0.667, Sup: 0.410) | Triples: 1
2025-05-31 07:40:27,347 - __main__ - INFO -       📝 Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:40:27,347 - __main__ - INFO -    4. Rank 4: passage_004 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-05-31 07:40:27,347 - __main__ - INFO -       📝 Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:40:27,348 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:40:27,348 - __main__ - INFO -    no_support: 1 passages (25.0%)
2025-05-31 07:40:27,348 - __main__ - INFO -    low_support: 3 passages (75.0%)
2025-05-31 07:40:27,348 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:40:27,348 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:40:27,348 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:40:27,348 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:40:27,349 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:40:27,349 - __main__ - INFO -    ➡️ Unchanged: 4
2025-05-31 07:40:27,349 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:40:27,349 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:40:27,349 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:40:27,349 - __main__ - INFO -    🏃 Passages/giây: 688.5
2025-05-31 07:40:27,350 - __main__ - INFO -    ⏱️ Avg time/passage: 0.001s
2025-05-31 07:40:27,350 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,351 - __main__ - INFO - 🚀 Quick ranking với strategy: hybrid_support_focused
2025-05-31 07:40:27,351 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:40:27,351 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:40:27,352 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:40:27,352 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:40:27,352 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:40:27,352 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:40:27,352 - __main__ - INFO -    📊 Strategy: hybrid_support_focused
2025-05-31 07:40:27,352 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:40:27,353 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:40:27,353 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:40:27,353 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,353 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:40:27,353 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,353 - __main__ - INFO - 📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:40:27,354 - __main__ - INFO - 📄 Raw passages: 4
2025-05-31 07:40:27,354 - __main__ - INFO - 🔗 Filtered triples: 4
2025-05-31 07:40:27,354 - __main__ - INFO - 🎯 Strategy: hybrid_support_focused
2025-05-31 07:40:27,354 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:40:27,355 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,355 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 4 filtered triples...
2025-05-31 07:40:27,355 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:40:27,355 - __main__ - INFO -    📊 Relevant triples: 4/4
2025-05-31 07:40:27,356 - __main__ - INFO -    📄 Passages with support: 3
2025-05-31 07:40:27,356 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:40:27,356 - __main__ - INFO -       1. passage_001: 2 triples
2025-05-31 07:40:27,356 - __main__ - INFO -       2. passage_002: 1 triples
2025-05-31 07:40:27,356 - __main__ - INFO -       3. passage_003: 1 triples
2025-05-31 07:40:27,357 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:40:27,357 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,357 - __main__ - INFO - 🧮 Đang tính scores cho 4 passages...
2025-05-31 07:40:27,357 - __main__ - INFO -    📊 Processed 4/4 passages
2025-05-31 07:40:27,358 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:40:27,358 - __main__ - INFO -    📊 Retrieval scores: min=0.150, max=0.750, avg=0.537
2025-05-31 07:40:27,358 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.680, avg=0.427
2025-05-31 07:40:27,358 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=3, high=0
2025-05-31 07:40:27,359 - __main__ - INFO - ✅ Hoàn thành tính scores cho 4 passages
2025-05-31 07:40:27,359 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:40:27,359 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,359 - __main__ - INFO - 🏆 Áp dụng ranking strategy: hybrid_support_focused
2025-05-31 07:40:27,360 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=0.30, support=0.70
2025-05-31 07:40:27,360 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:40:27,360 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:40:27,360 - __main__ - INFO -    🏆 Top passage: passage_001 với score 0.776
2025-05-31 07:40:27,360 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:40:27,361 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,361 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:40:27,361 - __main__ - INFO -    📊 Limited output: 4 → 4 passages
2025-05-31 07:40:27,362 - __main__ - INFO - ✅ Final processing hoàn thành: 4 ranked passages
2025-05-31 07:40:27,362 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:40:27,362 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,363 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:40:27,363 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,363 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:40:27,363 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,364 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:40:27,364 - __main__ - INFO -    📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:40:27,364 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:40:27,364 - __main__ - INFO -    📄 Passages: 4 → 4
2025-05-31 07:40:27,364 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:40:27,365 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:40:27,365 - __main__ - INFO -    1. Rank 1: passage_001 | Final: 0.776 (Ret: 1.000, Sup: 0.680) | Triples: 2
2025-05-31 07:40:27,365 - __main__ - INFO -       📝 Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:40:27,366 - __main__ - INFO -    2. Rank 2: passage_002 | Final: 0.709 (Ret: 0.917, Sup: 0.620) | Triples: 1
2025-05-31 07:40:27,366 - __main__ - INFO -       📝 Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:40:27,366 - __main__ - INFO -    3. Rank 3: passage_003 | Final: 0.487 (Ret: 0.667, Sup: 0.410) | Triples: 1
2025-05-31 07:40:27,366 - __main__ - INFO -       📝 Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:40:27,366 - __main__ - INFO -    4. Rank 4: passage_004 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-05-31 07:40:27,367 - __main__ - INFO -       📝 Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:40:27,367 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:40:27,367 - __main__ - INFO -    no_support: 1 passages (25.0%)
2025-05-31 07:40:27,367 - __main__ - INFO -    low_support: 3 passages (75.0%)
2025-05-31 07:40:27,367 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:40:27,368 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:40:27,368 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:40:27,368 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:40:27,368 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:40:27,369 - __main__ - INFO -    ➡️ Unchanged: 4
2025-05-31 07:40:27,369 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:40:27,369 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:40:27,369 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:40:27,370 - __main__ - INFO -    🏃 Passages/giây: 499.2
2025-05-31 07:40:27,370 - __main__ - INFO -    ⏱️ Avg time/passage: 0.002s
2025-05-31 07:40:27,370 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,372 - __main__ - INFO - 🚀 Quick ranking với strategy: retrieval_only
2025-05-31 07:40:27,372 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:40:27,372 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:40:27,372 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:40:27,372 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:40:27,373 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:40:27,373 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:40:27,373 - __main__ - INFO -    📊 Strategy: retrieval_only
2025-05-31 07:40:27,373 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:40:27,373 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:40:27,373 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:40:27,374 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,374 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:40:27,374 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,374 - __main__ - INFO - 📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:40:27,374 - __main__ - INFO - 📄 Raw passages: 4
2025-05-31 07:40:27,375 - __main__ - INFO - 🔗 Filtered triples: 4
2025-05-31 07:40:27,375 - __main__ - INFO - 🎯 Strategy: retrieval_only
2025-05-31 07:40:27,375 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:40:27,375 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,376 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 4 filtered triples...
2025-05-31 07:40:27,376 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:40:27,376 - __main__ - INFO -    📊 Relevant triples: 4/4
2025-05-31 07:40:27,376 - __main__ - INFO -    📄 Passages with support: 3
2025-05-31 07:40:27,376 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:40:27,376 - __main__ - INFO -       1. passage_001: 2 triples
2025-05-31 07:40:27,377 - __main__ - INFO -       2. passage_002: 1 triples
2025-05-31 07:40:27,377 - __main__ - INFO -       3. passage_003: 1 triples
2025-05-31 07:40:27,377 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:40:27,377 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,378 - __main__ - INFO - 🧮 Đang tính scores cho 4 passages...
2025-05-31 07:40:27,378 - __main__ - INFO -    📊 Processed 4/4 passages
2025-05-31 07:40:27,378 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:40:27,378 - __main__ - INFO -    📊 Retrieval scores: min=0.150, max=0.750, avg=0.537
2025-05-31 07:40:27,378 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.680, avg=0.427
2025-05-31 07:40:27,379 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=3, high=0
2025-05-31 07:40:27,379 - __main__ - INFO - ✅ Hoàn thành tính scores cho 4 passages
2025-05-31 07:40:27,379 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:40:27,380 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,380 - __main__ - INFO - 🏆 Áp dụng ranking strategy: retrieval_only
2025-05-31 07:40:27,380 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=1.00, support=0.00
2025-05-31 07:40:27,380 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:40:27,380 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:40:27,380 - __main__ - INFO -    🏆 Top passage: passage_001 với score 1.000
2025-05-31 07:40:27,382 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:40:27,382 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,382 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:40:27,382 - __main__ - INFO -    📊 Limited output: 4 → 4 passages
2025-05-31 07:40:27,382 - __main__ - INFO - ✅ Final processing hoàn thành: 4 ranked passages
2025-05-31 07:40:27,383 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:40:27,383 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,383 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:40:27,383 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,383 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:40:27,384 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,384 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:40:27,384 - __main__ - INFO -    📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:40:27,384 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:40:27,384 - __main__ - INFO -    📄 Passages: 4 → 4
2025-05-31 07:40:27,384 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:40:27,385 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:40:27,385 - __main__ - INFO -    1. Rank 1: passage_001 | Final: 1.000 (Ret: 1.000, Sup: 0.680) | Triples: 2
2025-05-31 07:40:27,385 - __main__ - INFO -       📝 Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:40:27,386 - __main__ - INFO -    2. Rank 2: passage_002 | Final: 0.917 (Ret: 0.917, Sup: 0.620) | Triples: 1
2025-05-31 07:40:27,386 - __main__ - INFO -       📝 Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:40:27,386 - __main__ - INFO -    3. Rank 3: passage_003 | Final: 0.667 (Ret: 0.667, Sup: 0.410) | Triples: 1
2025-05-31 07:40:27,386 - __main__ - INFO -       📝 Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:40:27,387 - __main__ - INFO -    4. Rank 4: passage_004 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-05-31 07:40:27,387 - __main__ - INFO -       📝 Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:40:27,387 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:40:27,387 - __main__ - INFO -    no_support: 1 passages (25.0%)
2025-05-31 07:40:27,388 - __main__ - INFO -    low_support: 3 passages (75.0%)
2025-05-31 07:40:27,388 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:40:27,388 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:40:27,388 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:40:27,388 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:40:27,389 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:40:27,389 - __main__ - INFO -    ➡️ Unchanged: 4
2025-05-31 07:40:27,389 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:40:27,389 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:40:27,389 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:40:27,389 - __main__ - INFO -    🏃 Passages/giây: 531.6
2025-05-31 07:40:27,390 - __main__ - INFO -    ⏱️ Avg time/passage: 0.002s
2025-05-31 07:40:27,390 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,391 - __main__ - INFO - 🚀 Quick ranking với strategy: adaptive
2025-05-31 07:40:27,391 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:40:27,391 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:40:27,392 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:40:27,392 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:40:27,392 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:40:27,392 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:40:27,392 - __main__ - INFO -    📊 Strategy: adaptive
2025-05-31 07:40:27,392 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:40:27,393 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:40:27,393 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:40:27,393 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,393 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:40:27,393 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,394 - __main__ - INFO - 📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:40:27,394 - __main__ - INFO - 📄 Raw passages: 4
2025-05-31 07:40:27,394 - __main__ - INFO - 🔗 Filtered triples: 4
2025-05-31 07:40:27,394 - __main__ - INFO - 🎯 Strategy: adaptive
2025-05-31 07:40:27,395 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:40:27,395 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,395 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 4 filtered triples...
2025-05-31 07:40:27,395 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:40:27,395 - __main__ - INFO -    📊 Relevant triples: 4/4
2025-05-31 07:40:27,396 - __main__ - INFO -    📄 Passages with support: 3
2025-05-31 07:40:27,396 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:40:27,396 - __main__ - INFO -       1. passage_001: 2 triples
2025-05-31 07:40:27,396 - __main__ - INFO -       2. passage_002: 1 triples
2025-05-31 07:40:27,396 - __main__ - INFO -       3. passage_003: 1 triples
2025-05-31 07:40:27,397 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:40:27,397 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,397 - __main__ - INFO - 🧮 Đang tính scores cho 4 passages...
2025-05-31 07:40:27,397 - __main__ - INFO -    📊 Processed 4/4 passages
2025-05-31 07:40:27,397 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:40:27,397 - __main__ - INFO -    📊 Retrieval scores: min=0.150, max=0.750, avg=0.537
2025-05-31 07:40:27,398 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.680, avg=0.427
2025-05-31 07:40:27,398 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=3, high=0
2025-05-31 07:40:27,398 - __main__ - INFO - ✅ Hoàn thành tính scores cho 4 passages
2025-05-31 07:40:27,398 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:40:27,398 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,399 - __main__ - INFO - 🏆 Áp dụng ranking strategy: adaptive
2025-05-31 07:40:27,399 - __main__ - INFO -    📊 Adaptive metrics:
2025-05-31 07:40:27,399 - __main__ - INFO -       📈 Retrieval variance: 0.055
2025-05-31 07:40:27,399 - __main__ - INFO -       🔗 Support variance: 0.071
2025-05-31 07:40:27,399 - __main__ - INFO -       📄 Support coverage: 75.00%
2025-05-31 07:40:27,400 - __main__ - INFO -    🎯 Balanced case → Moderate weights
2025-05-31 07:40:27,401 - __main__ - INFO -    🧠 Adaptive weights: retrieval=0.60, support=0.40
2025-05-31 07:40:27,401 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:40:27,401 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:40:27,401 - __main__ - INFO -    🏆 Top passage: passage_001 với score 0.872
2025-05-31 07:40:27,401 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:40:27,402 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,402 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:40:27,402 - __main__ - INFO -    📊 Limited output: 4 → 4 passages
2025-05-31 07:40:27,402 - __main__ - INFO - ✅ Final processing hoàn thành: 4 ranked passages
2025-05-31 07:40:27,402 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:40:27,403 - __main__ - INFO - ----------------------------------------
2025-05-31 07:40:27,403 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:40:27,403 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,403 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:40:27,404 - __main__ - INFO - ============================================================
2025-05-31 07:40:27,404 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:40:27,404 - __main__ - INFO -    📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:40:27,404 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:40:27,404 - __main__ - INFO -    📄 Passages: 4 → 4
2025-05-31 07:40:27,405 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:40:27,405 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:40:27,405 - __main__ - INFO -    1. Rank 1: passage_001 | Final: 0.872 (Ret: 1.000, Sup: 0.680) | Triples: 2
2025-05-31 07:40:27,405 - __main__ - INFO -       📝 Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:40:27,405 - __main__ - INFO -    2. Rank 2: passage_002 | Final: 0.798 (Ret: 0.917, Sup: 0.620) | Triples: 1
2025-05-31 07:40:27,406 - __main__ - INFO -       📝 Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:40:27,406 - __main__ - INFO -    3. Rank 3: passage_003 | Final: 0.564 (Ret: 0.667, Sup: 0.410) | Triples: 1
2025-05-31 07:40:27,406 - __main__ - INFO -       📝 Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:40:27,406 - __main__ - INFO -    4. Rank 4: passage_004 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-05-31 07:40:27,406 - __main__ - INFO -       📝 Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:40:27,407 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:40:27,407 - __main__ - INFO -    no_support: 1 passages (25.0%)
2025-05-31 07:40:27,407 - __main__ - INFO -    low_support: 3 passages (75.0%)
2025-05-31 07:40:27,407 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:40:27,407 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:40:27,407 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:40:27,408 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:40:27,408 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:40:27,408 - __main__ - INFO -    ➡️ Unchanged: 4
2025-05-31 07:40:27,408 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:40:27,408 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:40:27,409 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:40:27,409 - __main__ - INFO -    🏃 Passages/giây: 652.9
2025-05-31 07:40:27,409 - __main__ - INFO -    ⏱️ Avg time/passage: 0.002s
2025-05-31 07:40:27,409 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,481 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:43:58,481 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:43:58,482 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:43:58,482 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:43:58,483 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:43:58,483 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 1 filtered triples...
2025-05-31 07:43:58,483 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:43:58,483 - __main__ - INFO -    📊 Relevant triples: 1/1
2025-05-31 07:43:58,483 - __main__ - INFO -    📄 Passages with support: 1
2025-05-31 07:43:58,483 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:43:58,483 - __main__ - INFO -       1. test_passage_1: 1 triples
2025-05-31 07:43:58,485 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:43:58,485 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:43:58,485 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:43:58,486 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:43:58,486 - __main__ - INFO -    📊 Strategy: retrieval_only
2025-05-31 07:43:58,486 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:43:58,486 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:43:58,486 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:43:58,486 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,487 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:43:58,487 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,487 - __main__ - INFO - 📝 Query: 'test query'
2025-05-31 07:43:58,487 - __main__ - INFO - 📄 Raw passages: 3
2025-05-31 07:43:58,487 - __main__ - INFO - 🔗 Filtered triples: 2
2025-05-31 07:43:58,487 - __main__ - INFO - 🎯 Strategy: retrieval_only
2025-05-31 07:43:58,487 - __main__ - INFO - 
📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):
2025-05-31 07:43:58,488 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,488 - __main__ - INFO -    1. ID: p1
2025-05-31 07:43:58,488 - __main__ - INFO -       Text: High retrieval, high support...
2025-05-31 07:43:58,488 - __main__ - INFO -       Scores: BM25=0.900, Embed=0.800, Hybrid=0.850
2025-05-31 07:43:58,488 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,489 - __main__ - INFO -    2. ID: p2
2025-05-31 07:43:58,489 - __main__ - INFO -       Text: High retrieval, no support...
2025-05-31 07:43:58,489 - __main__ - INFO -       Scores: BM25=0.800, Embed=0.700, Hybrid=0.750
2025-05-31 07:43:58,489 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,490 - __main__ - INFO -    3. ID: p3
2025-05-31 07:43:58,490 - __main__ - INFO -       Text: Low retrieval, high support...
2025-05-31 07:43:58,490 - __main__ - INFO -       Scores: BM25=0.300, Embed=0.400, Hybrid=0.350
2025-05-31 07:43:58,490 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,491 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:43:58,491 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,491 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 2 filtered triples...
2025-05-31 07:43:58,491 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:43:58,492 - __main__ - INFO -    📊 Relevant triples: 2/2
2025-05-31 07:43:58,492 - __main__ - INFO -    📄 Passages with support: 2
2025-05-31 07:43:58,492 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:43:58,492 - __main__ - INFO -       1. p1: 1 triples
2025-05-31 07:43:58,492 - __main__ - INFO -       2. p3: 1 triples
2025-05-31 07:43:58,492 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:43:58,492 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,493 - __main__ - INFO - 🧮 Đang tính scores cho 3 passages...
2025-05-31 07:43:58,493 - __main__ - INFO -    📊 Processed 3/3 passages
2025-05-31 07:43:58,493 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:43:58,493 - __main__ - INFO -    📊 Retrieval scores: min=0.350, max=0.850, avg=0.650
2025-05-31 07:43:58,493 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.620, avg=0.390
2025-05-31 07:43:58,494 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=2, high=0
2025-05-31 07:43:58,494 - __main__ - INFO - ✅ Hoàn thành tính scores cho 3 passages
2025-05-31 07:43:58,494 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:43:58,495 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,495 - __main__ - INFO - 🏆 Áp dụng ranking strategy: retrieval_only
2025-05-31 07:43:58,495 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=1.00, support=0.00
2025-05-31 07:43:58,496 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:43:58,496 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:43:58,496 - __main__ - INFO -    🏆 Top passage: p1 với score 1.000
2025-05-31 07:43:58,496 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:43:58,497 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,497 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:43:58,497 - __main__ - INFO -    📊 Limited output: 3 → 3 passages
2025-05-31 07:43:58,498 - __main__ - INFO - ✅ Final processing hoàn thành: 3 ranked passages
2025-05-31 07:43:58,498 - __main__ - INFO - 
🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):
2025-05-31 07:43:58,498 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,498 - __main__ - INFO -    Giải thích thứ tự mới:
2025-05-31 07:43:58,499 - __main__ - INFO -    1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
2025-05-31 07:43:58,499 - __main__ - INFO -    2. Support score được tính từ số lượng và chất lượng của supporting triples
2025-05-31 07:43:58,499 - __main__ - INFO -    3. Passages có nhiều supporting triples sẽ được boost lên
2025-05-31 07:43:58,499 - __main__ - INFO -    4. Passages không có support sẽ bị penalty
2025-05-31 07:43:58,500 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,501 - __main__ - INFO -    Rank 1. ID: p1
2025-05-31 07:43:58,501 - __main__ - INFO -       Text: High retrieval, high support...
2025-05-31 07:43:58,501 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,501 - __main__ - INFO -          - Final score: 1.000
2025-05-31 07:43:58,502 - __main__ - INFO -          - Retrieval score: 1.000
2025-05-31 07:43:58,502 - __main__ - INFO -          - Support score: 0.620
2025-05-31 07:43:58,502 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,502 - __main__ - INFO -       Triple IDs: t1...
2025-05-31 07:43:58,503 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.9, 'embedding_score': 0.8, 'hybrid_score': 0.85, 'support_score': 0.6199999999999999, 'support_count': 1, 'normalized_retrieval': 1.0, 'alpha_retrieval': 1.0, 'alpha_support': 0.0, 'base_final_score': 1.0, 'final_score_after_modifiers': 1.0}
2025-05-31 07:43:58,503 - __main__ - INFO -    Rank 2. ID: p2
2025-05-31 07:43:58,503 - __main__ - INFO -       Text: High retrieval, no support...
2025-05-31 07:43:58,503 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,504 - __main__ - INFO -          - Final score: 0.640
2025-05-31 07:43:58,504 - __main__ - INFO -          - Retrieval score: 0.800
2025-05-31 07:43:58,504 - __main__ - INFO -          - Support score: 0.000
2025-05-31 07:43:58,504 - __main__ - INFO -       Supporting triples: 0
2025-05-31 07:43:58,505 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.8, 'embedding_score': 0.7, 'hybrid_score': 0.75, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.8, 'alpha_retrieval': 1.0, 'alpha_support': 0.0, 'base_final_score': 0.8, 'final_score_after_modifiers': 0.6400000000000001}
2025-05-31 07:43:58,505 - __main__ - INFO -    Rank 3. ID: p3
2025-05-31 07:43:58,505 - __main__ - INFO -       Text: Low retrieval, high support...
2025-05-31 07:43:58,506 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,506 - __main__ - INFO -          - Final score: 0.000
2025-05-31 07:43:58,506 - __main__ - INFO -          - Retrieval score: 0.000
2025-05-31 07:43:58,507 - __main__ - INFO -          - Support score: 0.550
2025-05-31 07:43:58,507 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,507 - __main__ - INFO -       Triple IDs: t2...
2025-05-31 07:43:58,507 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.3, 'embedding_score': 0.4, 'hybrid_score': 0.35, 'support_score': 0.5499999999999999, 'support_count': 1, 'normalized_retrieval': 0.0, 'alpha_retrieval': 1.0, 'alpha_support': 0.0, 'base_final_score': 0.0, 'final_score_after_modifiers': 0.0}
2025-05-31 07:43:58,508 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:43:58,508 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,508 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:43:58,508 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,508 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:43:58,509 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,509 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:43:58,509 - __main__ - INFO -    📝 Query: 'test query'
2025-05-31 07:43:58,509 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.02 giây
2025-05-31 07:43:58,509 - __main__ - INFO -    📄 Passages: 3 → 3
2025-05-31 07:43:58,509 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:43:58,509 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:43:58,510 - __main__ - INFO -    1. Rank 1: p1 | Final: 1.000 (Ret: 1.000, Sup: 0.620) | Triples: 1
2025-05-31 07:43:58,510 - __main__ - INFO -       📝 Text: High retrieval, high support...
2025-05-31 07:43:58,510 - __main__ - INFO -    2. Rank 2: p2 | Final: 0.640 (Ret: 0.800, Sup: 0.000) | Triples: 0
2025-05-31 07:43:58,510 - __main__ - INFO -       📝 Text: High retrieval, no support...
2025-05-31 07:43:58,511 - __main__ - INFO -    3. Rank 3: p3 | Final: 0.000 (Ret: 0.000, Sup: 0.550) | Triples: 1
2025-05-31 07:43:58,511 - __main__ - INFO -       📝 Text: Low retrieval, high support...
2025-05-31 07:43:58,511 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:43:58,511 - __main__ - INFO -    no_support: 1 passages (33.3%)
2025-05-31 07:43:58,511 - __main__ - INFO -    low_support: 2 passages (66.7%)
2025-05-31 07:43:58,511 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:43:58,512 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:43:58,512 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:43:58,512 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:43:58,512 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:43:58,512 - __main__ - INFO -    ➡️ Unchanged: 3
2025-05-31 07:43:58,513 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:43:58,513 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:43:58,513 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:43:58,513 - __main__ - INFO -    🏃 Passages/giây: 174.4
2025-05-31 07:43:58,513 - __main__ - INFO -    ⏱️ Avg time/passage: 0.006s
2025-05-31 07:43:58,514 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,514 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:43:58,515 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:43:58,515 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:43:58,515 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:43:58,515 - __main__ - INFO -    📊 Strategy: support_only
2025-05-31 07:43:58,515 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:43:58,516 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:43:58,516 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:43:58,516 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,516 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:43:58,516 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,516 - __main__ - INFO - 📝 Query: 'test query'
2025-05-31 07:43:58,517 - __main__ - INFO - 📄 Raw passages: 3
2025-05-31 07:43:58,517 - __main__ - INFO - 🔗 Filtered triples: 2
2025-05-31 07:43:58,517 - __main__ - INFO - 🎯 Strategy: support_only
2025-05-31 07:43:58,517 - __main__ - INFO - 
📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):
2025-05-31 07:43:58,517 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,517 - __main__ - INFO -    1. ID: p1
2025-05-31 07:43:58,518 - __main__ - INFO -       Text: High retrieval, high support...
2025-05-31 07:43:58,518 - __main__ - INFO -       Scores: BM25=0.900, Embed=0.800, Hybrid=0.850
2025-05-31 07:43:58,518 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,518 - __main__ - INFO -    2. ID: p2
2025-05-31 07:43:58,518 - __main__ - INFO -       Text: High retrieval, no support...
2025-05-31 07:43:58,518 - __main__ - INFO -       Scores: BM25=0.800, Embed=0.700, Hybrid=0.750
2025-05-31 07:43:58,518 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,519 - __main__ - INFO -    3. ID: p3
2025-05-31 07:43:58,519 - __main__ - INFO -       Text: Low retrieval, high support...
2025-05-31 07:43:58,519 - __main__ - INFO -       Scores: BM25=0.300, Embed=0.400, Hybrid=0.350
2025-05-31 07:43:58,519 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,519 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:43:58,519 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,520 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 2 filtered triples...
2025-05-31 07:43:58,520 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:43:58,520 - __main__ - INFO -    📊 Relevant triples: 2/2
2025-05-31 07:43:58,520 - __main__ - INFO -    📄 Passages with support: 2
2025-05-31 07:43:58,520 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:43:58,520 - __main__ - INFO -       1. p1: 1 triples
2025-05-31 07:43:58,521 - __main__ - INFO -       2. p3: 1 triples
2025-05-31 07:43:58,521 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:43:58,521 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,521 - __main__ - INFO - 🧮 Đang tính scores cho 3 passages...
2025-05-31 07:43:58,521 - __main__ - INFO -    📊 Processed 3/3 passages
2025-05-31 07:43:58,522 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:43:58,522 - __main__ - INFO -    📊 Retrieval scores: min=0.350, max=0.850, avg=0.650
2025-05-31 07:43:58,522 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.620, avg=0.390
2025-05-31 07:43:58,522 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=2, high=0
2025-05-31 07:43:58,522 - __main__ - INFO - ✅ Hoàn thành tính scores cho 3 passages
2025-05-31 07:43:58,523 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:43:58,523 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,523 - __main__ - INFO - 🏆 Áp dụng ranking strategy: support_only
2025-05-31 07:43:58,523 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=0.00, support=1.00
2025-05-31 07:43:58,523 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:43:58,524 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:43:58,524 - __main__ - INFO -    🏆 Top passage: p1 với score 0.620
2025-05-31 07:43:58,524 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:43:58,524 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,524 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:43:58,525 - __main__ - INFO -    📊 Limited output: 3 → 3 passages
2025-05-31 07:43:58,525 - __main__ - INFO - ✅ Final processing hoàn thành: 3 ranked passages
2025-05-31 07:43:58,525 - __main__ - INFO - 
🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):
2025-05-31 07:43:58,525 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,525 - __main__ - INFO -    Giải thích thứ tự mới:
2025-05-31 07:43:58,526 - __main__ - INFO -    1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
2025-05-31 07:43:58,526 - __main__ - INFO -    2. Support score được tính từ số lượng và chất lượng của supporting triples
2025-05-31 07:43:58,526 - __main__ - INFO -    3. Passages có nhiều supporting triples sẽ được boost lên
2025-05-31 07:43:58,526 - __main__ - INFO -    4. Passages không có support sẽ bị penalty
2025-05-31 07:43:58,526 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,527 - __main__ - INFO -    Rank 1. ID: p1
2025-05-31 07:43:58,527 - __main__ - INFO -       Text: High retrieval, high support...
2025-05-31 07:43:58,527 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,527 - __main__ - INFO -          - Final score: 0.620
2025-05-31 07:43:58,527 - __main__ - INFO -          - Retrieval score: 1.000
2025-05-31 07:43:58,527 - __main__ - INFO -          - Support score: 0.620
2025-05-31 07:43:58,527 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,528 - __main__ - INFO -       Triple IDs: t1...
2025-05-31 07:43:58,528 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.9, 'embedding_score': 0.8, 'hybrid_score': 0.85, 'support_score': 0.6199999999999999, 'support_count': 1, 'normalized_retrieval': 1.0, 'alpha_retrieval': 0.0, 'alpha_support': 1.0, 'base_final_score': 0.6199999999999999, 'final_score_after_modifiers': 0.6199999999999999}
2025-05-31 07:43:58,528 - __main__ - INFO -    Rank 2. ID: p3
2025-05-31 07:43:58,528 - __main__ - INFO -       Text: Low retrieval, high support...
2025-05-31 07:43:58,528 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,528 - __main__ - INFO -          - Final score: 0.550
2025-05-31 07:43:58,529 - __main__ - INFO -          - Retrieval score: 0.000
2025-05-31 07:43:58,529 - __main__ - INFO -          - Support score: 0.550
2025-05-31 07:43:58,529 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,529 - __main__ - INFO -       Triple IDs: t2...
2025-05-31 07:43:58,529 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.3, 'embedding_score': 0.4, 'hybrid_score': 0.35, 'support_score': 0.5499999999999999, 'support_count': 1, 'normalized_retrieval': 0.0, 'alpha_retrieval': 0.0, 'alpha_support': 1.0, 'base_final_score': 0.5499999999999999, 'final_score_after_modifiers': 0.5499999999999999}
2025-05-31 07:43:58,530 - __main__ - INFO -    Rank 3. ID: p2
2025-05-31 07:43:58,530 - __main__ - INFO -       Text: High retrieval, no support...
2025-05-31 07:43:58,530 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,530 - __main__ - INFO -          - Final score: 0.000
2025-05-31 07:43:58,530 - __main__ - INFO -          - Retrieval score: 0.800
2025-05-31 07:43:58,531 - __main__ - INFO -          - Support score: 0.000
2025-05-31 07:43:58,531 - __main__ - INFO -       Supporting triples: 0
2025-05-31 07:43:58,531 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.8, 'embedding_score': 0.7, 'hybrid_score': 0.75, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.8, 'alpha_retrieval': 0.0, 'alpha_support': 1.0, 'base_final_score': 0.0, 'final_score_after_modifiers': 0.0}
2025-05-31 07:43:58,531 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:43:58,532 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,532 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:43:58,532 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,532 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:43:58,532 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,532 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:43:58,533 - __main__ - INFO -    📝 Query: 'test query'
2025-05-31 07:43:58,533 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:43:58,533 - __main__ - INFO -    📄 Passages: 3 → 3
2025-05-31 07:43:58,533 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:43:58,533 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:43:58,533 - __main__ - INFO -    1. Rank 1: p1 | Final: 0.620 (Ret: 1.000, Sup: 0.620) | Triples: 1
2025-05-31 07:43:58,534 - __main__ - INFO -       📝 Text: High retrieval, high support...
2025-05-31 07:43:58,534 - __main__ - INFO -    2. Rank 2: p3 | Final: 0.550 (Ret: 0.000, Sup: 0.550) | Triples: 1
2025-05-31 07:43:58,534 - __main__ - INFO -       📝 Text: Low retrieval, high support...
2025-05-31 07:43:58,534 - __main__ - INFO -    3. Rank 3: p2 | Final: 0.000 (Ret: 0.800, Sup: 0.000) | Triples: 0
2025-05-31 07:43:58,534 - __main__ - INFO -       📝 Text: High retrieval, no support...
2025-05-31 07:43:58,535 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:43:58,535 - __main__ - INFO -    no_support: 1 passages (33.3%)
2025-05-31 07:43:58,535 - __main__ - INFO -    low_support: 2 passages (66.7%)
2025-05-31 07:43:58,535 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:43:58,535 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:43:58,536 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:43:58,536 - __main__ - INFO -    ⬆️ Moved up: 1
2025-05-31 07:43:58,536 - __main__ - INFO -    ⬇️ Moved down: 1
2025-05-31 07:43:58,536 - __main__ - INFO -    ➡️ Unchanged: 1
2025-05-31 07:43:58,536 - __main__ - INFO -    📈 Max improvement: 1 positions
2025-05-31 07:43:58,536 - __main__ - INFO -    📉 Max decline: 1 positions
2025-05-31 07:43:58,537 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:43:58,537 - __main__ - INFO -    🏃 Passages/giây: 245.3
2025-05-31 07:43:58,537 - __main__ - INFO -    ⏱️ Avg time/passage: 0.004s
2025-05-31 07:43:58,537 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,538 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:43:58,538 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:43:58,538 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:43:58,538 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:43:58,538 - __main__ - INFO -    📊 Strategy: hybrid_balanced
2025-05-31 07:43:58,539 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:43:58,539 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:43:58,539 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:43:58,540 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,540 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:43:58,540 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,540 - __main__ - INFO - 📝 Query: 'test query'
2025-05-31 07:43:58,541 - __main__ - INFO - 📄 Raw passages: 3
2025-05-31 07:43:58,541 - __main__ - INFO - 🔗 Filtered triples: 2
2025-05-31 07:43:58,541 - __main__ - INFO - 🎯 Strategy: hybrid_balanced
2025-05-31 07:43:58,541 - __main__ - INFO - 
📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):
2025-05-31 07:43:58,541 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,542 - __main__ - INFO -    1. ID: p1
2025-05-31 07:43:58,542 - __main__ - INFO -       Text: High retrieval, high support...
2025-05-31 07:43:58,542 - __main__ - INFO -       Scores: BM25=0.900, Embed=0.800, Hybrid=0.850
2025-05-31 07:43:58,542 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,542 - __main__ - INFO -    2. ID: p2
2025-05-31 07:43:58,542 - __main__ - INFO -       Text: High retrieval, no support...
2025-05-31 07:43:58,543 - __main__ - INFO -       Scores: BM25=0.800, Embed=0.700, Hybrid=0.750
2025-05-31 07:43:58,543 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,543 - __main__ - INFO -    3. ID: p3
2025-05-31 07:43:58,543 - __main__ - INFO -       Text: Low retrieval, high support...
2025-05-31 07:43:58,543 - __main__ - INFO -       Scores: BM25=0.300, Embed=0.400, Hybrid=0.350
2025-05-31 07:43:58,543 - __main__ - INFO -       Metadata: {}
2025-05-31 07:43:58,543 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:43:58,544 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,544 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 2 filtered triples...
2025-05-31 07:43:58,544 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:43:58,544 - __main__ - INFO -    📊 Relevant triples: 2/2
2025-05-31 07:43:58,544 - __main__ - INFO -    📄 Passages with support: 2
2025-05-31 07:43:58,545 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:43:58,545 - __main__ - INFO -       1. p1: 1 triples
2025-05-31 07:43:58,545 - __main__ - INFO -       2. p3: 1 triples
2025-05-31 07:43:58,546 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:43:58,546 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,546 - __main__ - INFO - 🧮 Đang tính scores cho 3 passages...
2025-05-31 07:43:58,546 - __main__ - INFO -    📊 Processed 3/3 passages
2025-05-31 07:43:58,547 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:43:58,547 - __main__ - INFO -    📊 Retrieval scores: min=0.350, max=0.850, avg=0.650
2025-05-31 07:43:58,547 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.620, avg=0.390
2025-05-31 07:43:58,547 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=2, high=0
2025-05-31 07:43:58,548 - __main__ - INFO - ✅ Hoàn thành tính scores cho 3 passages
2025-05-31 07:43:58,548 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:43:58,548 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,548 - __main__ - INFO - 🏆 Áp dụng ranking strategy: hybrid_balanced
2025-05-31 07:43:58,548 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=0.50, support=0.50
2025-05-31 07:43:58,548 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:43:58,549 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:43:58,549 - __main__ - INFO -    🏆 Top passage: p1 với score 0.810
2025-05-31 07:43:58,549 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:43:58,549 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,549 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:43:58,549 - __main__ - INFO -    📊 Limited output: 3 → 3 passages
2025-05-31 07:43:58,550 - __main__ - INFO - ✅ Final processing hoàn thành: 3 ranked passages
2025-05-31 07:43:58,550 - __main__ - INFO - 
🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):
2025-05-31 07:43:58,550 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,550 - __main__ - INFO -    Giải thích thứ tự mới:
2025-05-31 07:43:58,550 - __main__ - INFO -    1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
2025-05-31 07:43:58,551 - __main__ - INFO -    2. Support score được tính từ số lượng và chất lượng của supporting triples
2025-05-31 07:43:58,551 - __main__ - INFO -    3. Passages có nhiều supporting triples sẽ được boost lên
2025-05-31 07:43:58,551 - __main__ - INFO -    4. Passages không có support sẽ bị penalty
2025-05-31 07:43:58,551 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,551 - __main__ - INFO -    Rank 1. ID: p1
2025-05-31 07:43:58,551 - __main__ - INFO -       Text: High retrieval, high support...
2025-05-31 07:43:58,552 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,552 - __main__ - INFO -          - Final score: 0.810
2025-05-31 07:43:58,552 - __main__ - INFO -          - Retrieval score: 1.000
2025-05-31 07:43:58,552 - __main__ - INFO -          - Support score: 0.620
2025-05-31 07:43:58,552 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,552 - __main__ - INFO -       Triple IDs: t1...
2025-05-31 07:43:58,552 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.9, 'embedding_score': 0.8, 'hybrid_score': 0.85, 'support_score': 0.6199999999999999, 'support_count': 1, 'normalized_retrieval': 1.0, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.8099999999999999, 'final_score_after_modifiers': 0.8099999999999999}
2025-05-31 07:43:58,553 - __main__ - INFO -    Rank 2. ID: p2
2025-05-31 07:43:58,553 - __main__ - INFO -       Text: High retrieval, no support...
2025-05-31 07:43:58,553 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,553 - __main__ - INFO -          - Final score: 0.320
2025-05-31 07:43:58,553 - __main__ - INFO -          - Retrieval score: 0.800
2025-05-31 07:43:58,553 - __main__ - INFO -          - Support score: 0.000
2025-05-31 07:43:58,553 - __main__ - INFO -       Supporting triples: 0
2025-05-31 07:43:58,554 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.8, 'embedding_score': 0.7, 'hybrid_score': 0.75, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.8, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.4, 'final_score_after_modifiers': 0.32000000000000006}
2025-05-31 07:43:58,554 - __main__ - INFO -    Rank 3. ID: p3
2025-05-31 07:43:58,554 - __main__ - INFO -       Text: Low retrieval, high support...
2025-05-31 07:43:58,554 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,554 - __main__ - INFO -          - Final score: 0.275
2025-05-31 07:43:58,554 - __main__ - INFO -          - Retrieval score: 0.000
2025-05-31 07:43:58,555 - __main__ - INFO -          - Support score: 0.550
2025-05-31 07:43:58,555 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,555 - __main__ - INFO -       Triple IDs: t2...
2025-05-31 07:43:58,555 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.3, 'embedding_score': 0.4, 'hybrid_score': 0.35, 'support_score': 0.5499999999999999, 'support_count': 1, 'normalized_retrieval': 0.0, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.27499999999999997, 'final_score_after_modifiers': 0.27499999999999997}
2025-05-31 07:43:58,556 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:43:58,556 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,556 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:43:58,556 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,556 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:43:58,557 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,557 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:43:58,557 - __main__ - INFO -    📝 Query: 'test query'
2025-05-31 07:43:58,557 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:43:58,558 - __main__ - INFO -    📄 Passages: 3 → 3
2025-05-31 07:43:58,558 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:43:58,558 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:43:58,558 - __main__ - INFO -    1. Rank 1: p1 | Final: 0.810 (Ret: 1.000, Sup: 0.620) | Triples: 1
2025-05-31 07:43:58,558 - __main__ - INFO -       📝 Text: High retrieval, high support...
2025-05-31 07:43:58,559 - __main__ - INFO -    2. Rank 2: p2 | Final: 0.320 (Ret: 0.800, Sup: 0.000) | Triples: 0
2025-05-31 07:43:58,559 - __main__ - INFO -       📝 Text: High retrieval, no support...
2025-05-31 07:43:58,559 - __main__ - INFO -    3. Rank 3: p3 | Final: 0.275 (Ret: 0.000, Sup: 0.550) | Triples: 1
2025-05-31 07:43:58,559 - __main__ - INFO -       📝 Text: Low retrieval, high support...
2025-05-31 07:43:58,559 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:43:58,560 - __main__ - INFO -    no_support: 1 passages (33.3%)
2025-05-31 07:43:58,560 - __main__ - INFO -    low_support: 2 passages (66.7%)
2025-05-31 07:43:58,560 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:43:58,560 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:43:58,560 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:43:58,561 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:43:58,561 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:43:58,561 - __main__ - INFO -    ➡️ Unchanged: 3
2025-05-31 07:43:58,561 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:43:58,561 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:43:58,561 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:43:58,562 - __main__ - INFO -    🏃 Passages/giây: 230.7
2025-05-31 07:43:58,562 - __main__ - INFO -    ⏱️ Avg time/passage: 0.004s
2025-05-31 07:43:58,562 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,565 - __main__ - INFO - 🚀 Quick ranking với strategy: hybrid_balanced
2025-05-31 07:43:58,565 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:43:58,565 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:43:58,566 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:43:58,566 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:43:58,566 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:43:58,566 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:43:58,566 - __main__ - INFO -    📊 Strategy: hybrid_balanced
2025-05-31 07:43:58,566 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:43:58,567 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:43:58,567 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:43:58,567 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,567 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:43:58,567 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,567 - __main__ - INFO - 📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:43:58,568 - __main__ - INFO - 📄 Raw passages: 4
2025-05-31 07:43:58,568 - __main__ - INFO - 🔗 Filtered triples: 4
2025-05-31 07:43:58,568 - __main__ - INFO - 🎯 Strategy: hybrid_balanced
2025-05-31 07:43:58,568 - __main__ - INFO - 
📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):
2025-05-31 07:43:58,568 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,568 - __main__ - INFO -    1. ID: passage_002
2025-05-31 07:43:58,568 - __main__ - INFO -       Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,569 - __main__ - INFO -       Scores: BM25=0.600, Embed=0.800, Hybrid=0.700
2025-05-31 07:43:58,569 - __main__ - INFO -       Metadata: {'title': 'Vitamin C và miễn dịch', 'doc_id': 'health_002'}
2025-05-31 07:43:58,569 - __main__ - INFO -    2. ID: passage_001
2025-05-31 07:43:58,569 - __main__ - INFO -       Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,569 - __main__ - INFO -       Scores: BM25=0.800, Embed=0.700, Hybrid=0.750
2025-05-31 07:43:58,570 - __main__ - INFO -       Metadata: {'title': 'Lợi ích của táo', 'doc_id': 'health_001'}
2025-05-31 07:43:58,570 - __main__ - INFO -    3. ID: passage_003
2025-05-31 07:43:58,570 - __main__ - INFO -       Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,570 - __main__ - INFO -       Scores: BM25=0.500, Embed=0.600, Hybrid=0.550
2025-05-31 07:43:58,570 - __main__ - INFO -       Metadata: {'title': 'Chất xơ và tiêu hóa', 'doc_id': 'health_003'}
2025-05-31 07:43:58,571 - __main__ - INFO -    4. ID: passage_004
2025-05-31 07:43:58,571 - __main__ - INFO -       Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,571 - __main__ - INFO -       Scores: BM25=0.200, Embed=0.100, Hybrid=0.150
2025-05-31 07:43:58,571 - __main__ - INFO -       Metadata: {'title': 'Thời tiết', 'doc_id': 'weather_001'}
2025-05-31 07:43:58,571 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:43:58,571 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,572 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 4 filtered triples...
2025-05-31 07:43:58,572 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:43:58,572 - __main__ - INFO -    📊 Relevant triples: 4/4
2025-05-31 07:43:58,572 - __main__ - INFO -    📄 Passages with support: 3
2025-05-31 07:43:58,572 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:43:58,573 - __main__ - INFO -       1. passage_001: 2 triples
2025-05-31 07:43:58,573 - __main__ - INFO -       2. passage_002: 1 triples
2025-05-31 07:43:58,573 - __main__ - INFO -       3. passage_003: 1 triples
2025-05-31 07:43:58,573 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:43:58,573 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,574 - __main__ - INFO - 🧮 Đang tính scores cho 4 passages...
2025-05-31 07:43:58,574 - __main__ - INFO -    📊 Processed 4/4 passages
2025-05-31 07:43:58,574 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:43:58,574 - __main__ - INFO -    📊 Retrieval scores: min=0.150, max=0.750, avg=0.537
2025-05-31 07:43:58,574 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.680, avg=0.427
2025-05-31 07:43:58,575 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=3, high=0
2025-05-31 07:43:58,575 - __main__ - INFO - ✅ Hoàn thành tính scores cho 4 passages
2025-05-31 07:43:58,575 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:43:58,575 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,575 - __main__ - INFO - 🏆 Áp dụng ranking strategy: hybrid_balanced
2025-05-31 07:43:58,576 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=0.50, support=0.50
2025-05-31 07:43:58,576 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:43:58,576 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:43:58,577 - __main__ - INFO -    🏆 Top passage: passage_001 với score 0.840
2025-05-31 07:43:58,577 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:43:58,577 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,577 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:43:58,577 - __main__ - INFO -    📊 Limited output: 4 → 4 passages
2025-05-31 07:43:58,578 - __main__ - INFO - ✅ Final processing hoàn thành: 4 ranked passages
2025-05-31 07:43:58,578 - __main__ - INFO - 
🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):
2025-05-31 07:43:58,578 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,578 - __main__ - INFO -    Giải thích thứ tự mới:
2025-05-31 07:43:58,578 - __main__ - INFO -    1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
2025-05-31 07:43:58,578 - __main__ - INFO -    2. Support score được tính từ số lượng và chất lượng của supporting triples
2025-05-31 07:43:58,578 - __main__ - INFO -    3. Passages có nhiều supporting triples sẽ được boost lên
2025-05-31 07:43:58,579 - __main__ - INFO -    4. Passages không có support sẽ bị penalty
2025-05-31 07:43:58,579 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,579 - __main__ - INFO -    Rank 1. ID: passage_001
2025-05-31 07:43:58,579 - __main__ - INFO -       Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,579 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,579 - __main__ - INFO -          - Final score: 0.840
2025-05-31 07:43:58,579 - __main__ - INFO -          - Retrieval score: 1.000
2025-05-31 07:43:58,580 - __main__ - INFO -          - Support score: 0.680
2025-05-31 07:43:58,580 - __main__ - INFO -       Supporting triples: 2
2025-05-31 07:43:58,580 - __main__ - INFO -       Triple IDs: triple_001, triple_003...
2025-05-31 07:43:58,580 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.8, 'embedding_score': 0.7, 'hybrid_score': 0.75, 'support_score': 0.6799999999999999, 'support_count': 2, 'normalized_retrieval': 1.0, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.84, 'final_score_after_modifiers': 0.84}
2025-05-31 07:43:58,580 - __main__ - INFO -    Rank 2. ID: passage_002
2025-05-31 07:43:58,580 - __main__ - INFO -       Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,581 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,581 - __main__ - INFO -          - Final score: 0.768
2025-05-31 07:43:58,581 - __main__ - INFO -          - Retrieval score: 0.917
2025-05-31 07:43:58,581 - __main__ - INFO -          - Support score: 0.620
2025-05-31 07:43:58,581 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,581 - __main__ - INFO -       Triple IDs: triple_002...
2025-05-31 07:43:58,581 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.6, 'embedding_score': 0.8, 'hybrid_score': 0.7, 'support_score': 0.6199999999999999, 'support_count': 1, 'normalized_retrieval': 0.9166666666666666, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.7683333333333333, 'final_score_after_modifiers': 0.7683333333333333}
2025-05-31 07:43:58,582 - __main__ - INFO -    Rank 3. ID: passage_003
2025-05-31 07:43:58,582 - __main__ - INFO -       Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,582 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,582 - __main__ - INFO -          - Final score: 0.538
2025-05-31 07:43:58,582 - __main__ - INFO -          - Retrieval score: 0.667
2025-05-31 07:43:58,582 - __main__ - INFO -          - Support score: 0.410
2025-05-31 07:43:58,583 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,583 - __main__ - INFO -       Triple IDs: triple_004...
2025-05-31 07:43:58,583 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.5, 'embedding_score': 0.6, 'hybrid_score': 0.55, 'support_score': 0.41, 'support_count': 1, 'normalized_retrieval': 0.6666666666666667, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.5383333333333333, 'final_score_after_modifiers': 0.5383333333333333}
2025-05-31 07:43:58,583 - __main__ - INFO -    Rank 4. ID: passage_004
2025-05-31 07:43:58,583 - __main__ - INFO -       Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,583 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,584 - __main__ - INFO -          - Final score: 0.000
2025-05-31 07:43:58,584 - __main__ - INFO -          - Retrieval score: 0.000
2025-05-31 07:43:58,584 - __main__ - INFO -          - Support score: 0.000
2025-05-31 07:43:58,585 - __main__ - INFO -       Supporting triples: 0
2025-05-31 07:43:58,585 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.2, 'embedding_score': 0.1, 'hybrid_score': 0.15, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.0, 'alpha_retrieval': 0.5, 'alpha_support': 0.5, 'base_final_score': 0.0, 'final_score_after_modifiers': 0.0}
2025-05-31 07:43:58,585 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:43:58,585 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,585 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:43:58,586 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,586 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:43:58,586 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,586 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:43:58,586 - __main__ - INFO -    📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:43:58,586 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:43:58,587 - __main__ - INFO -    📄 Passages: 4 → 4
2025-05-31 07:43:58,587 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:43:58,587 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:43:58,587 - __main__ - INFO -    1. Rank 1: passage_001 | Final: 0.840 (Ret: 1.000, Sup: 0.680) | Triples: 2
2025-05-31 07:43:58,587 - __main__ - INFO -       📝 Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,587 - __main__ - INFO -    2. Rank 2: passage_002 | Final: 0.768 (Ret: 0.917, Sup: 0.620) | Triples: 1
2025-05-31 07:43:58,588 - __main__ - INFO -       📝 Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,588 - __main__ - INFO -    3. Rank 3: passage_003 | Final: 0.538 (Ret: 0.667, Sup: 0.410) | Triples: 1
2025-05-31 07:43:58,588 - __main__ - INFO -       📝 Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,588 - __main__ - INFO -    4. Rank 4: passage_004 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-05-31 07:43:58,589 - __main__ - INFO -       📝 Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,589 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:43:58,589 - __main__ - INFO -    no_support: 1 passages (25.0%)
2025-05-31 07:43:58,590 - __main__ - INFO -    low_support: 3 passages (75.0%)
2025-05-31 07:43:58,590 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:43:58,590 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:43:58,591 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:43:58,591 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:43:58,591 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:43:58,591 - __main__ - INFO -    ➡️ Unchanged: 4
2025-05-31 07:43:58,592 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:43:58,592 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:43:58,592 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:43:58,592 - __main__ - INFO -    🏃 Passages/giây: 292.2
2025-05-31 07:43:58,592 - __main__ - INFO -    ⏱️ Avg time/passage: 0.003s
2025-05-31 07:43:58,593 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,595 - __main__ - INFO - 🚀 Quick ranking với strategy: hybrid_support_focused
2025-05-31 07:43:58,595 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:43:58,596 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:43:58,596 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:43:58,597 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:43:58,597 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:43:58,597 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:43:58,598 - __main__ - INFO -    📊 Strategy: hybrid_support_focused
2025-05-31 07:43:58,598 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:43:58,598 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:43:58,598 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:43:58,598 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,598 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:43:58,599 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,599 - __main__ - INFO - 📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:43:58,599 - __main__ - INFO - 📄 Raw passages: 4
2025-05-31 07:43:58,599 - __main__ - INFO - 🔗 Filtered triples: 4
2025-05-31 07:43:58,599 - __main__ - INFO - 🎯 Strategy: hybrid_support_focused
2025-05-31 07:43:58,600 - __main__ - INFO - 
📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):
2025-05-31 07:43:58,600 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,600 - __main__ - INFO -    1. ID: passage_002
2025-05-31 07:43:58,600 - __main__ - INFO -       Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,600 - __main__ - INFO -       Scores: BM25=0.600, Embed=0.800, Hybrid=0.700
2025-05-31 07:43:58,601 - __main__ - INFO -       Metadata: {'title': 'Vitamin C và miễn dịch', 'doc_id': 'health_002'}
2025-05-31 07:43:58,601 - __main__ - INFO -    2. ID: passage_001
2025-05-31 07:43:58,601 - __main__ - INFO -       Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,601 - __main__ - INFO -       Scores: BM25=0.800, Embed=0.700, Hybrid=0.750
2025-05-31 07:43:58,602 - __main__ - INFO -       Metadata: {'title': 'Lợi ích của táo', 'doc_id': 'health_001'}
2025-05-31 07:43:58,602 - __main__ - INFO -    3. ID: passage_003
2025-05-31 07:43:58,602 - __main__ - INFO -       Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,602 - __main__ - INFO -       Scores: BM25=0.500, Embed=0.600, Hybrid=0.550
2025-05-31 07:43:58,602 - __main__ - INFO -       Metadata: {'title': 'Chất xơ và tiêu hóa', 'doc_id': 'health_003'}
2025-05-31 07:43:58,602 - __main__ - INFO -    4. ID: passage_004
2025-05-31 07:43:58,602 - __main__ - INFO -       Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,603 - __main__ - INFO -       Scores: BM25=0.200, Embed=0.100, Hybrid=0.150
2025-05-31 07:43:58,603 - __main__ - INFO -       Metadata: {'title': 'Thời tiết', 'doc_id': 'weather_001'}
2025-05-31 07:43:58,603 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:43:58,603 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,603 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 4 filtered triples...
2025-05-31 07:43:58,604 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:43:58,604 - __main__ - INFO -    📊 Relevant triples: 4/4
2025-05-31 07:43:58,604 - __main__ - INFO -    📄 Passages with support: 3
2025-05-31 07:43:58,604 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:43:58,604 - __main__ - INFO -       1. passage_001: 2 triples
2025-05-31 07:43:58,604 - __main__ - INFO -       2. passage_002: 1 triples
2025-05-31 07:43:58,605 - __main__ - INFO -       3. passage_003: 1 triples
2025-05-31 07:43:58,605 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:43:58,605 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,605 - __main__ - INFO - 🧮 Đang tính scores cho 4 passages...
2025-05-31 07:43:58,606 - __main__ - INFO -    📊 Processed 4/4 passages
2025-05-31 07:43:58,606 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:43:58,606 - __main__ - INFO -    📊 Retrieval scores: min=0.150, max=0.750, avg=0.537
2025-05-31 07:43:58,607 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.680, avg=0.427
2025-05-31 07:43:58,607 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=3, high=0
2025-05-31 07:43:58,607 - __main__ - INFO - ✅ Hoàn thành tính scores cho 4 passages
2025-05-31 07:43:58,607 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:43:58,607 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,608 - __main__ - INFO - 🏆 Áp dụng ranking strategy: hybrid_support_focused
2025-05-31 07:43:58,608 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=0.30, support=0.70
2025-05-31 07:43:58,608 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:43:58,608 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:43:58,608 - __main__ - INFO -    🏆 Top passage: passage_001 với score 0.776
2025-05-31 07:43:58,609 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:43:58,609 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,609 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:43:58,609 - __main__ - INFO -    📊 Limited output: 4 → 4 passages
2025-05-31 07:43:58,609 - __main__ - INFO - ✅ Final processing hoàn thành: 4 ranked passages
2025-05-31 07:43:58,610 - __main__ - INFO - 
🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):
2025-05-31 07:43:58,610 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,610 - __main__ - INFO -    Giải thích thứ tự mới:
2025-05-31 07:43:58,610 - __main__ - INFO -    1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
2025-05-31 07:43:58,610 - __main__ - INFO -    2. Support score được tính từ số lượng và chất lượng của supporting triples
2025-05-31 07:43:58,611 - __main__ - INFO -    3. Passages có nhiều supporting triples sẽ được boost lên
2025-05-31 07:43:58,611 - __main__ - INFO -    4. Passages không có support sẽ bị penalty
2025-05-31 07:43:58,611 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,611 - __main__ - INFO -    Rank 1. ID: passage_001
2025-05-31 07:43:58,611 - __main__ - INFO -       Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,611 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,612 - __main__ - INFO -          - Final score: 0.776
2025-05-31 07:43:58,612 - __main__ - INFO -          - Retrieval score: 1.000
2025-05-31 07:43:58,612 - __main__ - INFO -          - Support score: 0.680
2025-05-31 07:43:58,612 - __main__ - INFO -       Supporting triples: 2
2025-05-31 07:43:58,612 - __main__ - INFO -       Triple IDs: triple_001, triple_003...
2025-05-31 07:43:58,612 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.8, 'embedding_score': 0.7, 'hybrid_score': 0.75, 'support_score': 0.6799999999999999, 'support_count': 2, 'normalized_retrieval': 1.0, 'alpha_retrieval': 0.3, 'alpha_support': 0.7, 'base_final_score': 0.7759999999999999, 'final_score_after_modifiers': 0.7759999999999999}
2025-05-31 07:43:58,613 - __main__ - INFO -    Rank 2. ID: passage_002
2025-05-31 07:43:58,613 - __main__ - INFO -       Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,613 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,613 - __main__ - INFO -          - Final score: 0.709
2025-05-31 07:43:58,613 - __main__ - INFO -          - Retrieval score: 0.917
2025-05-31 07:43:58,614 - __main__ - INFO -          - Support score: 0.620
2025-05-31 07:43:58,614 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,614 - __main__ - INFO -       Triple IDs: triple_002...
2025-05-31 07:43:58,614 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.6, 'embedding_score': 0.8, 'hybrid_score': 0.7, 'support_score': 0.6199999999999999, 'support_count': 1, 'normalized_retrieval': 0.9166666666666666, 'alpha_retrieval': 0.3, 'alpha_support': 0.7, 'base_final_score': 0.7089999999999999, 'final_score_after_modifiers': 0.7089999999999999}
2025-05-31 07:43:58,614 - __main__ - INFO -    Rank 3. ID: passage_003
2025-05-31 07:43:58,614 - __main__ - INFO -       Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,615 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,615 - __main__ - INFO -          - Final score: 0.487
2025-05-31 07:43:58,615 - __main__ - INFO -          - Retrieval score: 0.667
2025-05-31 07:43:58,615 - __main__ - INFO -          - Support score: 0.410
2025-05-31 07:43:58,615 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,615 - __main__ - INFO -       Triple IDs: triple_004...
2025-05-31 07:43:58,615 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.5, 'embedding_score': 0.6, 'hybrid_score': 0.55, 'support_score': 0.41, 'support_count': 1, 'normalized_retrieval': 0.6666666666666667, 'alpha_retrieval': 0.3, 'alpha_support': 0.7, 'base_final_score': 0.487, 'final_score_after_modifiers': 0.487}
2025-05-31 07:43:58,616 - __main__ - INFO -    Rank 4. ID: passage_004
2025-05-31 07:43:58,616 - __main__ - INFO -       Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,616 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,616 - __main__ - INFO -          - Final score: 0.000
2025-05-31 07:43:58,616 - __main__ - INFO -          - Retrieval score: 0.000
2025-05-31 07:43:58,616 - __main__ - INFO -          - Support score: 0.000
2025-05-31 07:43:58,617 - __main__ - INFO -       Supporting triples: 0
2025-05-31 07:43:58,617 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.2, 'embedding_score': 0.1, 'hybrid_score': 0.15, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.0, 'alpha_retrieval': 0.3, 'alpha_support': 0.7, 'base_final_score': 0.0, 'final_score_after_modifiers': 0.0}
2025-05-31 07:43:58,617 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:43:58,617 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,617 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:43:58,617 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,618 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:43:58,618 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,618 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:43:58,618 - __main__ - INFO -    📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:43:58,618 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.01 giây
2025-05-31 07:43:58,618 - __main__ - INFO -    📄 Passages: 4 → 4
2025-05-31 07:43:58,619 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:43:58,619 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:43:58,619 - __main__ - INFO -    1. Rank 1: passage_001 | Final: 0.776 (Ret: 1.000, Sup: 0.680) | Triples: 2
2025-05-31 07:43:58,619 - __main__ - INFO -       📝 Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,619 - __main__ - INFO -    2. Rank 2: passage_002 | Final: 0.709 (Ret: 0.917, Sup: 0.620) | Triples: 1
2025-05-31 07:43:58,620 - __main__ - INFO -       📝 Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,621 - __main__ - INFO -    3. Rank 3: passage_003 | Final: 0.487 (Ret: 0.667, Sup: 0.410) | Triples: 1
2025-05-31 07:43:58,621 - __main__ - INFO -       📝 Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,621 - __main__ - INFO -    4. Rank 4: passage_004 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-05-31 07:43:58,621 - __main__ - INFO -       📝 Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,622 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:43:58,622 - __main__ - INFO -    no_support: 1 passages (25.0%)
2025-05-31 07:43:58,622 - __main__ - INFO -    low_support: 3 passages (75.0%)
2025-05-31 07:43:58,623 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:43:58,623 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:43:58,623 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:43:58,624 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:43:58,624 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:43:58,624 - __main__ - INFO -    ➡️ Unchanged: 4
2025-05-31 07:43:58,624 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:43:58,624 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:43:58,625 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:43:58,625 - __main__ - INFO -    🏃 Passages/giây: 275.6
2025-05-31 07:43:58,625 - __main__ - INFO -    ⏱️ Avg time/passage: 0.004s
2025-05-31 07:43:58,625 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,627 - __main__ - INFO - 🚀 Quick ranking với strategy: retrieval_only
2025-05-31 07:43:58,628 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:43:58,628 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:43:58,628 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:43:58,629 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:43:58,629 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:43:58,630 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:43:58,630 - __main__ - INFO -    📊 Strategy: retrieval_only
2025-05-31 07:43:58,630 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:43:58,631 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:43:58,631 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:43:58,631 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,632 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:43:58,632 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,632 - __main__ - INFO - 📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:43:58,633 - __main__ - INFO - 📄 Raw passages: 4
2025-05-31 07:43:58,633 - __main__ - INFO - 🔗 Filtered triples: 4
2025-05-31 07:43:58,633 - __main__ - INFO - 🎯 Strategy: retrieval_only
2025-05-31 07:43:58,633 - __main__ - INFO - 
📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):
2025-05-31 07:43:58,633 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,635 - __main__ - INFO -    1. ID: passage_002
2025-05-31 07:43:58,635 - __main__ - INFO -       Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,635 - __main__ - INFO -       Scores: BM25=0.600, Embed=0.800, Hybrid=0.700
2025-05-31 07:43:58,636 - __main__ - INFO -       Metadata: {'title': 'Vitamin C và miễn dịch', 'doc_id': 'health_002'}
2025-05-31 07:43:58,636 - __main__ - INFO -    2. ID: passage_001
2025-05-31 07:43:58,637 - __main__ - INFO -       Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,637 - __main__ - INFO -       Scores: BM25=0.800, Embed=0.700, Hybrid=0.750
2025-05-31 07:43:58,637 - __main__ - INFO -       Metadata: {'title': 'Lợi ích của táo', 'doc_id': 'health_001'}
2025-05-31 07:43:58,637 - __main__ - INFO -    3. ID: passage_003
2025-05-31 07:43:58,637 - __main__ - INFO -       Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,638 - __main__ - INFO -       Scores: BM25=0.500, Embed=0.600, Hybrid=0.550
2025-05-31 07:43:58,638 - __main__ - INFO -       Metadata: {'title': 'Chất xơ và tiêu hóa', 'doc_id': 'health_003'}
2025-05-31 07:43:58,638 - __main__ - INFO -    4. ID: passage_004
2025-05-31 07:43:58,638 - __main__ - INFO -       Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,639 - __main__ - INFO -       Scores: BM25=0.200, Embed=0.100, Hybrid=0.150
2025-05-31 07:43:58,639 - __main__ - INFO -       Metadata: {'title': 'Thời tiết', 'doc_id': 'weather_001'}
2025-05-31 07:43:58,639 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:43:58,639 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,639 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 4 filtered triples...
2025-05-31 07:43:58,640 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:43:58,640 - __main__ - INFO -    📊 Relevant triples: 4/4
2025-05-31 07:43:58,640 - __main__ - INFO -    📄 Passages with support: 3
2025-05-31 07:43:58,641 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:43:58,641 - __main__ - INFO -       1. passage_001: 2 triples
2025-05-31 07:43:58,641 - __main__ - INFO -       2. passage_002: 1 triples
2025-05-31 07:43:58,641 - __main__ - INFO -       3. passage_003: 1 triples
2025-05-31 07:43:58,642 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:43:58,642 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,642 - __main__ - INFO - 🧮 Đang tính scores cho 4 passages...
2025-05-31 07:43:58,642 - __main__ - INFO -    📊 Processed 4/4 passages
2025-05-31 07:43:58,642 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:43:58,643 - __main__ - INFO -    📊 Retrieval scores: min=0.150, max=0.750, avg=0.537
2025-05-31 07:43:58,643 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.680, avg=0.427
2025-05-31 07:43:58,643 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=3, high=0
2025-05-31 07:43:58,643 - __main__ - INFO - ✅ Hoàn thành tính scores cho 4 passages
2025-05-31 07:43:58,644 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:43:58,644 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,644 - __main__ - INFO - 🏆 Áp dụng ranking strategy: retrieval_only
2025-05-31 07:43:58,644 - __main__ - INFO -    ⚖️ Fixed weights: retrieval=1.00, support=0.00
2025-05-31 07:43:58,645 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:43:58,645 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:43:58,645 - __main__ - INFO -    🏆 Top passage: passage_001 với score 1.000
2025-05-31 07:43:58,645 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:43:58,646 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,646 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:43:58,646 - __main__ - INFO -    📊 Limited output: 4 → 4 passages
2025-05-31 07:43:58,647 - __main__ - INFO - ✅ Final processing hoàn thành: 4 ranked passages
2025-05-31 07:43:58,647 - __main__ - INFO - 
🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):
2025-05-31 07:43:58,647 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,647 - __main__ - INFO -    Giải thích thứ tự mới:
2025-05-31 07:43:58,647 - __main__ - INFO -    1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
2025-05-31 07:43:58,648 - __main__ - INFO -    2. Support score được tính từ số lượng và chất lượng của supporting triples
2025-05-31 07:43:58,648 - __main__ - INFO -    3. Passages có nhiều supporting triples sẽ được boost lên
2025-05-31 07:43:58,648 - __main__ - INFO -    4. Passages không có support sẽ bị penalty
2025-05-31 07:43:58,648 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,649 - __main__ - INFO -    Rank 1. ID: passage_001
2025-05-31 07:43:58,649 - __main__ - INFO -       Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,649 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,649 - __main__ - INFO -          - Final score: 1.000
2025-05-31 07:43:58,649 - __main__ - INFO -          - Retrieval score: 1.000
2025-05-31 07:43:58,649 - __main__ - INFO -          - Support score: 0.680
2025-05-31 07:43:58,650 - __main__ - INFO -       Supporting triples: 2
2025-05-31 07:43:58,650 - __main__ - INFO -       Triple IDs: triple_001, triple_003...
2025-05-31 07:43:58,650 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.8, 'embedding_score': 0.7, 'hybrid_score': 0.75, 'support_score': 0.6799999999999999, 'support_count': 2, 'normalized_retrieval': 1.0, 'alpha_retrieval': 1.0, 'alpha_support': 0.0, 'base_final_score': 1.0, 'final_score_after_modifiers': 1.0}
2025-05-31 07:43:58,650 - __main__ - INFO -    Rank 2. ID: passage_002
2025-05-31 07:43:58,651 - __main__ - INFO -       Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,651 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,651 - __main__ - INFO -          - Final score: 0.917
2025-05-31 07:43:58,651 - __main__ - INFO -          - Retrieval score: 0.917
2025-05-31 07:43:58,652 - __main__ - INFO -          - Support score: 0.620
2025-05-31 07:43:58,652 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,652 - __main__ - INFO -       Triple IDs: triple_002...
2025-05-31 07:43:58,652 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.6, 'embedding_score': 0.8, 'hybrid_score': 0.7, 'support_score': 0.6199999999999999, 'support_count': 1, 'normalized_retrieval': 0.9166666666666666, 'alpha_retrieval': 1.0, 'alpha_support': 0.0, 'base_final_score': 0.9166666666666666, 'final_score_after_modifiers': 0.9166666666666666}
2025-05-31 07:43:58,653 - __main__ - INFO -    Rank 3. ID: passage_003
2025-05-31 07:43:58,653 - __main__ - INFO -       Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,653 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,653 - __main__ - INFO -          - Final score: 0.667
2025-05-31 07:43:58,654 - __main__ - INFO -          - Retrieval score: 0.667
2025-05-31 07:43:58,654 - __main__ - INFO -          - Support score: 0.410
2025-05-31 07:43:58,654 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,655 - __main__ - INFO -       Triple IDs: triple_004...
2025-05-31 07:43:58,655 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.5, 'embedding_score': 0.6, 'hybrid_score': 0.55, 'support_score': 0.41, 'support_count': 1, 'normalized_retrieval': 0.6666666666666667, 'alpha_retrieval': 1.0, 'alpha_support': 0.0, 'base_final_score': 0.6666666666666667, 'final_score_after_modifiers': 0.6666666666666667}
2025-05-31 07:43:58,655 - __main__ - INFO -    Rank 4. ID: passage_004
2025-05-31 07:43:58,655 - __main__ - INFO -       Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,656 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,656 - __main__ - INFO -          - Final score: 0.000
2025-05-31 07:43:58,656 - __main__ - INFO -          - Retrieval score: 0.000
2025-05-31 07:43:58,656 - __main__ - INFO -          - Support score: 0.000
2025-05-31 07:43:58,656 - __main__ - INFO -       Supporting triples: 0
2025-05-31 07:43:58,657 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.2, 'embedding_score': 0.1, 'hybrid_score': 0.15, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.0, 'alpha_retrieval': 1.0, 'alpha_support': 0.0, 'base_final_score': 0.0, 'final_score_after_modifiers': 0.0}
2025-05-31 07:43:58,657 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:43:58,657 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,657 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:43:58,658 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,658 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:43:58,658 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,658 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:43:58,658 - __main__ - INFO -    📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:43:58,658 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.02 giây
2025-05-31 07:43:58,659 - __main__ - INFO -    📄 Passages: 4 → 4
2025-05-31 07:43:58,659 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:43:58,659 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:43:58,659 - __main__ - INFO -    1. Rank 1: passage_001 | Final: 1.000 (Ret: 1.000, Sup: 0.680) | Triples: 2
2025-05-31 07:43:58,659 - __main__ - INFO -       📝 Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,659 - __main__ - INFO -    2. Rank 2: passage_002 | Final: 0.917 (Ret: 0.917, Sup: 0.620) | Triples: 1
2025-05-31 07:43:58,660 - __main__ - INFO -       📝 Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,660 - __main__ - INFO -    3. Rank 3: passage_003 | Final: 0.667 (Ret: 0.667, Sup: 0.410) | Triples: 1
2025-05-31 07:43:58,660 - __main__ - INFO -       📝 Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,660 - __main__ - INFO -    4. Rank 4: passage_004 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-05-31 07:43:58,661 - __main__ - INFO -       📝 Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,661 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:43:58,661 - __main__ - INFO -    no_support: 1 passages (25.0%)
2025-05-31 07:43:58,661 - __main__ - INFO -    low_support: 3 passages (75.0%)
2025-05-31 07:43:58,661 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:43:58,662 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:43:58,662 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:43:58,662 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:43:58,662 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:43:58,662 - __main__ - INFO -    ➡️ Unchanged: 4
2025-05-31 07:43:58,663 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:43:58,663 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:43:58,663 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:43:58,663 - __main__ - INFO -    🏃 Passages/giây: 219.3
2025-05-31 07:43:58,663 - __main__ - INFO -    ⏱️ Avg time/passage: 0.005s
2025-05-31 07:43:58,664 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,665 - __main__ - INFO - 🚀 Quick ranking với strategy: adaptive
2025-05-31 07:43:58,665 - __main__ - INFO - ⚙️ Tạo default PassageRankerConfig...
2025-05-31 07:43:58,665 - __main__ - INFO - ✅ Default ranking config đã được tạo
2025-05-31 07:43:58,666 - __main__ - INFO - 📊 Khởi tạo SupportScoreCalculator...
2025-05-31 07:43:58,666 - __main__ - INFO -    🧮 Method: weighted_relevance
2025-05-31 07:43:58,666 - __main__ - INFO -    🎯 Relevance threshold: 0.3
2025-05-31 07:43:58,666 - __main__ - INFO - 🏆 Khởi tạo PassageRanker...
2025-05-31 07:43:58,666 - __main__ - INFO -    📊 Strategy: adaptive
2025-05-31 07:43:58,666 - __main__ - INFO -    🧮 Support method: weighted_relevance
2025-05-31 07:43:58,667 - __main__ - INFO -    📝 Max output: 10
2025-05-31 07:43:58,667 - __main__ - INFO -    ⚖️ Score normalization: Bật
2025-05-31 07:43:58,667 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,667 - __main__ - INFO - 🏆 BẮT ĐẦU PASSAGE RANKING
2025-05-31 07:43:58,667 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,667 - __main__ - INFO - 📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:43:58,667 - __main__ - INFO - 📄 Raw passages: 4
2025-05-31 07:43:58,668 - __main__ - INFO - 🔗 Filtered triples: 4
2025-05-31 07:43:58,668 - __main__ - INFO - 🎯 Strategy: adaptive
2025-05-31 07:43:58,668 - __main__ - INFO - 
📄 RAW PASSAGES (SẮP XẾP THEO EMBEDDING SCORE):
2025-05-31 07:43:58,668 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,668 - __main__ - INFO -    1. ID: passage_002
2025-05-31 07:43:58,668 - __main__ - INFO -       Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,669 - __main__ - INFO -       Scores: BM25=0.600, Embed=0.800, Hybrid=0.700
2025-05-31 07:43:58,669 - __main__ - INFO -       Metadata: {'title': 'Vitamin C và miễn dịch', 'doc_id': 'health_002'}
2025-05-31 07:43:58,669 - __main__ - INFO -    2. ID: passage_001
2025-05-31 07:43:58,669 - __main__ - INFO -       Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,669 - __main__ - INFO -       Scores: BM25=0.800, Embed=0.700, Hybrid=0.750
2025-05-31 07:43:58,670 - __main__ - INFO -       Metadata: {'title': 'Lợi ích của táo', 'doc_id': 'health_001'}
2025-05-31 07:43:58,670 - __main__ - INFO -    3. ID: passage_003
2025-05-31 07:43:58,670 - __main__ - INFO -       Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,670 - __main__ - INFO -       Scores: BM25=0.500, Embed=0.600, Hybrid=0.550
2025-05-31 07:43:58,670 - __main__ - INFO -       Metadata: {'title': 'Chất xơ và tiêu hóa', 'doc_id': 'health_003'}
2025-05-31 07:43:58,671 - __main__ - INFO -    4. ID: passage_004
2025-05-31 07:43:58,671 - __main__ - INFO -       Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,671 - __main__ - INFO -       Scores: BM25=0.200, Embed=0.100, Hybrid=0.150
2025-05-31 07:43:58,671 - __main__ - INFO -       Metadata: {'title': 'Thời tiết', 'doc_id': 'weather_001'}
2025-05-31 07:43:58,672 - __main__ - INFO - 
📊 BƯỚC 1: XÂY DỰNG SUPPORT MAPPING
2025-05-31 07:43:58,672 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,672 - __main__ - INFO - 🔗 Đang xây dựng support mapping cho 4 filtered triples...
2025-05-31 07:43:58,672 - __main__ - INFO - ✅ Support mapping completed:
2025-05-31 07:43:58,673 - __main__ - INFO -    📊 Relevant triples: 4/4
2025-05-31 07:43:58,673 - __main__ - INFO -    📄 Passages with support: 3
2025-05-31 07:43:58,673 - __main__ - INFO -    🏆 Top supported passages:
2025-05-31 07:43:58,673 - __main__ - INFO -       1. passage_001: 2 triples
2025-05-31 07:43:58,673 - __main__ - INFO -       2. passage_002: 1 triples
2025-05-31 07:43:58,674 - __main__ - INFO -       3. passage_003: 1 triples
2025-05-31 07:43:58,674 - __main__ - INFO - 
🧮 BƯỚC 2: TÍNH TOÁN SCORES
2025-05-31 07:43:58,674 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,674 - __main__ - INFO - 🧮 Đang tính scores cho 4 passages...
2025-05-31 07:43:58,675 - __main__ - INFO -    📊 Processed 4/4 passages
2025-05-31 07:43:58,675 - __main__ - INFO - 📈 Score distributions:
2025-05-31 07:43:58,675 - __main__ - INFO -    📊 Retrieval scores: min=0.150, max=0.750, avg=0.537
2025-05-31 07:43:58,675 - __main__ - INFO -    🔗 Support scores: min=0.000, max=0.680, avg=0.427
2025-05-31 07:43:58,675 - __main__ - INFO -    📄 Support levels: no=1, low=0, medium=3, high=0
2025-05-31 07:43:58,676 - __main__ - INFO - ✅ Hoàn thành tính scores cho 4 passages
2025-05-31 07:43:58,676 - __main__ - INFO - 
🏆 BƯỚC 3: ÁP DỤNG RANKING STRATEGY
2025-05-31 07:43:58,676 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,676 - __main__ - INFO - 🏆 Áp dụng ranking strategy: adaptive
2025-05-31 07:43:58,676 - __main__ - INFO -    📊 Adaptive metrics:
2025-05-31 07:43:58,677 - __main__ - INFO -       📈 Retrieval variance: 0.055
2025-05-31 07:43:58,677 - __main__ - INFO -       🔗 Support variance: 0.071
2025-05-31 07:43:58,677 - __main__ - INFO -       📄 Support coverage: 75.00%
2025-05-31 07:43:58,677 - __main__ - INFO -    🎯 Balanced case → Moderate weights
2025-05-31 07:43:58,677 - __main__ - INFO -    🧠 Adaptive weights: retrieval=0.60, support=0.40
2025-05-31 07:43:58,677 - __main__ - INFO -    📊 Scores đã được normalized
2025-05-31 07:43:58,678 - __main__ - INFO - ✅ Final scores calculated và sorted
2025-05-31 07:43:58,678 - __main__ - INFO -    🏆 Top passage: passage_001 với score 0.872
2025-05-31 07:43:58,678 - __main__ - INFO - 
🔧 BƯỚC 4: XỬ LÝ CUỐI CÙNG
2025-05-31 07:43:58,678 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,678 - __main__ - INFO - 🔧 Áp dụng final processing...
2025-05-31 07:43:58,679 - __main__ - INFO -    📊 Limited output: 4 → 4 passages
2025-05-31 07:43:58,679 - __main__ - INFO - ✅ Final processing hoàn thành: 4 ranked passages
2025-05-31 07:43:58,679 - __main__ - INFO - 
🏆 FINAL RANKED PASSAGES (SAU KHI TÍNH SUPPORT SCORE):
2025-05-31 07:43:58,679 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,679 - __main__ - INFO -    Giải thích thứ tự mới:
2025-05-31 07:43:58,680 - __main__ - INFO -    1. Final score = (alpha_retrieval * hybrid_retrieval_score) + (alpha_support * support_score)
2025-05-31 07:43:58,680 - __main__ - INFO -    2. Support score được tính từ số lượng và chất lượng của supporting triples
2025-05-31 07:43:58,680 - __main__ - INFO -    3. Passages có nhiều supporting triples sẽ được boost lên
2025-05-31 07:43:58,680 - __main__ - INFO -    4. Passages không có support sẽ bị penalty
2025-05-31 07:43:58,680 - __main__ - INFO - ------------------------------------------------------------
2025-05-31 07:43:58,680 - __main__ - INFO -    Rank 1. ID: passage_001
2025-05-31 07:43:58,681 - __main__ - INFO -       Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,681 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,681 - __main__ - INFO -          - Final score: 0.872
2025-05-31 07:43:58,681 - __main__ - INFO -          - Retrieval score: 1.000
2025-05-31 07:43:58,681 - __main__ - INFO -          - Support score: 0.680
2025-05-31 07:43:58,681 - __main__ - INFO -       Supporting triples: 2
2025-05-31 07:43:58,682 - __main__ - INFO -       Triple IDs: triple_001, triple_003...
2025-05-31 07:43:58,682 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.8, 'embedding_score': 0.7, 'hybrid_score': 0.75, 'support_score': 0.6799999999999999, 'support_count': 2, 'normalized_retrieval': 1.0, 'alpha_retrieval': 0.6, 'alpha_support': 0.4, 'base_final_score': 0.8719999999999999, 'final_score_after_modifiers': 0.8719999999999999}
2025-05-31 07:43:58,682 - __main__ - INFO -    Rank 2. ID: passage_002
2025-05-31 07:43:58,682 - __main__ - INFO -       Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,682 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,682 - __main__ - INFO -          - Final score: 0.798
2025-05-31 07:43:58,683 - __main__ - INFO -          - Retrieval score: 0.917
2025-05-31 07:43:58,683 - __main__ - INFO -          - Support score: 0.620
2025-05-31 07:43:58,683 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,683 - __main__ - INFO -       Triple IDs: triple_002...
2025-05-31 07:43:58,683 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.6, 'embedding_score': 0.8, 'hybrid_score': 0.7, 'support_score': 0.6199999999999999, 'support_count': 1, 'normalized_retrieval': 0.9166666666666666, 'alpha_retrieval': 0.6, 'alpha_support': 0.4, 'base_final_score': 0.7979999999999999, 'final_score_after_modifiers': 0.7979999999999999}
2025-05-31 07:43:58,684 - __main__ - INFO -    Rank 3. ID: passage_003
2025-05-31 07:43:58,684 - __main__ - INFO -       Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,684 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,684 - __main__ - INFO -          - Final score: 0.564
2025-05-31 07:43:58,684 - __main__ - INFO -          - Retrieval score: 0.667
2025-05-31 07:43:58,684 - __main__ - INFO -          - Support score: 0.410
2025-05-31 07:43:58,686 - __main__ - INFO -       Supporting triples: 1
2025-05-31 07:43:58,686 - __main__ - INFO -       Triple IDs: triple_004...
2025-05-31 07:43:58,686 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.5, 'embedding_score': 0.6, 'hybrid_score': 0.55, 'support_score': 0.41, 'support_count': 1, 'normalized_retrieval': 0.6666666666666667, 'alpha_retrieval': 0.6, 'alpha_support': 0.4, 'base_final_score': 0.5640000000000001, 'final_score_after_modifiers': 0.5640000000000001}
2025-05-31 07:43:58,687 - __main__ - INFO -    Rank 4. ID: passage_004
2025-05-31 07:43:58,687 - __main__ - INFO -       Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,687 - __main__ - INFO -       Scores:
2025-05-31 07:43:58,687 - __main__ - INFO -          - Final score: 0.000
2025-05-31 07:43:58,687 - __main__ - INFO -          - Retrieval score: 0.000
2025-05-31 07:43:58,688 - __main__ - INFO -          - Support score: 0.000
2025-05-31 07:43:58,688 - __main__ - INFO -       Supporting triples: 0
2025-05-31 07:43:58,688 - __main__ - INFO -       Score breakdown: {'bm25_score': 0.2, 'embedding_score': 0.1, 'hybrid_score': 0.15, 'support_score': 0.0, 'support_count': 0, 'normalized_retrieval': 0.0, 'alpha_retrieval': 0.6, 'alpha_support': 0.4, 'base_final_score': 0.0, 'final_score_after_modifiers': 0.0}
2025-05-31 07:43:58,688 - __main__ - INFO - 
📈 BƯỚC 5: TẠO KẾT QUẢ VÀ THỐNG KÊ
2025-05-31 07:43:58,689 - __main__ - INFO - ----------------------------------------
2025-05-31 07:43:58,689 - __main__ - INFO - 📈 Tạo ranking statistics...
2025-05-31 07:43:58,689 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,689 - __main__ - INFO - 🎉 PASSAGE RANKING HOÀN THÀNH
2025-05-31 07:43:58,690 - __main__ - INFO - ============================================================
2025-05-31 07:43:58,690 - __main__ - INFO - 📊 KẾT QUẢ TỔNG QUAN:
2025-05-31 07:43:58,690 - __main__ - INFO -    📝 Query: 'Lợi ích của táo cho sức khỏe là gì?'
2025-05-31 07:43:58,690 - __main__ - INFO -    ⏱️ Thời gian xử lý: 0.02 giây
2025-05-31 07:43:58,690 - __main__ - INFO -    📄 Passages: 4 → 4
2025-05-31 07:43:58,691 - __main__ - INFO -    📈 Efficiency: 100.00%
2025-05-31 07:43:58,691 - __main__ - INFO - 
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:43:58,691 - __main__ - INFO -    1. Rank 1: passage_001 | Final: 0.872 (Ret: 1.000, Sup: 0.680) | Triples: 2
2025-05-31 07:43:58,691 - __main__ - INFO -       📝 Text: Táo là loại trái cây rất tốt cho sức khỏe, chứa nhiều vitamin C và chất xơ....
2025-05-31 07:43:58,691 - __main__ - INFO -    2. Rank 2: passage_002 | Final: 0.798 (Ret: 0.917, Sup: 0.620) | Triples: 1
2025-05-31 07:43:58,692 - __main__ - INFO -       📝 Text: Vitamin C giúp tăng cường hệ miễn dịch và bảo vệ cơ thể khỏi bệnh tật....
2025-05-31 07:43:58,692 - __main__ - INFO -    3. Rank 3: passage_003 | Final: 0.564 (Ret: 0.667, Sup: 0.410) | Triples: 1
2025-05-31 07:43:58,692 - __main__ - INFO -       📝 Text: Chất xơ trong thực phẩm giúp cải thiện tiêu hóa và kiểm soát cholesterol....
2025-05-31 07:43:58,692 - __main__ - INFO -    4. Rank 4: passage_004 | Final: 0.000 (Ret: 0.000, Sup: 0.000) | Triples: 0
2025-05-31 07:43:58,692 - __main__ - INFO -       📝 Text: Thời tiết hôm nay rất đẹp, trời nắng và mát mẻ....
2025-05-31 07:43:58,692 - __main__ - INFO - 
📊 PHÂN BỐ SUPPORT:
2025-05-31 07:43:58,693 - __main__ - INFO -    no_support: 1 passages (25.0%)
2025-05-31 07:43:58,693 - __main__ - INFO -    low_support: 3 passages (75.0%)
2025-05-31 07:43:58,693 - __main__ - INFO -    medium_support: 0 passages (0.0%)
2025-05-31 07:43:58,693 - __main__ - INFO -    high_support: 0 passages (0.0%)
2025-05-31 07:43:58,693 - __main__ - INFO - 
🔄 THAY ĐỔI RANKING:
2025-05-31 07:43:58,693 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:43:58,693 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:43:58,694 - __main__ - INFO -    ➡️ Unchanged: 4
2025-05-31 07:43:58,694 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:43:58,694 - __main__ - INFO -    📉 Max decline: 0 positions
2025-05-31 07:43:58,694 - __main__ - INFO - 
⚡ PERFORMANCE:
2025-05-31 07:43:58,694 - __main__ - INFO -    🏃 Passages/giây: 259.3
2025-05-31 07:43:58,695 - __main__ - INFO -    ⏱️ Avg time/passage: 0.004s
2025-05-31 07:43:58,695 - __main__ - INFO - ============================================================

```

# Phân tích output 



Để biết thứ tự của các passage trước và sau khi được xếp hạng trong log, bạn cần xem xét hai phần chính:

---

## 1. Top Ranked Passages (Kết quả sau khi xếp hạng)

Sau khi quá trình xếp hạng hoàn tất, log sẽ hiển thị phần **"TOP 5 RANKED PASSAGES"**. Đây là danh sách các passage đã được sắp xếp theo điểm số cuối cùng của chúng, từ cao nhất đến thấp nhất.

Ví dụ từ log bạn cung cấp:

```
🏆 TOP 5 RANKED PASSAGES:
2025-05-31 07:40:27,294 - __main__ - INFO -    1. Rank 1: p1 | Final: 1.000 (Ret: 1.000, Sup: 0.620) | Triples: 1
2025-05-31 07:40:27,294 - __main__ - INFO -       📝 Text: High retrieval, high support...
2025-05-31 07:40:27,294 - __main__ - INFO -    2. Rank 2: p2 | Final: 0.640 (Ret: 0.800, Sup: 0.000) | Triples: 0
2025-05-31 07:40:27,294 - __main__ - INFO -       📝 Text: High retrieval, no support...
2025-05-31 07:40:27,295 - __main__ - INFO -    3. Rank 3: p3 | Final: 0.000 (Ret: 0.000, Sup: 0.550) | Triples: 1
2025-05-31 07:40:27,295 - __main__ - INFO -       📝 Text: Low retrieval, high support...
```

Trong phần này, bạn có thể thấy:
* **Thứ tự mới (Rank)**: Passage nào đứng đầu (Rank 1), tiếp theo là Rank 2, v.v.
* **Điểm số cuối cùng (Final Score)**: Đây là điểm số tổng hợp quyết định thứ hạng.
* **Điểm Retrieval (Ret)** và **Điểm Support (Sup)**: Các điểm thành phần dẫn đến điểm cuối cùng.

---

## 2. Thay đổi thứ hạng (Ranking Changes)

Log cũng có một phần thống kê về sự thay đổi thứ hạng, được gọi là **"THAY ĐỔI RANKING"**. Phần này cung cấp cái nhìn tổng quan về mức độ ảnh hưởng của quá trình xếp hạng lên thứ tự ban đầu của các passage.

Ví dụ từ log:

```
2025-05-31 07:40:27,296 - __main__ - INFO - 🔄 THAY ĐỔI RANKING:
2025-05-31 07:40:27,296 - __main__ - INFO -    ⬆️ Moved up: 0
2025-05-31 07:40:27,296 - __main__ - INFO -    ⬇️ Moved down: 0
2025-05-31 07:40:27,296 - __main__ - INFO -    ➡️ Unchanged: 3
2025-05-31 07:40:27,297 - __main__ - INFO -    📈 Max improvement: 0 positions
2025-05-31 07:40:27,297 - __main__ - INFO -    📉 Max decline: 0 positions
```

Phần này cho bạn biết:
* **Moved up**: Số lượng passage đã tăng thứ hạng.
* **Moved down**: Số lượng passage đã giảm thứ hạng.
* **Unchanged**: Số lượng passage không thay đổi thứ hạng.
* **Max improvement/decline**: Mức độ thay đổi vị trí lớn nhất.

Để biết **thứ tự ban đầu**, bạn có thể phải tìm các log trước đó ghi lại danh sách "raw passages" hoặc "initial passages" trước khi các điểm số được tính toán và xếp hạng. Tuy nhiên, phần "THAY ĐỔI RANKING" này giúp bạn hiểu được **mức độ xáo trộn** vị trí mà thuật toán xếp hạng đã gây ra so với thứ tự đầu vào của các passage.

Bạn có muốn xem xét một ví dụ cụ thể về sự thay đổi thứ tự giữa các chiến lược xếp hạng khác nhau không?



---

# Các chiến lược trong code 

---

Trong log bạn cung cấp, có **ba chiến lược ranking khác nhau** đã được chạy và hiển thị kết quả tuần tự. Bạn có thể xác định chiến lược nào đang được sử dụng bằng cách tìm dòng log sau:

```
2025-05-31 07:40:27,xxx - __main__ - INFO - 🎯 Strategy: [TÊN_CHIẾN_LƯỢC]
```

Dựa trên các log bạn đã gửi, dưới đây là các chiến lược đã được chạy:

1.  **Chiến lược đầu tiên: `retrieval_only`**
    ```
    2025-05-31 07:40:27,284 - __main__ - INFO - 🎯 Strategy: retrieval_only
    ```
    Đây là chiến lược mà bạn đã hỏi về trường hợp của P3. Nó chỉ dựa vào điểm retrieval.

2.  **Chiến lược thứ hai: `support_only`**
    ```
    2025-05-31 07:40:27,302 - __main__ - INFO - 🎯 Strategy: support_only
    ```
    Chiến lược này sẽ chỉ dựa vào điểm support để xếp hạng các passage.

3.  **Chiến lược thứ ba: `hybrid_balanced`**
    ```
    2025-05-31 07:40:27,320 - __main__ - INFO - 🎯 Strategy: hybrid_balanced
    ```
    Chiến lược này kết hợp cả điểm retrieval và support với trọng số cân bằng (0.5/0.5).

Ngoài ra, ở cuối log còn có thêm hai phần chạy "quick ranking" sử dụng lại các chiến lược:

* **`hybrid_balanced`**:
    ```
    2025-05-31 07:40:27,334 - __main__ - INFO - 🚀 Quick ranking với strategy: hybrid_balanced
    ```
* **`hybrid_support_focused`**: (log bị cắt ở đây nhưng rõ ràng là chiến lược này)
    ```
    2025-05-31 07:40:27,351 - __main__ - INFO - 🚀 Quick ranking với strategy: hybrid_support_focused
    ```

Tóm lại, log của bạn đang trình bày kết quả của việc chạy thử nghiệm và so sánh hiệu quả của **bốn chiến lược ranking khác nhau**: `retrieval_only`, `support_only`, `hybrid_balanced`, và `hybrid_support_focused`.