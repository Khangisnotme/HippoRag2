# 27/05/2025

```bash
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing> python run_offline_pipeline.py --excel test/test_data.xlsx
🚀 GraphRAG Offline Pipeline
==================================================
2025-05-29 15:01:21,450 - root - INFO - All dependencies are available

🔍 Environment Check:
========================================
Dependencies        : ✅ PASS
Neo4j Connection    : ✅ PASS
HuggingFace API     : ✅ PASS
========================================
🎉 Environment is ready!
2025-05-29 15:01:21,561 - utils.utils_excel_documents - INFO - Excel file validation passed: 10 rows
📊 Processing Excel file: test\test_data.xlsx
🔗 Synonym threshold: 0.85
🗃️ Clear existing graph: True
🌐 Neo4j URI: bolt://localhost:7687

2025-05-29 15:01:21,562 - pipeline_orchestrator - INFO - Initializing OfflinePipelineOrchestrator
2025-05-29 15:01:21,562 - module1_chunking - INFO - Initialized ChunkProcessor
2025-05-29 15:01:21,562 - module2_triple_extractor - INFO - Initializing TripleExtractor with Qwen2.5-7B    
2025-05-29 15:01:21,563 - module2_triple_extractor - INFO - Using model: Qwen/Qwen2.5-7B-Instruct
2025-05-29 15:01:21,563 - module3_synonym_detector - INFO - Initializing SynonymDetector with model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
2025-05-29 15:01:21,565 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu   
2025-05-29 15:01:21,565 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
2025-05-29 15:01:30,972 - module3_synonym_detector - INFO - Model loaded successfully
2025-05-29 15:01:30,972 - pipeline_orchestrator - INFO - Pipeline initialization completed
2025-05-29 15:01:30,972 - pipeline_orchestrator - INFO - 🚀 Starting complete offline pipeline...
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
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 58, in run_complete_pipeline
    logger.info("🚀 Starting complete offline pipeline...")
Message: '🚀 Starting complete offline pipeline...'
Arguments: ()
2025-05-29 15:01:30,987 - pipeline_orchestrator - INFO - Input file: test\test_data.xlsx
2025-05-29 15:01:30,987 - pipeline_orchestrator - INFO - Settings: clear_graph=True, synonym_threshold=0.85 
2025-05-29 15:01:30,987 - pipeline_orchestrator - INFO - 📊 Step 0: Loading documents from Excel...
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
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 64, in run_complete_pipeline
    logger.info("📊 Step 0: Loading documents from Excel...")
Message: '📊 Step 0: Loading documents from Excel...'
Arguments: ()
2025-05-29 15:01:31,002 - utils.utils_excel_documents - INFO - Loaded 10 documents from test\test_data.xlsx
2025-05-29 15:01:31,003 - utils.utils_excel_documents - INFO - Processed 10 documents
2025-05-29 15:01:31,004 - pipeline_orchestrator - INFO - Loaded 10 documents from Excel
2025-05-29 15:01:31,005 - pipeline_orchestrator - INFO - 📝 Step 1: Processing chunks...
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
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 71, in run_complete_pipeline
    logger.info("📝 Step 1: Processing chunks...")
Message: '📝 Step 1: Processing chunks...'
Arguments: ()
2025-05-29 15:01:31,005 - module1_chunking - INFO - Starting to process 10 documents
2025-05-29 15:01:31,005 - module1_chunking - INFO - Completed processing: 10 valid chunks created from 10 documents
2025-05-29 15:01:31,005 - module1_chunking - INFO - Chunking statistics: {'total_chunks': 10, 'avg_chunk_length': 446.0, 'min_chunk_length': 121, 'max_chunk_length': 1509, 'total_characters': 4460, 'chunking_method': 'keep_as_paragraph'}
2025-05-29 15:01:31,005 - pipeline_orchestrator - INFO - Created 10 chunks from 10 documents
2025-05-29 15:01:31,005 - pipeline_orchestrator - INFO - 🧠 Step 2: Extracting triples...
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
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 78, in run_complete_pipeline
    logger.info("🧠 Step 2: Extracting triples...")
Message: '🧠 Step 2: Extracting triples...'
Arguments: ()
2025-05-29 15:01:31,005 - module2_triple_extractor - INFO - Starting triple extraction from 10 chunks       
2025-05-29 15:01:31,005 - module2_triple_extractor - INFO - Processing chunk 1/10: chunk_PH_0_0
2025-05-29 15:01:32,323 - module2_triple_extractor - INFO - Parsed 5 valid triples from 5 matches
2025-05-29 15:01:32,323 - module2_triple_extractor - INFO - Successfully extracted 5 triples from chunk chunk_PH_0_0
2025-05-29 15:01:32,323 - module2_triple_extractor - INFO - Processing chunk 2/10: chunk_Diego Costa_1_0    
2025-05-29 15:01:33,384 - module2_triple_extractor - INFO - Parsed 6 valid triples from 7 matches
2025-05-29 15:01:33,384 - module2_triple_extractor - INFO - Successfully extracted 6 triples from chunk chunk_Diego Costa_1_0
2025-05-29 15:01:33,384 - module2_triple_extractor - INFO - Processing chunk 3/10: chunk_Diego Maradona_2_0 
2025-05-29 15:01:38,533 - module2_triple_extractor - INFO - Parsed 20 valid triples from 30 matches
2025-05-29 15:01:38,533 - module2_triple_extractor - INFO - Successfully extracted 20 triples from chunk chunk_Diego Maradona_2_0
2025-05-29 15:01:38,533 - module2_triple_extractor - INFO - Processing chunk 4/10: chunk_Danh sách Tổng thống Hoa Kỳ_3_0
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u1ed5' in position 100: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 79, in run_complete_pipeline
    triples = self.triple_extractor.extract_triples_from_chunks(chunks)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module2_triple_extractor.py", line 45, in extract_triples_from_chunks
    logger.info(f"Processing chunk {idx}/{len(chunks)}: {chunk['chunk_id']}")
Message: 'Processing chunk 4/10: chunk_Danh sách Tổng thống Hoa Kỳ_3_0'
Arguments: ()
2025-05-29 15:01:39,899 - module2_triple_extractor - INFO - Parsed 7 valid triples from 7 matches
2025-05-29 15:01:39,900 - module2_triple_extractor - INFO - Successfully extracted 7 triples from chunk chunk_Danh sách Tổng thống Hoa Kỳ_3_0
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u1ed5' in position 121: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 79, in run_complete_pipeline
    triples = self.triple_extractor.extract_triples_from_chunks(chunks)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module2_triple_extractor.py", line 46, in extract_triples_from_chunks
    chunk_triples = self.extract_triples_from_chunk(chunk)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module2_triple_extractor.py", line 80, in extract_triples_from_chunk
    logger.info(f"Successfully extracted {len(triples)} triples from chunk {chunk.get('chunk_id', '')}")    
Message: 'Successfully extracted 7 triples from chunk chunk_Danh sách Tổng thống Hoa Kỳ_3_0'
Arguments: ()
2025-05-29 15:01:39,905 - module2_triple_extractor - INFO - Processing chunk 5/10: chunk_Ernest Rutherford_4_0
2025-05-29 15:01:41,155 - module2_triple_extractor - INFO - Parsed 6 valid triples from 6 matches
2025-05-29 15:01:41,156 - module2_triple_extractor - INFO - Successfully extracted 6 triples from chunk chunk_Ernest Rutherford_4_0
2025-05-29 15:01:41,156 - module2_triple_extractor - INFO - Processing chunk 6/10: chunk_Helen Hayes_5_0    
2025-05-29 15:01:44,102 - module2_triple_extractor - INFO - Parsed 24 valid triples from 25 matches
2025-05-29 15:01:44,102 - module2_triple_extractor - INFO - Successfully extracted 24 triples from chunk chunk_Helen Hayes_5_0
2025-05-29 15:01:44,103 - module2_triple_extractor - INFO - Processing chunk 7/10: chunk_Thảo My_6_0        
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u1ea3' in position 91: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 79, in run_complete_pipeline
    triples = self.triple_extractor.extract_triples_from_chunks(chunks)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module2_triple_extractor.py", line 45, in extract_triples_from_chunks
    logger.info(f"Processing chunk {idx}/{len(chunks)}: {chunk['chunk_id']}")
Message: 'Processing chunk 7/10: chunk_Thảo My_6_0'
Arguments: ()
2025-05-29 15:01:45,145 - module2_triple_extractor - INFO - Parsed 6 valid triples from 6 matches
2025-05-29 15:01:45,145 - module2_triple_extractor - INFO - Successfully extracted 6 triples from chunk chunk_Thảo My_6_0
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u1ea3' in position 112: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 79, in run_complete_pipeline
    triples = self.triple_extractor.extract_triples_from_chunks(chunks)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module2_triple_extractor.py", line 46, in extract_triples_from_chunks
    chunk_triples = self.extract_triples_from_chunk(chunk)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module2_triple_extractor.py", line 80, in extract_triples_from_chunk
    logger.info(f"Successfully extracted {len(triples)} triples from chunk {chunk.get('chunk_id', '')}")    
Message: 'Successfully extracted 6 triples from chunk chunk_Thảo My_6_0'
Arguments: ()
2025-05-29 15:01:45,145 - module2_triple_extractor - INFO - Processing chunk 8/10: chunk_Isaac Hayes_7_0    
2025-05-29 15:01:47,777 - module2_triple_extractor - INFO - Parsed 7 valid triples from 11 matches
2025-05-29 15:01:47,777 - module2_triple_extractor - INFO - Successfully extracted 7 triples from chunk chunk_Isaac Hayes_7_0
2025-05-29 15:01:47,777 - module2_triple_extractor - INFO - Processing chunk 9/10: chunk_FOOD_0_0
2025-05-29 15:01:48,611 - module2_triple_extractor - INFO - Parsed 2 valid triples from 3 matches
2025-05-29 15:01:48,611 - module2_triple_extractor - INFO - Successfully extracted 2 triples from chunk chunk_FOOD_0_0
2025-05-29 15:01:48,611 - module2_triple_extractor - INFO - Processing chunk 10/10: chunk_WATER_0_0
2025-05-29 15:01:49,748 - module2_triple_extractor - INFO - Parsed 4 valid triples from 4 matches
2025-05-29 15:01:49,748 - module2_triple_extractor - INFO - Successfully extracted 4 triples from chunk chunk_WATER_0_0
2025-05-29 15:01:49,748 - module2_triple_extractor - INFO - Completed extraction: 87 total triples from 10 chunks
2025-05-29 15:01:49,748 - module2_triple_extractor - INFO - Extraction statistics: {'total_triples': 87, 'unique_subjects': 21, 'unique_predicates': 56, 'unique_objects': 82, 'avg_confidence': 1.0, 'most_common_predicates': [('chơi cho', 6), ('đoạt', 5), ('được trao', 5), ('được coi là', 4), ('quan hệ', 3)], 'most_common_subjects': [('Diego Armando Maradona', 19), ('Helen Hayes Brown', 14), ('Diego da Silva Costa', 6), ('chảo My', 6), ('Tổng thống', 5)]}
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u01a1' in position 229: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 211, in <module>
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 174, in main
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 80, in run_complete_pipeline
    triple_stats = self.triple_extractor.get_statistics()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module2_triple_extractor.py", line 204, in get_statistics
    logger.info(f"Extraction statistics: {stats}")
Message: "Extraction statistics: {'total_triples': 87, 'unique_subjects': 21, 'unique_predicates': 56, 'unique_objects': 82, 'avg_confidence': 1.0, 'most_common_predicates': [('chơi cho', 6), ('đoạt', 5), ('được trao', 5), ('được coi là', 4), ('quan hệ', 3)], 'most_common_subjects': [('Diego Armando Maradona', 19), ('Helen Hayes Brown', 14), ('Diego da Silva Costa', 6), ('chảo My', 6), ('Tổng thống', 5)]}"
Arguments: ()
2025-05-29 15:01:49,760 - pipeline_orchestrator - INFO - Extracted 87 triples from 10 chunks
2025-05-29 15:01:49,760 - pipeline_orchestrator - INFO - 🔗 Step 3: Detecting synonyms...
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
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 85, in run_complete_pipeline
    logger.info("🔗 Step 3: Detecting synonyms...")
Message: '🔗 Step 3: Detecting synonyms...'
Arguments: ()
2025-05-29 15:01:49,760 - module3_synonym_detector - INFO - Starting synonym detection from 87 triples      
2025-05-29 15:01:49,760 - module3_synonym_detector - INFO - Detecting synonyms among 100 unique phrases     
2025-05-29 15:01:49,760 - module3_synonym_detector - INFO - Generating embeddings for phrases...
Batches: 100%|███████████████████████████████████████████████████████████████| 4/4 [00:01<00:00,  2.14it/s] 
2025-05-29 15:01:51,628 - module3_synonym_detector - INFO - Computing similarity matrix...
2025-05-29 15:01:51,628 - module3_synonym_detector - INFO - Finding synonym pairs...
2025-05-29 15:01:51,628 - module3_synonym_detector - INFO - Found 9 synonym pairs with threshold 0.85       
2025-05-29 15:01:51,643 - module3_synonym_detector - INFO - Found 9 synonym pairs
2025-05-29 15:01:51,643 - module3_synonym_detector - INFO - Creating synonym mapping...
2025-05-29 15:01:51,644 - module3_synonym_detector - INFO - Created 8 synonym groups with 17 mappings       
2025-05-29 15:01:51,645 - module3_synonym_detector - INFO - Synonym detection statistics: {'total_synonym_pairs': 9, 'avg_similarity': np.float64(0.8930803404914008), 'min_similarity': np.float64(0.855204701423645), 'max_similarity': np.float64(0.9443460702896118), 'unique_phrases_with_synonyms': 17}
2025-05-29 15:01:51,645 - pipeline_orchestrator - INFO - Found 9 synonym pairs
2025-05-29 15:01:51,645 - pipeline_orchestrator - INFO - 🏗️ Step 4: Building Knowledge Graph...
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
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 95, in run_complete_pipeline
    logger.info("🏗️ Step 4: Building Knowledge Graph...")
Message: '🏗️ Step 4: Building Knowledge Graph...'
Arguments: ()
2025-05-29 15:01:51,645 - module4_graph_builder - INFO - Initializing GraphBuilder with Neo4j at bolt://localhost:7687
2025-05-29 15:01:51,730 - module4_graph_builder - INFO - Successfully connected to Neo4j
2025-05-29 15:01:51,730 - pipeline_orchestrator - INFO - Clearing existing graph...
2025-05-29 15:01:51,730 - module4_graph_builder - INFO - Clearing existing database...
2025-05-29 15:01:51,906 - utils.utils_neo4j - INFO - Cleared all data from Neo4j database
2025-05-29 15:01:52,172 - module4_graph_builder - INFO - Successfully cleared existing database
2025-05-29 15:01:52,172 - module4_graph_builder - INFO - Starting graph construction...
2025-05-29 15:01:52,172 - module4_graph_builder - INFO - Input data: 10 chunks, 87 triples, 9 synonym pairs 
2025-05-29 15:01:52,172 - module4_graph_builder - INFO - Setting up database constraints and indexes...     
2025-05-29 15:01:52,249 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (e:Phrase) REQUIRE (e.id) IS UNIQUE` has no effect.} {description: `CONSTRAINT phrase_id FOR (e:Phrase) REQUIRE (e.id) IS UNIQUE` already exists.} {position: None} for query: 'CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (p:Phrase) REQUIRE p.id IS UNIQUE'
2025-05-29 15:01:52,268 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (e:Passage) REQUIRE (e.id) IS UNIQUE` has no effect.} {description: `CONSTRAINT passage_id FOR (e:Passage) REQUIRE (e.id) IS UNIQUE` already exists.} {position: None} for query: 'CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (p:Passage) REQUIRE p.id IS UNIQUE'
2025-05-29 15:01:52,286 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (e:Phrase) ON EACH [e.text, e.normalized_text]` has no effect.} {description: `FULLTEXT INDEX phrase_text FOR (e:Phrase) ON EACH [e.text, e.normalized_text]` already exists.} {position: None} for query: 'CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (p:Phrase) ON EACH [p.text, p.normalized_text]'
2025-05-29 15:01:52,307 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (e:Passage) ON EACH [e.text, e.title]` has no effect.} {description: `FULLTEXT INDEX passage_text FOR (e:Passage) ON EACH [e.text, e.title]` already exists.} {position: None} for query: 'CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (p:Passage) ON EACH [p.text, p.title]'
2025-05-29 15:01:52,307 - module4_graph_builder - INFO - Database constraints and indexes setup completed   
2025-05-29 15:01:52,307 - module4_graph_builder - INFO - Building nodes...
2025-05-29 15:01:52,307 - module4_graph_builder - INFO - Creating 10 Passage nodes...
2025-05-29 15:01:52,313 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-29 15:01:52,313 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 12.13it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.97it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.70it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 14.84it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 15.45it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.56it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 11.75it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  7.64it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.21it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 21.56it/s]
2025-05-29 15:01:58,331 - module4_graph_builder - INFO - Created 10 Passage nodes
2025-05-29 15:01:58,331 - module4_graph_builder - INFO - Creating Phrase nodes...
2025-05-29 15:01:58,331 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu   
2025-05-29 15:01:58,331 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 22.75it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 61.73it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 33.80it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 51.21it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.67it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 45.16it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.31it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 26.21it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 35.88it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.09it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 24.83it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.80it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 59.20it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 36.91it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 79.75it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 38.61it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 45.84it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 55.10it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 39.78it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 47.43it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 28.83it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.24it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 25.19it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 44.98it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 34.44it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.28it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.86it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.25it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.59it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.52it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 34.90it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 44.80it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 59.39it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 43.27it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.58it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 39.76it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.98it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 35.52it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 63.86it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.11it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.92it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 33.76it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.53it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 60.51it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.57it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.12it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.95it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.16it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.97it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.97it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.98it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 45.37it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 63.86it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 61.64it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 64.00it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 64.48it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.98it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 28.46it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.99it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 59.56it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.95it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 38.78it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.84it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 60.11it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.90it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 29.55it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 59.55it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 40.47it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 46.47it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 49.90it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 24.53it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 39.02it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.58it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 57.04it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.00it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 50.92it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 18.30it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 26.54it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 40.01it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 34.71it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 64.02it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 42.23it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 38.19it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 35.68it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 27.40it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 36.97it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 63.94it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 30.89it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 52.57it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 31.96it/s]
Batches: 100%|███████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 32.04it/s]
2025-05-29 15:02:11,486 - module4_graph_builder - INFO - Created 91 Phrase nodes with embeddings
2025-05-29 15:02:11,486 - module4_graph_builder - INFO - Building edges...
2025-05-29 15:02:11,486 - module4_graph_builder - INFO - Creating 87 RELATION edges...
2025-05-29 15:02:12,967 - module4_graph_builder - INFO - Created 87 RELATION edges
2025-05-29 15:02:12,967 - module4_graph_builder - INFO - Creating 9 SYNONYM edges...
2025-05-29 15:02:13,158 - module4_graph_builder - INFO - Created 9 SYNONYM edges
2025-05-29 15:02:13,158 - module4_graph_builder - INFO - Creating CONTAINS edges...
2025-05-29 15:02:13,911 - module4_graph_builder - INFO - Created 96 CONTAINS edges
2025-05-29 15:02:13,911 - module4_graph_builder - INFO - Graph construction completed: 101 nodes, 192 edges 
2025-05-29 15:02:13,911 - module4_graph_builder - INFO - Getting graph statistics...
2025-05-29 15:02:13,980 - module4_graph_builder - INFO - Graph statistics: {'nodes': {'Passage': 10, 'Phrase': 91}, 'edges': {'RELATION': 87, 'CONTAINS': 96}, 'total_nodes': 101, 'total_edges': 183}
2025-05-29 15:02:13,980 - pipeline_orchestrator - INFO - Graph construction completed
2025-05-29 15:02:13,980 - pipeline_orchestrator - INFO - Saving intermediate results...
2025-05-29 15:02:13,980 - pipeline_orchestrator - INFO - Saving intermediate results to test
2025-05-29 15:02:13,980 - module2_triple_extractor - INFO - Saving 87 triples to test\extracted_triples.tsv 
2025-05-29 15:02:13,980 - module2_triple_extractor - INFO - Triples saved successfully
2025-05-29 15:02:13,980 - pipeline_orchestrator - INFO - Saved triples to test\extracted_triples.tsv        
2025-05-29 15:02:13,980 - module3_synonym_detector - INFO - Saving 9 synonym pairs to test\detected_synonyms.tsv
2025-05-29 15:02:13,980 - module3_synonym_detector - INFO - Synonym pairs saved successfully
2025-05-29 15:02:13,980 - pipeline_orchestrator - INFO - Saved synonyms to test\detected_synonyms.tsv       
2025-05-29 15:02:13,980 - pipeline_orchestrator - INFO - ✅ Pipeline completed successfully in 43.01 seconds
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
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 135, in run_complete_pipeline
    logger.info(f"✅ Pipeline completed successfully in {pipeline_duration:.2f} seconds")
Message: '✅ Pipeline completed successfully in 43.01 seconds'
Arguments: ()

============================================================
📊 OFFLINE PIPELINE SUMMARY
============================================================
⏱️  Execution Time: 43.01 seconds
📁 Input File: test\test_data.xlsx

📊 EXCEL PROCESSING:
   Documents Loaded: 10
   Avg Length: 446.0 chars

📝 CHUNKING:
   Total Chunks: 10
   Avg Chunk Length: 446.0 chars
   Method: keep_as_paragraph

🧠 TRIPLES:
   Total: 87
   Unique Subjects: 21
   Unique Predicates: 56
   Unique Objects: 82

🔗 SYNONYMS:
   Synonym Pairs: 9
   Avg Similarity: 0.893

🏗️ KNOWLEDGE GRAPH:
   Total Nodes: 101
   Total Edges: 183
   Passage Nodes: 10
   Phrase Nodes: 91
   RELATION Edges: 87
   CONTAINS Edges: 96
============================================================
✅ Pipeline completed successfully!
🌐 Access Neo4j Browser: http://localhost:7474
============================================================
2025-05-29 15:02:13,990 - pipeline_orchestrator - INFO - Closing graph builder connection...
2025-05-29 15:02:13,990 - module4_graph_builder - INFO - Closing Neo4j connection
2025-05-29 15:02:13,990 - utils.utils_neo4j - INFO - Neo4j connection closed
2025-05-29 15:02:13,995 - module4_graph_builder - INFO - Neo4j connection closed
2025-05-29 15:02:13,995 - root - INFO - Pipeline results saved to test\pipeline_results_test_data.json      
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
```


