```
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing> python run_offline_pipeline.py --excel test/test_data.xlsx
🚀 GraphRAG Offline Pipeline
==================================================
2025-05-28 03:53:08,318 - root - INFO - All dependencies are available

🔍 Environment Check:
========================================
Dependencies        : ✅ PASS
Neo4j Connection    : ✅ PASS
HuggingFace API     : ✅ PASS
========================================
🎉 Environment is ready!
2025-05-28 03:53:08,393 - utils.utils_excel_documents - INFO - Excel file validation passed: 10 rows
📊 Processing Excel file: test\test_data.xlsx
🔗 Synonym threshold: 0.85
🗃️ Clear existing graph: True
🌐 Neo4j URI: bolt://localhost:7687

2025-05-28 03:53:08,396 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-28 03:53:08,397 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
2025-05-28 03:53:15,214 - pipeline_orchestrator - INFO - 🚀 Starting complete offline pipeline...
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit      
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode      
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f680' in position 57: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>  
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main      
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 55, in run_complete_pipeline
    logger.info("🚀 Starting complete offline pipeline...")
Message: '🚀 Starting complete offline pipeline...'
Arguments: ()
2025-05-28 03:53:15,219 - pipeline_orchestrator - INFO - 📊 Step 0: Loading documents from Excel...
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit      
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode      
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4ca' in position 57: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>  
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main      
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 59, in run_complete_pipeline
    logger.info("📊 Step 0: Loading documents from Excel...")
Message: '📊 Step 0: Loading documents from Excel...'
Arguments: ()
2025-05-28 03:53:15,228 - utils.utils_excel_documents - INFO - Loaded 10 documents from test\test_data.xlsx
2025-05-28 03:53:15,229 - utils.utils_excel_documents - INFO - Processed 10 documents
2025-05-28 03:53:15,230 - pipeline_orchestrator - INFO - 📝 Step 1: Processing chunks...
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode      
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4dd' in position 57: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>  
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main      
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 64, in run_complete_pipeline
    logger.info("📝 Step 1: Processing chunks...")
Message: '📝 Step 1: Processing chunks...'
Arguments: ()
2025-05-28 03:53:15,234 - module1_chunking - INFO - Processed 10 documents into 10 chunks
2025-05-28 03:53:15,234 - pipeline_orchestrator - INFO - 🧠 Step 2: Extracting triples...
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit      
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode      
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f9e0' in position 57: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>  
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main      
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 69, in run_complete_pipeline
    logger.info("🧠 Step 2: Extracting triples...")
Message: '🧠 Step 2: Extracting triples...'
Arguments: ()
2025-05-28 03:53:33,853 - module2_triple_extractor - INFO - Extracted 85 triples from 10 chunks
2025-05-28 03:53:33,854 - pipeline_orchestrator - INFO - 🔗 Step 3: Detecting synonyms...
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit      
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode      
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f517' in position 57: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>  
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main      
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 74, in run_complete_pipeline
    logger.info("🔗 Step 3: Detecting synonyms...")
Message: '🔗 Step 3: Detecting synonyms...'
Arguments: ()
2025-05-28 03:53:33,859 - module3_synonym_detector - INFO - Detecting synonyms among 98 unique phrases
2025-05-28 03:53:33,859 - module3_synonym_detector - INFO - Generating embeddings...
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00,  6.06it/s] 
2025-05-28 03:53:34,522 - module3_synonym_detector - INFO - Found 6 synonym pairs
2025-05-28 03:53:34,523 - module3_synonym_detector - INFO - Created 6 synonym groups
2025-05-28 03:53:34,523 - pipeline_orchestrator - INFO - 🏗️ Step 4: Building Knowledge Graph...
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit      
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode      
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode characters in position 57-58: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>  
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main      
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 82, in run_complete_pipeline
    logger.info("🏗️ Step 4: Building Knowledge Graph...")
Message: '🏗️ Step 4: Building Knowledge Graph...'
Arguments: ()
2025-05-28 03:53:34,593 - utils.utils_neo4j - INFO - Cleared all data from Neo4j database
2025-05-28 03:53:34,610 - module4_graph_builder - INFO - Cleared existing database
2025-05-28 03:53:34,611 - module4_graph_builder - INFO - Starting graph construction...
2025-05-28 03:53:34,616 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (e:Phrase) REQUIRE (e.id) IS UNIQUE` has no effect.} {description: `CONSTRAINT phrase_id FOR (e:Phrase) REQUIRE (e.id) IS UNIQUE` already exists.} {position: None} for query: 'CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (p:Phrase) REQUIRE p.id IS UNIQUE'
2025-05-28 03:53:34,620 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (e:Passage) REQUIRE (e.id) IS UNIQUE` has no effect.} {description: `CONSTRAINT passage_id FOR (e:Passage) REQUIRE (e.id) IS UNIQUE` already exists.} {position: None} for query: 'CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (p:Passage) REQUIRE p.id IS UNIQUE'
2025-05-28 03:53:34,626 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (e:Phrase) ON EACH [e.text, e.normalized_text]` has no effect.} {description: `FULLTEXT INDEX phrase_text FOR (e:Phrase) ON EACH [e.text, e.normalized_text]` already exists.} {position: None} for query: 'CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (p:Phrase) ON EACH [p.text, p.normalized_text]'
2025-05-28 03:53:34,630 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (e:Passage) ON EACH [e.text, e.title]` has no effect.} {description: `FULLTEXT INDEX passage_text FOR (e:Passage) ON EACH [e.text, e.title]` already exists.} {position: None} for query: 'CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (p:Passage) ON EACH [p.text, p.title]'
2025-05-28 03:53:34,630 - module4_graph_builder - INFO - Database constraints and indexes setup completed
2025-05-28 03:53:34,634 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-28 03:53:34,635 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 14.42it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.03it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.96it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 16.31it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 14.05it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.30it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.88it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 10.75it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 24.77it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 27.50it/s]
2025-05-28 03:53:40,123 - module4_graph_builder - INFO - Created 10 Passage nodes
2025-05-28 03:53:40,123 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-28 03:53:40,123 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.35it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 52.20it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 38.04it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 48.66it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.06it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 79.13it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 39.13it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 47.36it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 40.30it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 42.69it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 55.73it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 46.97it/s]
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 116.57it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 45.62it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 53.43it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 37.56it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 56.89it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 25.45it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 47.75it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 37.69it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 25.90it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 43.87it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 41.97it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 47.13it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 44.04it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 42.49it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 34.80it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 28.21it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 25.15it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 33.95it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 36.04it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 41.58it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 61.88it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 42.68it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 47.40it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 48.67it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 55.01it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 43.28it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 47.05it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 39.31it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 46.62it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 37.86it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 81.21it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 36.61it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 59.09it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 51.08it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 40.80it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 35.76it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 55.11it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 43.20it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.62it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 26.74it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 23.46it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 42.40it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 28.14it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 23.95it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 37.72it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 36.77it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 37.21it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 50.67it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 47.67it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 27.61it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 35.43it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 43.28it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 43.35it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 34.30it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.80it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 40.06it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 41.20it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 36.65it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.36it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 40.97it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 25.61it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 38.71it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 47.43it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 35.21it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 33.28it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 41.45it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.65it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 37.57it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.67it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 35.11it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.03it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 34.94it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 56.84it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 40.03it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 35.04it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.36it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 38.58it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 40.20it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 37.41it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.60it/s]
2025-05-28 03:53:53,435 - module4_graph_builder - INFO - Created 92 Phrase nodes with embeddings
2025-05-28 03:53:54,631 - module4_graph_builder - INFO - Created 85 RELATION edges
2025-05-28 03:53:54,729 - module4_graph_builder - INFO - Created 6 SYNONYM edges
2025-05-28 03:53:55,462 - module4_graph_builder - INFO - Created CONTAINS edges
2025-05-28 03:53:55,462 - module4_graph_builder - INFO - Graph construction completed: 102 nodes, 189 edges
2025-05-28 03:53:55,497 - pipeline_orchestrator - INFO - Saved triples to test\extracted_triples.tsv
2025-05-28 03:53:55,497 - pipeline_orchestrator - INFO - Saved synonyms to test\detected_synonyms.tsv
2025-05-28 03:53:55,497 - pipeline_orchestrator - INFO - ✅ Pipeline completed successfully in 40.28 seconds
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit      
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode      
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 57: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>  
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main      
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 118, in run_complete_pipeline
    logger.info(f"✅ Pipeline completed successfully in {pipeline_duration:.2f} seconds")
Message: '✅ Pipeline completed successfully in 40.28 seconds'
Arguments: ()

============================================================
📊 OFFLINE PIPELINE SUMMARY
============================================================
⏱️  Execution Time: 40.28 seconds
📁 Input File: test\test_data.xlsx

📊 EXCEL PROCESSING:
   Documents Loaded: 10
   Avg Length: 446.0 chars

📝 CHUNKING:
   Total Chunks: 10
   Avg Chunk Length: 446.0 chars
   Method: keep_as_paragraph

🧠 TRIPLES:
   Total: 85
   Unique Subjects: 23
   Unique Predicates: 61
   Unique Objects: 79

🔗 SYNONYMS:
   Synonym Pairs: 6
   Avg Similarity: 0.890

🏗️ KNOWLEDGE GRAPH:
   Total Nodes: 102
   Total Edges: 183
   Passage Nodes: 10
   Phrase Nodes: 92
   RELATION Edges: 85
   CONTAINS Edges: 98
============================================================
✅ Pipeline completed successfully!
🌐 Access Neo4j Browser: http://localhost:7474
============================================================
2025-05-28 03:53:55,506 - utils.utils_neo4j - INFO - Neo4j connection closed
2025-05-28 03:53:55,507 - root - INFO - Pipeline results saved to test\pipeline_results_test_data.json
💾 Results saved to: test\pipeline_results_test_data.json

🎉 Offline pipeline completed successfully!
🌐 Access Neo4j Browser: http://localhost:7474
   Username: neo4j
   Password: graphrag123

📝 Next steps:
   1. Explore graph in Neo4j Browser
   2. Run query tests: python test_query_functions.py
   3. Check intermediate results in output files
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing> 
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing> 
```