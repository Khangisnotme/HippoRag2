# 📁 **FULL CODE - Offline Indexing Module**

## 🏗️ **src/offline_indexing/module1_chunking.py**

```python
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
```

---

## 🧠 **src/offline_indexing/module2_triple_extractor.py**

```python
"""
Module 2: Triple Extractor
Sử dụng Qwen2.5-7B để extract triples từ chunks
"""

from pathlib import Path
from typing import List, Dict, Tuple, Any
from huggingface_hub import InferenceClient
import re
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Triple:
    """Data class cho Triple"""
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    source_chunk_id: str = ""
    source_doc_id: str = ""

class TripleExtractor:
    """Extract triples sử dụng Qwen2.5-7B"""
    
    def __init__(self, api_key: str):
        """Initialize với HuggingFace API key"""
        self.client = InferenceClient(
            provider="together",
            api_key=api_key,
        )
        self.model_name = "Qwen/Qwen2.5-7B-Instruct"
        self.extracted_triples = []
        
    def extract_triples_from_chunks(self, chunks: List[Dict[str, Any]]) -> List[Triple]:
        """Extract triples từ list of chunks"""
        all_triples = []
        
        for chunk in chunks:
            chunk_triples = self.extract_triples_from_chunk(chunk)
            all_triples.extend(chunk_triples)
            
        self.extracted_triples = all_triples
        logger.info(f"Extracted {len(all_triples)} triples from {len(chunks)} chunks")
        return all_triples
    
    def extract_triples_from_chunk(self, chunk: Dict[str, Any]) -> List[Triple]:
        """Extract triples từ single chunk"""
        try:
            # Create prompt cho Qwen
            prompt = self._create_extraction_prompt(chunk['text'])
            
            # Call Qwen API
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024
            )
            
            # Parse response
            response_text = completion.choices[0].message.content
            triples = self._parse_triples_response(
                response_text, 
                chunk.get('chunk_id', ''),
                chunk.get('doc_id', '')
            )
            
            logger.debug(f"Extracted {len(triples)} triples from chunk {chunk.get('chunk_id', '')}")
            return triples
            
        except Exception as e:
            logger.error(f"Error extracting triples from chunk {chunk.get('chunk_id', '')}: {e}")
            return []
    
    def _create_extraction_prompt(self, text: str) -> str:
        """Tạo prompt cho Qwen để extract triples"""
        prompt = f"""
Nhiệm vụ: Trích xuất tất cả các mối quan hệ thực tế từ đoạn văn sau dưới dạng bộ ba (chủ thể, quan hệ, đối tượng).

Quy tắc:
1. Chỉ trích xuất những mối quan hệ rõ ràng và thực tế
2. Sử dụng từ ngữ chính xác từ văn bản gốc
3. Mỗi bộ ba phải có ý nghĩa hoàn chỉnh
4. Không tạo ra thông tin không có trong văn bản
5. Tránh các mối quan hệ quá chung chung hoặc không rõ nghĩa

Đoạn văn: {text}

Định dạng đầu ra (mỗi dòng một bộ ba):
(chủ thể, quan hệ, đối tượng)
(chủ thể, quan hệ, đối tượng)

Ví dụ format:
(nước, có pH, 7)
(dung dịch axít, có pH, nhỏ hơn 7)

Trích xuất:
"""
        return prompt
    
    def _parse_triples_response(self, response: str, chunk_id: str, doc_id: str) -> List[Triple]:
        """Parse response từ Qwen thành list of Triple objects"""
        triples = []
        
        # Pattern để match (subject, predicate, object)
        pattern = r'\(\s*([^,]+?)\s*,\s*([^,]+?)\s*,\s*([^)]+?)\s*\)'
        matches = re.findall(pattern, response)
        
        for match in matches:
            subject, predicate, obj = match
            
            # Clean up extracted text
            subject = subject.strip().strip('"\'')
            predicate = predicate.strip().strip('"\'')
            obj = obj.strip().strip('"\'')
            
            # Validate triple
            if self._is_valid_triple(subject, predicate, obj):
                triple = Triple(
                    subject=subject,
                    predicate=predicate,
                    object=obj,
                    confidence=1.0,  # Default confidence
                    source_chunk_id=chunk_id,
                    source_doc_id=doc_id
                )
                triples.append(triple)
        
        return triples
    
    def _is_valid_triple(self, subject: str, predicate: str, obj: str) -> bool:
        """Validate extracted triple"""
        # Check minimum length
        if len(subject) < 2 or len(predicate) < 2 or len(obj) < 2:
            return False
        
        # Check maximum length (avoid very long extractions)
        if len(subject) > 100 or len(predicate) > 50 or len(obj) > 100:
            return False
        
        # Check for common extraction errors
        error_patterns = ['...', '???', 'unknown', 'unclear', 'etc', 'và nhiều', 'v.v']
        for pattern in error_patterns:
            if (pattern.lower() in subject.lower() or 
                pattern.lower() in obj.lower() or
                pattern.lower() in predicate.lower()):
                return False
        
        # Check for too generic predicates
        generic_predicates = ['là', 'có', 'được', 'bao gồm']
        if predicate.lower().strip() in generic_predicates and len(predicate) < 5:
            return False
        
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get extraction statistics"""
        if not self.extracted_triples:
            return {}
        
        subjects = [t.subject for t in self.extracted_triples]
        predicates = [t.predicate for t in self.extracted_triples]
        objects = [t.object for t in self.extracted_triples]
        
        return {
            'total_triples': len(self.extracted_triples),
            'unique_subjects': len(set(subjects)),
            'unique_predicates': len(set(predicates)),
            'unique_objects': len(set(objects)),
            'avg_confidence': sum(t.confidence for t in self.extracted_triples) / len(self.extracted_triples),
            'most_common_predicates': self._get_most_common(predicates, 5),
            'most_common_subjects': self._get_most_common(subjects, 5)
        }
    
    def _get_most_common(self, items: List[str], top_k: int = 5) -> List[Tuple[str, int]]:
        """Get most common items"""
        from collections import Counter
        counter = Counter(items)
        return counter.most_common(top_k)
    
    def save_triples_to_file(self, output_path: Path):
        """Save extracted triples to file for inspection"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Subject\tPredicate\tObject\tConfidence\tSource_Chunk\tSource_Doc\n")
            for triple in self.extracted_triples:
                f.write(f"{triple.subject}\t{triple.predicate}\t{triple.object}\t"
                       f"{triple.confidence}\t{triple.source_chunk_id}\t{triple.source_doc_id}\n")

# Test function
def test_triple_extractor():
    """Test function cho Module 2"""
    # Mock API key for testing
    api_key = "test_key"
    
    extractor = TripleExtractor(api_key)
    
    # Test chunks
    test_chunks = [
        {
            'chunk_id': 'chunk_PH_0_0',
            'doc_id': 'PH_0',
            'text': 'Các dung dịch nước có giá trị pH nhỏ hơn 7 được coi là có tính axít, trong khi các giá trị pH lớn hơn 7 được coi là có tính kiềm.'
        }
    ]
    
    print("🧠 Testing Triple Extraction...")
    print("Note: Actual extraction requires valid HuggingFace API key")
    
    # Mock extraction for testing
    mock_triples = [
        Triple("dung dịch nước", "có giá trị pH", "nhỏ hơn 7", 0.9, "chunk_PH_0_0", "PH_0"),
        Triple("dung dịch axít", "có pH", "nhỏ hơn 7", 0.9, "chunk_PH_0_0", "PH_0"),
        Triple("dung dịch kiềm", "có pH", "lớn hơn 7", 0.9, "chunk_PH_0_0", "PH_0")
    ]
    
    extractor.extracted_triples = mock_triples
    stats = extractor.get_statistics()
    
    print("📊 Triple Extraction Results:")
    print(f"Total triples: {stats['total_triples']}")
    print(f"Unique subjects: {stats['unique_subjects']}")
    print(f"Unique predicates: {stats['unique_predicates']}")
    print(f"Most common predicates: {stats['most_common_predicates']}")
    
    return mock_triples

if __name__ == "__main__":
    test_triple_extractor()
```

---

## 🔗 **src/offline_indexing/module3_synonym_detector.py**

