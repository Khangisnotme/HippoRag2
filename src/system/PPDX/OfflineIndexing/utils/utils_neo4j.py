"""
Neo4j Database Utilities - Updated for HippoRAG 2 Style
Handle Neo4j operations, connections, và basic CRUD
Added methods for ID-based edge creation
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
                embedding: $embedding,
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
                       text_length=properties.get('text_length', 0),
                       embedding=properties.get('embedding', []))
    
    def create_phrase_node(self, phrase_id: str, properties: Dict[str, Any]):
        """Create a Phrase node"""
        with self.driver.session() as session:
            query = """
            CREATE (p:Phrase {
                id: $id,
                text: $text,
                normalized_text: $normalized_text,
                text_length: $text_length,
                occurrence_count: $occurrence_count,
                embedding: $embedding,
                created_at: datetime()
            })
            """
            
            session.run(query,
                       id=phrase_id,
                       text=properties.get('text', ''),
                       normalized_text=properties.get('normalized_text', ''),
                       text_length=properties.get('text_length', 0),
                       occurrence_count=properties.get('occurrence_count', 0),
                       embedding=properties.get('embedding', []))
    
    def create_relation_edge(self, subject_text: str, object_text: str, properties: Dict[str, Any]):
        """Create RELATION edge giữa hai Phrase nodes (legacy method - by text)"""
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
    
    def create_relation_edge_by_id(self, subject_id: str, object_id: str, properties: Dict[str, Any]):
        """Create RELATION edge giữa hai Phrase nodes by ID (HippoRAG 2 style)"""
        with self.driver.session() as session:
            query = """
            MATCH (s:Phrase {id: $subject_id})
            MATCH (o:Phrase {id: $object_id})
            CREATE (s)-[:RELATION {
                predicate: $predicate,
                confidence: $confidence,
                source_chunk: $source_chunk,
                source_doc: $source_doc,
                created_at: datetime()
            }]->(o)
            """
            
            session.run(query,
                       subject_id=subject_id,
                       object_id=object_id,
                       predicate=properties.get('predicate', ''),
                       confidence=properties.get('confidence', 1.0),
                       source_chunk=properties.get('source_chunk', ''),
                       source_doc=properties.get('source_doc', ''))
    
    def create_synonym_edge(self, phrase1_text: str, phrase2_text: str, properties: Dict[str, Any]):
        """Create SYNONYM edge giữa hai Phrase nodes (legacy method - by text)"""
        with self.driver.session() as session:
            # Kiểm tra sự tồn tại của node Phrase
            check_p1 = session.run("MATCH (p:Phrase) WHERE toLower(p.normalized_text) = toLower($phrase) RETURN p LIMIT 1", 
                                  phrase=phrase1_text).single()
            check_p2 = session.run("MATCH (p:Phrase) WHERE toLower(p.normalized_text) = toLower($phrase) RETURN p LIMIT 1", 
                                  phrase=phrase2_text).single()
            
            if not check_p1:
                logger.warning(f"Node Phrase with normalized_text='{phrase1_text}' not found")
                return False
            if not check_p2:
                logger.warning(f"Node Phrase with normalized_text='{phrase2_text}' not found")
                return False
            
            # Lấy ID thực tế của node để tạo cạnh chính xác
            p1_id = check_p1["p"]["id"]
            p2_id = check_p2["p"]["id"]
            
            # Tạo cạnh sử dụng ID thay vì normalized_text
            query = """
            MATCH (p1:Phrase {id: $p1_id})
            MATCH (p2:Phrase {id: $p2_id})
            CREATE (p1)-[:SYNONYM {
                similarity_score: $similarity,
                created_at: datetime()
            }]->(p2)
            RETURN p1, p2
            """
            
            result = session.run(query,
                       p1_id=p1_id,
                       p2_id=p2_id,
                       similarity=properties.get('similarity_score', 1.0))
            
            if result.peek():
                logger.info(f"Created SYNONYM edge: '{phrase1_text}' <-> '{phrase2_text}'")
                return True
            else:
                logger.warning(f"Failed to create SYNONYM edge: '{phrase1_text}' <-> '{phrase2_text}'")
                return False
    
    def create_synonym_edge_by_id(self, phrase1_id: str, phrase2_id: str, properties: Dict[str, Any]):
        """Create SYNONYM edge giữa hai Phrase nodes by ID (HippoRAG 2 style)"""
        with self.driver.session() as session:
            # Create bidirectional synonym edges
            query = """
            MATCH (p1:Phrase {id: $phrase1_id})
            MATCH (p2:Phrase {id: $phrase2_id})
            CREATE (p1)-[:SYNONYM {
                similarity_score: $similarity,
                created_at: datetime()
            }]->(p2)
            CREATE (p2)-[:SYNONYM {
                similarity_score: $similarity,
                created_at: datetime()
            }]->(p1)
            RETURN p1, p2
            """
            
            result = session.run(query,
                       phrase1_id=phrase1_id,
                       phrase2_id=phrase2_id,
                       similarity=properties.get('similarity_score', 1.0))
            
            if result.peek():
                logger.debug(f"Created bidirectional SYNONYM edges between {phrase1_id} <-> {phrase2_id}")
                return True
            else:
                logger.warning(f"Failed to create SYNONYM edges between {phrase1_id} <-> {phrase2_id}")
                return False
    
    def create_contains_edge(self, passage_id: str, phrase_text: str, properties: Dict[str, Any]):
        """Create CONTAINS edge từ Passage đến Phrase (legacy method - by text)"""
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
    
    def create_contains_edge_by_id(self, passage_id: str, phrase_id: str, properties: Dict[str, Any]):
        """Create CONTAINS edge từ Passage đến Phrase by ID (HippoRAG 2 style)"""
        with self.driver.session() as session:
            query = """
            MATCH (passage:Passage {id: $passage_id})
            MATCH (phrase:Phrase {id: $phrase_id})
            CREATE (passage)-[:CONTAINS {
                created_at: datetime()
            }]->(phrase)
            """
            
            session.run(query,
                       passage_id=passage_id,
                       phrase_id=phrase_id)
    
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
    
    def get_synonym_edge_statistics(self) -> Dict[str, Any]:
        """Get detailed synonym edge statistics (HippoRAG 2 specific)"""
        with self.driver.session() as session:
            # Count synonym edges
            synonym_count = session.run("""
                MATCH ()-[r:SYNONYM]->()
                RETURN count(r) as synonym_edges
            """).single()["synonym_edges"]
            
            # Average similarity score
            avg_similarity = session.run("""
                MATCH ()-[r:SYNONYM]->()
                RETURN avg(r.similarity_score) as avg_similarity
            """).single()["avg_similarity"]
            
            # Phrase nodes with synonyms
            phrases_with_synonyms = session.run("""
                MATCH (p:Phrase)-[:SYNONYM]->()
                RETURN count(DISTINCT p) as phrases_with_synonyms
            """).single()["phrases_with_synonyms"]
            
            return {
                'synonym_edges': synonym_count,
                'avg_similarity_score': avg_similarity or 0.0,
                'phrases_with_synonyms': phrases_with_synonyms
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
    print("Testing Neo4j Manager (HippoRAG 2 Style)...")
    
    try:
        manager = Neo4jManager()
        
        # Test connection
        if manager.test_connection():
            print("Neo4j connection successful")
            
            # Get statistics
            stats = manager.get_graph_statistics()
            print(f"Current nodes: {stats['total_nodes']}")
            print(f"Current edges: {stats['total_edges']}")
            
            # Get synonym statistics
            synonym_stats = manager.get_synonym_edge_statistics()
            print(f"Synonym edges: {synonym_stats['synonym_edges']}")
            print(f"Phrases with synonyms: {synonym_stats['phrases_with_synonyms']}")
        else:
            print("Neo4j connection failed")
        
        manager.close()
        
    except Exception as e:
        print(f"Error testing Neo4j Manager: {e}")

if __name__ == "__main__":
    test_neo4j_manager()