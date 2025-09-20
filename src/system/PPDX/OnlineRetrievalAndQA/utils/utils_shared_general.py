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
    
    text = text.lower()
    
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