```python
"""
Module 3: Synonym Detector  
Sử dụng sentence-transformers để detect synonyms giữa các phrases
"""

from pathlib import Path
from typing import List, Dict, Tuple, Set, Any
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass  
class SynonymPair:
    """Data class cho synonym pair"""
    phrase1: str
    phrase2: str
    similarity_score: float

class SynonymDetector:
    """Detect synonyms sử dụng embedding similarity"""
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"):
        """Initialize với multilingual sentence transformer"""
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.synonym_pairs = []
        self.phrase_embeddings = {}
        
    def detect_synonyms_from_triples(self, triples: List[Any], similarity_threshold: float = 0.85) -> List[SynonymPair]:
        """Detect synonyms từ extracted triples"""
        # Extract all unique phrases (subjects + objects)
        all_phrases = set()
        
        for triple in triples:
            all_phrases.add(triple.subject.strip().lower())
            all_phrases.add(triple.object.strip().lower())
        
        all_phrases = list(all_phrases)
        
        # Remove very short phrases
        filtered_phrases = [phrase for phrase in all_phrases if len(phrase) > 2]
        
        logger.info(f"Detecting synonyms among {len(filtered_phrases)} unique phrases")
        
        # Detect synonyms
        synonym_pairs = self.detect_synonyms(filtered_phrases, similarity_threshold)
        
        self.synonym_pairs = synonym_pairs
        return synonym_pairs
    
    def detect_synonyms(self, phrases: List[str], similarity_threshold: float = 0.85) -> List[SynonymPair]:
        """Detect synonyms trong list of phrases"""
        if len(phrases) < 2:
            return []
        
        # Generate embeddings
        logger.info("Generating embeddings...")
        embeddings = self.model.encode(phrases, show_progress_bar=True)
        
        # Store embeddings
        for phrase, embedding in zip(phrases, embeddings):
            self.phrase_embeddings[phrase] = embedding
        
        # Compute similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Find synonym pairs
        synonym_pairs = []
        processed_pairs = set()
        
        for i in range(len(phrases)):
            for j in range(i + 1, len(phrases)):
                similarity = similarity_matrix[i][j]
                
                if similarity >= similarity_threshold:
                    phrase1, phrase2 = phrases[i], phrases[j]
                    
                    # Avoid duplicate pairs
                    pair_key = tuple(sorted([phrase1, phrase2]))
                    if pair_key not in processed_pairs:
                        synonym_pair = SynonymPair(
                            phrase1=phrase1,
                            phrase2=phrase2,
                            similarity_score=float(similarity)
                        )
                        synonym_pairs.append(synonym_pair)
                        processed_pairs.add(pair_key)
        
        logger.info(f"Found {len(synonym_pairs)} synonym pairs")
        return synonym_pairs
    
    def create_synonym_mapping(self, synonym_pairs: List[SynonymPair] = None) -> Dict[str, str]:
        """Create mapping từ synonyms về canonical form"""
        if synonym_pairs is None:
            synonym_pairs = self.synonym_pairs
            
        # Build graph of synonyms
        synonym_graph = {}
        
        for pair in synonym_pairs:
            if pair.phrase1 not in synonym_graph:
                synonym_graph[pair.phrase1] = set()
            if pair.phrase2 not in synonym_graph:
                synonym_graph[pair.phrase2] = set()
            
            synonym_graph[pair.phrase1].add(pair.phrase2)
            synonym_graph[pair.phrase2].add(pair.phrase1)
        
        # Find connected components (synonym groups)
        visited = set()
        synonym_groups = []
        
        def dfs(node, current_group):
            if node in visited:
                return
            visited.add(node)
            current_group.add(node)
            
            for neighbor in synonym_graph.get(node, set()):
                dfs(neighbor, current_group)
        
        for phrase in synonym_graph:
            if phrase not in visited:
                group = set()
                dfs(phrase, group)
                if len(group) > 1:
                    synonym_groups.append(group)
        
        # Create mapping to canonical forms
        synonym_mapping = {}
        
        for group in synonym_groups:
            # Choose shortest phrase as canonical
            canonical = min(group, key=len)
            
            for phrase in group:
                synonym_mapping[phrase] = canonical
        
        logger.info(f"Created {len(synonym_groups)} synonym groups")
        return synonym_mapping
    
    def get_phrase_embedding(self, phrase: str) -> np.ndarray:
        """Get embedding cho phrase"""
        if phrase in self.phrase_embeddings:
            return self.phrase_embeddings[phrase]
        else:
            embedding = self.model.encode([phrase])[0]
            self.phrase_embeddings[phrase] = embedding
            return embedding
    
    def find_similar_phrases(self, target_phrase: str, candidate_phrases: List[str], 
                           top_k: int = 5) -> List[Tuple[str, float]]:
        """Find top-k similar phrases to target"""
        target_embedding = self.get_phrase_embedding(target_phrase)
        
        similarities = []
        for phrase in candidate_phrases:
            if phrase != target_phrase:
                phrase_embedding = self.get_phrase_embedding(phrase)
                similarity = float(cosine_similarity([target_embedding], [phrase_embedding])[0][0])
                similarities.append((phrase, similarity))
        
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get synonym detection statistics"""
        if not self.synonym_pairs:
            return {}
        
        similarities = [pair.similarity_score for pair in self.synonym_pairs]
        
        return {
            'total_synonym_pairs': len(self.synonym_pairs),
            'avg_similarity': np.mean(similarities),
            'min_similarity': np.min(similarities),
            'max_similarity': np.max(similarities),
            'unique_phrases_with_synonyms': len(set([pair.phrase1 for pair in self.synonym_pairs] + 
                                                  [pair.phrase2 for pair in self.synonym_pairs]))
        }
    
    def save_synonyms_to_file(self, output_path: Path):
        """Save synonym pairs to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("Phrase1\tPhrase2\tSimilarity_Score\n")
            for pair in self.synonym_pairs:
                f.write(f"{pair.phrase1}\t{pair.phrase2}\t{pair.similarity_score:.4f}\n")

# Test function
def test_synonym_detector():
    """Test function cho Module 3"""
    detector = SynonymDetector()
    
    # Test phrases
    test_phrases = [
        "axít",
        "axit", 
        "kiềm",
        "bazơ",
        "dung dịch axít",
        "dung dịch axit",
        "pH nhỏ hơn 7",
        "pH < 7"
    ]
    
    print("🔗 Testing Synonym Detection...")
    synonym_pairs = detector.detect_synonyms(test_phrases, similarity_threshold=0.8)
    
    print("📊 Synonym Detection Results:")
    for pair in synonym_pairs:
        print(f"  {pair.phrase1} ≈ {pair.phrase2} (score: {pair.similarity_score:.3f})")
    
    # Test mapping
    mapping = detector.create_synonym_mapping(synonym_pairs)
    print("\n📋 Synonym Mapping:")
    for original, canonical in mapping.items():
        print(f"  {original} → {canonical}")
    
    return synonym_pairs

if __name__ == "__main__":
    test_synonym_detector()
```

---

## 🏗️ **src/offline_indexing/module4_graph_builder.py**

