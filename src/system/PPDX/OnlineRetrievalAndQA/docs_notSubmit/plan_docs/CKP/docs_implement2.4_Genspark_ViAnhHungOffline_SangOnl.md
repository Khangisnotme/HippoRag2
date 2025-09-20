# docs_implement2.4_Genspark_ViAnhHungOffline_SangOnl.md: Ko còn nhiều time và các lần thử Cursor, Manus thất bại quá -> mình đã chạy Claude Opus rồi nhưng tạm bỏ -> qua genspark trước vì tỉ lệ thành công ở nó siêu cao. CHECK XEM NHỚ RÕ PHA ONLINE VÀ OFFLINE KO? ----- QUÊN MẤT THÀNH CÔNG CỦA GENSPARK LÀ TỪ PDF REPORT RA LUÔN THẲNG TỪNG FILE CODE MỖI FILE 400-500 DÒNG, HẾT LẠI CONTINUE --- Đi đường vòng nào là genspark và cursor ra CLASS, DEF, DOCS --- xong lại code tiếp bằng cursor, manus, claude, ... VẪN BUG --- QUAY LẠI VỚI MANUS 1 PHÁT THẲNG RA CODE LUÔN KO CẦN QUA CLASS, DEF, DOCS TRƯỚC. 

# 2. 🏗️ **Nhớ rõ pha Offline! Đây là luồng 4 modules:**

## 🎯 **Tóm tắt Offline Phase (4 Modules):**

### **📋 Workflow Overview:**
```
Documents → Module 1 → Module 2 → Module 3 → Module 4 → Knowledge Graph
```

---

## 🔄 **Chi tiết từng bước:**

### **📄 Module 1: Document Chunking**
**🎯 Mục đích:** Chia documents thành passages có nghĩa
- **Input:** Raw documents (Excel files)
- **Process:** Simple chunking - giữ nguyên paragraphs từ Excel
- **Output:** Document chunks với metadata
- **Implementation:** Keep as paragraph (1 document = 1 chunk)

### **🧠 Module 2: Triple Extraction (OpenIE)**
**🎯 Mục đích:** Extract structured knowledge từ text
- **Input:** Document chunks
- **Process:** 
  - **Primary:** Qwen2.5-7B extract triples `(subject, predicate, object)`
  - **Backup:** GPT-3.5-Turbo khi Qwen fail
- **Output:** Extracted triples với metadata
- **Schema:** Schema-less open KG (không giới hạn relation types)

### **🔗 Module 3: Synonym Detection**
**🎯 Mục đích:** Tìm các phrases đồng nghĩa
- **Input:** Extracted triples
- **Process:**
  - Extract unique phrases từ subjects/objects
  - Generate embeddings (paraphrase-multilingual-mpnet-base-v2)
  - Calculate similarity (cosine similarity)
  - Threshold = 0.8 (HippoRAG 2 style)
- **Output:** Synonym pairs với similarity scores

### **🏗️ Module 4: Graph Builder (KG Integration)**
**🎯 Mục đích:** Xây dựng complete Knowledge Graph
- **Input:** Chunks + Triples + Synonym pairs
- **Process:**
  - Create **Passage nodes** (documents)
  - Create **Phrase nodes** (entities/concepts) 
  - Create **RELATION edges** (subject→object)
  - Create **SYNONYM edges** (bidirectional)
  - Create **CONTAINS edges** (passage→phrases)
- **Output:** Complete KG trong Neo4j

---

## 🏗️ **HippoRAG 2 Style Implementation:**

### **🔑 Key Design Decisions:**

#### **✅ NO Canonical Mapping:**
- **Preserve all surface forms** - không merge synonyms thành 1 node
- **Individual nodes** cho mỗi phrase variant
- **SYNONYM edges** connect similar phrases

#### **✅ Synonym Edges:**
- **Threshold 0.8** (HippoRAG 2 standard)
- **Bidirectional edges** với similarity scores
- **Enable semantic connectivity** giữa phrase variants