# 29/05/2025: Fix bug sysnonym edge. 

Để hiểu cách các cạnh synonym được tìm thấy, tôi sẽ phân tích luồng xử lý từ đầu đến cuối:

1. **Quá trình phát hiện synonym (Module 3)**:


Ran tool
Dựa trên code, tôi sẽ giải thích quy trình phát hiện và tạo các cạnh synonym:

1. **Phát hiện Synonym (Module 3 - SynonymDetector)**:
- Sử dụng model `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` để tạo embeddings cho các cụm từ
- Quy trình:
  1. Thu thập tất cả các cụm từ duy nhất từ triples (subject và object)
  2. Lọc bỏ các cụm từ quá ngắn (< 3 ký tự)
  3. Tạo embeddings cho mỗi cụm từ
  4. Tính ma trận tương đồng (similarity matrix) giữa các embeddings
  5. Tìm các cặp có độ tương đồng >= ngưỡng (mặc định 0.85)
  6. Tạo các SynonymPair objects chứa thông tin về cặp đồng nghĩa

2. **Tạo Synonym Mapping**:
- Từ các synonym pairs, tạo một mapping từ các cụm từ về dạng chuẩn (canonical form)
- Sử dụng thuật toán tìm thành phần liên thông (connected components) trong đồ thị
- Mỗi nhóm synonym sẽ chọn một cụm từ làm dạng chuẩn

