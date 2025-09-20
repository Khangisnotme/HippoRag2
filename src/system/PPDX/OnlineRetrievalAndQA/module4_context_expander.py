"""
OnlineRetrievalAndQA/module4_context_expander.py
Module 4: Context Expansion based on Filtered Triples (Mở rộng Context dựa trên Triple đã lọc)
Updated để work với real data từ Knowledge Graph
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple, Set
import logging
import time
import json
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, Counter
import math
import datetime

# Neo4j connection
from neo4j import GraphDatabase

# Shared utilities
from utils.utils_shared_general import (
    setup_logger,
    log_performance,
    validate_query,
    clean_text,
    save_json,
    load_json,
    PerformanceStats
)

# Module imports
from module1_dual_retrieval import RetrievedItem
from module2_triple_filter import FilteredTriple, RelevanceLevel

# Setup logger with file output
log_file = Path("outputs/log/module4_context_expander_{}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
logger = setup_logger(__name__, log_file=log_file)

# ==================== ENUMS AND CONSTANTS ====================

class ExpansionStrategy(Enum):
    """Các chiến lược mở rộng context khác nhau"""
    SUBJECT_FOCUSED = "subject_focused"
    OBJECT_FOCUSED = "object_focused"
    BIDIRECTIONAL = "bidirectional"
    RELATION_AWARE = "relation_aware"
    ADAPTIVE = "adaptive"

class ContextRelevanceLevel(Enum):
    """Các mức độ liên quan của expanded context"""
    DIRECT = "direct"
    INDIRECT = "indirect" 
    SUPPLEMENTARY = "supplementary"
    PERIPHERAL = "peripheral"

class ExpansionDirection(Enum):
    """Hướng mở rộng trên graph"""
    OUTGOING = "outgoing"
    INCOMING = "incoming" 
    BOTH = "both"

# ==================== DATA CLASSES ====================

@dataclass
class ContextExpansionConfig:
    """Cấu hình toàn diện cho hệ thống mở rộng context"""
    # Core expansion parameters
    expansion_strategy: ExpansionStrategy = ExpansionStrategy.BIDIRECTIONAL
    expansion_direction: ExpansionDirection = ExpansionDirection.BOTH
    max_expansion_depth: int = 1
    max_expanded_items: int = 50
    
    # Filtering parameters
    relevance_threshold: float = 0.3
    enable_context_filtering: bool = True
    enable_synonym_expansion: bool = True
    
    # Relation filtering
    relation_type_filter: List[str] = None
    exclude_relation_types: List[str] = None
    
    # Context quality parameters
    context_diversity_threshold: float = 0.8
    enable_context_ranking: bool = True
    boost_factor_direct_relations: float = 1.2
    penalty_factor_distant_context: float = 0.8
    
    # Neo4j connection parameters
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "graphrag123"
    
    def __post_init__(self):
        """Validate configuration sau khi khởi tạo"""
        if self.max_expansion_depth > 1:
            logger.warning(f"⚠️ Max expansion depth {self.max_expansion_depth} > 1, chỉ hỗ trợ 1-hop trong version này")
            self.max_expansion_depth = 1
        
        if self.relation_type_filter is None:
            self.relation_type_filter = []
        
        if self.exclude_relation_types is None:
            self.exclude_relation_types = []

@dataclass
class ExpandedContext:
    """Context item đã được mở rộng với comprehensive metadata"""
    context_id: str
    context_type: str
    source_triple_id: str
    expansion_path: str
    context_text: str
    relevance_score: float
    relevance_level: ContextRelevanceLevel
    distance_from_source: int
    supporting_evidence: Dict[str, Any]
    expansion_metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi ExpandedContext object thành dictionary"""
        result = asdict(self)
        result['relevance_level'] = self.relevance_level.value
        return result
    
    def is_relevant(self, threshold: Optional[float] = None) -> bool:
        """Kiểm tra context có relevant không"""
        if threshold is None:
            threshold = 0.3
        return self.relevance_score >= threshold
    
    def get_summary(self) -> str:
        """Tạo summary ngắn gọn về expanded context"""
        return (f"{self.context_type.title()}: {self.context_text[:60]}... | "
                f"Relevance: {self.relevance_score:.3f} ({self.relevance_level.value}) | "
                f"Path: {self.expansion_path}")

