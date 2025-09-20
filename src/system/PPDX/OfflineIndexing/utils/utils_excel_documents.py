"""
Excel Document Processing Utilities
Load và process documents từ Excel files
"""

from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class ExcelDocumentProcessor:
    """Process documents từ Excel files"""
    
    def __init__(self):
        self.processed_documents = []
        
    def load_excel_file(self, file_path: Path) -> pd.DataFrame:
        """Load Excel file và validate structure"""
        try:
            df = pd.read_excel(file_path)
            
            # Validate required columns
            required_cols = ['doc_id', 'title', 'text']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Remove empty rows
            df = df.dropna(subset=['doc_id', 'text'])
            
            logger.info(f"Loaded {len(df)} documents from {file_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            raise
    
    def process_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process DataFrame thành list of documents"""
        documents = []
        
        for _, row in df.iterrows():
            doc = {
                'doc_id': str(row['doc_id']).strip(),
                'title': str(row['title']).strip() if pd.notna(row['title']) else "",
                'text': str(row['text']).strip(),
                'metadata': {
                    'source': 'excel_input',
                    'original_length': len(str(row['text'])),
                    'row_index': row.name if hasattr(row, 'name') else 0
                }
            }
            
            # Basic text cleaning
            doc['text'] = self._clean_text(doc['text'])
            
            # Skip empty documents
            if len(doc['text'].strip()) > 0:
                documents.append(doc)
        
        self.processed_documents = documents
        logger.info(f"Processed {len(documents)} documents")
        return documents
    
    def load_and_process_excel(self, file_path: Path) -> List[Dict[str, Any]]:
        """Complete workflow: load Excel và process documents"""
        df = self.load_excel_file(file_path)
        documents = self.process_dataframe(df)
        return documents
    
    def _clean_text(self, text: str) -> str:
        """Basic text cleaning"""
        if not text or pd.isna(text):
            return ""
        
        # Remove extra whitespaces
        text = ' '.join(text.split())
        
        # Basic cleaning - keep Vietnamese characters
        # text = re.sub(r'[^\w\s\u00C0-\u017F]', '', text)  # Uncomment if needed
        
        return text.strip()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        if not self.processed_documents:
            return {}
        
        texts = [doc['text'] for doc in self.processed_documents]
        
        return {
            'total_documents': len(self.processed_documents),
            'avg_text_length': sum(len(text) for text in texts) / len(texts),
            'min_text_length': min(len(text) for text in texts),
            'max_text_length': max(len(text) for text in texts),
            'total_characters': sum(len(text) for text in texts)
        }
    
    def validate_excel_structure(self, file_path: Path) -> bool:
        """Validate Excel file có đúng structure không"""
        try:
            df = pd.read_excel(file_path)
            required_columns = ['doc_id', 'title', 'text']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                return False
            
            if df.empty:
                logger.error("Excel file is empty")
                return False
            
            # Check for empty essential columns
            if df['doc_id'].isna().any() or df['text'].isna().any():
                logger.error("Found empty doc_id or text values")
                return False
            
            logger.info(f"Excel file validation passed: {len(df)} rows")
            return True
            
        except Exception as e:
            logger.error(f"Error validating Excel file: {e}")
            return False

# Test function
def test_excel_processor():
    """Test Excel document processor"""
    processor = ExcelDocumentProcessor()
    
    # Test with sample data
    test_data = pd.DataFrame({
        'doc_id': ['PH_0', 'PH_1'],
        'title': ['pH Basics', 'Chemistry'],
        'text': [
            'Các dung dịch nước có giá trị pH nhỏ hơn 7 được coi là có tính axít.',
            'Nước tinh khiết có pH = 7, được coi là trung tính.'
        ]
    })
    
    docs = processor.process_dataframe(test_data)
    stats = processor.get_statistics()
    
    print("📊 Excel Processing Results:")
    print(f"Total docs: {stats['total_documents']}")
    print(f"Avg length: {stats['avg_text_length']:.1f} chars")
    
    for doc in docs:
        print(f"  {doc['doc_id']}: {doc['text'][:50]}...")
    
    return docs

if __name__ == "__main__":
    test_excel_processor()