#### **✅ Robust Extraction:**
- **Primary:** Qwen2.5-7B-Instruct
- **Backup:** GPT-3.5-Turbo automatic fallback
- **Zero failure rate** với backup system

---

## 📊 **Graph Architecture:**

### **🔷 Nodes:**
- **Passage Nodes:** Represent document chunks
- **Phrase Nodes:** Represent entities/concepts (ALL surface forms preserved)

### **🔗 Edges:**
- **RELATION:** `(subject) -[predicate]-> (object)`
- **SYNONYM:** `(phrase1) <-[similarity]-> (phrase2)`
- **CONTAINS:** `(passage) -[contains]-> (phrase)`

### **📈 Example Graph:**
```
Passage_1 -[CONTAINS]-> "táo"
Passage_1 -[CONTAINS]-> "apple" 
"táo" -[SYNONYM]-> "apple" (similarity: 0.96)
"táo" -[RELATION]-> "chất xơ" (predicate: "chứa")
```

---

## 📂 **Architecture Mapping:**

| Module | File | Key Function | Output |
|--------|------|--------------|---------|
| **1** | `module1_chunking.py` | `process_documents()` | Document chunks |
| **2** | `module2_triple_extractor.py` | `extract_triples()` | Extracted triples |
| **3** | `module3_synonym_detector.py` | `detect_synonyms()` | Synonym pairs |
| **4** | `module4_graph_builder.py` | `build_graph()` | Complete KG |

### **🎯 Orchestration:**
- **`pipeline_orchestrator.py`** - Coordinates all modules
- **`run_offline_pipeline.py`** - Main entry point

---

## 🧪 **Execution Results (From Previous Run):**

### **📊 Performance Stats:**
```
✅ Pipeline completed successfully in 42.21 seconds
📊 Documents: 10 → Chunks: 10 → Triples: 87 → Synonyms: 22
🏗️ Graph: 111 nodes, 234 edges
🤖 LLM Usage: Qwen 71 triples + GPT 16 triples (backup rescue)
```

### **🔢 Graph Statistics:**
- **Passage Nodes:** 10
- **Phrase Nodes:** 101 (all surface forms preserved)
- **RELATION Edges:** 87
- **SYNONYM Edges:** 44 (22 pairs × 2 bidirectional)
- **CONTAINS Edges:** 103

---

## 🎯 **HippoRAG 2 Compliance:**

| Feature | HippoRAG 2 Standard | Our Implementation | Status |
|---------|-------------------|-------------------|--------|
| **Surface Form Preservation** | Required | ✅ All preserved | ✅ |
| **Synonym Edges** | High volume | 44 edges | ✅ |
| **Bidirectional Synonyms** | Required | ✅ Implemented | ✅ |
| **No Node Merging** | Required | ✅ Confirmed | ✅ |
| **Threshold 0.8** | Standard | ✅ Used | ✅ |
| **Semantic Embeddings** | Required | ✅ All nodes | ✅ |

---

## 🚀 **Integration với Online:**

### **📋 Data Flow:**
```
Offline: Excel → KG in Neo4j
Online: Query → KG retrieval → Answer
```

### **🔗 Connection Point:**
- **Neo4j Database** - Bridge giữa Offline và Online
- **Same connection**: `bolt://localhost:7687`
- **Ready for retrieval** - Graph sẵn sàng cho Online queries

---

## 📁 **File Structure (Implemented):**

```bash
📁 OfflineIndexing/
├── 📄 module1_chunking.py              ✅ DONE
├── 🧠 module2_triple_extractor.py      ✅ DONE  
├── 🔗 module3_synonym_detector.py      ✅ DONE
├── 🏗️ module4_graph_builder.py         ✅ DONE
├── 🎯 pipeline_orchestrator.py         ✅ DONE
├── 🚀 run_offline_pipeline.py          ✅ DONE
└── 📁 utils/ (Neo4j, Excel, General)   ✅ DONE
```

---

## ✅ **Confirmed - Offline Phase Complete!**

**🎉 Hoàn toàn nhớ rõ Offline Phase! Đã được implement và tested thành công.**

