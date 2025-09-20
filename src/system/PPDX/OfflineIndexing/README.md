

# 🧠 GraphRAG Offline Indexing Pipeline

Knowledge Graph construction pipeline cho GraphRAG system với Vietnamese support.

## 🏗️ Architecture

```bash
📁 src/offline_indexing/
├── 📝 module1_chunking.py           # Keep paragraphs as-is
├── 🧠 module2_triple_extractor.py   # Qwen2.5-7B OpenIE
├── 🔗 module3_synonym_detector.py   # Multilingual embedding similarity
├── 🏗️ module4_graph_builder.py      # Neo4j graph construction
├── 🎯 pipeline_orchestrator.py      # Main coordinator
├── 📁 utils/                        # Utilities
└── 📁 test/                         # Testing & execution
```





```bash
system/
├── 📖 README.md
├── 📋 requirements.txt  
├── 🌍 .env.example
├── 📁 baselineRAG/
├── 📁 eval/
├── 📁 PPDX/
│   ├── 📁 DB/
│   │   └── 🐳 docker-compose.yml
│   │
│   └── 📁 offline_indexing/
│       ├── 📋 offline_indexing_requirements.txt
│       │
│       ├── 📄 module1_chunking.py
│       ├── 🧠 module2_triple_extractor.py  
│       ├── 🔗 module3_synonym_detector.py
│       ├── 🏗️ module4_graph_builder.py
│       ├── 🎯 pipeline_orchestrator.py
│       │
│       ├── 📁 utils/
│       │   ├── 🔧 utils_general.py
│       │   ├── 📊 utils_excel_documents.py
│       │   └── 🗃️ utils_neo4j.py
│       │
│       └── 📁 test/
│           ├── 📊 test_data.py
│           ├── 🚀 run_offline_pipeline.py
│           ├── 🧪 test_offline_pipeline.py
│           └── 🔍 test_query_functions.py
│
└── 📁 frontend
```




## 🚀 Quick Start
- Đọc file: command_run_offline_pipeline.sh




## 📊 Excel Input Format

Required columns:
- `doc_id`: Unique document identifier
- `title`: Document title
- `text`: Document content (Vietnamese supported)

Example:
```
doc_id | title        | text
PH_0   | pH Basics    | Các dung dịch nước có pH nhỏ hơn 7...
PH_1   | Neutral Water| Nước tinh khiết có pH = 7...
```

## 🌐 Access Neo4j

- **Browser**: http://localhost:7474
- **Username**: neo4j  
- **Password**: graphrag123


## 📋 Sample Neo4j Queries

```cypher
// View graph overview
MATCH (n) RETURN n LIMIT 50

// Count nodes and edges
MATCH (n) RETURN labels(n)[0] as type, count(*)
MATCH ()-[r]->() RETURN type(r) as type, count(*)

// View sample triples
MATCH (s:Phrase)-[r:RELATION]->(o:Phrase) 
RETURN s.text, r.predicate, o.text LIMIT 10

// Multi-hop exploration
MATCH path = (start:Phrase)-[:RELATION*1..3]->(end:Phrase)
WHERE start.text CONTAINS "pH"
RETURN path LIMIT 5
```

