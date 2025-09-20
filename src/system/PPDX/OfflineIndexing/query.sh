Nếu query trả về 0 SYNONYM edges, có thể có vấn đề. Hãy kiểm tra các bước debug sau:

## **1. Kiểm tra tất cả relationship types có trong database:**

```cypher
// Xem tất cả các loại relationship
MATCH ()-[r]->()
RETURN DISTINCT type(r) as relationship_types, count(r) as count
ORDER BY count DESC
```

## **2. Kiểm tra tất cả nodes và edges tổng quan:**

```cypher
// Tổng quan database
MATCH (n)
OPTIONAL MATCH (n)-[r]->()
RETURN labels(n) as node_types, count(DISTINCT n) as node_count, 
       type(r) as edge_type, count(r) as edge_count
```

## **3. Kiểm tra cụ thể Phrase nodes:**

```cypher
// Kiểm tra Phrase nodes
MATCH (p:Phrase)
RETURN count(p) as total_phrases
LIMIT 10
```

```cypher
// Xem một vài Phrase nodes mẫu
MATCH (p:Phrase)
RETURN p.id, p.text, p.normalized_text
LIMIT 10
```

## **4. Kiểm tra relationships của Phrase nodes:**

```cypher
// Xem tất cả relationships của Phrase nodes
MATCH (p:Phrase)-[r]->(target)
RETURN p.text as source_phrase, 
       type(r) as relationship_type, 
       labels(target) as target_labels,
       count(r) as count
```

## **5. Kiểm tra properties của relationships:**

```cypher
// Kiểm tra có relationship nào có property similarity không
MATCH ()-[r]->()
WHERE EXISTS(r.similarity)
RETURN type(r) as rel_type, 
       r.similarity as similarity,
       count(*) as count
```

## **6. Kiểm tra trong log files:**

Kiểm tra file log để xem có error nào không:
```bash
# Trong thư mục logs/
cat logs/offline_pipeline_test_data.log | grep -i "synonym\|error"
```

## **7. Kiểm tra file synonym output:**

```bash
# Kiểm tra file detected_synonyms.tsv
cat test/detected_synonyms.tsv
```

## **Các nguyên nhân có thể:**

1. **Transaction không commit:** SYNONYM edges được tạo nhưng không commit
2. **Case sensitivity:** Relationship type có thể là "Synonym" thay vì "SYNONYM"
3. **Database connection issue:** Edges được tạo trong session khác
4. **Error trong quá trình tạo edges:** Có exception nhưng không hiển thị

## **Query alternative để tìm synonyms:**

```cypher
// Thử tìm với case khác nhau
MATCH ()-[r]->()
WHERE toLower(type(r)) CONTAINS "synonym"
RETURN type(r), count(r)
```

```cypher
// Tìm relationships có similarity property
MATCH ()-[r]->()
WHERE EXISTS(r.similarity)
RETURN type(r), r.similarity, count(*)
```

**Hãy chạy các query debug này và cho tôi biết kết quả để tìm ra nguyên nhân!**