**🔗 Ready to connect với Online Phase:**
- KG đã sẵn sàng trong Neo4j
- Architecture HippoRAG 2 compliant
- Robust extraction với backup system
- All surface forms preserved với synonym edges

**Bây giờ implement Online Phase để complete full system! 🚀**



# 3. 🌐 **Nhớ rõ pha Online! Đây là luồng 5 bước:**

## 🎯 **Tóm tắt Online Phase (5 Modules):**

### **📋 Workflow Overview:**
```
Query → Module 1 → Module 2 → Module 3 → Module 4 (Optional) → Module 5 → Answer
```

---

## 🔄 **Chi tiết từng bước:**

### **🔍 Module 1: Dual/Hybrid Retrieval**
**🎯 Mục đích:** Tận dụng Hybrid Search
- **Input:** User query
- **Process:** 
  - **Passages:** BM25 + Embedding → Top-K passages (20-50)
  - **Triples:** BM25 + Embedding → Top-N triples (20-50)
- **Output:** Raw Passages + Raw Triples

### **🤖 Module 2: LLM Triple Filtering**
**🎯 Mục đích:** Giữ lại triples phù hợp với query
- **Input:** Raw Triples + Original Query
- **Process:** Qwen2.5-7B (+ GPT-3.5 backup) đánh giá và chọn facts cốt lõi
- **Output:** Filtered Triples (Top-M, ~10-20 triples chất lượng cao)

### **📊 Module 3: Passage Ranking based on Triples**
**🎯 Mục đích:** Lọc passages nhiễu bằng cách tính support score
- **Input:** Raw Passages + Filtered Triples
- **Process:**
  - Tính **Support Score:** đếm triples mà passage hỗ trợ
  - **Final Score = α × hybrid_retrieval_score + (1-α) × Support_Score**
  - Chọn Top-P passages (5-10 passages tốt nhất)
- **Output:** Ranked Passages

### **🎯 Module 4: Context Expansion (Optional)**
**🎯 Mục đích:** Mở rộng 1-hop cho Filtered Triples
- **Input:** Filtered Triples
- **Process:** 1-hop traversal trên Knowledge Graph (không lan rộng như PPR)
- **Output:** Expanded Context

### **🗣️ Module 5: Answer Generation**
**🎯 Mục đích:** Tạo câu trả lời cuối cùng
- **Input:** Query + Ranked Passages + Filtered Triples + Expanded Context
- **Process:**
  - Format thành structured prompt
  - Qwen2.5-7B (+ GPT-3.5 backup) generate answer
- **Output:** Final Answer với citations

---

## 🧠 **Core Innovation:**

### **🔑 Key Insight:**
**Sử dụng Filtered Triples làm "cầu nối" để cải thiện Passage Ranking**

### **💡 Workflow Logic:**
1. **Retrieve** cả passages và triples
2. **Filter triples** để có core facts 
3. **Use filtered triples** để re-rank passages
4. **Expand context** nếu cần (1-hop)
5. **Generate answer** từ tất cả context

### **⚡ Advantages:**
- **Bổ sung thông tin:** Passages (context) + Triples (facts)
- **Loại bỏ nhiễu:** Filtered Triples → Better Passage Selection
- **Mở rộng ngữ cảnh:** 1-hop expansion cho more info
- **Robust LLM:** Qwen primary + GPT backup = zero failures

---

## 📊 **Architecture Mapping:**

| Module | File | Key Function | Output |
|--------|------|--------------|---------|
| **1** | `module1_dual_retrieval.py` | `retrieve_dual()` | Raw Passages + Triples |
| **2** | `module2_triple_filter.py` | `filter_triples()` | Filtered Triples |
| **3** | `module3_passage_ranker.py` | `rank_passages()` | Ranked Passages |
| **4** | `module4_context_expander.py` | `expand_context()` | Expanded Context |
| **5** | `module5_answer_generator.py` | `generate_answer()` | Final Answer |

---

## 🚀 **Execution Modes:**

