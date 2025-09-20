```bash
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\test> python test_offline_pipeline.py
🧪 GraphRAG Offline Pipeline Tests
==================================================

🔧 Testing Individual Modules...

🧪 Testing Excel Processing...
📊 Excel Processing Results:
Total docs: 2
Avg length: 59.0 chars
  PH_0: Các dung dịch nước có giá trị pH nhỏ hơn 7 được co...
  PH_1: Nước tinh khiết có pH = 7, được coi là trung tính....
✅ Excel Processing passed

🧪 Testing Chunking...
📝 Chunking Results:
Total chunks: 2
Avg length: 59.0 chars
Method: keep_as_paragraph
  chunk_PH_0_0: Các dung dịch nước có giá trị pH nhỏ hơn 7 được co...
  chunk_PH_1_0: Nước tinh khiết có pH = 7, được coi là trung tính....
✅ Chunking passed

🧪 Testing Triple Extraction...
🧠 Testing Triple Extraction...
Note: Actual extraction requires valid HuggingFace API key
📊 Triple Extraction Results:
Total triples: 3
Unique subjects: 3
Unique predicates: 2
Most common predicates: [('có pH', 2), ('có giá trị pH', 1)]
✅ Triple Extraction passed

🧪 Testing Synonym Detection...
🔗 Testing Synonym Detection...
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00,  1.02it/s] 
📊 Synonym Detection Results:
  axít ≈ axit (score: 0.921)
  axít ≈ dung dịch axít (score: 0.866)
  axit ≈ dung dịch axít (score: 0.869)
  axit ≈ dung dịch axit (score: 0.834)
  kiềm ≈ bazơ (score: 0.863)
  dung dịch axít ≈ dung dịch axit (score: 0.936)
  pH nhỏ hơn 7 ≈ pH < 7 (score: 0.947)

📋 Synonym Mapping:
  axít → axít
  dung dịch axít → axít
  axit → axít
  dung dịch axit → axít
  kiềm → kiềm
  bazơ → kiềm
  pH nhỏ hơn 7 → pH < 7
  pH < 7 → pH < 7
✅ Synonym Detection passed

🧪 Testing Graph Building...
🏗️ Testing Graph Builder...
📊 Current Graph Statistics:
  Nodes: 8
  Edges: 13
✅ Graph Building passed

📊 Module Tests Summary: 5/5 passed

🎯 All module tests passed! Testing complete pipeline...
🧪 Testing Complete Offline Pipeline
==================================================
2025-05-28 03:23:43,739 - root - INFO - All dependencies are available

🔍 Environment Check:
========================================
Dependencies        : ✅ PASS
Neo4j Connection    : ✅ PASS
HuggingFace API     : ✅ PASS
========================================
🎉 Environment is ready!

📊 Step 1: Creating test data...
✅ Created small test file: small_test_data.xlsx

🚀 Step 2: Running pipeline...
2025-05-28 03:23:43,924 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-28 03:23:43,924 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
2025-05-28 03:23:48,860 - pipeline_orchestrator - INFO - 🚀 Starting complete offline pipeline...
2025-05-28 03:23:48,860 - pipeline_orchestrator - INFO - 📊 Step 0: Loading documents from Excel...
2025-05-28 03:23:48,894 - utils.utils_excel_documents - INFO - Loaded 2 documents from small_test_data.xlsx
2025-05-28 03:23:48,894 - utils.utils_excel_documents - INFO - Processed 2 documents
2025-05-28 03:23:48,900 - pipeline_orchestrator - INFO - 📝 Step 1: Processing chunks...
2025-05-28 03:23:48,900 - module1_chunking - INFO - Processed 2 documents into 2 chunks
2025-05-28 03:23:48,900 - pipeline_orchestrator - INFO - 🧠 Step 2: Extracting triples...
2025-05-28 03:23:51,213 - module2_triple_extractor - INFO - Extracted 5 triples from 2 chunks
2025-05-28 03:23:51,213 - pipeline_orchestrator - INFO - 🔗 Step 3: Detecting synonyms...
2025-05-28 03:23:51,213 - module3_synonym_detector - INFO - Detecting synonyms among 8 unique phrases
2025-05-28 03:23:51,221 - module3_synonym_detector - INFO - Generating embeddings...
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.97it/s] 
2025-05-28 03:23:51,482 - module3_synonym_detector - INFO - Found 2 synonym pairs
2025-05-28 03:23:51,483 - module3_synonym_detector - INFO - Created 2 synonym groups
2025-05-28 03:23:51,483 - pipeline_orchestrator - INFO - 🏗️ Step 4: Building Knowledge Graph...   
2025-05-28 03:23:51,753 - utils.utils_neo4j - INFO - Cleared all data from Neo4j database
2025-05-28 03:23:52,030 - module4_graph_builder - INFO - Cleared existing database
2025-05-28 03:23:52,030 - module4_graph_builder - INFO - Starting graph construction...
2025-05-28 03:23:52,155 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (e:Phrase) REQUIRE (e.id) IS UNIQUE` has no effect.} {description: `CONSTRAINT phrase_id FOR (e:Phrase) REQUIRE (e.id) IS UNIQUE` already exists.} {position: None} for query: 'CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (p:Phrase) REQUIRE p.id IS UNIQUE'
2025-05-28 03:23:52,168 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (e:Passage) REQUIRE (e.id) IS UNIQUE` has no effect.} {description: `CONSTRAINT passage_id FOR (e:Passage) REQUIRE (e.id) IS UNIQUE` already exists.} {position: None} for query: 'CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (p:Passage) REQUIRE p.id IS UNIQUE'
2025-05-28 03:23:52,204 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (e:Phrase) ON EACH [e.text, e.normalized_text]` has no effect.} {description: `FULLTEXT INDEX phrase_text FOR (e:Phrase) ON EACH [e.text, e.normalized_text]` already exists.} {position: None} for query: 'CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (p:Phrase) ON EACH [p.text, p.normalized_text]'
2025-05-28 03:23:52,218 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (e:Passage) ON EACH [e.text, e.title]` has no effect.} {description: `FULLTEXT INDEX passage_text FOR (e:Passage) ON EACH [e.text, e.title]` already exists.} {position: None} for query: 'CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (p:Passage) ON EACH [p.text, p.title]'
2025-05-28 03:23:52,220 - module4_graph_builder - INFO - Database constraints and indexes setup completed
2025-05-28 03:23:52,220 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-28 03:23:52,220 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00,  3.58it/s]
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00, 26.23it/s]
2025-05-28 03:23:58,085 - module4_graph_builder - INFO - Created 2 Passage nodes
2025-05-28 03:23:58,085 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-28 03:23:58,085 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.53it/s]
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.98it/s]
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00, 42.04it/s]
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.09it/s]
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.84it/s]
Batches: 100%|█████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.76it/s]
2025-05-28 03:24:04,882 - module4_graph_builder - INFO - Created 6 Phrase nodes with embeddings
2025-05-28 03:24:05,650 - module4_graph_builder - INFO - Created 5 RELATION edges
2025-05-28 03:24:05,816 - module4_graph_builder - INFO - Created 2 SYNONYM edges
2025-05-28 03:24:06,197 - module4_graph_builder - INFO - Created CONTAINS edges
2025-05-28 03:24:06,197 - module4_graph_builder - INFO - Graph construction completed: 8 nodes, 15 edges
2025-05-28 03:24:06,215 - pipeline_orchestrator - INFO - Saved triples to extracted_triples.tsv
2025-05-28 03:24:06,215 - pipeline_orchestrator - INFO - Saved synonyms to detected_synonyms.tsv  
2025-05-28 03:24:06,215 - pipeline_orchestrator - INFO - ✅ Pipeline completed successfully in 17.35 seconds

============================================================
📊 OFFLINE PIPELINE SUMMARY
============================================================
⏱️  Execution Time: 17.35 seconds
📁 Input File: small_test_data.xlsx

📊 EXCEL PROCESSING:
   Documents Loaded: 2
   Avg Length: 68.0 chars

📝 CHUNKING:
   Total Chunks: 2
   Avg Chunk Length: 68.0 chars
   Method: keep_as_paragraph

🧠 TRIPLES:
   Total: 5
   Unique Subjects: 4
   Unique Predicates: 2
   Unique Objects: 4

🔗 SYNONYMS:
   Synonym Pairs: 2
   Avg Similarity: 0.898

🏗️ KNOWLEDGE GRAPH:
   Total Nodes: 8
   Total Edges: 13
   Passage Nodes: 2
   Phrase Nodes: 6
   RELATION Edges: 5
   CONTAINS Edges: 8
============================================================
✅ Pipeline completed successfully!
🌐 Access Neo4j Browser: http://localhost:7474
============================================================
2025-05-28 03:24:06,223 - utils.utils_neo4j - INFO - Neo4j connection closed

✅ Step 3: Validating results...
🔍 Validating pipeline results...
✅ Pipeline results validation passed!
   📊 2 documents processed
   📝 2 chunks created
   🧠 5 triples extracted
   🏗️ 8 nodes, 13 edges created
🎉 All tests passed!

==================================================
🎉 ALL TESTS PASSED!
✅ Pipeline results validation passed!
   📊 2 documents processed
   📝 2 chunks created
   🧠 5 triples extracted
   🏗️ 8 nodes, 13 edges created
🎉 All tests passed!

✅ Pipeline results validation passed!
   📊 2 documents processed
   📝 2 chunks created
   🧠 5 triples extracted
   🏗️ 8 nodes, 13 edges created
🎉 All tests passed!
✅ Pipeline results validation passed!
   📊 2 documents processed
   📝 2 chunks created
   🧠 5 triples extracted
✅ Pipeline results validation passed!
   📊 2 documents processed
   📝 2 chunks created
✅ Pipeline results validation passed!
   📊 2 documents processed
✅ Pipeline results validation passed!
✅ Pipeline results validation passed!
   📊 2 documents processed
✅ Pipeline results validation passed!
✅ Pipeline results validation passed!
   📊 2 documents processed
   📝 2 chunks created
   🧠 5 triples extracted
   🏗️ 8 nodes, 13 edges created
🎉 All tests passed!

==================================================
🎉 ALL TESTS PASSED!
✅ Pipeline is ready for production use

📝 Next steps:
   1. Set HF_API_KEY environment variable
   2. Run: python run_offline_pipeline.py --excel your_data.xlsx
   3. Explore graph at: http://localhost:7474
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\test> python test_offline_pipeline.pypython test_offline_pipelipython test_offline_pipeline.pypython test_offline_pipeline.pypython test_offline_pipeline.py^C
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\test> python test_query_functions.py
🔍 GraphRAG Query Functions Test
🧪 Running Graph Query Function Tests
============================================================
🔍 Test 1: Basic Graph Structure
   📊 Node types found: ['Passage', 'Phrase']
   ✅ Graph structure OK: 8 total nodes
      Passage: 2 nodes
      Phrase: 6 nodes

🔗 Test 2: Edge Relationships
   📊 Edge types found: ['RELATION', 'CONTAINS']
   ✅ Edge relationships OK: 13 total edges
      RELATION: 5 edges
      CONTAINS: 8 edges

📄 Test 3: Passage-Phrase Connections
   ✅ Found 8 sample connections:
      TEST_0 → nhỏ hơn 7...
      TEST_0 → bằng 7...
      TEST_0 → axít...
      TEST_0 → kiềm...
      TEST_0 → chủ thể...

🧠 Test 4: Relation Network
   ✅ Found 5 sample relations:
      (chủ thể) --[quan hệ]--> (chủ thể)
      (chủ thể) --[quan hệ]--> (chủ thể)
      (nước tinh khiết) --[có pH]--> (bằng 7)
      (kiềm) --[có pH]--> (bằng 7)
      (axít) --[có pH]--> (nhỏ hơn 7)

🔗 Test 5: Synonym Detection
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownRelationshipTypeWarning} {category: UNRECOGNIZED} {title: The provided relationship type is not in the database.} {description: One of the relationship types in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing relationship type is: SYNONYM)} {position: line: 2, column: 34, offset: 34} for query: '\n            MATCH (p1:Phrase)-[s:SYNONYM]->(p2:Phrase)\n            RETURN p1.text as phrase1, p2.text as phrase2, s.similarity_score as score\n            LIMIT 10\n            '
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.UnknownPropertyKeyWarning} {category: UNRECOGNIZED} {title: The provided property key is not in the database} {description: One of the property names in your query is not available in the database, make sure you didn't misspell it or that the label is available when you run this statement in your application (the missing property name is: similarity_score)} {position: line: 3, column: 62, offset: 117} for query: '\n            MATCH (p1:Phrase)-[s:SYNONYM]->(p2:Phrase)\n            RETURN p1.text as phrase1, p2.text as phrase2, s.similarity_score as score\n            LIMIT 10\n            '
   ⚠️  No SYNONYM edges found (may be normal if no synonyms detected)

🌐 Test 6: Multi-hop Traversal
   ✅ Found 3 multi-hop paths:
      kiềm --1 hops--> bằng 7
      axít --1 hops--> nhỏ hơn 7
      nước tinh khiết --1 hops--> bằng 7

🔍 Test 7: Search Capabilities
   📊 Search for 'pH' or 'axít': 1 results
      axít
   📄 Passages containing 'pH': 2
      TEST_0: pH Cơ bản
      TEST_1: Nước

📊 Test 8: Graph Statistics
   📈 Total nodes: 8
   📈 Total edges: 13
   📋 Node breakdown:
      Passage: 2
      Phrase: 6
   📋 Edge breakdown:
      RELATION: 5
      CONTAINS: 8

💡 Test 9: Sample Demonstration Queries
   🔬 Concepts related to pH (0 found):
   ⚖️ Passages discussing both acid and base (1 found):
      • TEST_0: pH Cơ bản

============================================================
📊 Test Results: 9/9 tests passed
🎉 All tests passed! Graph is working correctly.

💡 Useful Neo4j Browser Queries:
========================================

// View graph overview
MATCH (n) RETURN n LIMIT 50

// Count all nodes by type
MATCH (n) RETURN labels(n)[0] as type, count(*) as count

// Count all edges by type
MATCH ()-[r]->() RETURN type(r) as type, count(*) as count

// View sample triples
MATCH (s:Phrase)-[r:RELATION]->(o:Phrase) RETURN s.text, r.predicate, o.text LIMIT 10

// Find multi-hop paths
MATCH path = (start:Phrase)-[:RELATION*1..3]->(end:Phrase) RETURN path LIMIT 5

// Search for pH concepts
MATCH (p:Phrase) WHERE p.text CONTAINS 'pH' RETURN p.text

// View passage-phrase connections
MATCH (passage:Passage)-[:CONTAINS]->(phrase:Phrase) RETURN passage.title, phrase.text LIMIT 10

✅ All query functions working correctly!
🌐 Explore the graph manually at: http://localhost:7474
   Username: neo4j
   Password: graphrag123
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\test>

```