3. **Tạo Synonym Edges (Module 4 - GraphBuilder)**:
- Sử dụng các synonym pairs đã phát hiện để tạo các cạnh SYNONYM trong Neo4j
- Quy trình:
  1. Với mỗi synonym pair:
     - Chuẩn hóa text (lowercase và strip)
     - Tạo SYNONYM edge giữa hai Phrase nodes
     - Lưu similarity score và metadata
  2. Edge được tạo với các thuộc tính:
     - similarity_score: độ tương đồng giữa hai cụm từ
     - detection_method: phương pháp phát hiện
     - created_at: thời gian tạo

4. **Ví dụ từ logs**:
```
Found 9 synonym pairs with threshold 0.85
Created 8 synonym groups with 17 mappings
Synonym detection statistics: {
    'total_synonym_pairs': 9, 
    'avg_similarity': 0.904, 
    'min_similarity': 0.858, 
    'max_similarity': 0.952, 
    'unique_phrases_with_synonyms': 17
}
```

5. **Lợi ích**:
- Giúp kết nối các cụm từ có nghĩa tương tự
- Hỗ trợ tìm kiếm semantic (tìm thông tin qua synonyms)
- Tạo cấu trúc đồ thị nhất quán với canonical forms
- Lưu trữ metadata về độ tương đồng và phương pháp phát hiện