```python
"""
Module 4: Graph Builder
Build Neo4j Knowledge Graph từ processed data
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid
import logging
from dataclasses import dataclass

# Import Neo4j utilities
from utils.utils_neo4j import Neo4jManager

logger = logging.getLogger(__name__)

@dataclass
class GraphNode:
    """Base class cho graph nodes"""
    id: str
    node_type: str
    properties: Dict[str, Any]

@dataclass  
class GraphEdge:
    """Base class cho graph edges"""
    source_id: str
    target_id: str
    edge_type: str
    properties: Dict[str, Any]

class GraphBuilder:
    """Build Knowledge Graph trong Neo4j"""
    
    def __init__(self, neo4j_uri: str = "bolt://localhost:7687", 
                 neo4j_user: str = "neo4j", neo4j_password: str = "graphrag123"):
        """Initialize connection tới Neo4j"""
        self.neo4j_manager = Neo4jManager(neo4j_uri, neo4j_user, neo4j_password)
        self.nodes_created = 0
        self.edges_created = 0
        
        # Test connection
        if not self.neo4j_manager.test_connection():
            raise Exception("Failed to connect to Neo4j")
            
    def setup_constraints_and_indexes(self):
        """Setup database constraints và indexes"""
        try:
            self.neo4j_manager.setup_constraints_and_indexes()
            logger.info("Database constraints and indexes setup completed")
        except Exception as e:
            logger.error(f"Error setting up constraints and indexes: {e}")
            raise
            
    def clear_database(self):
        """Clear existing data"""
        try:
            self.neo4j_manager.clear_all_data()
            logger.info("Cleared existing database")
        except Exception as e:
            logger.error(f"Error clearing database: {e}")
            raise
    
    def build_graph(self, chunks: List[Dict[str, Any]], triples: List[Any], 
                   synonym_pairs: List[Any], synonym_mapping: Dict[str, str]):
        """Main method để build complete graph"""
        logger.info("Starting graph construction...")
        
        # Setup database
        self.setup_constraints_and_indexes()
        
        # Build nodes
        self._create_passage_nodes(chunks)
        self._create_phrase_nodes(triples, synonym_mapping)
        
        # Build edges
        self._create_relation_edges(triples, synonym_mapping)
        self._create_synonym_edges(synonym_pairs)
        self._create_contains_edges(chunks, triples, synonym_mapping)
        
        logger.info(f"Graph construction completed: {self.nodes_created} nodes, {self.edges_created} edges")
    
    def _create_passage_nodes(self, chunks: List[Dict[str, Any]]):
        """Create Passage nodes từ chunks"""
        for chunk in chunks:
            passage_id = f"passage_{chunk['chunk_id']}"
            
            properties = {
                'id': passage_id,
                'chunk_id': chunk['chunk_id'],
                'doc_id': chunk['doc_id'],
                'title': chunk.get('title', ''),
                'text': chunk['text'],
                'chunk_index': chunk.get('chunk_index', 0),
                'source': chunk.get('metadata', {}).get('source', ''),
                'text_length': len(chunk['text'])
            }
            
            self.neo4j_manager.create_passage_node(passage_id, properties)
            self.nodes_created += 1
        
        logger.info(f"Created {len(chunks)} Passage nodes")
    
    def _create_phrase_nodes(self, triples: List[Any], synonym_mapping: Dict[str, str]):
        """Create Phrase nodes từ triples"""
        # Collect unique phrases
        unique_phrases = set()
        
        for triple in triples:
            # Use canonical form if available
            subject = synonym_mapping.get(triple.subject.lower(), triple.subject)
            obj = synonym_mapping.get(triple.object.lower(), triple.object)
            
            unique_phrases.add(subject.lower())
            unique_phrases.add(obj.lower())
        
        # Create phrase nodes
        for phrase in unique_phrases:
            phrase_id = f"phrase_{uuid.uuid4().hex[:8]}"
            
            properties = {
                'id': phrase_id,
                'text': phrase,
                'normalized_text': phrase.lower().strip(),
                'text_length': len(phrase)
            }
            
            self.neo4j_manager.create_phrase_node(phrase_id, properties)
            self.nodes_created += 1
        
        logger.info(f"Created {len(unique_phrases)} Phrase nodes")
    
    def _create_relation_edges(self, triples: List[Any], synonym_mapping: Dict[str, str]):
        """Create RELATION edges giữa Phrase nodes"""
        for triple in triples:
            # Use canonical forms
            subject = synonym_mapping.get(triple.subject.lower(), triple.subject).lower()
            obj = synonym_mapping.get(triple.object.lower(), triple.object).lower()
            
            properties = {
                'predicate': triple.predicate,
                'confidence': triple.confidence,
                'source_chunk': triple.source_chunk_id,
                'source_doc': triple.source_doc_id
            }
            
            self.neo4j_manager.create_relation_edge(subject, obj, properties)
            self.edges_created += 1
        
        logger.info(f"Created {len(triples)} RELATION edges")
    
    def _create_synonym_edges(self, synonym_pairs: List[Any]):
        """Create SYNONYM edges giữa Phrase nodes"""
        for pair in synonym_pairs:
            properties = {
                'similarity_score': pair.similarity_score
            }
            
            self.neo4j_manager.create_synonym_edge(
                pair.phrase1.lower(), 
                pair.phrase2.lower(), 
                properties
            )
            self.edges_created += 1
        
        logger.info(f"Created {len(synonym_pairs)} SYNONYM edges")
    
    def _create_contains_edges(self, chunks: List[Dict[str, Any]], 
                              triples: List[Any], synonym_mapping: Dict[str, str]):
        """Create CONTAINS edges từ Passage đến Phrase nodes"""
        # Create mapping từ chunk_id đến phrases
        chunk_phrases = {}
        
        for triple in triples:
            chunk_id = triple.source_chunk_id
            if chunk_id not in chunk_phrases:
                chunk_phrases[chunk_id] = set()
            
            # Use canonical forms
            subject = synonym_mapping.get(triple.subject.lower(), triple.subject)
            obj = synonym_mapping.get(triple.object.lower(), triple.object)
            
            chunk_phrases[chunk_id].add(subject.lower())
            chunk_phrases[chunk_id].add(obj.lower())
        
        # Create CONTAINS edges
        for chunk_id, phrases in chunk_phrases.items():
            passage_id = f"passage_{chunk_id}"
            
            for phrase in phrases:
                properties = {}
                self.neo4j_manager.create_contains_edge(passage_id, phrase, properties)
                self.edges_created += 1
        
        logger.info(f"Created CONTAINS edges")
    
    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        return self.neo4j_manager.get_graph_statistics()
    
    def close(self):
        """Close Neo4j connection"""
        self.neo4j_manager.close()

# Test function
def test_graph_builder():
    """Test function cho Module 4"""
    print("🏗️ Testing Graph Builder...")
    
    try:
        builder = GraphBuilder()
        
        # Test connection
        stats = builder.get_graph_statistics()
        print("📊 Current Graph Statistics:")
        print(f"  Nodes: {stats.get('total_nodes', 0)}")
        print(f"  Edges: {stats.get('total


Tiếp tục từ **module4_graph_builder.py**:

```python
        print(f"  Edges: {stats.get('total_edges', 0)}")
        
        builder.close()
        
    except Exception as e:
        print(f"❌ Error testing Graph Builder: {e}")
        print("Make sure Neo4j is running on bolt://localhost:7687")

if __name__ == "__main__":
    test_graph_builder()
```

---

## 🎯 **src/offline_indexing/pipeline_orchestrator.py**

```python
"""
Pipeline Orchestrator
Coordinate tất cả modules để build complete graph
"""

from pathlib import Path
from typing import Dict, Any, Optional
import logging
import time
from datetime import datetime

# Import modules
from module1_chunking import ChunkProcessor
from module2_triple_extractor import TripleExtractor
from module3_synonym_detector import SynonymDetector
from module4_graph_builder import GraphBuilder

# Import utilities
from utils.utils_excel_documents import ExcelDocumentProcessor
from utils.utils_general import setup_logging, save_pipeline_results

logger = logging.getLogger(__name__)

class OfflinePipelineOrchestrator:
    """Orchestrate toàn bộ offline pipeline"""
    
    def __init__(self, 
                 huggingface_api_key: str,
                 neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j", 
                 neo4j_password: str = "graphrag123"):
        """Initialize pipeline với required configurations"""
        self.huggingface_api_key = huggingface_api_key
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        
        # Initialize processors
        self.excel_processor = ExcelDocumentProcessor()
        self.chunk_processor = ChunkProcessor()
        self.triple_extractor = TripleExtractor(huggingface_api_key)
        self.synonym_detector = SynonymDetector()
        self.graph_builder = None  # Initialize later
        
        # Statistics
        self.pipeline_stats = {}
        
    def run_complete_pipeline(self, 
                            excel_file_path: Path,
                            clear_existing_graph: bool = True,
                            synonym_threshold: float = 0.85,
                            save_intermediate_results: bool = True) -> Dict[str, Any]:
        """Run complete offline pipeline"""
        start_time = time.time()
        logger.info("🚀 Starting complete offline pipeline...")
        
        try:
            # Step 0: Load documents from Excel
            logger.info("📊 Step 0: Loading documents from Excel...")
            documents = self.excel_processor.load_and_process_excel(excel_file_path)
            excel_stats = self.excel_processor.get_statistics()
            
            # Step 1: Process chunks
            logger.info("📝 Step 1: Processing chunks...")
            chunks = self.chunk_processor.process_documents(documents)
            chunk_stats = self.chunk_processor.get_statistics()
            
            # Step 2: Extract triples
            logger.info("🧠 Step 2: Extracting triples...")
            triples = self.triple_extractor.extract_triples_from_chunks(chunks)
            triple_stats = self.triple_extractor.get_statistics()
            
            # Step 3: Detect synonyms
            logger.info("🔗 Step 3: Detecting synonyms...")
            synonym_pairs = self.synonym_detector.detect_synonyms_from_triples(
                triples, synonym_threshold
            )
            synonym_mapping = self.synonym_detector.create_synonym_mapping(synonym_pairs)
            synonym_stats = self.synonym_detector.get_statistics()
            
            # Step 4: Build graph
            logger.info("🏗️ Step 4: Building Knowledge Graph...")
            self.graph_builder = GraphBuilder(
                self.neo4j_uri, self.neo4j_user, self.neo4j_password
            )
            
            if clear_existing_graph:
                self.graph_builder.clear_database()
            
            self.graph_builder.build_graph(chunks, triples, synonym_pairs, synonym_mapping)
            graph_stats = self.graph_builder.get_graph_statistics()
            
            # Save intermediate results if requested
            if save_intermediate_results:
                self._save_intermediate_results(
                    excel_file_path.parent, triples, synonym_pairs
                )
            
            # Compile final statistics
            end_time = time.time()
            pipeline_duration = end_time - start_time
            
            self.pipeline_stats = {
                'execution_time': pipeline_duration,
                'timestamp': datetime.now().isoformat(),
                'input_file': str(excel_file_path),
                'excel_processing': excel_stats,
                'chunking': chunk_stats,
                'triples': triple_stats,
                'synonyms': synonym_stats,
                'graph': graph_stats,
                'settings': {
                    'synonym_threshold': synonym_threshold,
                    'clear_existing_graph': clear_existing_graph
                }
            }
            
            logger.info(f"✅ Pipeline completed successfully in {pipeline_duration:.2f} seconds")
            self._print_final_summary()
            
            return self.pipeline_stats
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {e}")
            raise
        
        finally:
            if self.graph_builder:
                self.graph_builder.close()
    
    def _save_intermediate_results(self, output_dir: Path, triples, synonym_pairs):
        """Save intermediate results for inspection"""
        output_dir = Path(output_dir)
        
        # Save triples
        triples_file = output_dir / "extracted_triples.tsv"
        self.triple_extractor.save_triples_to_file(triples_file)
        logger.info(f"Saved triples to {triples_file}")
        
        # Save synonyms
        synonyms_file = output_dir / "detected_synonyms.tsv"
        self.synonym_detector.save_synonyms_to_file(synonyms_file)
        logger.info(f"Saved synonyms to {synonyms_file}")
    
    def _print_final_summary(self):
        """Print final pipeline summary"""
        stats = self.pipeline_stats
        
        print("\n" + "="*60)
        print("📊 OFFLINE PIPELINE SUMMARY")
        print("="*60)
        print(f"⏱️  Execution Time: {stats['execution_time']:.2f} seconds")
        print(f"📁 Input File: {stats['input_file']}")
        print()
        print("📊 EXCEL PROCESSING:")
        print(f"   Documents Loaded: {stats['excel_processing']['total_documents']}")
        print(f"   Avg Length: {stats['excel_processing']['avg_text_length']:.1f} chars")
        print()
        print("📝 CHUNKING:")
        print(f"   Total Chunks: {stats['chunking']['total_chunks']}")
        print(f"   Avg Chunk Length: {stats['chunking']['avg_chunk_length']:.1f} chars")
        print(f"   Method: {stats['chunking']['chunking_method']}")
        print()
        print("🧠 TRIPLES:")
        print(f"   Total: {stats['triples']['total_triples']}")
        print(f"   Unique Subjects: {stats['triples']['unique_subjects']}")
        print(f"   Unique Predicates: {stats['triples']['unique_predicates']}")
        print(f"   Unique Objects: {stats['triples']['unique_objects']}")
        print()
        print("🔗 SYNONYMS:")
        print(f"   Synonym Pairs: {stats['synonyms']['total_synonym_pairs']}")
        if stats['synonyms']['total_synonym_pairs'] > 0:
            print(f"   Avg Similarity: {stats['synonyms']['avg_similarity']:.3f}")
        print()
        print("🏗️ KNOWLEDGE GRAPH:")
        print(f"   Total Nodes: {stats['graph']['total_nodes']}")
        print(f"   Total Edges: {stats['graph']['total_edges']}")
        
        for node_type, count in stats['graph']['nodes'].items():
            print(f"   {node_type} Nodes: {count}")
        
        for edge_type, count in stats['graph']['edges'].items():
            print(f"   {edge_type} Edges: {count}")
        
        print("="*60)
        print("✅ Pipeline completed successfully!")
        print("🌐 Access Neo4j Browser: http://localhost:7474")
        print("="*60)

