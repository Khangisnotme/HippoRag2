Tôi sẽ phân tích code để tìm ra tại sao có 10 passages nhưng chỉ 7 passages có CONTAINS edges.## 🔍 **ROOT CAUSE ANALYSIS**

### **Primary Issue: API Failures = Missing CONTAINS Edges**

Từ logs của bạn, tôi thấy **3 chunks failed triple extraction**:
```
chunk_Isaac Hayes_7_0: 402 Payment Required
chunk_FOOD_0_0: 402 Payment Required  
chunk_WATER_0_0: 402 Payment Required
```

**Logic flow trong code:**
1. **10 passages created** ✅
2. **Triple extraction**: 7 success + 3 API failures 
3. **CONTAINS edge creation**: Only processes chunks **có triples**

### **Code Bug Analysis:**## 🔧 **BUGS FOUND:**

### **Bug #1: API Failure Handling**
**Issue**: Code không handle API failures gracefully
**Impact**: 3/10 chunks có API errors → no triples → no CONTAINS edges

### **Bug #2: CONTAINS Logic Assumption**
**Issue**: Code assumes tất cả chunks sẽ có triples
**Impact**: Chunks without triples bị bỏ qua hoàn toàn

## 🚨 **Additional Issues Found:**

### **Bug #3: Missing `title` Property (Neo4j Display)**
Trong `utils_neo4j.py`, Phrase nodes thiếu `title` property:## 📋 **SUMMARY OF ALL BUGS:**

| **Bug** | **Location** | **Issue** | **Impact** |
|---|---|---|---|
| **API Failure** | `module2_triple_extractor.py` | No graceful handling of API errors | 3/10 chunks fail → no CONTAINS edges |
| **CONTAINS Logic** | `module4_graph_builder.py` | Assumes all chunks have triples | Orphan passages without edges |
| **Missing Title** | `utils_neo4j.py` | Phrase nodes missing `title` property | Neo4j shows numbers instead of text |
| **Error Propagation** | Pipeline level | Continues processing despite failures | Inconsistent graph structure |

## 🔧 **IMMEDIATE VERIFICATION QUERIES:**

```cypher
-- Verify the 3 failed chunks
MATCH (p:Passage)
WHERE p.chunk_id IN ['chunk_Isaac Hayes_7_0', 'chunk_FOOD_0_0', 'chunk_WATER_0_0']
OPTIONAL MATCH (p)-[:CONTAINS]->(phrase:Phrase)
RETURN p.chunk_id, p.title, count(phrase) as phrase_count
ORDER BY p.chunk_id;

-- Should return 0 phrases for all 3 chunks
```

```cypher
-- Check if these chunks had any triple extraction
MATCH ()-[r:RELATION]->()
WHERE r.source_chunk IN ['chunk_Isaac Hayes_7_0', 'chunk_FOOD_0_0', 'chunk_WATER_0_0']
RETURN r.source_chunk, count(*) as triple_count;

-- Should return 0 rows (no triples extracted)
```

**Conclusion**: Đây là **expected behavior** do API failures, không phải code bug logic. Cần implement better error handling và fallback strategies! 🎯