Bạn có muốn tôi giải thích thêm về bất kỳ phần nào không?


---


# 30/05/2025: Fix bug sysnonym edge

```bash
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing> python run_offline_pipeline.py --excel test/test_data.xlsx
============================================================
GraphRAG Offline Pipeline - HippoRAG 2 Style + GPT Fallback
============================================================
Features:
- No canonical synonym mapping
- All phrase surface forms preserved
- Synonym edges connect similar phrases
- Lower similarity threshold (0.8)
- Bidirectional synonym connectivity
- GPT-3.5 Turbo fallback for API failures
============================================================
2025-05-30 22:27:39,309 - root - INFO - All dependencies are available

🔍 Environment Check:
========================================
Dependencies        : ✅ PASS
Neo4j Connection    : ✅ PASS
HuggingFace API     : ✅ PASS
========================================
🎉 Environment is ready!
🔑 API Configuration:
   HuggingFace: ✅ Set
   OpenAI GPT-3.5: ✅ Set
   Fallback Mode: ✅ Enabled

2025-05-30 22:27:39,408 - utils.utils_excel_documents - INFO - Excel file validation passed: 10 rows
📊 Processing Excel file: test\test_data.xlsx
🔗 Synonym threshold: 0.8 (HippoRAG 2 style)
🗃️ Clear existing graph: True
🌐 Neo4j URI: bolt://localhost:7687
🎯 Pipeline style: HippoRAG 2 (no canonical mapping)
🤖 Extraction: HuggingFace + GPT-3.5 fallback

2025-05-30 22:27:44,157 - module2_triple_extractor - INFO - OpenAI GPT-3.5 Turbo fallback enabled (OpenAI >= 1.0.0)
2025-05-30 22:27:44,157 - module3_synonym_detector - INFO - Initializing SynonymDetector with model: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
2025-05-30 22:27:44,157 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-30 22:27:44,157 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
2025-05-30 22:27:53,700 - module3_synonym_detector - INFO - Model loaded successfully
2025-05-30 22:27:53,700 - pipeline_orchestrator - INFO - Initialized pipeline with GPT fallback: True
2025-05-30 22:27:53,701 - pipeline_orchestrator - INFO - GPT-3.5 Turbo fallback enabled
2025-05-30 22:27:53,702 - pipeline_orchestrator - INFO - Starting complete offline pipeline (HippoRAG 2 style with GPT fallback)...
2025-05-30 22:27:53,702 - pipeline_orchestrator - INFO - Step 0: Loading documents from Excel...
2025-05-30 22:27:53,712 - utils.utils_excel_documents - INFO - Loaded 10 documents from test\test_data.xlsx
2025-05-30 22:27:53,713 - utils.utils_excel_documents - INFO - Processed 10 documents
2025-05-30 22:27:53,713 - pipeline_orchestrator - INFO - Step 1: Processing chunks...
2025-05-30 22:27:53,713 - module1_chunking - INFO - Processed 10 documents into 10 chunks
2025-05-30 22:27:53,713 - pipeline_orchestrator - INFO - Step 2: Extracting triples (with GPT fallback support)...
2025-05-30 22:28:07,037 - module2_triple_extractor - ERROR - HF extraction failed for chunk chunk_Isaac Hayes_7_0: 402 Client Error: Payment Required for url: https://router.huggingface.co/together/v1/chat/completions (Request ID: Root=1-6839ce97-12d449495e45e4c62490dedf;18f53311-5a51-4487-a338-41bf195d401d)   

You have exceeded your monthly included credits for Inference Providers. Subscribe to PRO to get 20x more monthly included credits.
2025-05-30 22:28:07,037 - module2_triple_extractor - INFO - Attempting GPT-3.5 fallback for chunk chunk_Isaac Hayes_7_0
2025-05-30 22:28:11,283 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-05-30 22:28:11,287 - module2_triple_extractor - INFO - GPT fallback successful: 10 triples from chunk_Isaac Hayes_7_0
2025-05-30 22:28:11,570 - module2_triple_extractor - ERROR - HF extraction failed for chunk chunk_FOOD_0_0: 402 Client Error: Payment Required for url: https://router.huggingface.co/together/v1/chat/completions (Request ID: Root=1-6839ce9b-08f8b24a75bf905c3852fd8f;b8a031a1-1a9e-4bbe-8d19-578179a9c9f2)

You have exceeded your monthly included credits for Inference Providers. Subscribe to PRO to get 20x more monthly included credits.
2025-05-30 22:28:11,570 - module2_triple_extractor - INFO - Attempting GPT-3.5 fallback for chunk chunk_FOOD_0_0
2025-05-30 22:28:12,986 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-05-30 22:28:12,996 - module2_triple_extractor - INFO - GPT fallback successful: 4 triples from chunk_FOOD_0_0
2025-05-30 22:28:13,261 - module2_triple_extractor - ERROR - HF extraction failed for chunk chunk_WATER_0_0: 402 Client Error: Payment Required for url: https://router.huggingface.co/together/v1/chat/completions (Request ID: Root=1-6839ce9d-6c7d3e1a63c7e38053555e92;1862764b-3dad-4121-8a3f-2ecfc8b1e555)

You have exceeded your monthly included credits for Inference Providers. Subscribe to PRO to get 20x more monthly included credits.
2025-05-30 22:28:13,261 - module2_triple_extractor - INFO - Attempting GPT-3.5 fallback for chunk chunk_WATER_0_0
2025-05-30 22:28:15,051 - httpx - INFO - HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-05-30 22:28:15,051 - module2_triple_extractor - INFO - GPT fallback successful: 5 triples from chunk_WATER_0_0
2025-05-30 22:28:15,051 - module2_triple_extractor - INFO - Extraction completed: 85 triples from 10 chunks
2025-05-30 22:28:15,061 - module2_triple_extractor - INFO - HF success: 7, HF failed: 3
2025-05-30 22:28:15,061 - module2_triple_extractor - INFO - GPT success: 3, GPT failed: 0
2025-05-30 22:28:15,061 - pipeline_orchestrator - INFO - Triple extraction summary:
2025-05-30 22:28:15,064 - pipeline_orchestrator - INFO -   HF successful: 7/10
2025-05-30 22:28:15,065 - pipeline_orchestrator - INFO -   GPT fallback used: 3/3
2025-05-30 22:28:15,066 - pipeline_orchestrator - INFO -   Total failures: 0  
2025-05-30 22:28:15,066 - pipeline_orchestrator - INFO - Step 3: Detecting synonyms (no canonical mapping)...
2025-05-30 22:28:15,067 - module3_synonym_detector - INFO - Starting synonym detection from 85 triples
2025-05-30 22:28:15,069 - module3_synonym_detector - INFO - Detecting synonyms among 101 unique phrases
2025-05-30 22:28:15,070 - module3_synonym_detector - INFO - Generating embeddings for phrases...
Batches: 100%|█████████████████████████████████| 4/4 [00:01<00:00,  2.30it/s] 
2025-05-30 22:28:16,819 - module3_synonym_detector - INFO - Computing similarity matrix...
2025-05-30 22:28:16,822 - module3_synonym_detector - INFO - Finding synonym pairs...
2025-05-30 22:28:16,824 - module3_synonym_detector - INFO - Found 19 synonym pairs with threshold 0.8
2025-05-30 22:28:16,824 - module3_synonym_detector - INFO - Found 19 synonym pairs
2025-05-30 22:28:16,824 - module3_synonym_detector - INFO - Synonym detection statistics: {'total_synonym_pairs': 19, 'avg_similarity': np.float64(0.8545261464620891), 'min_similarity': np.float64(0.8044243454933167), 'max_similarity': np.float64(0.9845235347747803), 'unique_phrases_with_synonyms': 29}
2025-05-30 22:28:16,825 - pipeline_orchestrator - INFO - Step 4: Building Knowledge Graph (HippoRAG 2 style)...
2025-05-30 22:28:16,825 - module4_graph_builder - INFO - Initializing GraphBuilder (HippoRAG 2 style) with Neo4j at bolt://localhost:7687
2025-05-30 22:28:16,881 - module4_graph_builder - INFO - Successfully connected to Neo4j
2025-05-30 22:28:16,881 - module4_graph_builder - INFO - Clearing existing database...
2025-05-30 22:28:16,924 - utils.utils_neo4j - INFO - Cleared all data from Neo4j database
2025-05-30 22:28:17,021 - module4_graph_builder - INFO - Successfully cleared existing database
2025-05-30 22:28:17,021 - module4_graph_builder - INFO - Starting graph construction (HippoRAG 2 style with meaningful IDs)...
2025-05-30 22:28:17,021 - module4_graph_builder - INFO - Input data: 10 chunks, 85 triples, 19 synonym pairs
2025-05-30 22:28:17,021 - module4_graph_builder - INFO - NOTE: No canonical mapping - preserving all phrase surface forms
2025-05-30 22:28:17,022 - module4_graph_builder - INFO - Using normalized phrase text as node IDs for better readability
2025-05-30 22:28:17,022 - module4_graph_builder - INFO - Setting up database constraints and indexes...
2025-05-30 22:28:17,033 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (e:Phrase) REQUIRE (e.id) IS UNIQUE` has no effect.} {description: `CONSTRAINT phrase_id FOR (e:Phrase) REQUIRE (e.id) IS UNIQUE` already exists.} {position: None} for query: 'CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (p:Phrase) REQUIRE p.id IS UNIQUE'
2025-05-30 22:28:17,038 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (e:Passage) REQUIRE (e.id) IS UNIQUE` has no effect.} {description: `CONSTRAINT passage_id FOR (e:Passage) REQUIRE (e.id) IS UNIQUE` already exists.} {position: None} for query: 'CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (p:Passage) REQUIRE p.id IS UNIQUE'
2025-05-30 22:28:17,043 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (e:Phrase) ON EACH [e.text, e.normalized_text]` has no effect.} {description: `FULLTEXT INDEX phrase_text FOR (e:Phrase) ON EACH [e.text, e.normalized_text]` already exists.} {position: None} for query: 'CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (p:Phrase) ON EACH [p.text, p.normalized_text]'
2025-05-30 22:28:17,046 - neo4j.notifications - INFO - Received notification from DBMS server: {severity: INFORMATION} {code: Neo.ClientNotification.Schema.IndexOrConstraintAlreadyExists} {category: SCHEMA} {title: `CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (e:Passage) ON EACH [e.text, e.title]` has no effect.} {description: `FULLTEXT INDEX passage_text FOR (e:Passage) ON EACH [e.text, e.title]` already exists.} {position: None} for query: 'CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (p:Passage) ON EACH [p.text, p.title]'
2025-05-30 22:28:17,047 - module4_graph_builder - INFO - Database constraints and indexes setup completed
2025-05-30 22:28:17,047 - module4_graph_builder - INFO - Building nodes (preserving all surface forms)...
2025-05-30 22:28:17,047 - module4_graph_builder - INFO - Creating 10 Passage nodes...
2025-05-30 22:28:17,050 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-30 22:28:17,050 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00,  9.79it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 11.35it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00,  8.19it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 15.28it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 13.44it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00,  8.13it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00,  9.57it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00,  8.07it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 21.15it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 20.56it/s]
2025-05-30 22:28:22,706 - module4_graph_builder - INFO - Created 10 Passage nodes
2025-05-30 22:28:22,706 - module4_graph_builder - INFO - Creating Phrase nodes (HippoRAG 2 style - meaningful IDs)...
2025-05-30 22:28:22,707 - module4_graph_builder - INFO - Found 102 unique phrases (all surface forms preserved)
2025-05-30 22:28:22,710 - sentence_transformers.SentenceTransformer - INFO - Use pytorch device_name: cpu
2025-05-30 22:28:22,710 - sentence_transformers.SentenceTransformer - INFO - Load pretrained SentenceTransformer: sentence-transformers/paraphrase-multilingual-mpnet-base-v2
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 12.45it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 36.21it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 27.49it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 26.35it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 31.51it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.93it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 30.16it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.55it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.55it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 25.32it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.59it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 14.04it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.66it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.35it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 41.95it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 24.95it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 39.23it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 39.88it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 39.84it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 43.35it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 49.68it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 39.57it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.39it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.50it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 41.88it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 40.92it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.02it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 24.28it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 24.17it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 19.68it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 27.38it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 30.55it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.58it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 41.94it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.38it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 34.78it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 36.86it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 22.54it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 26.61it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 41.02it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 40.26it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.31it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 41.24it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.26it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.45it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.92it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 26.68it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.82it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.39it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.67it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.29it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.19it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 30.02it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 39.64it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 23.50it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 22.09it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 18.20it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 22.39it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 25.05it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 27.71it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.22it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 30.08it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 39.24it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 34.62it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 31.47it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.52it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 20.87it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 29.60it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 29.48it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 18.78it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 32.28it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 10.93it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 16.22it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 29.42it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 19.14it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.53it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 29.11it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 32.72it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 31.41it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 36.91it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 25.19it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 36.20it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.39it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 34.99it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 25.57it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.97it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.66it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.64it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 29.77it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.94it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 33.43it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.23it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 35.32it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 27.45it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 34.11it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 29.97it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 17.53it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 22.53it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.78it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 29.23it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 31.88it/s]
Batches: 100%|█████████████████████████████████| 1/1 [00:00<00:00, 28.67it/s]
2025-05-30 22:28:38,283 - module4_graph_builder - INFO - Created 102 Phrase nodes with meaningful IDs
2025-05-30 22:28:38,293 - module4_graph_builder - INFO - Example phrase ID mappings:
2025-05-30 22:28:38,293 - module4_graph_builder - INFO -   'hầu hết các cầu thủ khác' -> 'hầu_hết_các_cầu_thủ_khác'
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit       
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode       
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u1ea7' in position 61: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 239, in <module>   
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 176, in main       
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 129, in run_complete_pipeline
    self.graph_builder.build_graph_hipporag_style(chunks, triples, synonym_pairs)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 115, in build_graph_hipporag_style
    self._create_phrase_nodes_hipporag_style(triples)  # NO canonical mapping 
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 241, in _create_phrase_nodes_hipporag_style
    safe_unicode_log(logger, f"  '{phrase}' -> '{phrase_id}'", "info")        
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 19, in safe_unicode_log
    getattr(logger, level)(message)