### **🔍 Retrieval-Only (`run_retrieval_pipeline.py`):**
```bash
python run_retrieval_pipeline.py --query "..." --enable_expansion True/False
# Output: Retrieved + Filtered + Ranked content (no answer)
```

### **🌐 Full Pipeline (`run_retrieval_and_qa_pipeline.py`):**
```bash
python run_retrieval_and_qa_pipeline.py --query "..." --enable_expansion True/False  
# Output: Complete answer với all intermediate results
```

---

## 🎯 **So với HippoRAG 2:**

| Aspect | HippoRAG 2 | Our Approach |
|--------|------------|--------------|
| **Graph Usage** | PPR (complex) | 1-hop expansion (simple) |
| **Triple Role** | Node selection | Passage filtering |
| **LLM Integration** | Limited | Robust (primary + backup) |
| **Focus** | Graph algorithms | Hybrid retrieval + LLM |

---

## ✅ **Confirmed - Ready to implement!**

**🎉 Hoàn toàn nhớ rõ Online Phase! Architecture đã được finalize và sẵn sàng coding.**

Bạn muốn bắt đầu implement module nào trước? 🚀


---

# 2.4.1 Code: utils/utils_shared_general.py 🚀 Bắt đầu code pha Online!

**Tôi sẽ bám sát style và patterns từ pha Offline đã implement.**

## 🎯 **Thứ tự implement:**

1. ✅ **utils/utils_shared_general.py** (foundation)
2. 🔍 **module1_dual_retrieval.py**
3. 🤖 **module2_triple_filter.py** 
4. 📊 **module3_passage_ranker.py**
5. 🎯 **module4_context_expander.py**
6. 🗣️ **module5_answer_generator.py**
7. 🎯 **online_pipeline_orchestrator.py**
8. 🚀 **run files**

---

## 📝 **File đầu tiên: utils/utils_shared_general.py**

