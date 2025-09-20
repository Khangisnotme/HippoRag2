```bash
Trong HippoRAG2: https://arxiv.org/pdf/2502.14802

Các passages Node và phrase Node lưu cái gì ? 


 Relation Edge
 Synonym Edge
 Context Edge

3 loại cạnh này lưu cái gì trong code ??? 
```

---


# 📖 **HIPPORAG2 NODE & EDGE STRUCTURES**

## 🔍 **Phân tích từ Paper HippoRAG2**

### **📊 Node Types & Storage:**

#### **🔵 Phrase Node (Entity Node):**
```python
# Lưu trữ:
{
    "id": "phrase_abc123",
    "text": "insulin",           # Original text
    "normalized_text": "insulin",  # Canonical form
    "type": "entity",              # Node type
    "embedding": [0.1, 0.2, ...], # Dense vector representation
    "frequency": 15,               # Xuất hiện bao nhiều lần
    "aliases": ["insulin hormone", "INS"], # Các biến thể
    "entity_type": "protein"       # Optional: biology, chemistry, etc.
}
```

#### **🟣 Passage Node (Document Node):**
```python
# Lưu trữ:
{
    "id": "passage_doc1_chunk2",
    "text": "Insulin regulates glucose...", # Full paragraph text
    "title": "Diabetes Research",           # Document title
    "doc_id": "doc1",                      # Source document
    "chunk_index": 2,                      # Chunk position
    "embedding": [0.3, 0.4, ...],        # Dense vector của paragraph
    "length": 256,                         # Text length
    "source": "medical_journal",           # Source type
    "metadata": {
        "author": "Dr. Smith",
        "year": 2023,
        "journal": "Nature Medicine"
    }
}
```

---

## 🔗 **Edge Types & Properties:**

### **1. 🧠 Relation Edge (Factual Knowledge):**
```python
# Lưu giữa 2 Phrase Nodes
{
    "source": "phrase_insulin",
    "target": "phrase_glucose", 
    "type": "RELATION",
    "properties": {
        "predicate": "regulates",           # Semantic relationship
        "confidence": 0.95,                 # Extraction confidence
        "frequency": 8,                     # Xuất hiện bao nhiều lần
        "source_passages": ["passage_1", "passage_5"], # Supporting evidence
        "relation_type": "biochemical",     # Domain-specific type
        "directionality": "directed",       # directed/undirected
        "strength": 0.87                    # Relationship strength
    }
}
```

### **2. 🔗 Synonym Edge (Semantic Equivalence):**
```python
# Lưu giữa 2 Phrase Nodes đồng nghĩa
{
    "source": "phrase_diabetes",
    "target": "phrase_diabetic_mellitus",
    "type": "SYNONYM", 
    "properties": {
        "similarity_score": 0.92,          # Embedding similarity
        "synonym_type": "exact",            # exact/partial/abbreviation
        "algorithm": "multilingual-mpnet",  # Detection method
        "manual_verified": False,           # Human verification
        "context_similarity": 0.88,        # Context-based similarity
        "bidirectional": True               # Symmetric relationship
    }
}
```

### **3. 📄 Context Edge (Containment):**
```python
# Lưu từ Passage Node → Phrase Node
{
    "source": "passage_doc1_chunk2",
    "target": "phrase_insulin",
    "type": "CONTAINS",
    "properties": {
        "positions": [(45, 52), (123, 130)], # Text positions (start, end)
        "frequency": 2,                       # Xuất hiện bao nhiều lần trong passage
        "context_window": "...diabetes insulin regulates...", # Surrounding text
        "salience": 0.75,                    # Importance trong passage
        "tf_idf_score": 0.82,               # Term frequency score
        "entity_role": "subject"             # subject/object/modifier
    }
}
```

---

## 🏗️ **Trong Code Implementation:**

