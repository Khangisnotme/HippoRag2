"""
General Utilities
Common helper functions cho offline pipeline
"""

from pathlib import Path
from typing import Dict, Any, List
import json
import logging
from datetime import datetime
import os

def setup_logging(log_level: str = "INFO", log_file: Path = None):
    """Setup logging configuration"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup handlers
    handlers = [logging.StreamHandler()]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    # Configure logging
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def save_pipeline_results(results: Dict[str, Any], output_path: Path):
    """Save pipeline results to JSON"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        logging.info(f"Pipeline results saved to {output_path}")
        
    except Exception as e:
        logging.error(f"Error saving pipeline results: {e}")

def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration từ JSON file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        logging.info(f"Configuration loaded from {config_path}")
        return config
        
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return {}

def check_dependencies() -> bool:
    """Check if all required dependencies are available"""
    dependencies = {
        'neo4j': 'Neo4j driver',
        'pandas': 'Data processing', 
        'sentence_transformers': 'Embedding models',
        'huggingface_hub': 'HF Inference API',
        'openpyxl': 'Excel file support',
        'sklearn': 'Machine learning utilities'
    }
    
    missing_deps = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            logging.debug(f"✅ {dep}: {description}")
        except ImportError:
            missing_deps.append(dep)
            logging.error(f"❌ {dep}: {description} - MISSING")
    
    if missing_deps:
        logging.error(f"Missing dependencies: {missing_deps}")
        logging.error("Install with: pip install " + " ".join(missing_deps))
        return False
    
    logging.info("All dependencies are available")
    return True

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"

def get_file_info(file_path: Path) -> Dict[str, Any]:
    """Get comprehensive file information"""
    if not file_path.exists():
        return {'exists': False}
    
    stat = file_path.stat()
    
    return {
        'exists': True,
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'modified_time': datetime.fromtimestamp(stat.st_mtime),
        'created_time': datetime.fromtimestamp(stat.st_ctime),
        'is_file': file_path.is_file(),
        'is_dir': file_path.is_dir(),
        'suffix': file_path.suffix,
        'name': file_path.name
    }

def check_environment() -> bool:
    """Check if environment is properly setup"""
    checks = {
        'Dependencies': check_dependencies(),
        'Neo4j Connection': _check_neo4j_connection(),
        'HuggingFace API': _check_huggingface_api()
    }
    
    print("\n🔍 Environment Check:")
    print("=" * 40)
    
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:<20}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 40)
    
    if all_passed:
        print("🎉 Environment is ready!")
    else:
        print("⚠️  Please fix the issues above")
    
    return all_passed

def _check_neo4j_connection() -> bool:
    """Check Neo4j connection"""
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "graphrag123"))
        with driver.session() as session:
            session.run("RETURN 1")
        driver.close()
        return True
    except:
        return False

def _check_huggingface_api() -> bool:
    """Check HuggingFace API availability"""
    try:
        from huggingface_hub import InferenceClient
        # Just check if we can create client (don't make actual call)
        client = InferenceClient(provider="together", api_key="test")
        return True
    except:
        return False

def create_directory_structure(base_path: Path):
    """Create project directory structure"""
    directories = [
        base_path / "data" / "raw",
        base_path / "data" / "processed", 
        base_path / "data" / "outputs",
        base_path / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {directory}")

def get_api_key_from_env() -> str:
    """Get HuggingFace API key từ environment variables"""
    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        raise ValueError("HF_API_KEY environment variable not set")
    return api_key

if __name__ == "__main__":
    check_environment()