```python
"""
Shared utilities cho OnlineRetrievalAndQA
Minimal utilities thực sự được share across modules
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import logging
import json
import time
import os
from datetime import datetime
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ==================== TEXT PROCESSING ====================

def normalize_text(text: str) -> str:
    """
    Normalize text cho consistent processing
    
    Args:
        text (str): Input text cần normalize
        
    Returns:
        str: Normalized text
    """
    if not text:
        return ""
    
    # Basic normalization
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces -> single space
    text = re.sub(r'\n+', ' ', text)  # Multiple newlines -> space
    
    return text

def clean_text(text: str) -> str:
    """
    Clean and preprocess text cho retrieval
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = normalize_text(text)
    
    # Remove special characters nhưng giữ Vietnamese
    text = re.sub(r'[^\w\s\u00C0-\u024F\u1E00-\u1EFF]', ' ', text)
    
    # Remove extra spaces again
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def validate_query(query: str) -> bool:
    """
    Validate user query
    
    Args:
        query (str): User query
        
    Returns:
        bool: True nếu query hợp lệ
    """
    if not query or not isinstance(query, str):
        return False
    
    query = query.strip()
    
    # Check minimum length
    if len(query) < 3:
        return False
    
    # Check maximum length
    if len(query) > 1000:
        return False
    
    # Check if not only special characters
    if not re.search(r'[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]', query):
        return False
    
    return True

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords từ text cho BM25
    
    Args:
        text (str): Input text
        max_keywords (int): Maximum keywords to extract
        
    Returns:
        List[str]: Extracted keywords
    """
    if not text:
        return []
    
    # Clean text
    text = clean_text(text.lower())
    
    # Split into words
    words = text.split()
    
    # Filter words (minimum 2 characters)
    keywords = [word for word in words if len(word) >= 2]
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for word in keywords:
        if word not in seen:
            seen.add(word)
            unique_keywords.append(word)
    
    return unique_keywords[:max_keywords]

# ==================== FILE I/O ====================

def save_json(data: Dict[str, Any], filepath: Path, indent: int = 2):
    """
    Save data to JSON file
    
    Args:
        data (Dict): Data to save
        filepath (Path): File path
        indent (int): JSON indentation
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    
    logger.debug(f"Saved JSON to {filepath}")

def load_json(filepath: Path) -> Dict[str, Any]:
    """
    Load data from JSON file
    
    Args:
        filepath (Path): File path
        
    Returns:
        Dict[str, Any]: Loaded data
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    logger.debug(f"Loaded JSON from {filepath}")
    return data

def save_text(text: str, filepath: Path):
    """
    Save text to file
    
    Args:
        text (str): Text to save
        filepath (Path): File path
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    logger.debug(f"Saved text to {filepath}")

def load_text(filepath: Path) -> str:
    """
    Load text from file
    
    Args:
        filepath (Path): File path
        
    Returns:
        str: Loaded text
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    logger.debug(f"Loaded text from {filepath}")
    return text

# ==================== LOGGING ====================

def setup_logger(name: str, level: str = "INFO", log_file: Optional[Path] = None) -> logging.Logger:
    """
    Setup logger với consistent format
    
    Args:
        name (str): Logger name
        level (str): Logging level
        log_file (Optional[Path]): Optional log file
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_performance(func_name: str, start_time: float, end_time: float, 
                   extra_info: Optional[Dict[str, Any]] = None):
    """
    Log performance metrics
    
    Args:
        func_name (str): Function name
        start_time (float): Start timestamp
        end_time (float): End timestamp
        extra_info (Optional[Dict]): Additional information
    """
    duration = end_time - start_time
    
    log_msg = f"{func_name} completed in {duration:.2f} seconds"
    
    if extra_info:
        info_str = ", ".join([f"{k}={v}" for k, v in extra_info.items()])
        log_msg += f" ({info_str})"
    
    logger.info(log_msg)

# ==================== VALIDATION ====================

def validate_pipeline_input(data: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Validate pipeline input data
    
    Args:
        data (Dict): Input data
        required_keys (List[str]): Required keys
        
    Returns:
        bool: True nếu valid
    """
    if not isinstance(data, dict):
        return False
    
    for key in required_keys:
        if key not in data:
            logger.error(f"Missing required key: {key}")
            return False
    
    return True

def validate_module_output(data: Any, module_name: str, expected_type: type = dict) -> bool:
    """
    Validate module output format
    
    Args:
        data (Any): Module output
        module_name (str): Module name for logging
        expected_type (type): Expected data type
        
    Returns:
        bool: True nếu valid
    """
    if not isinstance(data, expected_type):
        logger.error(f"{module_name} output has invalid type: {type(data)}, expected: {expected_type}")
        return False
    
    if expected_type == list and len(data) == 0:
        logger.warning(f"{module_name} returned empty list")
    
    return True

def validate_passages(passages: List[Dict[str, Any]]) -> bool:
    """
    Validate passages format
    
    Args:
        passages (List[Dict]): Passages to validate
        
    Returns:
        bool: True nếu valid
    """
    if not isinstance(passages, list):
        return False
    
    required_keys = ['passage_id', 'text']
    
    for passage in passages:
        if not isinstance(passage, dict):
            return False
        
        for key in required_keys:
            if key not in passage:
                logger.error(f"Passage missing key: {key}")
                return False
    
    return True

def validate_triples(triples: List[Dict[str, Any]]) -> bool:
    """
    Validate triples format
    
    Args:
        triples (List[Dict]): Triples to validate
        
    Returns:
        bool: True nếu valid
    """
    if not isinstance(triples, list):
        return False
    
    required_keys = ['subject', 'predicate', 'object']
    
    for triple in triples:
        if not isinstance(triple, dict):
            return False
        
        for key in required_keys:
            if key not in triple:
                logger.error(f"Triple missing key: {key}")
                return False
    
    return True

# ==================== ENVIRONMENT ====================

def load_environment_variables(env_file: Optional[Path] = None) -> Dict[str, str]:
    """
    Load environment variables từ .env file
    
    Args:
        env_file (Optional[Path]): Path to .env file
        
    Returns:
        Dict[str, str]: Environment variables
    """
    env_vars = {}
    
    # Load from system environment
    env_vars.update(dict(os.environ))
    
    # Load from .env file if exists
    if env_file is None:
        env_file = Path('.env')
    
    env_file = Path(env_file)
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"\'')
    
    return env_vars

def get_api_key(service: str, env_vars: Optional[Dict[str, str]] = None) -> Optional[str]:
    """
    Get API key cho specific service
    
    Args:
        service (str): Service name (huggingface, openai, etc.)
        env_vars (Optional[Dict]): Environment variables
        
    Returns:
        Optional[str]: API key nếu found
    """
    if env_vars is None:
        env_vars = load_environment_variables()
    
    # Common API key patterns
    key_patterns = {
        'huggingface': ['HUGGINGFACE_API_KEY', 'HF_API_KEY', 'HUGGINGFACE_TOKEN'],
        'openai': ['OPENAI_API_KEY', 'OPENAI_TOKEN'],
        'anthropic': ['ANTHROPIC_API_KEY', 'ANTHROPIC_TOKEN']
    }
    
    service = service.lower()
    if service in key_patterns:
        for pattern in key_patterns[service]:
            if pattern in env_vars:
                return env_vars[pattern]
    
    # Try direct service name
    service_key = f"{service.upper()}_API_KEY"
    if service_key in env_vars:
        return env_vars[service_key]
    
    logger.warning(f"API key not found for service: {service}")
    return None

# ==================== DATA CLASSES ====================

@dataclass
class PerformanceStats:
    """
    Data class cho performance statistics
    """
    start_time: float
    end_time: float
    duration: float
    operation: str
    success: bool = True
    error_message: Optional[str] = None
    extra_info: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.duration,
            'operation': self.operation,
            'success': self.success,
            'error_message': self.error_message,
            'extra_info': self.extra_info or {}
        }

@dataclass
class QueryMetadata:
    """
    Data class cho query metadata
    """
    query: str
    query_id: str
    timestamp: str
    normalized_query: str
    keywords: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'query': self.query,
            'query_id': self.query_id,
            'timestamp': self.timestamp,
            'normalized_query': self.normalized_query,
            'keywords': self.keywords
        }

# ==================== UTILITY FUNCTIONS ====================

def generate_id(prefix: str = "") -> str:
    """
    Generate unique ID với timestamp
    
    Args:
        prefix (str): Optional prefix
        
    Returns:
        str: Unique ID
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    if prefix:
        return f"{prefix}_{timestamp}"
    return timestamp

def create_query_metadata(query: str) -> QueryMetadata:
    """
    Create query metadata object
    
    Args:
        query (str): User query
        
    Returns:
        QueryMetadata: Query metadata
    """
    query_id = generate_id("query")
    timestamp = datetime.now().isoformat()
    normalized_query = normalize_text(query)
    keywords = extract_keywords(query)
    
    return QueryMetadata(
        query=query,
        query_id=query_id,
        timestamp=timestamp,
        normalized_query=normalized_query,
        keywords=keywords
    )

def merge_scores(scores: List[float], weights: List[float] = None) -> float:
    """
    Merge multiple scores với optional weights
    
    Args:
        scores (List[float]): Scores to merge
        weights (List[float]): Optional weights
        
    Returns:
        float: Merged score
    """
    if not scores:
        return 0.0
    
    if weights is None:
        weights = [1.0] * len(scores)
    
    if len(scores) != len(weights):
        raise ValueError("Scores and weights must have same length")
    
    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
    total_weight = sum(weights)
    
    return weighted_sum / total_weight if total_weight > 0 else 0.0

# ==================== TEST FUNCTIONS ====================

def test_utilities():
    """Test basic utilities"""
    print("🧪 Testing shared utilities...")
    
    # Test text processing
    test_text = "  Đây là   text\n\n  có nhiều khoảng trắng  "
    normalized = normalize_text(test_text)
    print(f"Normalized: '{normalized}'")
    
    # Test query validation
    valid_query = "Lợi ích của táo là gì?"
    invalid_query = "x"
    print(f"Valid query: {validate_query(valid_query)}")
    print(f"Invalid query: {validate_query(invalid_query)}")
    
    # Test keywords extraction
    keywords = extract_keywords("Lợi ích của táo đối với sức khỏe con người")
    print(f"Keywords: {keywords}")
    
    # Test query metadata
    metadata = create_query_metadata("Test query")
    print(f"Query metadata: {metadata.to_dict()}")
    
    # Test score merging
    merged_score = merge_scores([0.8, 0.6, 0.9], [0.5, 0.3, 0.2])
    print(f"Merged score: {merged_score}")
    
    print("✅ Utilities test completed!")

if __name__ == "__main__":
    test_utilities()
```

