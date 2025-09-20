# Tìm lỗi: tại sao có 10 passages tất mà, cả có 3 passages ko được nối CONTAINER? 

## 🔧 **Diagnostic Queries:**

### **1. Tìm passages không có CONTAINS edges:**
```cypher
MATCH (p:Passage)
WHERE NOT (p)-[:CONTAINS]->()
RETURN p.id, p.title, p.doc_id, p.text_length
ORDER BY p.id;
```

### **2. Check lý do tại sao missing:**
```cypher
// Check if these passages have triples extracted
MATCH (p:Passage)
WHERE NOT (p)-[:CONTAINS]->()
WITH p
MATCH ()-[r:RELATION]->()
WHERE r.source_chunk = p.chunk_id
RETURN p.id, count(r) as relations_from_this_passage;
```

### **3. Verify chunking vs triple extraction:**
```cypher
// All passages with their phrase counts
MATCH (p:Passage)
OPTIONAL MATCH (p)-[:CONTAINS]->(phrase:Phrase)
RETURN p.id, p.title, count(phrase) as phrase_count
ORDER BY phrase_count ASC;
```

## 🚨 **Possible Causes:**

1. **Triple extraction failed** cho 3 passages đó (API errors)
2. **Text quá ngắn** → không extract được triples  
3. **Special characters** → triple extraction skip
4. **Empty/invalid content** trong những passages đó

## 🔧 **Quick Fix Check:**

```cypher
// Check content của passages không có edges
MATCH (p:Passage)
WHERE NOT (p)-[:CONTAINS]->()
RETURN p.id, p.title, 
       substring(p.text, 0, 100) as text_preview,
       p.text_length
ORDER BY p.text_length ASC;
```
