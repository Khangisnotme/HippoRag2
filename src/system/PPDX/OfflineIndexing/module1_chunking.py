"""
Module 1: Chunking
Simple chunking - giữ nguyên paragraphs từ Excel input
"""

from pathlib import Path
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ChunkProcessor:
    """Simple chunking processor - keeps paragraphs as-is"""
    
    def __init__(self):
        self.processed_chunks = []
        
    def process_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process documents into chunks
        Trong implementation này, mỗi document = 1 chunk (keep as-is)
        """
        chunks = []
        
        for doc in documents:
            # Simple approach: 1 document = 1 chunk
            chunk = {
                'chunk_id': f"chunk_{doc['doc_id']}_0",
                'doc_id': doc['doc_id'],
                'title': doc.get('title', ''),
                'text': doc['text'],
                'chunk_index': 0,
                'total_chunks': 1,
                'metadata': {
                    'source': doc.get('metadata', {}).get('source', ''),
                    'original_length': len(doc['text']),
                    'chunking_method': 'keep_as_paragraph'
                }
            }
            
            # Basic validation
            if len(chunk['text'].strip()) > 0:
                chunks.append(chunk)
                
        self.processed_chunks = chunks
        logger.info(f"Processed {len(documents)} documents into {len(chunks)} chunks")
        return chunks
    
    def process_single_document(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process single document into chunks"""
        return self.process_documents([doc])
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get chunking statistics"""
        if not self.processed_chunks:
            return {}
        
        texts = [chunk['text'] for chunk in self.processed_chunks]
        
        return {
            'total_chunks': len(self.processed_chunks),
            'avg_chunk_length': sum(len(text) for text in texts) / len(texts),
            'min_chunk_length': min(len(text) for text in texts),
            'max_chunk_length': max(len(text) for text in texts),
            'total_characters': sum(len(text) for text in texts),
            'chunking_method': 'keep_as_paragraph'
        }

# Test function
def test_chunking():
    """Test function cho Module 1"""
    processor = ChunkProcessor()
    
    # Test data
    test_docs = [
        {
            'doc_id': 'PH_0',
            'title': 'PH Basics',
            'text': 'Các dung dịch nước có giá trị pH nhỏ hơn 7 được coi là có tính axít.',
            'metadata': {'source': 'test'}
        },
        {
            'doc_id': 'PH_1', 
            'title': 'Neutral Water',
            'text': 'Nước tinh khiết có pH = 7, được coi là trung tính.',
            'metadata': {'source': 'test'}
        }
    ]
    
    chunks = processor.process_documents(test_docs)
    stats = processor.get_statistics()
    
    print("📝 Chunking Results:")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Avg length: {stats['avg_chunk_length']:.1f} chars")
    print(f"Method: {stats['chunking_method']}")
    
    for chunk in chunks:
        print(f"  {chunk['chunk_id']}: {chunk['text'][:50]}...")
    
    return chunks

if __name__ == "__main__":
    test_chunking()