## ✅ **File đầu tiên hoàn thành!**

**Key features:**
- **Text processing** cho Vietnamese + English
- **File I/O** với proper error handling  
- **Logging** setup consistent với Offline phase
- **Validation** cho pipeline data
- **Environment** management
- **Performance** tracking utilities
- **Data classes** cho structured data

**🎯 Style consistency với Offline:**
- Same logging patterns
- Same error handling approach  
- Same validation philosophy
- Same documentation style

**Tiếp theo: Module 1 - Dual Retrieval! 🔍**



```bash
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OnlineRetrievalAndQA> python .\utils\utils_shared_general.py
🧪 Testing shared utilities...
Normalized: 'Đây là text có nhiều khoảng trắng'
Valid query: True
Invalid query: False
Keywords: ['lợi', 'ích', 'của', 'táo', 'đối', 'với', 'sức', 'khỏe', 'con', 'người']
Query metadata: {'query': 'Test query', 'query_id': 'query_20250531_033111_862', 'timestamp': '2025-05-31T03:31:11.863474', 'normalized_query': 'Test query', 'keywords': ['test', 'query']}
Merged score: 0.76
✅ Utilities test completed!
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\PPDX\OnlineRetrievalAndQA>
```


# ✅ **Excellent! Utilities hoạt động perfect!**