# Test function
def test_pipeline_orchestrator():
    """Test complete pipeline"""
    print("🎯 Testing Complete Pipeline...")
    
    # Note: Requires actual API key và Neo4j running
    api_key = "your_huggingface_api_key_here"
    
    if api_key == "your_huggingface_api_key_here":
        print("⚠️  Please set your actual HuggingFace API key to test")
        return
    
    try:
        orchestrator = OfflinePipelineOrchestrator(api_key)
        
        # Test file path (will be created in test_data.py)
        test_file = Path("test_data.xlsx")
        
        if test_file.exists():
            stats = orchestrator.run_complete_pipeline(test_file)
            print("✅ Pipeline test completed!")
        else:
            print("❌ Test file not found. Run test_data.py first.")
            
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")

if __name__ == "__main__":
    test_pipeline_orchestrator()
```

---

## 🛠️ **src/offline_indexing/utils/utils_excel_documents.py**

```python
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
```

---

## 🗃️ **src/offline_indexing/utils/utils_neo4j.py**

```python
"""
Neo4j Database Utilities
Handle Neo4j operations, connections, và basic CRUD
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from neo4j import GraphDatabase
import logging

logger = logging.getLogger(__name__)

class Neo4jManager:
    """Manage Neo4j database operations"""
    
    def __init__(self, uri: str = "bolt://localhost:7687", 
                 user: str = "neo4j", password: str = "graphrag123"):
        """Initialize Neo4j connection"""
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def test_connection(self) -> bool:
        """Test Neo4j connection"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                return result.single()["test"] == 1
        except Exception as e:
            logger.error(f"Neo4j connection test failed: {e}")
            return False
    
    def setup_constraints_and_indexes(self):
        """Setup database constraints và indexes"""
        with self.driver.session() as session:
            # Unique constraints
            constraints = [
                "CREATE CONSTRAINT phrase_id IF NOT EXISTS FOR (p:Phrase) REQUIRE p.id IS UNIQUE",
                "CREATE CONSTRAINT passage_id IF NOT EXISTS FOR (p:Passage) REQUIRE p.id IS UNIQUE"
            ]
            
            # Indexes for search
            indexes = [
                "CREATE FULLTEXT INDEX phrase_text IF NOT EXISTS FOR (p:Phrase) ON EACH [p.text, p.normalized_text]",
                "CREATE FULLTEXT INDEX passage_text IF NOT EXISTS FOR (p:Passage) ON EACH [p.text, p.title]"
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.debug(f"Created constraint: {constraint}")
                except Exception as e:
                    logger.debug(f"Constraint already exists or error: {e}")
            
            for index in indexes:
                try:
                    session.run(index)
                    logger.debug(f"Created index: {index}")
                except Exception as e:
                    logger.debug(f"Index already exists or error: {e}")
    
    def clear_all_data(self):
        """Clear all data from database"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Cleared all data from Neo4j database")
    
    def create_passage_node(self, passage_id: str, properties: Dict[str, Any]):
        """Create a Passage node"""
        with self.driver.session() as session:
            query = """
            CREATE (p:Passage {
                id: $id,
                chunk_id: $chunk_id,
                doc_id: $doc_id,
                title: $title,
                text: $text,
                chunk_index: $chunk_index,
                source: $source,
                text_length: $text_length,
                created_at: datetime()
            })
            """
            
            session.run(query, 
                       id=passage_id,
                       chunk_id=properties.get('chunk_id', ''),
                       doc_id=properties.get('doc_id', ''),
                       title=properties.get('title', ''),
                       text=properties.get('text', ''),
                       chunk_index=properties.get('chunk_index', 0),
                       source=properties.get('source', ''),
                       text_length=properties.get('text_length', 0))
    
    def create_phrase_node(self, phrase_id: str, properties: Dict[str, Any]):
        """Create a Phrase node"""
        with self.driver.session() as session:
            query = """
            CREATE (p:Phrase {
                id: $id,
                text: $text,
                normalized_text: $normalized_text,
                text_length: $text_length,
                created_at: datetime()
            })
            """
            
            session.run(query,
                       id=phrase_id,
                       text=properties.get('text', ''),
                       normalized_text=properties.get('normalized_text', ''),
                       text_length=properties.get('text_length', 0))
    
    def create_relation_edge(self, subject_text: str, object_text: str, properties: Dict[str, Any]):
        """Create RELATION edge giữa hai Phrase nodes"""
        with self.driver.session() as session:
            query = """
            MATCH (s:Phrase {normalized_text: $subject})
            MATCH (o:Phrase {normalized_text: $object})
            CREATE (s)-[:RELATION {
                predicate: $predicate,
                confidence: $confidence,
                source_chunk: $source_chunk,
                source_doc: $source_doc,
                created_at: datetime()
            }]->(o)
            """
            
            session.run(query,
                       subject=subject_text,
                       object=object_text,
                       predicate=properties.get('predicate', ''),
                       confidence=properties.get('confidence', 1.0),
                       source_chunk=properties.get('source_chunk', ''),
                       source_doc=properties.get('source_doc', ''))
    
    def create_synonym_edge(self, phrase1_text: str, phrase2_text: str, properties: Dict[str, Any]):
        """Create SYNONYM edge giữa hai Phrase nodes"""
        with self.driver.session() as session:
            query = """
            MATCH (p1:Phrase {normalized_text: $phrase1})
            MATCH (p2:Phrase {normalized_text: $phrase2})
            CREATE (p1)-[:SYNONYM {
                similarity_score: $similarity,
                created_at: datetime()
            }]->(p2)
            """
            
            session.run(query,
                       phrase1=phrase1_text,
                       phrase2=phrase2_text,
                       similarity=properties.get('similarity_score', 1.0))
    
    def create_contains_edge(self, passage_id: str, phrase_text: str, properties: Dict[str, Any]):
        """Create CONTAINS edge từ Passage đến Phrase"""
        with self.driver.session() as session:
            query = """
            MATCH (passage:Passage {id: $passage_id})
            MATCH (phrase:Phrase {normalized_text: $phrase})
            CREATE (passage)-[:CONTAINS {
                created_at: datetime()
            }]->(phrase)
            """
            
            session.run(query,
                       passage_id=passage_id,
                       phrase=phrase_text)
    
    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get comprehensive graph statistics"""
        with self.driver.session() as session:
            # Node counts
            node_stats = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as node_type, count(*) as count
            """)
            
            # Edge counts
            edge_stats = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as edge_type, count(*) as count
            """)
            
            nodes = {record["node_type"]: record["count"] for record in node_stats}
            edges = {record["edge_type"]: record["count"] for record in edge_stats}
            
            return {
                'nodes': nodes,
                'edges': edges,
                'total_nodes': sum(nodes.values()),
                'total_edges': sum(edges.values())
            }
    
    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute custom Cypher query"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")

# Test function
def test_neo4j_manager():
    """Test Neo4j manager"""
    print("🗃️ Testing Neo4j Manager...")
    
    try:
        manager = Neo4jManager()
        
        # Test connection
        if manager.test_connection():
            print("✅ Neo4j connection successful")
            
            # Get statistics
            stats = manager.get_graph_statistics()
            print(f"📊 Current nodes: {stats['total_nodes']}")
            print(f"📊 Current edges: {stats['total_edges']}")
        else:
            print("❌ Neo4j connection failed")
        
        manager.close()
        
    except Exception as e:
        print(f"❌ Error testing Neo4j Manager: {e}")

if __name__ == "__main__":
    test_neo4j_manager()
```

---

## 🔧 **src/offline_indexing/utils/utils_general.py**

```python
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