@dataclass
class ExpansionResult:
    """Kết quả hoàn chỉnh của quá trình context expansion"""
    expanded_contexts: List[ExpandedContext]
    source_triples_count: int
    expanded_contexts_count: int
    expansion_time: float
    query: str
    statistics: Dict[str, Any]
    expansion_config: ContextExpansionConfig
    
    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi ExpansionResult thành dictionary"""
        result = asdict(self)
        result['expansion_config'] = asdict(self.expansion_config)
        result['expansion_config']['expansion_strategy'] = self.expansion_config.expansion_strategy.value
        result['expansion_config']['expansion_direction'] = self.expansion_config.expansion_direction.value
        return result
    
    def save_to_file(self, filepath: Path):
        """Lưu kết quả expansion vào file JSON"""
        save_json(self.to_dict(), filepath, indent=2)
        logger.info(f"💾 Đã lưu kết quả expansion vào file: {filepath}")
        logger.info(f"   📊 Contexts: {self.source_triples_count} → {self.expanded_contexts_count}")
        logger.info(f"   ⏱️ Thời gian: {self.expansion_time:.2f} giây")
    
    def get_expansion_efficiency(self) -> float:
        """Tính hiệu suất expansion"""
        if self.source_triples_count == 0:
            return 0.0
        return self.expanded_contexts_count / self.source_triples_count
    
    def get_relevance_distribution(self) -> Dict[str, int]:
        """Thống kê phân bố relevance levels"""
        distribution = {}
        for level in ContextRelevanceLevel:
            count = sum(1 for context in self.expanded_contexts 
                       if context.relevance_level == level)
            distribution[level.value] = count
        return distribution

# ==================== NEO4J DATA ACCESS UTILITIES ====================

class Neo4jDataAccess:
    """Utility class cho Neo4j data access"""
    
    def __init__(self, uri: str, user: str, password: str):
        """Khởi tạo kết nối Neo4j"""
        logger.info(f"🗃️ Đang kết nối đến Neo4j: {uri}")
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("✅ Kết nối Neo4j thành công")
        except Exception as e:
            logger.error(f"❌ Lỗi kết nối Neo4j: {e}")
            raise
    
    def close(self):
        """Đóng kết nối database"""
        if self.driver:
            self.driver.close()
            logger.info("🔐 Đã đóng kết nối Neo4j")
    
    def get_all_triples(self) -> List[Dict[str, Any]]:
        """Lấy tất cả relation triples từ Neo4j"""
        logger.info("🔗 Đang truy vấn tất cả triples từ Neo4j...")
        
        with self.driver.session() as session:
            query = """
            MATCH (s:Phrase)-[r:RELATION]->(o:Phrase)
            RETURN s.text as subject, r.predicate as predicate, o.text as object,
                   r.confidence as confidence, r.source_chunk as source_passage_id,
                   r.original_subject as original_subject, r.original_object as original_object
            ORDER BY r.confidence DESC
            """
            
            result = session.run(query)
            triples = []
            
            for record in result:
                triple = {
                    'subject': record['subject'] or '',
                    'predicate': record['predicate'] or '',
                    'object': record['object'] or '',
                    'confidence': record['confidence'] or 1.0,
                    'source_passage_id': record['source_passage_id'] or '',
                    'original_subject': record['original_subject'] or record['subject'] or '',
                    'original_object': record['original_object'] or record['object'] or ''
                }
                triples.append(triple)
            
            logger.info(f"✅ Đã truy xuất {len(triples)} triples từ Neo4j")
            return triples
    
    def check_graph_status(self) -> Dict[str, Any]:
        """Kiểm tra trạng thái Knowledge Graph"""
        with self.driver.session() as session:
            stats = {}
            
            # Count all nodes
            result = session.run("MATCH (n) RETURN count(n) as total_nodes")
            stats['total_nodes'] = result.single()['total_nodes']
            
            # Count phrase nodes
            result = session.run("MATCH (p:Phrase) RETURN count(p) as phrase_nodes")
            stats['phrase_nodes'] = result.single()['phrase_nodes']
            
            # Count passage nodes
            result = session.run("MATCH (p:Passage) RETURN count(p) as passage_nodes")
            stats['passage_nodes'] = result.single()['passage_nodes']
            
            # Count relation edges
            result = session.run("MATCH ()-[r:RELATION]->() RETURN count(r) as relation_edges")
            stats['relation_edges'] = result.single()['relation_edges']
            
            # Count synonym edges
            result = session.run("MATCH ()-[s:SYNONYM]-() RETURN count(s) as synonym_edges")
            stats['synonym_edges'] = result.single()['synonym_edges']
            
            # Sample phrases
            result = session.run("MATCH (p:Phrase) RETURN p.text LIMIT 5")
            stats['sample_phrases'] = [record['p.text'] for record in result]
            
            return stats

# ==================== CORE COMPONENTS ====================

class GraphTraverser:
    """Component thực hiện 1-hop traversal trên Neo4j Knowledge Graph"""
    
    def __init__(self, config: ContextExpansionConfig):
        """Khởi tạo GraphTraverser với Neo4j connection"""
        self.config = config
        self.driver = None
        
        logger.info("🔗 Khởi tạo GraphTraverser...")
        logger.info(f"   🎯 Strategy: {config.expansion_strategy.value}")
        logger.info(f"   📍 Direction: {config.expansion_direction.value}")
        logger.info(f"   📊 Max items: {config.max_expanded_items}")
        
        self._connect_neo4j()
    
    def _connect_neo4j(self):
        """Kết nối đến Neo4j database"""
        try:
            logger.info(f"🗃️ Đang kết nối đến Neo4j: {self.config.neo4j_uri}")
            self.driver = GraphDatabase.driver(
                self.config.neo4j_uri,
                auth=(self.config.neo4j_user, self.config.neo4j_password)
            )
            
            # Test connection và log graph status
            neo4j_access = Neo4jDataAccess(self.config.neo4j_uri, self.config.neo4j_user, self.config.neo4j_password)
            graph_stats = neo4j_access.check_graph_status()
            neo4j_access.close()
            
            logger.info("✅ Kết nối Neo4j thành công")
            logger.info(f"   📊 Graph Stats: {graph_stats['total_nodes']} nodes, {graph_stats['relation_edges']} relations")
            logger.info(f"   📝 Sample entities: {graph_stats['sample_phrases'][:3]}")
            
        except Exception as e:
            logger.error(f"❌ Lỗi kết nối Neo4j: {e}")
            raise
    
    def expand_from_triples(self, filtered_triples: List[FilteredTriple]) -> List[Dict[str, Any]]:
        """Mở rộng context từ danh sách filtered triples"""
        logger.info(f"🔗 Bắt đầu expansion từ {len(filtered_triples)} filtered triples...")
        
        all_expanded_contexts = []
        processed_entities = set()
        
        for i, triple in enumerate(filtered_triples, 1):
            logger.info(f"   📊 Processing triple {i}/{len(filtered_triples)}: {triple.triple_id}")
            logger.info(f"      🔗 Triple: {triple.subject} → {triple.predicate} → {triple.object}")
            
            # Extract entities để expand
            entities_to_expand = self._extract_expansion_entities(triple)
            logger.info(f"      🎯 Entities to expand: {entities_to_expand}")
            
            for entity in entities_to_expand:
                if entity and entity not in processed_entities:
                    # Expand từ entity này
                    entity_contexts = self._expand_from_entity(entity, triple)
                    all_expanded_contexts.extend(entity_contexts)
                    processed_entities.add(entity)
                    
                    logger.info(f"         🔍 Expanded từ '{entity}': {len(entity_contexts)} contexts")
        
        # Remove duplicates và apply limits
        unique_contexts = self._deduplicate_contexts(all_expanded_contexts)
        limited_contexts = unique_contexts[:self.config.max_expanded_items]
        
        logger.info(f"✅ Expansion hoàn thành:")
        logger.info(f"   📊 Raw contexts: {len(all_expanded_contexts)}")
        logger.info(f"   🔄 After dedup: {len(unique_contexts)}")
        logger.info(f"   📋 Final contexts: {len(limited_contexts)}")
        
        return limited_contexts
    
    def _extract_expansion_entities(self, triple: FilteredTriple) -> List[str]:
        """Trích xuất entities để expand dựa trên strategy"""
        entities = []
        
        if self.config.expansion_strategy == ExpansionStrategy.SUBJECT_FOCUSED:
            entities.append(triple.subject)
        elif self.config.expansion_strategy == ExpansionStrategy.OBJECT_FOCUSED:
            entities.append(triple.object)
        elif self.config.expansion_strategy == ExpansionStrategy.BIDIRECTIONAL:
            entities.extend([triple.subject, triple.object])
        elif self.config.expansion_strategy == ExpansionStrategy.RELATION_AWARE:
            if self._should_expand_relation(triple.predicate):
                entities.extend([triple.subject, triple.object])
        elif self.config.expansion_strategy == ExpansionStrategy.ADAPTIVE:
            if triple.query_relevance_score >= 0.7:
                entities.extend([triple.subject, triple.object])
            elif triple.query_relevance_score >= 0.5:
                entities.append(triple.subject)
        
        return entities
    
    def _should_expand_relation(self, predicate: str) -> bool:
        """Kiểm tra có nên expand relation này không"""
        if self.config.relation_type_filter:
            if predicate not in self.config.relation_type_filter:
                return False
        
        if self.config.exclude_relation_types:
            if predicate in self.config.exclude_relation_types:
                return False
        
        return True
    
    def _expand_from_entity(self, entity: str, source_triple: FilteredTriple) -> List[Dict[str, Any]]:
        """Mở rộng 1-hop từ một entity với improved query strategies"""
        expanded_contexts = []
        
        with self.driver.session() as session:
            # Trước tiên check entity có tồn tại không
            entity_exists = self._check_entity_exists(session, entity)
            logger.info(f"         📍 Entity '{entity}' exists: {entity_exists}")
            
            if not entity_exists:
                # Try fuzzy matching
                similar_entities = self._find_similar_entities(session, entity)
                if similar_entities:
                    logger.info(f"         🔍 Found similar entities: {similar_entities[:3]}")
                    # Use first similar entity
                    entity = similar_entities[0]
                else:
                    logger.info(f"         ❌ No similar entities found for '{entity}'")
                    return []
            
            # Query dựa trên expansion direction
            if self.config.expansion_direction in [ExpansionDirection.OUTGOING, ExpansionDirection.BOTH]:
                outgoing_contexts = self._get_outgoing_contexts(session, entity, source_triple)
                expanded_contexts.extend(outgoing_contexts)
            
            if self.config.expansion_direction in [ExpansionDirection.INCOMING, ExpansionDirection.BOTH]:
                incoming_contexts = self._get_incoming_contexts(session, entity, source_triple)
                expanded_contexts.extend(incoming_contexts)
            
            # Synonym expansion nếu enabled
            if self.config.enable_synonym_expansion:
                synonym_contexts = self._get_synonym_contexts(session, entity, source_triple)
                expanded_contexts.extend(synonym_contexts)
        
        return expanded_contexts
    
    def _check_entity_exists(self, session, entity: str) -> bool:
        """Kiểm tra entity có tồn tại trong KG không"""
        query = "MATCH (p:Phrase {text: $entity}) RETURN count(p) as count"
        result = session.run(query, entity=entity)
        count = result.single()['count']
        return count > 0
    
    def _find_similar_entities(self, session, entity: str) -> List[str]:
        """Tìm entities tương tự"""
        # Strategy 1: Contains search
        query = """
        MATCH (p:Phrase) 
        WHERE p.text CONTAINS $partial_entity 
        RETURN p.text 
        LIMIT 10
        """
        result = session.run(query, partial_entity=entity[:min(3, len(entity))])
        similar = [record['p.text'] for record in result]
        
        if not similar and len(entity) > 3:
            # Strategy 2: Broader contains search
            query = """
            MATCH (p:Phrase) 
            WHERE toLower(p.text) CONTAINS toLower($entity) OR toLower($entity) CONTAINS toLower(p.text)
            RETURN p.text 
            LIMIT 10
            """
            result = session.run(query, entity=entity)
            similar = [record['p.text'] for record in result]
        
        return similar
    
    def _get_outgoing_contexts(self, session, entity: str, source_triple: FilteredTriple) -> List[Dict[str, Any]]:
        """Lấy outgoing contexts với improved queries"""
        query = """
        MATCH (source:Phrase {text: $entity})-[r:RELATION]->(target:Phrase)
        RETURN source.text as source_text, r.predicate as predicate, 
               target.text as target_text, r.confidence as confidence,
               r.source_chunk as source_chunk
        LIMIT 20
        """
        
        result = session.run(query, entity=entity)
        contexts = []
        
        for record in result:
            if self._should_expand_relation(record['predicate']):
                context = {
                    'context_type': 'triple',
                    'source_triple_id': source_triple.triple_id,
                    'expansion_path': f"{entity} → {record['predicate']} → {record['target_text']}",
                    'context_text': f"{record['source_text']} {record['predicate']} {record['target_text']}",
                    'relation_confidence': record['confidence'] or 0.8,
                    'source_chunk': record['source_chunk'] or '',
                    'expansion_direction': 'outgoing',
                    'distance_from_source': 1
                }
                contexts.append(context)
        
        return contexts
    
    def _get_incoming_contexts(self, session, entity: str, source_triple: FilteredTriple) -> List[Dict[str, Any]]:
        """Lấy incoming contexts"""
        query = """
        MATCH (source:Phrase)-[r:RELATION]->(target:Phrase {text: $entity})
        RETURN source.text as source_text, r.predicate as predicate,
               target.text as target_text, r.confidence as confidence,
               r.source_chunk as source_chunk
        LIMIT 20
        """
        
        result = session.run(query, entity=entity)
        contexts = []
        
        for record in result:
            if self._should_expand_relation(record['predicate']):
                context = {
                    'context_type': 'triple',
                    'source_triple_id': source_triple.triple_id,
                    'expansion_path': f"{record['source_text']} → {record['predicate']} → {entity}",
                    'context_text': f"{record['source_text']} {record['predicate']} {record['target_text']}",
                    'relation_confidence': record['confidence'] or 0.8,
                    'source_chunk': record['source_chunk'] or '',
                    'expansion_direction': 'incoming',
                    'distance_from_source': 1
                }
                contexts.append(context)
        
        return contexts
    
    def _get_synonym_contexts(self, session, entity: str, source_triple: FilteredTriple) -> List[Dict[str, Any]]:
        """Lấy synonym contexts qua SYNONYM edges"""
        query = """
        MATCH (entity:Phrase {text: $entity})-[s:SYNONYM]-(synonym:Phrase)
        RETURN entity.text as entity_text, synonym.text as synonym_text,
               s.similarity as similarity
        LIMIT 10
        """
        
        result = session.run(query, entity=entity)
        contexts = []
        
        for record in result:
            similarity = record['similarity'] or 0.8
            if similarity >= 0.7:
                context = {
                    'context_type': 'synonym',
                    'source_triple_id': source_triple.triple_id,
                    'expansion_path': f"{entity} ↔ {record['synonym_text']} (synonym)",
                    'context_text': f"{record['synonym_text']} (synonym of {entity})",
                    'similarity_score': similarity,
                    'expansion_direction': 'synonym',
                    'distance_from_source': 1
                }
                contexts.append(context)
        
        return contexts
    
    def _deduplicate_contexts(self, contexts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Loại bỏ duplicate contexts"""
        seen_texts = set()
        unique_contexts = []
        
        for context in contexts:
            context_text = context.get('context_text', '')
            
            if context_text and context_text not in seen_texts:
                seen_texts.add(context_text)
                unique_contexts.append(context)
        
        return unique_contexts
    
    def close(self):
        """Đóng kết nối Neo4j"""
        if self.driver:
            self.driver.close()
            logger.info("🔐 Đã đóng kết nối Neo4j trong GraphTraverser")