### **📄 Passage Node Storage:**
```python
class PassageNode:
    def __init__(self):
        self.id = f"passage_{chunk_id}"
        self.text = chunk['text']                    # Full paragraph
        self.title = chunk.get('title', '')         # Document title  
        self.doc_id = chunk['doc_id']               # Source document
        self.chunk_index = chunk.get('chunk_index', 0)
        self.embedding = self.encoder.encode(text)   # Dense vector
        self.metadata = {
            'source': chunk.get('source', ''),
            'length': len(text),
            'created_at': datetime.now()
        }
```

### **🔵 Phrase Node Storage:**
```python
class PhraseNode:
    def __init__(self):
        self.id = f"phrase_{uuid4().hex[:8]}"
        self.text = original_phrase                  # "insulin"
        self.normalized_text = phrase.lower().strip() # "insulin"  
        self.embedding = self.encoder.encode(text)   # Dense vector
        self.aliases = synonym_list                  # ["INS", "insulin hormone"]
        self.frequency = occurrence_count            # Xuất hiện bao nhiều lần
        self.entity_type = detected_type             # "protein", "disease", etc.
```

### **🧠 Relation Edge Storage:**
```python
class RelationEdge:
    def __init__(self):
        self.source_id = subject_phrase_id
        self.target_id = object_phrase_id
        self.predicate = "regulates"                 # Semantic relation
        self.confidence = triple.confidence          # LLM extraction confidence
        self.source_passages = [passage_id]         # Supporting evidence
        self.frequency = relation_count              # Cross-document frequency
        self.relation_embedding = self.encode_relation() # Optional: relation vector
```

### **🔗 Synonym Edge Storage:**
```python
class SynonymEdge:
    def __init__(self):
        self.source_id = phrase1_id
        self.target_id = phrase2_id  
        self.similarity_score = cosine_similarity    # 0.92
        self.detection_method = "multilingual-mpnet" # Algorithm used
        self.synonym_type = "exact"                  # exact/partial/abbreviation
        self.bidirectional = True                    # Symmetric relationship
        self.context_similarity = context_score     # Contextual similarity
```

### **📄 Context Edge Storage:**
```python
class ContextEdge:
    def __init__(self):
        self.source_id = passage_id
        self.target_id = phrase_id
        self.positions = [(start, end)]              # Text positions
        self.frequency = occurrence_count            # Frequency trong passage
        self.tf_idf_score = calculate_tfidf()       # Term importance
        self.salience = calculate_salience()         # Entity importance
        self.context_window = extract_context()      # Surrounding text
```

---

## 📊 **Storage Comparison:**

| Component | HippoRAG2 Paper | Our Implementation |
|-----------|-----------------|-------------------|
| **Phrase Node** | Entity + embedding + frequency | ✅ Text + normalized + embedding |
| **Passage Node** | Full text + metadata + embedding | ✅ Text + metadata + embedding |
| **Relation Edge** | Predicate + confidence + frequency | ✅ Predicate + confidence + source |
| **Synonym Edge** | Similarity + algorithm + type | ✅ Similarity score + method |
| **Context Edge** | Positions + frequency + salience | ✅ Basic containment (can enhance) |

---

## 🎯 **Key Insights từ HippoRAG2:**

### **💡 Enhanced Features chúng ta có thể thêm:**

1. **📊 Frequency Tracking:**
   ```python
   # Track cross-document frequency
   relation_frequency = count_across_all_passages(subject, predicate, object)
   ```

2. **🎯 Salience Scoring:**
   ```python
   # Entity importance trong passage
   salience = tf_idf_score * position_weight * context_relevance
   ```

3. **📍 Position Information:**
   ```python
   # Exact text positions
   positions = [(char_start, char_end) for match in text_matches]
   ```

4. **🔄 Bidirectional Relations:**
   ```python
   # Some relations are symmetric
   if relation_type in ["synonym", "equivalent"]:
       create_bidirectional_edge()
   ```

**→ Cấu trúc hiện tại của chúng ta đã capture được core concepts của HippoRAG2, có thể enhance thêm các features trên!** 🚀