
# toàn bộ file pdf + code của phần Offline + mô tả ngắn gọn luồng Online. + Cây cấu trúc code của phần offline vào => Mục tiêu là ra cấu trúc của phần Online  => Mục tiêu là ra: Code các class các hàm cho từng file, viết docs thật chi tiết cho từng class, từng hàm (tuyệt đối ko code detail)  - GENSPARK VÀ MANUS. 

Chốt kiến trúc như này: 
```bash
📁 OnlineRetrievalAndQA/                      # 🌐 ONLINE PHASE
├── 📋 online_requirements.txt                # Dependencies for online phase
│
├── 🔍 module1_dual_retrieval.py              # Bước 1: Dual/Hybrid Retrieval
├── 🤖 module2_triple_filter.py               # Bước 2: LLM Triple Filtering  
├── 📊 module3_passage_ranker.py              # Bước 3: Triple-based Passage Ranking
├── 🎯 module4_context_expander.py            # Bước 4: 1-hop Context Expansion (Optional)
├── 🗣️ module5_answer_generator.py            # Bước 5: Final Answer Generation
│
├── 🎯 online_pipeline_orchestrator.py        # Pipeline Logic Coordinator (Core orchestration)
│
├── 🔍 run_retrieval_pipeline.py              # Run Retrieval Only (Steps 1-3/4)
│                                             # Args: --enable_expansion True/False
├── 🌐 run_retrieval_and_qa_pipeline.py       # Run Full Pipeline (Steps 1-5)
│                                             # Args: --enable_expansion True/False
│
├── 📁 utils/                                 # 🔧 UTILS BY MODULE
│   ├── 📁 module1_utils/                     # 🔍 Dual Retrieval Utils
│   │   ├── 🔤 utils_bm25.py                  # BM25 implementation
│   │   ├── 🧠 utils_embedding.py             # Dense retrieval utilities
│   │   └── 🎭 utils_hybrid_scoring.py        # Score combination methods
│   │
│   ├── 📁 module2_utils/                     # 🤖 Triple Filter Utils
│   │   ├── 🤖 utils_llm_filter.py            # LLM filtering utilities
│   │   └── 📝 utils_filter_prompts.py        # Triple filtering prompts
│   │
│   ├── 📁 module3_utils/                     # 📊 Passage Ranker Utils
│   │   ├── 📈 utils_ranking.py               # Ranking algorithms
│   │   └── 🎯 utils_relevance.py             # Relevance calculation
│   │
│   ├── 📁 module4_utils/                     # 🎯 Context Expander Utils
│   │   ├── 🔗 utils_graph_query.py           # Neo4j/KG query utilities
│   │   └── 🔄 utils_expansion.py             # 1-hop expansion logic
│   │
│   ├── 📁 module5_utils/                     # 🗣️ Answer Generator Utils
│   │   ├── 🤖 utils_llm_generator.py         # LLM generation utilities
│   │   ├── 📝 utils_answer_prompts.py        # Answer generation prompts
│   │   └── 🎨 utils_formatting.py            # Response formatting
│   │
│   └── 📁 shared_utils/                      # 🔧 Shared Utilities
│       ├── 🔧 utils_general.py               # General online utilities
│       ├── 📊 utils_logging.py               # Logging utilities
│       └── ⚙️ utils_config.py                # Configuration management
│
└── 📁 test/                                  # 🧪 TESTING
    ├── 🧪 test_dual_retrieval.py             # Test Module 1
    ├── 🤖 test_triple_filter.py              # Test Module 2  
    ├── 📊 test_passage_ranker.py             # Test Module 3
    ├── 🎯 test_context_expander.py           # Test Module 4
    ├── 🗣️ test_answer_generator.py           # Test Module 5
    ├── 🔍 test_retrieval_pipeline.py         # Test retrieval only
    ├── 🌐 test_full_pipeline.py              # Test full pipeline
    ├── 🎯 test_queries.json                  # Sample test queries
    └── 📊 test_expected_results.json         # Expected outputs
├── 📖 README.md
├── 📚 docs/
│   ├── 🚀 quickstart.md
│   └── 🔧 api_reference.md
├── 📁 outputs/
│   ├── 📁 retrieval_results/
│   └── 📁 final_answers/
├── 📁 configs/
│   └── ⚙️ config.yaml
```


Code các class các hàm cho từng file, viết docs thật chi tiết cho từng class, từng hàm 
(tuyệt đối ko code detail)



```bash
toàn bộ file pdf + code của phần Offline + cây cấu trúc của toàn bộ dự án và mô tả ngắn gọn luồng Online. 

===
1. Summary lại pha offline và online tôi đã gửi 
2. Hiểu và summary lại code pha online tôi gửi 
3. Hiểu kiến trúc code tôi đã gửi 
```