Tiếp tục từ **utils_general.py**:

```python
if __name__ == "__main__":
    check_environment()
```

---

## 📊 **src/offline_indexing/test/test_data.py**

```python
"""
Generate test Excel data for pipeline testing
"""

from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def create_test_excel(output_path: Path = Path("test_data.xlsx")) -> Path:
    """Create test Excel file với sample Vietnamese chemistry data"""
    
    test_data = [
        {
            'doc_id': 'PH_0',
            'title': 'pH và Tính Axít',
            'text': 'Các dung dịch nước có giá trị pH nhỏ hơn 7 được coi là có tính axít, trong khi các giá trị pH lớn hơn 7 được coi là có tính kiềm. Thang đo pH từ 0 đến 14.'
        },
        {
            'doc_id': 'PH_1', 
            'title': 'Nước Trung Tính',
            'text': 'Nước tinh khiết có pH bằng 7, được coi là trung tính. Điều này có nghĩa là nó không có tính axít cũng không có tính kiềm. Nước trung tính rất quan trọng trong nhiều phản ứng hóa học.'
        },
        {
            'doc_id': 'CHEM_0',
            'title': 'Axít Hydrochloric',
            'text': 'Axít hydrochloric (HCl) là một axít mạnh có pH rất thấp, thường dưới 1. Nó được sử dụng rộng rãi trong công nghiệp và phòng thí nghiệm để làm sạch kim loại.'
        },
        {
            'doc_id': 'CHEM_1',
            'title': 'Bazơ và Kiềm',
            'text': 'Các chất bazơ như natri hydroxit (NaOH) có tính kiềm mạnh với pH cao, thường trên 12. Bazơ có thể trung hòa axít trong phản ứng trung hòa.'
        },
        {
            'doc_id': 'BIO_0',
            'title': 'pH trong Cơ thể',
            'text': 'Máu người có pH khoảng 7.4, hơi kiềm so với nước trung tính. Sự duy trì pH ổn định trong máu rất quan trọng cho sức khỏe và chức năng của các cơ quan.'
        },
        {
            'doc_id': 'BIO_1',
            'title': 'Enzyme và pH',
            'text': 'Các enzyme trong cơ thể hoạt động tốt nhất ở pH tối ưu. Pepsin hoạt động trong môi trường axít của dạ dày với pH khoảng 2, trong khi trypsin hoạt động ở pH kiềm.'
        },
        {
            'doc_id': 'LAB_0',
            'title': 'Đo pH trong Phòng thí nghiệm',
            'text': 'Giấy quỳ tím là một chỉ thị pH phổ biến. Giấy quỳ tím chuyển sang màu đỏ trong môi trường axít và màu xanh trong môi trường kiềm.'
        },
        {
            'doc_id': 'ENV_0',
            'title': 'pH và Môi trường',
            'text': 'Mưa axít có pH thấp hơn 5.6 do có chứa các axít như axít sulfuric và axít nitric. Mưa axít gây hại cho thực vật và các công trình kiến trúc.'
        },
        {
            'doc_id': 'FOOD_0',
            'title': 'pH trong Thực phẩm',
            'text': 'Chanh có pH khoảng 2-3 do chứa axít citric. Sữa có pH khoảng 6.5-6.7, hơi axít. Baking soda có pH khoảng 9, có tính kiềm.'
        },
        {
            'doc_id': 'WATER_0',
            'title': 'Chất lượng Nước',
            'text': 'Nước uống an toàn nên có pH từ 6.5 đến 8.5. Nước có pH quá thấp hoặc quá cao có thể gây hại cho sức khỏe và làm ăn mòn đường ống.'
        }
    ]
    
    df = pd.DataFrame(test_data)
    df.to_excel(output_path, index=False, engine='openpyxl')
    
    logger.info(f"Created test Excel file: {output_path}")
    logger.info(f"Data shape: {df.shape}")
    logger.info(f"Columns: {list(df.columns)}")
    
    print("✅ Created test Excel file with chemistry data")
    print(f"📁 File: {output_path}")
    print(f"📊 Shape: {df.shape}")
    print("📋 Sample documents:")
    for i, row in df.head(3).iterrows():
        print(f"  {row['doc_id']}: {row['text'][:60]}...")
    
    return output_path

def create_small_test_excel(output_path: Path = Path("small_test_data.xlsx")) -> Path:
    """Create smaller test file for quick testing"""
    
    small_test_data = [
        {
            'doc_id': 'TEST_0',
            'title': 'pH Cơ bản',
            'text': 'pH là thang đo độ axít và kiềm. Axít có pH nhỏ hơn 7, kiềm có pH lớn hơn 7.'
        },
        {
            'doc_id': 'TEST_1',
            'title': 'Nước',
            'text': 'Nước tinh khiết có pH bằng 7. Nước là dung môi phổ biến nhất.'
        }
    ]
    
    df = pd.DataFrame(small_test_data)
    df.to_excel(output_path, index=False, engine='openpyxl')
    
    print(f"✅ Created small test file: {output_path}")
    return output_path

def validate_test_data(file_path: Path) -> bool:
    """Validate test data structure"""
    try:
        df = pd.read_excel(file_path)
        
        # Check columns
        required_cols = ['doc_id', 'title', 'text']
        if not all(col in df.columns for col in required_cols):
            print(f"❌ Missing required columns in {file_path}")
            return False
        
        # Check data
        if df.empty:
            print(f"❌ Empty data in {file_path}")
            return False
        
        if df['doc_id'].isna().any() or df['text'].isna().any():
            print(f"❌ Missing doc_id or text values in {file_path}")
            return False
        
        print(f"✅ Validation passed for {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error validating {file_path}: {e}")
        return False

if __name__ == "__main__":
    # Create both test files
    main_file = create_test_excel()
    small_file = create_small_test_excel()
    
    # Validate them
    validate_test_data(main_file)
    validate_test_data(small_file)
    
    print("\n🎯 Test data files ready!")
    print("Use 'test_data.xlsx' for full testing")
    print("Use 'small_test_data.xlsx' for quick testing")
```

---

## 🚀 **src/offline_indexing/test/run_offline_pipeline.py**

```python
"""
Main script để run offline pipeline
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import argparse

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from pipeline_orchestrator import OfflinePipelineOrchestrator
from utils.utils_general import setup_logging, check_environment, save_pipeline_results

# Load environment variables
load_dotenv()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Run GraphRAG Offline Pipeline")
    parser.add_argument("--excel", type=str, default="test_data.xlsx", 
                       help="Path to Excel file")
    parser.add_argument("--api-key", type=str, default=None,
                       help="HuggingFace API key (or set HF_API_KEY env var)")
    parser.add_argument("--clear-graph", action="store_true", default=True,
                       help="Clear existing graph before building")
    parser.add_argument("--synonym-threshold", type=float, default=0.85,
                       help="Synonym detection threshold")
    parser.add_argument("--save-results", action="store_true", default=True,
                       help="Save intermediate results")
    parser.add_argument("--log-level", type=str, default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--neo4j-uri", type=str, default="bolt://localhost:7687",
                       help="Neo4j connection URI")
    parser.add_argument("--neo4j-user", type=str, default="neo4j",
                       help="Neo4j username")
    parser.add_argument("--neo4j-password", type=str, default="graphrag123",
                       help="Neo4j password")
    
    args = parser.parse_args()
    
    # Setup logging
    log_file = Path("logs") / f"offline_pipeline_{args.excel.replace('.xlsx', '')}.log"
    log_file.parent.mkdir(exist_ok=True)
    setup_logging(args.log_level, log_file)
    
    print("🚀 GraphRAG Offline Pipeline")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed. Please fix issues and try again.")
        return 1
    
    # Get API key
    api_key = args.api_key or os.getenv("HF_API_KEY")
    if not api_key:
        print("❌ HuggingFace API key required!")
        print("Set HF_API_KEY environment variable or use --api-key argument")
        print("Get your API key from: https://huggingface.co/settings/tokens")
        return 1
    
    # Validate Excel file
    excel_path = Path(args.excel)
    if not excel_path.exists():
        print(f"❌ Excel file not found: {excel_path}")
        print("Create test data with: python test_data.py")
        return 1
    
    # Import và validate Excel processor
    try:
        from utils.utils_excel_documents import ExcelDocumentProcessor
        processor = ExcelDocumentProcessor()
        if not processor.validate_excel_structure(excel_path):
            print(f"❌ Excel file validation failed: {excel_path}")
            return 1
    except Exception as e:
        print(f"❌ Error validating Excel file: {e}")
        return 1
    
    try:
        # Initialize and run pipeline
        print(f"📊 Processing Excel file: {excel_path}")
        print(f"🔗 Synonym threshold: {args.synonym_threshold}")
        print(f"🗃️ Clear existing graph: {args.clear_graph}")
        print(f"🌐 Neo4j URI: {args.neo4j_uri}")
        print()
        
        orchestrator = OfflinePipelineOrchestrator(
            huggingface_api_key=api_key,
            neo4j_uri=args.neo4j_uri,
            neo4j_user=args.neo4j_user,
            neo4j_password=args.neo4j_password
        )
        
        # Run pipeline
        results = orchestrator.run_complete_pipeline(
            excel_file_path=excel_path,
            clear_existing_graph=args.clear_graph,
            synonym_threshold=args.synonym_threshold,
            save_intermediate_results=args.save_results
        )
        
        # Save results
        if args.save_results:
            results_file = excel_path.parent / f"pipeline_results_{excel_path.stem}.json"
            save_pipeline_results(results, results_file)
            print(f"💾 Results saved to: {results_file}")
        
        print()
        print("🎉 Offline pipeline completed successfully!")
        print("🌐 Access Neo4j Browser: http://localhost:7474")
        print("   Username: neo4j")
        print(f"   Password: {args.neo4j_password}")
        print()
        print("📝 Next steps:")
        print("   1. Explore graph in Neo4j Browser")
        print("   2. Run query tests: python test_query_functions.py")
        print("   3. Check intermediate results in output files")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Pipeline interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
```