class ContextFilter:
    """Component lọc và đánh giá relevance của expanded contexts"""
    
    def __init__(self, config: ContextExpansionConfig):
        """Khởi tạo ContextFilter"""
        self.config = config
        
        logger.info("🔍 Khởi tạo ContextFilter...")
        logger.info(f"   🎯 Relevance threshold: {config.relevance_threshold}")
        logger.info(f"   🔧 Context filtering: {'Bật' if config.enable_context_filtering else 'Tắt'}")
        logger.info(f"   📊 Context ranking: {'Bật' if config.enable_context_ranking else 'Tắt'}")
    
    def filter_and_score_contexts(self, raw_contexts: List[Dict[str, Any]], 
                                 query: str, 
                                 source_triples: List[FilteredTriple]) -> List[ExpandedContext]:
        """Lọc và scoring expanded contexts"""
        logger.info(f"🔍 Đang filter và score {len(raw_contexts)} raw contexts...")
        
        scored_contexts = []
        
        for i, raw_context in enumerate(raw_contexts, 1):
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(raw_context, query, source_triples)
            
            # Determine relevance level
            relevance_level = self._determine_relevance_level(relevance_score, raw_context)
            
            # Apply filtering nếu enabled
            if self.config.enable_context_filtering:
                if relevance_score < self.config.relevance_threshold:
                    logger.debug(f"   🚫 Filtered context {i}: score {relevance_score:.3f} < threshold {self.config.relevance_threshold}")
                    continue
            
            # Create ExpandedContext object
            expanded_context = ExpandedContext(
                context_id=f"context_{i:04d}",
                context_type=raw_context.get('context_type', 'unknown'),
                source_triple_id=raw_context.get('source_triple_id', ''),
                expansion_path=raw_context.get('expansion_path', ''),
                context_text=raw_context.get('context_text', ''),
                relevance_score=relevance_score,
                relevance_level=relevance_level,
                distance_from_source=raw_context.get('distance_from_source', 1),
                supporting_evidence={
                    'relation_confidence': raw_context.get('relation_confidence', 0.0),
                    'similarity_score': raw_context.get('similarity_score', 0.0),
                    'expansion_direction': raw_context.get('expansion_direction', 'unknown')
                },
                expansion_metadata={
                    'source_chunk': raw_context.get('source_chunk', ''),
                    'processing_timestamp': time.time()
                }
            )
            
            scored_contexts.append(expanded_context)
            
            if i % 10 == 0 or i == len(raw_contexts):
                logger.info(f"   📊 Processed {i}/{len(raw_contexts)} contexts")
        
        # Sort by relevance nếu ranking enabled
        if self.config.enable_context_ranking:
            scored_contexts.sort(key=lambda c: c.relevance_score, reverse=True)
            logger.info("   📈 Contexts đã được sorted theo relevance score")
        
        logger.info(f"✅ Context filtering hoàn thành: {len(raw_contexts)} → {len(scored_contexts)} contexts")
        return scored_contexts
    
    def _calculate_relevance_score(self, raw_context: Dict[str, Any], 
                                  query: str, 
                                  source_triples: List[FilteredTriple]) -> float:
        """Tính relevance score cho expanded context"""
        # Base score from context type và direction
        base_score = 0.5
        
        # Boost based on context type
        context_type = raw_context.get('context_type', '')
        if context_type == 'triple':
            base_score = 0.6
        elif context_type == 'synonym':
            base_score = 0.7
        
        # Boost based on relation confidence
        relation_confidence = raw_context.get('relation_confidence', 0.0)
        if relation_confidence > 0:
            confidence_boost = min(0.2, relation_confidence * 0.2)
            base_score += confidence_boost
        
        # Boost based on similarity (for synonyms)
        similarity_score = raw_context.get('similarity_score', 0.0)
        if similarity_score > 0:
            similarity_boost = min(0.15, similarity_score * 0.15)
            base_score += similarity_boost
        
        # Keyword matching với query
        context_text = raw_context.get('context_text', '').lower()
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # Count keyword matches
        keyword_matches = sum(1 for word in query_words if word in context_text)
        if query_words:
            keyword_ratio = keyword_matches / len(query_words)
            keyword_boost = keyword_ratio * 0.2
            base_score += keyword_boost
        
        # Find source triple relevance
        source_triple_id = raw_context.get('source_triple_id', '')
        source_triple = next((t for t in source_triples if t.triple_id == source_triple_id), None)
        
        if source_triple:
            source_relevance_boost = source_triple.query_relevance_score * 0.1
            base_score += source_relevance_boost
        
        # Apply modifiers
        expansion_direction = raw_context.get('expansion_direction', '')
        if expansion_direction == 'outgoing':
            base_score *= self.config.boost_factor_direct_relations
        elif expansion_direction in ['incoming', 'synonym']:
            base_score *= 1.1  # Slight boost
        
        # Distance penalty (for future multi-hop)
        distance = raw_context.get('distance_from_source', 1)
        if distance > 1:
            distance_penalty = self.config.penalty_factor_distant_context ** (distance - 1)
            base_score *= distance_penalty
        
        # Cap at 1.0
        final_score = min(base_score, 1.0)
        
        return final_score
    
    def _determine_relevance_level(self, relevance_score: float, raw_context: Dict[str, Any]) -> ContextRelevanceLevel:
        """Xác định relevance level dựa trên score và context properties"""
        # Base determination từ score
        if relevance_score >= 0.8:
            level = ContextRelevanceLevel.DIRECT
        elif relevance_score >= 0.6:
            level = ContextRelevanceLevel.INDIRECT
        elif relevance_score >= 0.4:
            level = ContextRelevanceLevel.SUPPLEMENTARY
        else:
            level = ContextRelevanceLevel.PERIPHERAL
        
        # Adjust based on context properties
        context_type = raw_context.get('context_type', '')
        
        # Synonyms usually direct
        if context_type == 'synonym' and level != ContextRelevanceLevel.DIRECT:
            if relevance_score >= 0.7:
                level = ContextRelevanceLevel.DIRECT
        
        # High confidence relations
        relation_confidence = raw_context.get('relation_confidence', 0.0)
        if relation_confidence >= 0.9 and level == ContextRelevanceLevel.PERIPHERAL:
            level = ContextRelevanceLevel.SUPPLEMENTARY
        
        return level