## 🎯 **Analysis của test results:**

### **🔥 All functions work correctly:**

1. **✅ Text Normalization:**
   ```
   Input:  "  Đây là   text\n\n  có nhiều khoảng trắng  "
   Output: 'Đây là text có nhiều khoảng trắng'
   ```
   - Perfect cleanup của extra spaces và newlines

2. **✅ Query Validation:**
   ```
   Valid query: True    # "Lợi ích của táo là gì?" - hợp lệ
   Invalid query: False # "x" - quá ngắn
   ```
   - Logic validation chính xác

3. **✅ Keywords Extraction:**
   ```
   Input: "Lợi ích của táo đối với sức khỏe con người"
   Output: ['lợi', 'ích', 'của', 'táo', 'đối', 'với', 'sức', 'khỏe', 'con', 'người']
   ```
   - Vietnamese text processing hoạt động tốt
   - Properly lowercase và split

4. **✅ Query Metadata Generation:**
   ```
   {
     'query': 'Test query',
     'query_id': 'query_20250531_033111_862',  # Unique timestamp-based ID
     'timestamp': '2025-05-31T03:31:11.863474', # ISO format
     'normalized_query': 'Test query',
     'keywords': ['test', 'query']
   }
   ```
   - Perfect metadata structure for tracking

5. **✅ Score Merging:**
   ```
   Scores: [0.8, 0.6, 0.9]
   Weights: [0.5, 0.3, 0.2]
   Result: 0.76 = (0.8×0.5 + 0.6×0.3 + 0.9×0.2) / (0.5+0.3+0.2)
   ```
   - Weighted average calculation chính xác

---

## 🚀 **Ready for Module 1!**

**Foundation utilities đã solid:**
- ✅ Vietnamese text handling
- ✅ Data validation
- ✅ Performance tracking
- ✅ Metadata generation
- ✅ Score calculations

**🔍 Tiếp theo: Module 1 - Dual Retrieval**

Bắt đầu implement `module1_dual_retrieval.py` với:
- BM25 + Embedding hybrid search
- Neo4j connection (reuse từ Offline)
- Passage và Triple retrieval
- Score combination

**Sẵn sàng code Module 1! 🚀**