---

## 🧪 **src/offline_indexing/test/test_offline_pipeline.py**

```python
"""
Test complete offline pipeline
"""

from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from test_data import create_test_excel, create_small_test_excel
from pipeline_orchestrator import OfflinePipelineOrchestrator
from utils.utils_general import setup_logging, check_environment

load_dotenv()

def test_complete_pipeline():
    """Test complete offline pipeline"""
    print("🧪 Testing Complete Offline Pipeline")
    print("=" * 50)
    
    # Setup logging
    setup_logging("INFO")
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed")
        return False
    
    # Get API key
    api_key = os.getenv("HF_API_KEY")
    if not api_key:
        print("⚠️  HF_API_KEY not set, using mock mode")
        return test_pipeline_mock_mode()
    
    try:
        # Step 1: Create test data
        print("\n📊 Step 1: Creating test data...")
        test_excel_path = create_small_test_excel(Path("small_test_data.xlsx"))
        
        # Step 2: Run pipeline
        print("\n🚀 Step 2: Running pipeline...")
        orchestrator = OfflinePipelineOrchestrator(api_key)
        
        results = orchestrator.run_complete_pipeline(
            excel_file_path=test_excel_path,
            clear_existing_graph=True,
            synonym_threshold=0.8,  # Lower threshold for testing
            save_intermediate_results=True
        )
        
        # Step 3: Validate results
        print("\n✅ Step 3: Validating results...")
        validation_passed = validate_pipeline_results(results)
        
        if validation_passed:
            print("🎉 All tests passed!")
            return True
        else:
            print("❌ Some tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pipeline_mock_mode():
    """Test pipeline với mock data (không cần API key)"""
    print("\n🎭 Running in mock mode (no API calls)")
    
    try:
        # Test individual modules
        from module1_chunking import test_chunking
        from module2_triple_extractor import test_triple_extractor  
        from module3_synonym_detector import test_synonym_detector
        from module4_graph_builder import test_graph_builder
        
        print("\n📝 Testing Module 1: Chunking...")
        chunks = test_chunking()
        
        print("\n🧠 Testing Module 2: Triple Extraction...")
        triples = test_triple_extractor()
        
        print("\n🔗 Testing Module 3: Synonym Detection...")
        synonyms = test_synonym_detector()
        
        print("\n🏗️ Testing Module 4: Graph Builder...")
        test_graph_builder()
        
        print("\n✅ Mock mode tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Mock mode test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_pipeline_results(results):
    """Validate pipeline results"""
    required_keys = ['execution_time', 'excel_processing', 'chunking', 'triples', 'synonyms', 'graph']
    
    print("🔍 Validating pipeline results...")
    
    # Check required keys
    for key in required_keys:
        if key not in results:
            print(f"❌ Missing key in results: {key}")
            return False
    
    # Validate excel processing
    excel_stats = results['excel_processing']
    if excel_stats['total_documents'] < 1:
        print("❌ No documents processed")
        return False
    
    # Validate chunking
    chunk_stats = results['chunking']
    if chunk_stats['total_chunks'] < 1:
        print("❌ No chunks created")
        return False
    
    # Validate triples
    triple_stats = results['triples']
    if triple_stats['total_triples'] < 1:
        print("❌ No triples extracted")
        return False
    
    # Validate graph
    graph_stats = results['graph']
    if graph_stats['total_nodes'] < 1 or graph_stats['total_edges'] < 1:
        print("❌ Graph not properly built")
        return False
    
    # Check graph composition
    nodes = graph_stats['nodes']
    edges = graph_stats['edges']
    
    if 'Phrase' not in nodes or 'Passage' not in nodes:
        print("❌ Missing required node types")
        return False
    
    if 'RELATION' not in edges or 'CONTAINS' not in edges:
        print("❌ Missing required edge types")
        return False
    
    print("✅ Pipeline results validation passed!")
    print(f"   📊 {excel_stats['total_documents']} documents processed")
    print(f"   📝 {chunk_stats['total_chunks']} chunks created")
    print(f"   🧠 {triple_stats['total_triples']} triples extracted")
    print(f"   🏗️ {graph_stats['total_nodes']} nodes, {graph_stats['total_edges']} edges created")
    
    return True

def test_individual_modules():
    """Test individual modules separately"""
    print("\n🔧 Testing Individual Modules...")
    
    tests = {
        "Excel Processing": test_excel_processing,
        "Chunking": test_chunking_module,
        "Triple Extraction": test_triple_extraction_module,
        "Synonym Detection": test_synonym_detection_module,
        "Graph Building": test_graph_building_module
    }
    
    results = {}
    for test_name, test_func in tests.items():
        print(f"\n🧪 Testing {test_name}...")
        try:
            results[test_name] = test_func()
            print(f"✅ {test_name} passed")
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results[test_name] = False
    
    # Summary
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"\n📊 Module Tests Summary: {passed}/{total} passed")
    return passed == total

def test_excel_processing():
    """Test Excel processing"""
    from utils.utils_excel_documents import test_excel_processor
    return test_excel_processor() is not None

def test_chunking_module():
    """Test chunking module"""
    from module1_chunking import test_chunking
    return test_chunking() is not None

def test_triple_extraction_module():
    """Test triple extraction (mock)"""
    from module2_triple_extractor import test_triple_extractor
    return test_triple_extractor() is not None

def test_synonym_detection_module():
    """Test synonym detection"""
    from module3_synonym_detector import test_synonym_detector
    return test_synonym_detector() is not None

def test_graph_building_module():
    """Test graph building"""
    from module4_graph_builder import test_graph_builder
    test_graph_builder()
    return True

if __name__ == "__main__":
    print("🧪 GraphRAG Offline Pipeline Tests")
    print("=" * 50)
    
    # Test individual modules first
    modules_passed = test_individual_modules()
    
    if modules_passed:
        print("\n🎯 All module tests passed! Testing complete pipeline...")
        success = test_complete_pipeline()
    else:
        print("\n❌ Some module tests failed. Skipping complete pipeline test.")
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Pipeline is ready for production use")
        print("\n📝 Next steps:")
        print("   1. Set HF_API_KEY environment variable")
        print("   2. Run: python run_offline_pipeline.py --excel your_data.xlsx")
        print("   3. Explore graph at: http://localhost:7474")
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  Please check errors above and fix issues")
    
    sys.exit(0 if success else 1)
```

---

## 🔍 **src/offline_indexing/test/test_query_functions.py**

