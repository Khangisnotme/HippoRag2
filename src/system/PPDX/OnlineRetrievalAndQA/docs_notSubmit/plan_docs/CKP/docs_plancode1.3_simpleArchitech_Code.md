# 📁 Cấu trúc OnlineRetrievalAndQA (Updated Utils Structure)

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
├── 📁 utils/                                 # 🔧 UTILS FLATTENED BY MODULE
│   ├── 🔍 utils_module1_dual_retrieval.py    # All Module 1 utilities
│   ├── 🤖 utils_module2_triple_filter.py     # All Module 2 utilities
│   ├── 📊 utils_module3_passage_ranker.py    # All Module 3 utilities
│   ├── 🎯 utils_module4_context_expander.py  # All Module 4 utilities
│   ├── 🗣️ utils_module5_answer_generator.py  # All Module 5 utilities
│   ├── 🔧 utils_shared_general.py            # General shared utilities
│   ├── 📊 utils_shared_logging.py            # Logging utilities
│   └── ⚙️ utils_shared_config.py             # Configuration management
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
├── .env.example
```

---

## 🗂️ **Utils Files Breakdown:**

### **📁 utils/ (Flattened Structure)**

#### **🔍 utils_module1_dual_retrieval.py**
```python
# Contains all Module 1 utilities:
# - BM25 implementation
# - Dense retrieval utilities  
# - Score combination methods
# - Hybrid scoring algorithms
```

#### **🤖 utils_module2_triple_filter.py**
```python
# Contains all Module 2 utilities:
# - LLM filtering utilities (Qwen + GPT backup)
# - Triple filtering prompts
# - Response parsing logic
# - Batch filtering support
```

#### **📊 utils_module3_passage_ranker.py**
```python
# Contains all Module 3 utilities:
# - Ranking algorithms
# - Relevance calculation methods
# - Triple-passage support scoring
# - Score combination logic
```

#### **🎯 utils_module4_context_expander.py**
```python
# Contains all Module 4 utilities:
# - Neo4j/KG query utilities
# - 1-hop expansion logic
# - Graph traversal methods
# - Context scoring algorithms
```

#### **🗣️ utils_module5_answer_generator.py**
```python
# Contains all Module 5 utilities:
# - LLM generation utilities (Qwen + GPT backup)
# - Answer generation prompts
# - Response formatting
# - Citation handling
```

#### **🔧 utils_shared_general.py**
```python
# Contains shared utilities:
# - Text processing functions
# - Data validation methods
# - Common helper functions
# - Error handling utilities
```

#### **📊 utils_shared_logging.py**
```python
# Contains logging utilities:
# - Logger setup and configuration
# - Performance monitoring
# - Statistics collection
# - Debug utilities
```

#### **⚙️ utils_shared_config.py**
```python
# Contains configuration utilities:
# - Configuration loading
# - Parameter validation
# - Environment setup
# - Settings management
```

---

## 📦 **Import Examples với New Structure:**

### **Module Imports:**
```python
# In module1_dual_retrieval.py
from utils.utils_module1_dual_retrieval import (
    BM25Retriever,
    EmbeddingRetriever, 
    HybridScorer,
    combine_hybrid_retrieval_scores
)
from utils.utils_shared_general import normalize_text, validate_query
from utils.utils_shared_logging import get_logger

# In module2_triple_filter.py  
from utils.utils_module2_triple_filter import (
    LLMTripleFilter,
    FilterPromptTemplate,
    parse_llm_response,
    batch_filter_triples
)
from utils.utils_shared_config import load_llm_config
from utils.utils_shared_logging import get_logger

# In module3_passage_ranker.py
from utils.utils_module3_passage_ranker import (
    TripleBasedRanker,
    RelevanceCalculator,
    PassageScorer,
    combine_ranking_scores
)
from utils.utils_shared_general import validate_passages
```

---

## ✅ **Benefits của Flattened Utils Structure:**

### **1. 🎯 Simplicity**
- **Ít folders hơn**: Easier navigation
- **Clear naming**: Tên file explicit về module
- **Direct imports**: Straightforward import paths

### **2. 📦 Module Cohesion**  
- **All utilities** cho một module trong một file
- **Related functions** grouped together
- **Easy maintenance** của module-specific code

### **3. 🔧 Import Clarity**
- **Explicit imports**: Rõ ràng utilities nào từ module nào
- **Reduced nesting**: Ít nested folders
- **Clean structure**: Dễ understand và navigate

### **4. 📊 File Organization**
| File | Purpose | Contains |
|------|---------|----------|
| `utils_module1_dual_retrieval.py` | Module 1 support | BM25, Embedding, Hybrid scoring |
| `utils_module2_triple_filter.py` | Module 2 support | LLM filtering, Prompts, Parsing |
| `utils_module3_passage_ranker.py` | Module 3 support | Ranking, Relevance, Scoring |
| `utils_module4_context_expander.py` | Module 4 support | Graph queries, Expansion logic |
| `utils_module5_answer_generator.py` | Module 5 support | Generation, Prompts, Formatting |
| `utils_shared_*.py` | Cross-module | General, Logging, Config utilities |

---

## 🔄 **Migration từ Nested Structure:**

### **Before (Nested):**
```python
from utils.module1_utils.utils_bm25 import BM25Retriever
from utils.module1_utils.utils_embedding import EmbeddingRetriever  
from utils.shared_utils.utils_general import normalize_text
```

### **After (Flattened):**
```python
from utils.utils_module1_dual_retrieval import BM25Retriever, EmbeddingRetriever
from utils.utils_shared_general import normalize_text
```

---

## 🎯 **Final Structure Assessment:**

### **✅ Pros của Flattened Utils:**
- **Simpler navigation** - less clicking through folders
- **Clear module association** - tên file explicit
- **Easier imports** - shorter import paths
- **Better file organization** - related code grouped

### **⚠️ Considerations:**
- **Larger files** - more code per file (but manageable)
- **Potential for long files** - need good internal organization

### **📋 Recommendation:**
**✅ Flattened structure is BETTER** cho project này vì:
- Simplicity outweighs complexity
- Clear module-to-utils mapping
- Easier maintenance và navigation
- More straightforward for development

**🎉 Updated structure approved và ready for implementation!**