"""
Doan Ngoc Cuong - 30/05/2025
OfflineIndexing/module4_graph_builder.py
Module 4: Graph Builder - HippoRAG 2 Style with Meaningful Phrase IDs
Build Neo4j Knowledge Graph WITHOUT canonical mapping
Uses actual phrase text as node IDs for better readability
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import re
import logging
from dataclasses import dataclass

# Import Neo4j utilities
from utils.utils_neo4j import Neo4jManager

def safe_unicode_log(logger, message, level="info"):
    """
    IMPROVED: Safely log messages with Vietnamese characters
    Handles all possible Unicode encoding errors
    """
    try:
        # First attempt: normal logging
        getattr(logger, level)(message)
    except (UnicodeEncodeError, UnicodeError, Exception) as e:
        # Fallback 1: ASCII replacement
        try:
            safe_message = message.encode('ascii', errors='replace').decode('ascii')
            getattr(logger, level)(f"{safe_message} [Unicode replaced]")
        except Exception:
            # Fallback 2: Just log the action without content
            try:
                getattr(logger, level)(f"[Phrase mapping completed - {len(message)} characters]")
            except Exception:
                # Ultimate fallback: Silent (do nothing)
                pass

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
    """Build Knowledge Graph trong Neo4j - HippoRAG 2 Style với meaningful IDs"""
    
    def __init__(self, neo4j_uri: str = "bolt://localhost:7687", 
                 neo4j_user: str = "neo4j", neo4j_password: str = "graphrag123"):
        """Initialize connection tới Neo4j"""
        logger.info(f"Initializing GraphBuilder (HippoRAG 2 style) with Neo4j at {neo4j_uri}")
        self.neo4j_manager = Neo4jManager(neo4j_uri, neo4j_user, neo4j_password)
        self.nodes_created = 0
        self.edges_created = 0
        
        # Test connection
        if not self.neo4j_manager.test_connection():
            logger.error("Failed to connect to Neo4j")
            raise Exception("Failed to connect to Neo4j")
        logger.info("Successfully connected to Neo4j")
    
    def _normalize_phrase_for_id(self, phrase: str) -> str:
        """Convert phrase text to valid Neo4j node ID"""
        # Convert to lowercase and strip
        normalized = phrase.lower().strip()
        
        # Replace spaces and special characters with underscores
        normalized = re.sub(r'[^\w\s]', '', normalized)  # Remove special chars
        normalized = re.sub(r'\s+', '_', normalized)     # Spaces to underscores
        normalized = re.sub(r'_+', '_', normalized)      # Multiple underscores to single
        normalized = normalized.strip('_')               # Remove leading/trailing underscores
        
        # Ensure it starts with letter (Neo4j requirement for some operations)
        if normalized and not normalized[0].isalpha():
            normalized = f"phrase_{normalized}"
        
        # Handle empty case
        if not normalized:
            normalized = "empty_phrase"
            
        return normalized
    
    def setup_constraints_and_indexes(self):
        """Setup database constraints và indexes"""
        try:
            logger.info("Setting up database constraints and indexes...")
            self.neo4j_manager.setup_constraints_and_indexes()
            logger.info("Database constraints and indexes setup completed")
        except Exception as e:
            logger.error(f"Error setting up constraints and indexes: {str(e)}")
            logger.exception("Detailed error trace:")
            raise
            
    def clear_database(self):
        """Clear existing data"""
        try:
            logger.info("Clearing existing database...")
            self.neo4j_manager.clear_all_data()
            logger.info("Successfully cleared existing database")
        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")
            logger.exception("Detailed error trace:")
            raise
    
    def build_graph_hipporag_style(self, chunks: List[Dict[str, Any]], triples: List[Any], 
                                 synonym_pairs: List[Any]):
        """Main method để build complete graph - HippoRAG 2 style (NO canonical mapping)"""
        logger.info("Starting graph construction (HippoRAG 2 style with meaningful IDs)...")
        logger.info(f"Input data: {len(chunks)} chunks, {len(triples)} triples, {len(synonym_pairs)} synonym pairs")
        logger.info("NOTE: No canonical mapping - preserving all phrase surface forms")
        logger.info("Using normalized phrase text as node IDs for better readability")
        
        # Setup database
        self.setup_constraints_and_indexes()
        
        # Build nodes (NO canonical mapping)
        logger.info("Building nodes (preserving all surface forms)...")
        self._create_passage_nodes(chunks)
        self._create_phrase_nodes_hipporag_style(triples)  # NO canonical mapping
        
        # Build edges
        logger.info("Building edges...")
        self._create_relation_edges_hipporag_style(triples)  # NO canonical mapping
        self._create_synonym_edges(synonym_pairs)
        self._create_contains_edges_hipporag_style(chunks, triples)  # NO canonical mapping
        
        logger.info(f"Graph construction completed: {self.nodes_created} nodes, {self.edges_created} edges")
        logger.info("HippoRAG 2 style: All phrase variants preserved, connected via synonym edges")
    
    def _create_passage_nodes(self, chunks: List[Dict[str, Any]]):
        """Create Passage nodes từ chunks"""
        logger.info(f"Creating {len(chunks)} Passage nodes...")
        
        # Initialize encoder
        from sentence_transformers import SentenceTransformer
        logger.debug("Initializing sentence transformer for embeddings")
        encoder = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        
        for idx, chunk in enumerate(chunks, 1):
            passage_id = f"passage_{chunk['chunk_id']}"
            logger.debug(f"Processing chunk {idx}/{len(chunks)}: {passage_id}")
            
            # Compute embedding
            logger.debug(f"Computing embedding for passage {passage_id}")
            embedding = encoder.encode(chunk['text']).tolist()
            
            properties = {
                'id': passage_id,
                'chunk_id': chunk['chunk_id'],
                'doc_id': chunk['doc_id'],
                'title': chunk.get('title', ''),
                'text': chunk['text'],
                'chunk_index': chunk.get('chunk_index', 0),
                'source': chunk.get('metadata', {}).get('source', ''),
                'text_length': len(chunk['text']),
                'embedding': embedding
            }
            
            self.neo4j_manager.create_passage_node(passage_id, properties)
            self.nodes_created += 1
            logger.debug(f"Created Passage node {passage_id}")
        
        logger.info(f"Created {len(chunks)} Passage nodes")
    
    def _create_phrase_nodes_hipporag_style(self, triples: List[Any]):
        """Create Phrase nodes từ triples - HippoRAG 2 style với meaningful IDs"""
        logger.info("Creating Phrase nodes (HippoRAG 2 style - meaningful IDs)...")
        
        # Collect ALL phrases (including duplicates/variants)
        all_phrases = []
        phrase_to_triple_map = {}  # Track which triples contain each phrase
        
        for triple in triples:
            subject = triple.subject.strip().lower()
            obj = triple.object.strip().lower()
            
            all_phrases.append(subject)
            all_phrases.append(obj)
            
            # Track source triples for each phrase
            if subject not in phrase_to_triple_map:
                phrase_to_triple_map[subject] = []
            if obj not in phrase_to_triple_map:
                phrase_to_triple_map[obj] = []
                
            phrase_to_triple_map[subject].append(triple)
            phrase_to_triple_map[obj].append(triple)
        
        # Get unique phrases but preserve original forms
        unique_phrases = list(set(all_phrases))
        logger.info(f"Found {len(unique_phrases)} unique phrases (all surface forms preserved)")
        
        # Initialize encoder for embeddings
        from sentence_transformers import SentenceTransformer
        logger.debug("Initializing sentence transformer for phrase embeddings")
        encoder = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        
        # Create phrase nodes - MEANINGFUL IDs từ phrase text
        phrase_id_mapping = {}  # phrase_text -> phrase_id
        id_collisions = {}      # Track ID collisions
        
        for idx, phrase in enumerate(unique_phrases, 1):
            # Create meaningful ID from phrase text
            base_phrase_id = self._normalize_phrase_for_id(phrase)
            
            # Handle ID collisions (different phrases with same normalized form)
            phrase_id = base_phrase_id
            collision_count = 1
            while phrase_id in id_collisions:
                phrase_id = f"{base_phrase_id}_{collision_count}"
                collision_count += 1
            
            id_collisions[phrase_id] = phrase
            phrase_id_mapping[phrase] = phrase_id
            
            logger.debug(f"Processing phrase {idx}/{len(unique_phrases)}: ID: '{phrase_id}'")
            
            # Compute embedding
            embedding = encoder.encode(phrase).tolist()
            
            # Count occurrences across triples
            occurrence_count = len(phrase_to_triple_map.get(phrase, []))
            
            properties = {
                'id': phrase_id,
                'text': phrase,                    # Original phrase text
                'normalized_text': phrase.lower().strip(),  # For text matching
                'text_length': len(phrase),
                'occurrence_count': occurrence_count,
                'embedding': embedding
            }
            
            self.neo4j_manager.create_phrase_node(phrase_id, properties)
            self.nodes_created += 1
            logger.debug(f"Created Phrase node '{phrase_id}'")
        
        # Store mapping for later use
        self.phrase_id_mapping = phrase_id_mapping
        logger.info(f"Created {len(unique_phrases)} Phrase nodes with meaningful IDs")
        
        # FIXED: Safe logging without Unicode issues
        logger.info(f"Phrase ID mapping completed: {len(phrase_id_mapping)} phrases processed")
        logger.info("Phrase examples available in Neo4j database (check Phrase nodes with 'text' property)")
    
    def _create_relation_edges_hipporag_style(self, triples: List[Any]):
        """Create RELATION edges giữa Phrase nodes - HippoRAG 2 style"""
        logger.info(f"Creating {len(triples)} RELATION edges (no canonical mapping)...")
        
        for idx, triple in enumerate(triples, 1):
            # Use original phrase forms (no canonical mapping)
            subject = triple.subject.strip().lower()
            obj = triple.object.strip().lower()
            
            # Get phrase IDs
            subject_id = self.phrase_id_mapping.get(subject)
            obj_id = self.phrase_id_mapping.get(obj)
            
            if not subject_id or not obj_id:
                logger.warning(f"Missing phrase ID for triple {idx}: {subject} -> {obj}")
                continue
            
            properties = {
                'predicate': triple.predicate,
                'confidence': triple.confidence,
                'source_chunk': triple.source_chunk_id,
                'source_doc': triple.source_doc_id,
                'extraction_method': getattr(triple, 'extraction_method', 'unknown')
            }
            
            # Create edge using meaningful phrase IDs
            self.neo4j_manager.create_relation_edge_by_id(subject_id, obj_id, properties)
            self.edges_created += 1
            logger.debug(f"Created RELATION edge {idx}: '{subject_id}' -> '{obj_id}'")
        
        logger.info(f"Created {len(triples)} RELATION edges")
    
    def _create_synonym_edges(self, synonym_pairs: List[Any]):
        """Create SYNONYM edges giữa Phrase nodes - KEY FEATURE của HippoRAG 2"""
        logger.info(f"Creating {len(synonym_pairs)} SYNONYM edges (HippoRAG 2 style)...")
        
        if not synonym_pairs:
            logger.info("No synonym pairs found - skipping synonym edge creation")
            return
        
        for idx, pair in enumerate(synonym_pairs, 1):
            phrase1 = pair.phrase1.strip().lower()
            phrase2 = pair.phrase2.strip().lower()
            
            # Get phrase IDs
            phrase1_id = self.phrase_id_mapping.get(phrase1)
            phrase2_id = self.phrase_id_mapping.get(phrase2)
            
            if not phrase1_id or not phrase2_id:
                logger.warning(f"Missing phrase ID for synonym pair {idx}: {phrase1} <-> {phrase2}")
                continue
            
            properties = {
                'similarity_score': pair.similarity_score
            }
            
            # Create bidirectional synonym edges (like HippoRAG 2)
            self.neo4j_manager.create_synonym_edge_by_id(phrase1_id, phrase2_id, properties)
            self.edges_created += 1
            logger.debug(f"Created SYNONYM edge {idx}: '{phrase1_id}' <-> '{phrase2_id}' (score: {pair.similarity_score:.3f})")
        
        logger.info(f"Created {len(synonym_pairs)} SYNONYM edges")
        logger.info("SYNONYM edges enable semantic connectivity between phrase variants")
    
    def _create_contains_edges_hipporag_style(self, chunks: List[Dict[str, Any]], 
                                            triples: List[Any]):
        """Create CONTAINS edges từ Passage đến Phrase nodes - HippoRAG 2 style"""
        logger.info("Creating CONTAINS edges (no canonical mapping)...")
        
        # Create mapping từ chunk_id đến phrases (original forms)
        chunk_phrases = {}
        
        for triple in triples:
            chunk_id = triple.source_chunk_id
            if chunk_id not in chunk_phrases:
                chunk_phrases[chunk_id] = set()
            
            # Use original phrase forms (no canonical mapping)
            subject = triple.subject.strip().lower()
            obj = triple.object.strip().lower()
            
            chunk_phrases[chunk_id].add(subject)
            chunk_phrases[chunk_id].add(obj)
        
        logger.debug(f"Found phrases for {len(chunk_phrases)} chunks")
        
        # Create CONTAINS edges
        total_edges = 0
        for chunk_id, phrases in chunk_phrases.items():
            passage_id = f"passage_{chunk_id}"
            logger.debug(f"Creating CONTAINS edges for passage {passage_id} with {len(phrases)} phrases")
            
            for phrase in phrases:
                phrase_id = self.phrase_id_mapping.get(phrase)
                if phrase_id:
                    properties = {}
                    self.neo4j_manager.create_contains_edge_by_id(passage_id, phrase_id, properties)
                    self.edges_created += 1
                    total_edges += 1
                else:
                    logger.warning(f"Missing phrase ID for CONTAINS edge: {phrase}")
        
        logger.info(f"Created {total_edges} CONTAINS edges")
    
    def get_graph_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        logger.info("Getting graph statistics...")
        stats = self.neo4j_manager.get_graph_statistics()
        
        # Add HippoRAG 2 specific stats
        stats['hipporag_style'] = True
        stats['canonical_mapping'] = False
        stats['surface_forms_preserved'] = True
        stats['meaningful_phrase_ids'] = True
        
        logger.info(f"Graph statistics: {stats}")
        return stats
    
    def close(self):
        """Close Neo4j connection"""
        logger.info("Closing Neo4j connection")
        self.neo4j_manager.close()
        logger.info("Neo4j connection closed")

# Test function
def test_graph_builder():
    """Test function cho Module 4 with meaningful IDs"""
    logger.info("Starting graph builder test (HippoRAG 2 style with meaningful IDs)")
    print("Testing Graph Builder (HippoRAG 2 Style with Meaningful IDs)...")
    
    # Test phrase ID normalization
    builder = GraphBuilder()
    
    test_phrases = [
        "dung dịch axít",
        "pH nhỏ hơn 7",
        "nước tinh khiết",
        "H2O",
        "axít-bazơ"
    ]
    
    print("\nTesting phrase ID normalization:")
    for phrase in test_phrases:
        normalized_id = builder._normalize_phrase_for_id(phrase)
        print(f"  '{phrase}' -> '{normalized_id}'")
    
    try:
        # Test connection
        stats = builder.get_graph_statistics()
        print(f"\nCurrent Graph Statistics:")
        print(f"  Nodes: {stats.get('total_nodes', 0)}")
        print(f"  Edges: {stats.get('total_edges', 0)}")
        print(f"  HippoRAG Style: {stats.get('hipporag_style', False)}")
        print(f"  Meaningful IDs: {stats.get('meaningful_phrase_ids', False)}")
        
        builder.close()
        logger.info("Graph builder test completed successfully")
        
    except Exception as e:
        logger.error(f"Error testing Graph Builder: {str(e)}")
        logger.exception("Detailed error trace:")
        print(f"Error testing Graph Builder: {e}")
        print("Make sure Neo4j is running on bolt://localhost:7687")

if __name__ == "__main__":
    test_graph_builder()