class ContextExpander:
    """Main class cho Context Expansion system"""
    
    def __init__(self, config: Optional[ContextExpansionConfig] = None):
        """Khởi tạo ContextExpander"""
        self.config = config or ContextExpansionConfig()
        
        logger.info("🚀 Khởi tạo ContextExpander system...")
        logger.info(f"   🎯 Strategy: {self.config.expansion_strategy.value}")
        logger.info(f"   📍 Direction: {self.config.expansion_direction.value}")
        logger.info(f"   📊 Max items: {self.config.max_expanded_items}")
        logger.info(f"   🔍 Relevance threshold: {self.config.relevance_threshold}")
        
        # Initialize components
        self.graph_traverser = GraphTraverser(self.config)
        self.context_filter = ContextFilter(self.config)
        
        logger.info("✅ ContextExpander components đã được khởi tạo")
    
    def expand_context(self, filtered_triples: List[FilteredTriple], query: str) -> ExpansionResult:
        """Main method để expand context từ filtered triples"""
        logger.info("=" * 60)
        logger.info("🔗 BẮT ĐẦU CONTEXT EXPANSION")
        logger.info("=" * 60)
        logger.info(f"📝 Query: '{query}'")
        logger.info(f"🔗 Filtered triples: {len(filtered_triples)}")
        logger.info(f"🎯 Strategy: {self.config.expansion_strategy.value}")
        
        start_time = time.time()
        
        # Validate inputs
        if not filtered_triples:
            logger.warning("⚠️ Không có filtered triples để expand")
            return self._create_empty_result(query, 0, "no_triples")
        
        if not validate_query(query):
            logger.error("❌ Invalid query")
            return self._create_empty_result(query, len(filtered_triples), "invalid_query")
        
        # Step 1: Graph traversal
        logger.info(f"\n🔗 BƯỚC 1: GRAPH TRAVERSAL")
        logger.info("-" * 40)
        raw_contexts = self.graph_traverser.expand_from_triples(filtered_triples)
        
        # Step 2: Context filtering và scoring
        logger.info(f"\n🔍 BƯỚC 2: CONTEXT FILTERING VÀ SCORING")
        logger.info("-" * 40)
        expanded_contexts = self.context_filter.filter_and_score_contexts(
            raw_contexts, query, filtered_triples
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Step 3: Create result với statistics
        logger.info(f"\n📈 BƯỚC 3: TẠO KẾT QUẢ VÀ THỐNG KÊ")
        logger.info("-" * 40)
        statistics = self._create_expansion_statistics(
            filtered_triples, expanded_contexts, total_time
        )
        
        result = ExpansionResult(
            expanded_contexts=expanded_contexts,
            source_triples_count=len(filtered_triples),
            expanded_contexts_count=len(expanded_contexts),
            expansion_time=total_time,
            query=query,
            statistics=statistics,
            expansion_config=self.config
        )
        
        # Log final summary
        self._log_expansion_summary(result)
        
        return result
    
    def _create_expansion_statistics(self, source_triples: List[FilteredTriple],
                                   expanded_contexts: List[ExpandedContext],
                                   processing_time: float) -> Dict[str, Any]:
        """Tạo comprehensive statistics cho expansion process"""
        logger.info("📈 Tạo expansion statistics...")
        
        # Basic counts
        source_count = len(source_triples)
        expanded_count = len(expanded_contexts)
        
        # Context type distribution
        context_types = Counter(context.context_type for context in expanded_contexts)
        
        # Relevance distribution
        relevance_distribution = {}
        for level in ContextRelevanceLevel:
            count = sum(1 for context in expanded_contexts 
                       if context.relevance_level == level)
            relevance_distribution[level.value] = count
        
        # Score statistics
        if expanded_contexts:
            relevance_scores = [c.relevance_score for c in expanded_contexts]
            score_stats = {
                'min': min(relevance_scores),
                'max': max(relevance_scores),
                'avg': sum(relevance_scores) / len(relevance_scores),
                'median': sorted(relevance_scores)[len(relevance_scores) // 2]
            }
        else:
            score_stats = {'min': 0, 'max': 0, 'avg': 0, 'median': 0}
        
        # Expansion path analysis
        expansion_paths = [c.expansion_path for c in expanded_contexts]
        unique_paths = len(set(expansion_paths))
        
        # Source triple analysis
        source_relevance_scores = [t.query_relevance_score for t in source_triples]
        source_score_avg = sum(source_relevance_scores) / len(source_relevance_scores) if source_relevance_scores else 0
        
        # Performance metrics
        performance_stats = {
            'total_time_seconds': processing_time,
            'contexts_per_second': expanded_count / processing_time if processing_time > 0 else 0,
            'expansion_rate': expanded_count / source_count if source_count > 0 else 0
        }
        
        # Configuration info
        config_stats = {
            'expansion_strategy': self.config.expansion_strategy.value,
            'expansion_direction': self.config.expansion_direction.value,
            'max_expanded_items': self.config.max_expanded_items,
            'relevance_threshold': self.config.relevance_threshold,
            'synonym_expansion_enabled': self.config.enable_synonym_expansion,
            'context_filtering_enabled': self.config.enable_context_filtering
        }
        
        return {
            'processing_counts': {
                'source_triples': source_count,
                'expanded_contexts': expanded_count,
                'expansion_efficiency': expanded_count / source_count if source_count > 0 else 0
            },
            'context_type_distribution': dict(context_types),
            'relevance_distribution': relevance_distribution,
            'score_statistics': score_stats,
            'source_triple_analysis': {
                'avg_source_relevance': source_score_avg,
                'high_relevance_sources': sum(1 for score in source_relevance_scores if score >= 0.7)
            },
            'expansion_path_analysis': {
                'total_paths': len(expansion_paths),
                'unique_paths': unique_paths,
                'path_diversity': unique_paths / len(expansion_paths) if expansion_paths else 0
            },
            'performance_metrics': performance_stats,
            'configuration': config_stats,
            'timestamp': time.time()
        }
    
    def _create_empty_result(self, query: str, source_count: int, reason: str) -> ExpansionResult:
        """Tạo empty ExpansionResult khi có lỗi"""
        logger.warning(f"🔄 Tạo empty expansion result (reason: {reason})")
        
        return ExpansionResult(
            expanded_contexts=[],
            source_triples_count=source_count,
            expanded_contexts_count=0,
            expansion_time=0.0,
            query=query,
            statistics={
                'error_info': {
                    'reason': reason,
                    'timestamp': time.time()
                }
            },
            expansion_config=self.config
        )
    
    def _log_expansion_summary(self, result: ExpansionResult):
        """Log comprehensive summary của expansion process"""
        logger.info("=" * 60)
        logger.info("🎉 CONTEXT EXPANSION HOÀN THÀNH")
        logger.info("=" * 60)
        
        # Basic metrics
        logger.info(f"📊 KẾT QUẢ TỔNG QUAN:")
        logger.info(f"   📝 Query: '{result.query}'")
        logger.info(f"   ⏱️ Thời gian xử lý: {result.expansion_time:.2f} giây")
        logger.info(f"   🔗 Triples: {result.source_triples_count} → {result.expanded_contexts_count} contexts")
        logger.info(f"   📈 Expansion rate: {result.get_expansion_efficiency():.2f} contexts/triple")
        
        # Context type distribution
        stats = result.statistics
        if 'context_type_distribution' in stats:
            type_dist = stats['context_type_distribution']
            logger.info(f"\n📊 PHÂN BỐ CONTEXT TYPES:")
            for context_type, count in type_dist.items():
                percentage = (count / result.expanded_contexts_count * 100) if result.expanded_contexts_count > 0 else 0
                logger.info(f"   {context_type}: {count} contexts ({percentage:.1f}%)")
        
        # Relevance distribution
        relevance_dist = result.get_relevance_distribution()
        logger.info(f"\n📈 PHÂN BỐ RELEVANCE:")
        for level, count in relevance_dist.items():
            percentage = (count / result.expanded_contexts_count * 100) if result.expanded_contexts_count > 0 else 0
            logger.info(f"   {level}: {count} contexts ({percentage:.1f}%)")
        
        # Performance metrics
        if 'performance_metrics' in stats:
            perf = stats['performance_metrics']
            logger.info(f"\n⚡ PERFORMANCE:")
            logger.info(f"   🏃 Contexts/giây: {perf['contexts_per_second']:.1f}")
            logger.info(f"   📊 Expansion rate: {perf['expansion_rate']:.2f}")
        
        logger.info("=" * 60)
    
    def close(self):
        """Đóng tất cả connections và cleanup resources"""
        logger.info("🔐 Đang đóng ContextExpander...")
        self.graph_traverser.close()
        logger.info("✅ ContextExpander đã được đóng")

# ==================== UTILITY FUNCTIONS ====================

def create_default_expansion_config() -> ContextExpansionConfig:
    """Tạo cấu hình mặc định cho Context Expander"""
    logger.info("⚙️ Tạo default ContextExpansionConfig...")
    
    config = ContextExpansionConfig(
        expansion_strategy=ExpansionStrategy.BIDIRECTIONAL,
        expansion_direction=ExpansionDirection.BOTH,
        max_expanded_items=50,
        relevance_threshold=0.3,
        enable_context_filtering=True,
        enable_synonym_expansion=True,
        enable_context_ranking=True
    )
    
    logger.info("✅ Default expansion config đã được tạo")
    return config

def quick_expand_context(filtered_triples: List[FilteredTriple], 
                        query: str,
                        strategy: str = "bidirectional") -> ExpansionResult:
    """Quick utility function để expand context với cấu hình đơn giản"""
    logger.info(f"🚀 Quick expansion với strategy: {strategy}")
    
    # Create config based on strategy
    config = create_default_expansion_config()
    config.expansion_strategy = ExpansionStrategy(strategy)
    
    # Initialize expander và process
    expander = ContextExpander(config)
    result = expander.expand_context(filtered_triples, query)
    expander.close()
    
    return result

# ==================== TEST FUNCTIONS ====================

def test_context_expansion_with_mock_data():
    """Test Context Expansion với mock data"""
    print("🧪 BẮT ĐẦU TEST CONTEXT EXPANSION")
    print("=" * 50)
    
    # Mock filtered triples từ Module 2
    from module2_triple_filter import RelevanceLevel as TripleRelevanceLevel
    
    mock_filtered_triples = [
        FilteredTriple(
            triple_id="triple_001",
            subject="táo",
            predicate="chứa",
            object="vitamin C",
            original_text="táo chứa vitamin C",
            query_relevance_score=0.9,
            relevance_level=TripleRelevanceLevel.HIGHLY_RELEVANT,
            confidence_score=0.85,
            llm_explanation="Triple trả lời trực tiếp về thành phần dinh dưỡng của táo",
            source_passage_id="passage_001",
            original_hybrid_retrieval_score=0.75,
            filtering_metadata={}
        ),
        FilteredTriple(
            triple_id="triple_002",
            subject="vitamin C",
            predicate="tăng cường",
            object="hệ miễn dịch",
            original_text="vitamin C tăng cường hệ miễn dịch",
            query_relevance_score=0.8,
            relevance_level=TripleRelevanceLevel.HIGHLY_RELEVANT,
            confidence_score=0.9,
            llm_explanation="Triple giải thích lợi ích sức khỏe của vitamin C",
            source_passage_id="passage_002",
            original_hybrid_retrieval_score=0.7,
            filtering_metadata={}
        )
    ]
    
    test_query = "Lợi ích của táo cho sức khỏe là gì?"
    
    print(f"📝 Test query: '{test_query}'")
    print(f"🔗 Mock filtered triples: {len(mock_filtered_triples)}")
    print("⚠️ LƯU Ý: Test này yêu cầu Neo4j đang chạy với Knowledge Graph data")
    
    try:
        # Test với different strategies
        strategies = ["bidirectional", "subject_focused", "adaptive"]
        
        for strategy in strategies:
            print(f"\n🎯 Testing với strategy: {strategy}")
            print("-" * 40)
            
            try:
                result = quick_expand_context(mock_filtered_triples, test_query, strategy)
                
                print(f"   📊 Kết quả: {result.source_triples_count} → {result.expanded_contexts_count} contexts")
                print(f"   ⏱️ Thời gian: {result.expansion_time:.2f}s")
                print(f"   📈 Expansion rate: {result.get_expansion_efficiency():.2f}")
                
                # Show top expanded contexts
                if result.expanded_contexts:
                    print(f"   🏆 Top 3 contexts:")
                    for i, context in enumerate(result.expanded_contexts[:3], 1):
                        print(f"      {i}. {context.get_summary()}")
                else:
                    print(f"   📝 Không có contexts được tìm thấy (có thể do empty KG hoặc không match)")
                        
            except Exception as e:
                print(f"   ❌ Strategy {strategy} failed: {e}")
                print(f"      💡 Có thể do Neo4j chưa chạy hoặc KG chưa có data")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        logger.exception("Chi tiết lỗi test:")
        print("💡 Gợi ý:")
        print("   - Đảm bảo Neo4j đang chạy (bolt://localhost:7687)")
        print("   - Đảm bảo có Knowledge Graph data từ Offline phase")
        print("   - Kiểm tra credentials Neo4j")

def test_individual_expansion_components():
    """Test các components riêng lẻ của expansion system"""
    print("\n🧪 TEST INDIVIDUAL EXPANSION COMPONENTS")
    print("=" * 50)
    
    # Test ExpansionStrategy enum
    print("🎯 Test ExpansionStrategy enum:")
    for strategy in ExpansionStrategy:
        print(f"   {strategy.value}")
    
    # Test ContextRelevanceLevel enum
    print("\n📊 Test ContextRelevanceLevel enum:")
    for level in ContextRelevanceLevel:
        print(f"   {level.value}")
    
    # Test ExpansionDirection enum
    print("\n📍 Test ExpansionDirection enum:")
    for direction in ExpansionDirection:
        print(f"   {direction.value}")
    
    # Test ContextExpansionConfig
    print("\n⚙️ Test ContextExpansionConfig:")
    config = create_default_expansion_config()
    print(f"   Expansion strategy: {config.expansion_strategy.value}")
    print(f"   Expansion direction: {config.expansion_direction.value}")
    print(f"   Max expanded items: {config.max_expanded_items}")
    print(f"   Relevance threshold: {config.relevance_threshold}")
    print(f"   Synonym expansion: {config.enable_synonym_expansion}")
    print(f"   Context filtering: {config.enable_context_filtering}")

def test_mock_expansion_without_neo4j():
    """Test expansion logic với mock data mà không cần Neo4j"""
    print("\n🎭 TEST MOCK EXPANSION (NO NEO4J)")
    print("=" * 40)
    
    # Mock ExpandedContext objects
    mock_contexts = [
        ExpandedContext(
            context_id="context_001",
            context_type="triple",
            source_triple_id="triple_001",
            expansion_path="táo → có → đường",
            context_text="táo có đường tự nhiên",
            relevance_score=0.7,
            relevance_level=ContextRelevanceLevel.INDIRECT,
            distance_from_source=1,
            supporting_evidence={'relation_confidence': 0.8},
            expansion_metadata={'source_chunk': 'chunk_001'}
        ),
        ExpandedContext(
            context_id="context_002",
            context_type="synonym",
            source_triple_id="triple_001",
            expansion_path="táo ↔ quả táo (synonym)",
            context_text="quả táo (synonym of táo)",
            relevance_score=0.85,
            relevance_level=ContextRelevanceLevel.DIRECT,
            distance_from_source=1,
            supporting_evidence={'similarity_score': 0.9},
            expansion_metadata={'source_chunk': 'chunk_001'}
        )
    ]
    
    print(f"📊 Mock contexts created: {len(mock_contexts)}")
    for i, context in enumerate(mock_contexts, 1):
        print(f"   {i}. {context.get_summary()}")
    
    # Test relevance distribution
    relevance_dist = {}
    for level in ContextRelevanceLevel:
        count = sum(1 for context in mock_contexts if context.relevance_level == level)
        relevance_dist[level.value] = count
    
    print(f"\n📈 Relevance distribution:")
    for level, count in relevance_dist.items():
        print(f"   {level}: {count} contexts")

if __name__ == "__main__":
    print("🚀 BẮT ĐẦU CHẠY TẤT CẢ TESTS CHO MODULE 4")
    print("=" * 60)
    
    # Test 1: Individual components
    test_individual_expansion_components()
    
    print("\n" + "=" * 60)
    
    # Test 2: Mock expansion logic
    test_mock_expansion_without_neo4j()
    
    print("\n" + "=" * 60)
    
    # Test 3: Full expansion (yêu cầu Neo4j)
    print("🔗 Test tiếp theo yêu cầu Neo4j với Knowledge Graph data")
    user_input = input("Nhấn Enter để test với Neo4j (hoặc 's' để skip): ")
    
    if user_input.lower() != 's':
        test_context_expansion_with_mock_data()
    else:
        print("⏭️ Skipped Neo4j test")
    
    print("\n🎉 HOÀN THÀNH TẤT CẢ TESTS CHO MODULE 4!")
    print("=" * 60)