Message: "  'hầu hết các cầu thủ khác' -> 'hầu_hết_các_cầu_thủ_khác'"
Arguments: ()
2025-05-30 22:28:38,299 - module4_graph_builder - INFO -   'giải oscar' -> 'giải_oscar'
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit       
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode       
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u1ea3' in position 62: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 239, in <module>   
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 176, in main       
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 129, in run_complete_pipeline
    self.graph_builder.build_graph_hipporag_style(chunks, triples, synonym_pairs)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 115, in build_graph_hipporag_style
    self._create_phrase_nodes_hipporag_style(triples)  # NO canonical mapping 
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 241, in _create_phrase_nodes_hipporag_style
    safe_unicode_log(logger, f"  '{phrase}' -> '{phrase_id}'", "info")        
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 19, in safe_unicode_log
    getattr(logger, level)(message)
Message: "  'giải oscar' -> 'giải_oscar'"
Arguments: ()
2025-05-30 22:28:38,303 - module4_graph_builder - INFO -   '35 tuổi' -> 'phrase_35_tuổi'
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit       
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode       
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u1ed5' in position 65: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 239, in <module>   
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 176, in main       
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 129, in run_complete_pipeline
    self.graph_builder.build_graph_hipporag_style(chunks, triples, synonym_pairs)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 115, in build_graph_hipporag_style
    self._create_phrase_nodes_hipporag_style(triples)  # NO canonical mapping 
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 241, in _create_phrase_nodes_hipporag_style
    safe_unicode_log(logger, f"  '{phrase}' -> '{phrase_id}'", "info")        
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 19, in safe_unicode_log
    getattr(logger, level)(message)