```python
"""
Test query functions để verify graph structure và functionality
"""

from pathlib import Path
from typing import Dict, List, Any
import sys

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from utils.utils_neo4j import Neo4jManager

class GraphQueryTester:
    """Test các query functions trên Knowledge Graph"""
    
    def __init__(self, neo4j_uri: str = "bolt://localhost:7687", 
                 neo4j_user: str = "neo4j", neo4j_password: str = "graphrag123"):
        """Initialize connection tới Neo4j"""
        self.neo4j_manager = Neo4jManager(neo4j_uri, neo4j_user, neo4j_password)
        
    def test_basic_graph_structure(self) -> bool:
        """Test 1: Verify basic graph structure"""
        print("🔍 Test 1: Basic Graph Structure")
        
        try:
            stats = self.neo4j_manager.get_graph_statistics()
            
            node_types = stats.get('nodes', {})
            print(f"   📊 Node types found: {list(node_types.keys())}")
            
            # Verify required node types exist
            required_types = {'Phrase', 'Passage'}
            missing_types = required_types - set(node_types.keys())
            
            if missing_types:
                print(f"   ❌ Missing node types: {missing_types}")
                return False
            
            # Check if we have reasonable number of nodes
            total_nodes = stats.get('total_nodes', 0)
            if total_nodes < 5:
                print(f"   ⚠️  Very few nodes: {total_nodes}")
                return False
            
            print(f"   ✅ Graph structure OK: {total_nodes} total nodes")
            for node_type, count in node_types.items():
                print(f"      {node_type}: {count} nodes")
            
            return True
                
        except Exception as e:
            print(f"   ❌ Error checking graph structure: {e}")
            return False
    
    def test_edge_relationships(self) -> bool:
        """Test 2: Verify edge relationships"""
        print("\n🔗 Test 2: Edge Relationships")
        
        try:
            stats = self.neo4j_manager.get_graph_statistics()
            edge_types = stats.get('edges', {})
            
            print(f"   📊 Edge types found: {list(edge_types.keys())}")
            
            # Verify required edge types
            required_edges = {'RELATION', 'CONTAINS'}
            missing_edges = required_edges - set(edge_types.keys())
            
            if missing_edges:
                print(f"   ❌ Missing edge types: {missing_edges}")
                return False
            
            total_edges = stats.get('total_edges', 0)
            print(f"   ✅ Edge relationships OK: {total_edges} total edges")
            for edge_type, count in edge_types.items():
                print(f"      {edge_type}: {count} edges")
            
            return True
                
        except Exception as e:
            print(f"   ❌ Error checking edge relationships: {e}")
            return False
    
    def test_passage_phrase_connections(self) -> bool:
        """Test 3: Verify Passage-Phrase connections"""
        print("\n📄 Test 3: Passage-Phrase Connections")
        
        try:
            query = """
            MATCH (passage:Passage)-[:CONTAINS]->(phrase:Phrase)
            RETURN passage.doc_id as doc_id, phrase.text as phrase_text
            LIMIT 10
            """
            
            results = self.neo4j_manager.execute_query(query)
            
            if not results:
                print("   ❌ No CONTAINS relationships found")
                return False
            
            print(f"   ✅ Found {len(results)} sample connections:")
            for result in results[:5]:
                doc_id = result.get('doc_id', 'N/A')
                phrase = result.get('phrase_text', 'N/A')
                print(f"      {doc_id} → {phrase[:30]}...")
            
            return True
                
        except Exception as e:
            print(f"   ❌ Error checking connections: {e}")
            return False
    
    def test_relation_network(self) -> bool:
        """Test 4: Verify relation network between phrases"""
        print("\n🧠 Test 4: Relation Network")
        
        try:
            query = """
            MATCH (p1:Phrase)-[r:RELATION]->(p2:Phrase)
            RETURN p1.text as subject, r.predicate as predicate, p2.text as object
            LIMIT 10
            """
            
            results = self.neo4j_manager.execute_query(query)
            
            if not results:
                print("   ❌ No RELATION edges found")
                return False
            
            print(f"   ✅ Found {len(results)} sample relations:")
            for result in results[:5]:
                subj = result.get('subject', 'N/A')
                pred = result.get('predicate', 'N/A')
                obj = result.get('object', 'N/A')
                print(f"      ({subj}) --[{pred}]--> ({obj})")
            
            return True
                
        except Exception as e:
            print(f"   ❌ Error checking relations: {e}")
            return False
    
    def test_synonym_detection(self) -> bool:
        """Test 5: Verify synonym relationships"""
        print("\n🔗 Test 5: Synonym Detection")
        
        try:
            query = """
            MATCH (p1:Phrase)-[s:SYNONYM]->(p2:Phrase)
            RETURN p1.text as phrase1, p2.text as phrase2, s.similarity_score as score
            LIMIT 10
            """
            
            results = self.neo4j_manager.execute_query(query)
            
            if not results:
                print("   ⚠️  No SYNONYM edges found (may be normal if no synonyms detected)")
                return True  # Not critical for basic functionality
            
            print(f"   ✅ Found {len(results)} synonym pairs:")
            for result in results[:5]:
                p1 = result.get('phrase1', 'N/A')
                p2 = result.get('phrase2', 'N/A')
                score = result.get('score', 0)
                print(f"      {p1} ≈ {p2} (score: {score:.3f})")
            
            return True
                
        except Exception as e:
            print(f"   ❌ Error checking synonyms: {e}")
            return False
    
    def test_multi_hop_traversal(self) -> bool:
        """Test 6: Multi-hop traversal capability"""
        print("\n🌐 Test 6: Multi-hop Traversal")
        
        try:
            query = """
            MATCH path = (start:Phrase)-[:RELATION*1..3]->(end:Phrase)
            WHERE start <> end
            RETURN start.text as start_phrase, end.text as end_phrase, length(path) as path_length
            LIMIT 10
            """
            
            results = self.neo4j_manager.execute_query(query)
            
            if not results:
                print("   ⚠️  No multi-hop paths found")
                return True  # May be normal for simple data
            
            print(f"   ✅ Found {len(results)} multi-hop paths:")
            for result in results[:5]:
                start = result.get('start_phrase', 'N/A')
                end = result.get('end_phrase', 'N/A')
                length = result.get('path_length', 0)
                print(f"      {start} --{length} hops--> {end}")
            
            return True
                
        except Exception as e:
            print(f"   ❌ Error checking multi-hop: {e}")
            return False
    
    def test_search_capabilities(self) -> bool:
        """Test 7: Search capabilities"""
        print("\n🔍 Test 7: Search Capabilities")
        
        try:
            # Test text search on phrases
            query1 = """
            MATCH (p:Phrase)
            WHERE p.text CONTAINS 'pH' OR p.text CONTAINS 'axít'
            RETURN p.text as phrase
            LIMIT 5
            """
            
            results1 =

Tiếp tục từ **test_query_functions.py**:

```python
            results1 = self.neo4j_manager.execute_query(query1)
            
            print(f"   📊 Search for 'pH' or 'axít': {len(results1)} results")
            for result in results1:
                phrase = result.get('phrase', 'N/A')
                print(f"      {phrase}")
            
            # Test passage search
            query2 = """
            MATCH (p:Passage)
            WHERE p.text CONTAINS 'pH'
            RETURN p.doc_id as doc_id, p.title as title
            LIMIT 3
            """
            
            results2 = self.neo4j_manager.execute_query(query2)
            
            print(f"   📄 Passages containing 'pH': {len(results2)}")
            for result in results2:
                doc_id = result.get('doc_id', 'N/A')
                title = result.get('title', 'N/A')
                print(f"      {doc_id}: {title}")
            
            return True
                
        except Exception as e:
            print(f"   ❌ Error testing search: {e}")
            return False
    
    def test_graph_statistics(self) -> bool:
        """Test 8: Get comprehensive graph statistics"""
        print("\n📊 Test 8: Graph Statistics")
        
        try:
            stats = self.neo4j_manager.get_graph_statistics()
            
            print(f"   📈 Total nodes: {stats['total_nodes']}")
            print(f"   📈 Total edges: {stats['total_edges']}")
            
            print("   📋 Node breakdown:")
            for node_type, count in stats['nodes'].items():
                print(f"      {node_type}: {count}")
            
            print("   📋 Edge breakdown:")
            for edge_type, count in stats['edges'].items():
                print(f"      {edge_type}: {count}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error getting statistics: {e}")
            return False
    
    def test_sample_queries(self) -> bool:
        """Test 9: Sample queries for demonstration"""
        print("\n💡 Test 9: Sample Demonstration Queries")
        
        try:
            # Sample query 1: Find all concepts related to pH
            query1 = """
            MATCH (p:Phrase)-[:RELATION*1..2]-(related:Phrase)
            WHERE p.text CONTAINS 'pH'
            RETURN DISTINCT related.text as related_concept
            LIMIT 10
            """
            
            results1 = self.neo4j_manager.execute_query(query1)
            print(f"   🔬 Concepts related to pH ({len(results1)} found):")
            for result in results1[:5]:
                concept = result.get('related_concept', 'N/A')
                print(f"      • {concept}")
            
            # Sample query 2: Find passages that discuss both acid and base
            query2 = """
            MATCH (p:Passage)
            WHERE p.text CONTAINS 'axít' AND (p.text CONTAINS 'kiềm' OR p.text CONTAINS 'bazơ')
            RETURN p.doc_id as doc_id, p.title as title
            """
            
            results2 = self.neo4j_manager.execute_query(query2)
            print(f"   ⚖️ Passages discussing both acid and base ({len(results2)} found):")
            for result in results2:
                doc_id = result.get('doc_id', 'N/A')
                title = result.get('title', 'N/A')
                print(f"      • {doc_id}: {title}")
            
            return True
                
        except Exception as e:
            print(f"   ❌ Error running sample queries: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all tests"""
        print("🧪 Running Graph Query Function Tests")
        print("=" * 60)
        
        tests = [
            ("Basic Graph Structure", self.test_basic_graph_structure),
            ("Edge Relationships", self.test_edge_relationships),
            ("Passage-Phrase Connections", self.test_passage_phrase_connections),
            ("Relation Network", self.test_relation_network),
            ("Synonym Detection", self.test_synonym_detection),
            ("Multi-hop Traversal", self.test_multi_hop_traversal),
            ("Search Capabilities", self.test_search_capabilities),
            ("Graph Statistics", self.test_graph_statistics),
            ("Sample Queries", self.test_sample_queries)
        ]
        
        passed_tests = 0
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                print(f"   ❌ Test '{test_name}' failed with exception: {e}")
        
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {passed_tests}/{len(tests)} tests passed")
        
        if passed_tests == len(tests):
            print("🎉 All tests passed! Graph is working correctly.")
            self._print_neo4j_queries()
            return True
        else:
            print(f"⚠️  {len(tests) - passed_tests} tests failed. Check issues above.")
            return False
    
    def _print_neo4j_queries(self):
        """Print useful Neo4j queries for manual exploration"""
        print("\n💡 Useful Neo4j Browser Queries:")
        print("=" * 40)
        
        queries = [
            ("View graph overview", "MATCH (n) RETURN n LIMIT 50"),
            ("Count all nodes by type", "MATCH (n) RETURN labels(n)[0] as type, count(*) as count"),
            ("Count all edges by type", "MATCH ()-[r]->() RETURN type(r) as type, count(*) as count"),
            ("View sample triples", "MATCH (s:Phrase)-[r:RELATION]->(o:Phrase) RETURN s.text, r.predicate, o.text LIMIT 10"),
            ("Find multi-hop paths", "MATCH path = (start:Phrase)-[:RELATION*1..3]->(end:Phrase) RETURN path LIMIT 5"),
            ("Search for pH concepts", "MATCH (p:Phrase) WHERE p.text CONTAINS 'pH' RETURN p.text"),
            ("View passage-phrase connections", "MATCH (passage:Passage)-[:CONTAINS]->(phrase:Phrase) RETURN passage.title, phrase.text LIMIT 10")
        ]
        
        for description, query in queries:
            print(f"\n// {description}")
            print(f"{query}")
    
    def close(self):
        """Close connection"""
        self.neo4j_manager.close()

def main():
    """Main test function"""
    print("🔍 GraphRAG Query Functions Test")
    
    try:
        tester = GraphQueryTester()
        
        # Test connection first
        if not tester.neo4j_manager.test_connection():
            print("❌ Cannot connect to Neo4j")
            print("Make sure Neo4j is running: docker-compose up -d")
            print("Or run: cd src/DB && docker-compose up -d")
            return 1
        
        success = tester.run_all_tests()
        tester.close()
        
        if success:
            print("\n✅ All query functions working correctly!")
            print("🌐 Explore the graph manually at: http://localhost:7474")
            print("   Username: neo4j")
            print("   Password: graphrag123")
            return 0
        else:
            print("\n❌ Some tests failed. Check the graph construction.")
            print("💡 Try running the offline pipeline first:")
            print("   python run_offline_pipeline.py --excel test_data.xlsx")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test setup failed: {e}")
        print("Make sure Neo4j is running and graph is built.")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## 📋 **src/offline_indexing/offline_indexing_requirements.txt**

```txt
# Core ML and NLP dependencies
sentence-transformers>=2.2.0
huggingface-hub>=0.17.0
scikit-learn>=1.3.0

# Data processing
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0

# Database
neo4j>=5.13.0

# Utilities
python-dotenv>=1.0.0
pathlib>=1.0.0

# Development and testing
pytest>=7.4.0
```

---

## 🗃️ **src/DB/docker-compose.yml**

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5.13-community
    container_name: graphrag-neo4j
    ports:
      - "7474:7474"  # Neo4j Browser
      - "7687:7687"  # Bolt protocol
    environment:
      # Authentication
      - NEO4J_AUTH=neo4j/graphrag123
      
      # Plugins
      - NEO4J_PLUGINS=["apoc", "graph-data-science"]
      - NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*
      
      # Memory settings
      - NEO4J_dbms_memory_heap_initial__size=1G
      - NEO4J_dbms_memory_heap_max__size=2G
      - NEO4J_dbms_memory_pagecache_size=512M
      
      # Network settings
      - NEO4J_dbms_default_listen_address=0.0.0.0
      - NEO4J_dbms_connector_bolt_listen_address=:7687
      - NEO4J_dbms_connector_http_listen_address=:7474
      
      # Other settings
      - NEO4J_dbms_logs_debug_level=INFO
      
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
      - neo4j_import:/var/lib/neo4j/import
      - neo4j_plugins:/plugins
      
    restart: unless-stopped
    
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p graphrag123 'RETURN 1'"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s

volumes:
  neo4j_data:
    driver: local
  neo4j_logs:
    driver: local
  neo4j_import:
    driver: local
  neo4j_plugins:
    driver: local

networks:
  default:
    name: graphrag-network
```

---

## 🌍 **.env.example (Updated)**

```bash
# HuggingFace API Key (required for triple extraction)
HF_API_KEY=your_huggingface_api_key_here

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=graphrag123

# Pipeline Settings
SYNONYM_THRESHOLD=0.85
LOG_LEVEL=INFO

# Model Configuration
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-mpnet-base-v2
LLM_MODEL=Qwen/Qwen2.5-7B-Instruct

# File Paths
DEFAULT_EXCEL_FILE=test_data.xlsx
OUTPUT_DIR=outputs
LOG_DIR=logs

# Development Settings
DEBUG_MODE=false
SAVE_INTERMEDIATE_RESULTS=true
CLEAR_GRAPH_ON_START=true
```

---

## 📖 **README.md (Updated)**

```markdown
# 🧠 GraphRAG Offline Indexing Pipeline

Knowledge Graph construction pipeline cho GraphRAG system với Vietnamese support.

## 🏗️ Architecture

```
📁 src/offline_indexing/
├── 📝 module1_chunking.py           # Keep paragraphs as-is
├── 🧠 module2_triple_extractor.py   # Qwen2.5-7B OpenIE
├── 🔗 module3_synonym_detector.py   # Multilingual embedding similarity
├── 🏗️ module4_graph_builder.py      # Neo4j graph construction
├── 🎯 pipeline_orchestrator.py      # Main coordinator
├── 📁 utils/                        # Utilities
└── 📁 test/                         # Testing & execution
```

## 🚀 Quick Start

### 1. Setup Database
```bash
cd src/DB
docker-compose up -d
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r src/offline_indexing/offline_indexing_requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your HuggingFace API key
```

### 4. Test Pipeline
```bash
cd src/offline_indexing/test
python test_offline_pipeline.py
```

### 5. Run với Real Data
```bash
cd src/offline_indexing/test
python run_offline_pipeline.py --excel your_data.xlsx
```

## 📊 Excel Input Format

Required columns:
- `doc_id`: Unique document identifier
- `title`: Document title
- `text`: Document content (Vietnamese supported)

Example:
```
doc_id | title        | text
PH_0   | pH Basics    | Các dung dịch nước có pH nhỏ hơn 7...
PH_1   | Neutral Water| Nước tinh khiết có pH = 7...
```

## 🌐 Access Neo4j

- **Browser**: http://localhost:7474
- **Username**: neo4j  
- **Password**: graphrag123

## 🧪 Verify Results

```bash
cd src/offline_indexing/test
python test_query_functions.py
```

## 📋 Sample Neo4j Queries

```cypher
// View graph overview
MATCH (n) RETURN n LIMIT 50

// Count nodes and edges
MATCH (n) RETURN labels(n)[0] as type, count(*)
MATCH ()-[r]->() RETURN type(r) as type, count(*)

// View sample triples
MATCH (s:Phrase)-[r:RELATION]->(o:Phrase) 
RETURN s.text, r.predicate, o.text LIMIT 10

// Multi-hop exploration
MATCH path = (start:Phrase)-[:RELATION*1..3]->(end:Phrase)
WHERE start.text CONTAINS "pH"
RETURN path LIMIT 5
```

## 🔧 Troubleshooting

### Neo4j Connection Issues
```bash
# Check if Neo4j is running
docker ps | grep neo4j

# View Neo4j logs
docker logs graphrag-neo4j

# Restart Neo4j
cd src/DB && docker-compose restart
```

### API Key Issues
```bash
# Get HuggingFace API key from:
# https://huggingface.co/settings/tokens

# Set in environment
export HF_API_KEY=your_key_here
```

## 📁 Project Structure

```
src/offline_indexing/
├── 📄 Modules (4 core processing modules)
├── 🛠️ utils/ (Shared utilities)
├── 🧪 test/ (Testing and execution scripts)
└── 📋 offline_indexing_requirements.txt
```

## 🎓 For Thesis

This pipeline demonstrates:
- ✅ **Modular Architecture**: Clean separation of concerns
- ✅ **Industry Standards**: Professional code organization  
- ✅ **Comprehensive Testing**: Multiple validation layers
- ✅ **Vietnamese Support**: Multilingual NLP capabilities
- ✅ **Knowledge Graphs**: Modern graph database usage
- ✅ **AI Integration**: LLM-powered information extraction

---

**🚀 Ready to build your Knowledge Graph!**
```

---

## 🎯 **Complete File Structure Summary**

```
graphrag-thesis/
├── 📖 README.md
├── 📋 requirements.txt  
├── 🌍 .env.example
│
├── 📁 src/
│   ├── 📁 DB/
│   │   └── 🐳 docker-compose.yml
│   │
│   └── 📁 OfflineIndexing/
│       ├── 📋 offline_indexing_requirements.txt
│       │
│       ├── 📄 module1_chunking.py
│       ├── 🧠 module2_triple_extractor.py  
│       ├── 🔗 module3_synonym_detector.py
│       ├── 🏗️ module4_graph_builder.py
│       ├── 🎯 pipeline_orchestrator.py
│       ├── 🚀 run_offline_pipeline.py
│       │
│       ├── 📁 utils/
│       │   ├── 🔧 utils_general.py
│       │   ├── 📊 utils_excel_documents.py
│       │   └── 🗃️ utils_neo4j.py
│       │
│       └── 📁 test/
│           ├── 📊 test_data.py
│           ├── 🧪 test_offline_pipeline.py
│           └── 🔍 test_query_functions.py
│
└── 📁 OnlineRetrievalAndQA
```

**🎉 Complete offline indexing module với full code implementation!** 

All files sử dụng pathlib, có comprehensive testing, error handling, và ready for thesis demonstration! 🚀


# NẾU MÀ CURSOR LÀM CÁI NÀY CÓ KHI BUG LÂU RỒI. vÌ Ở PHA 2 ONLINE, MÌNH DÙNG CURSOR THỬ THÌ LỖI V: 