Message: "  '35 tuổi' -> 'phrase_35_tuổi'"
Arguments: ()
2025-05-30 22:28:38,308 - module4_graph_builder - INFO -   'sữa' -> 'sữa'     
--- Logging error ---
Traceback (most recent call last):
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\logging\__init__.py", line 1163, in emit       
    stream.write(msg + self.terminator)
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\Lib\encodings\cp1252.py", line 19, in encode       
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u1eef' in position 61: character maps to <undefined>
Call stack:
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 239, in <module>   
    exit_code = main()
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\run_offline_pipeline.py", line 176, in main       
    results = orchestrator.run_complete_pipeline(
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\pipeline_orchestrator.py", line 129, in run_complete_pipeline
    self.graph_builder.build_graph_hipporag_style(chunks, triples, synonym_pairs)
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 115, in build_graph_hipporag_style
    self._create_phrase_nodes_hipporag_style(triples)  # NO canonical mapping 
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 241, in _create_phrase_nodes_hipporag_style
    safe_unicode_log(logger, f"  '{phrase}' -> '{phrase_id}'", "info")        
  File "D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing\module4_graph_builder.py", line 19, in safe_unicode_log
    getattr(logger, level)(message)
Message: "  'sữa' -> 'sữa'"
Arguments: ()
2025-05-30 22:28:38,308 - module4_graph_builder - INFO -   'a singer' -> 'a_singer'
2025-05-30 22:28:38,313 - module4_graph_builder - INFO - Building edges...    
2025-05-30 22:28:38,313 - module4_graph_builder - INFO - Creating 85 RELATION edges (no canonical mapping)...
2025-05-30 22:28:39,100 - module4_graph_builder - INFO - Created 85 RELATION edges
2025-05-30 22:28:39,100 - module4_graph_builder - INFO - Creating 19 SYNONYM edges (HippoRAG 2 style)...
2025-05-30 22:28:39,304 - module4_graph_builder - INFO - Created 19 SYNONYM edges
2025-05-30 22:28:39,304 - module4_graph_builder - INFO - SYNONYM edges enable semantic connectivity between phrase variants
2025-05-30 22:28:39,305 - module4_graph_builder - INFO - Creating CONTAINS edges (no canonical mapping)...
2025-05-30 22:28:39,883 - module4_graph_builder - INFO - Created 104 CONTAINS edges
2025-05-30 22:28:39,883 - module4_graph_builder - INFO - Graph construction completed: 112 nodes, 208 edges
2025-05-30 22:28:39,883 - module4_graph_builder - INFO - HippoRAG 2 style: All phrase variants preserved, connected via synonym edges
2025-05-30 22:28:39,883 - module4_graph_builder - INFO - Getting graph statistics...
2025-05-30 22:28:39,883 - module4_graph_builder - INFO - Graph statistics: {'nodes': {'Passage': 10, 'Phrase': 102}, 'edges': {'RELATION': 85, 'SYNONYM': 38, 'CONTAINS': 104}, 'total_nodes': 112, 'total_edges': 227, 'hipporag_style': True, 'canonical_mapping': False, 'surface_forms_preserved': True, 'meaningful_phrase_ids': True}
2025-05-30 22:28:39,893 - pipeline_orchestrator - INFO - Saved triples with extraction methods to test\extracted_triples_with_methods.tsv
2025-05-30 22:28:39,893 - module3_synonym_detector - INFO - Saving 19 synonym pairs to test\detected_synonyms.tsv
2025-05-30 22:28:39,893 - module3_synonym_detector - INFO - Synonym pairs saved successfully
2025-05-30 22:28:39,896 - pipeline_orchestrator - INFO - Saved synonyms to test\detected_synonyms.tsv
2025-05-30 22:28:39,896 - pipeline_orchestrator - INFO - Pipeline completed successfully in 46.19 seconds

============================================================
OFFLINE PIPELINE SUMMARY (HippoRAG 2 Style + GPT Fallback)
============================================================
Execution Time: 46.19 seconds
Input File: test\test_data.xlsx
Pipeline Style: HippoRAG_2_with_GPT_Fallback
Canonical Mapping: False
GPT Fallback: True

EXCEL PROCESSING:
   Documents Loaded: 10
   Avg Length: 446.0 chars

CHUNKING:
   Total Chunks: 10
   Avg Chunk Length: 446.0 chars
   Method: keep_as_paragraph

TRIPLES (ROBUST EXTRACTION):
   Total: 85
   Unique Subjects: 28
   Unique Predicates: 55
   Unique Objects: 75
   Qwen Extracted: 66
   GPT-3.5 Extracted: 19
   HF Success Rate: 70.0% (7/10)
   GPT Fallback Success: 3/3 failures rescued
   Total Failures: 0
   ✅ All chunks successfully processed!

SYNONYMS (HippoRAG 2 Style):
   Synonym Pairs: 19
   Avg Similarity: 0.855
   Threshold Used: 0.8
   NOTE: No canonical mapping - all phrase variants preserved

KNOWLEDGE GRAPH:
   Total Nodes: 112
   Total Edges: 227
   Passage Nodes: 10
   Phrase Nodes: 102
   RELATION Edges: 85
   SYNONYM Edges: 38
   CONTAINS Edges: 104

HIPPORAG 2 + GPT FALLBACK FEATURES:
   - All phrase surface forms preserved
   - Synonym edges connect similar phrases
   - No information loss from canonical mapping
   - Robust extraction with GPT-3.5 fallback
   - Higher completion rate despite API failures
   - Ready for Personalized PageRank traversal
============================================================
Pipeline completed successfully!
Access Neo4j Browser: http://localhost:7474
============================================================
2025-05-30 22:28:39,903 - module4_graph_builder - INFO - Closing Neo4j connection
2025-05-30 22:28:39,903 - utils.utils_neo4j - INFO - Neo4j connection closed  
2025-05-30 22:28:39,903 - module4_graph_builder - INFO - Neo4j connection closed
2025-05-30 22:28:39,903 - root - INFO - Pipeline results saved to test\pipeline_results_hipporag_test_data.json
💾 Results saved to: test\pipeline_results_hipporag_test_data.json

============================================================
✅ PIPELINE COMPLETED SUCCESSFULLY (HippoRAG 2 Style)
============================================================
🌐 Access Neo4j Browser: http://localhost:7474
   Username: neo4j
   Password: graphrag123

📈 Extraction Statistics:
   HuggingFace successful: 7
   HuggingFace failed: 3
   GPT-3.5 fallback used: 3
   Total failures: 0

🏗️ HippoRAG 2 Graph Structure:
   - Passage nodes: Document chunks with embeddings
   - Phrase nodes: All surface forms preserved
   - RELATION edges: Semantic relationships
   - SYNONYM edges: Similarity connections
   - CONTAINS edges: Passage -> Phrase relationships

📝 Query Examples:
   1. Find synonyms: MATCH (p1:Phrase)-[:SYNONYM]-(p2:Phrase) RETURN p1, p2   
   2. Explore relations: MATCH (p1:Phrase)-[:RELATION]-(p2:Phrase) RETURN p1, p2
   3. Find passages: MATCH (passage:Passage)-[:CONTAINS]->(phrase:Phrase) RETURN passage, phrase
   4. Check extraction methods: MATCH ()-[r:RELATION]->() RETURN r.extraction_method, count(*)

🚀 Next steps:
   1. Explore graph in Neo4j Browser
   2. Run Personalized PageRank queries
   3. Test semantic search capabilities
   4. Check intermediate results in output files
   5. Verify all passages have CONTAINS edges
============================================================
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OfflineIndexing>
```