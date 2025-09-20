"""
OfflineIndexing/module3_sysnonym_detector.py
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
    """
    Data class để lưu trữ thông tin của một cặp từ đồng nghĩa
    
    Attributes:
        phrase1 (str): Cụm từ thứ nhất
        phrase2 (str): Cụm từ thứ hai
        similarity_score (float): Điểm tương tự giữa hai cụm từ (0-1)
    """
    phrase1: str
    phrase2: str
    similarity_score: float

class SynonymDetector:
    """
    Class chính để detect synonyms sử dụng embedding similarity
    
    Workflow:
    1. Initialize model sentence-transformers
    2. Extract unique phrases từ triples
    3. Generate embeddings cho tất cả phrases
    4. Compute similarity matrix
    5. Find synonym pairs dựa trên threshold
    6. Create synonym mapping cho canonical forms
    """
    
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"):
        """
        Initialize SynonymDetector với multilingual sentence transformer
        
        Args:
            model_name (str): Tên model sentence-transformers để sử dụng
                            Default: paraphrase-multilingual-mpnet-base-v2 
                            (hỗ trợ đa ngôn ngữ, tốt cho tiếng Việt)
        
        Initializes:
            - self.model: SentenceTransformer model
            - self.synonym_pairs: List lưu các cặp synonyms đã tìm được
            - self.phrase_embeddings: Dict cache embeddings đã tính
        """
        logger.info(f"Initializing SynonymDetector with model: {model_name}")
        self.model_name = model_name
        # Load pre-trained sentence transformer model
        self.model = SentenceTransformer(model_name)
        # List để lưu các synonym pairs đã detect được
        self.synonym_pairs = []
        # Dict để cache embeddings đã tính (tránh tính lại)
        self.phrase_embeddings = {}
        logger.info("Model loaded successfully")
        
    def detect_synonyms_from_triples(self, triples: List[Any], similarity_threshold: float = 0.85) -> List[SynonymPair]:
        """
        Main function để detect synonyms từ extracted triples
        
        Args:
            triples (List[Any]): List các triple objects có attributes .subject và .object
            similarity_threshold (float): Ngưỡng similarity để coi là synonym (0-1)
                                        Default: 0.85 (khá strict)
        
        Returns:
            List[SynonymPair]: List các cặp synonyms đã tìm được
            
        Process:
            1. Extract all unique phrases từ subjects và objects
            2. Filter phrases (loại bỏ phrases quá ngắn)
            3. Call detect_synonyms() để tìm synonym pairs
        """
        logger.info(f"Starting synonym detection from {len(triples)} triples")
        
        # STEP 1: Extract all unique phrases từ triples
        all_phrases = set()
        
        for triple in triples:
            # Lấy subject và object, strip whitespace và lowercase để normalize
            all_phrases.add(triple.subject.strip().lower())
            all_phrases.add(triple.object.strip().lower())
        
        all_phrases = list(all_phrases)
        logger.debug(f"Found {len(all_phrases)} unique phrases")
        
        # STEP 2: Filter phrases - loại bỏ phrases quá ngắn (< 3 chars)
        # Vì phrases ngắn thường không có ý nghĩa rõ ràng
        filtered_phrases = [phrase for phrase in all_phrases if len(phrase) > 2]
        logger.debug(f"Filtered to {len(filtered_phrases)} valid phrases (length > 2)")
        
        logger.info(f"Detecting synonyms among {len(filtered_phrases)} unique phrases")
        
        # STEP 3: Gọi detect_synonyms để tìm synonym pairs
        synonym_pairs = self.detect_synonyms(filtered_phrases, similarity_threshold)
        
        # Lưu kết quả vào instance variable
        self.synonym_pairs = synonym_pairs
        logger.info(f"Found {len(synonym_pairs)} synonym pairs")
        return synonym_pairs
    
    def detect_synonyms(self, phrases: List[str], similarity_threshold: float = 0.85) -> List[SynonymPair]:
        """
        Core function để detect synonyms trong list of phrases
        
        Args:
            phrases (List[str]): List các phrases cần tìm synonyms
            similarity_threshold (float): Ngưỡng similarity (0-1)
        
        Returns:
            List[SynonymPair]: List các synonym pairs
            
        Algorithm:
            1. Generate embeddings cho tất cả phrases
            2. Compute similarity matrix (cosine similarity)
            3. Find pairs có similarity >= threshold
            4. Avoid duplicate pairs
        """
        # Kiểm tra input đủ để so sánh
        if len(phrases) < 2:
            logger.warning("Not enough phrases for synonym detection")
            return []
        
        # STEP 1: Generate embeddings cho tất cả phrases
        logger.info("Generating embeddings for phrases...")
        # model.encode() convert text thành vector embeddings
        # show_progress_bar=True để hiển thị progress
        embeddings = self.model.encode(phrases, show_progress_bar=True)
        logger.debug(f"Generated {len(embeddings)} embeddings")
        
        # STEP 2: Store embeddings vào cache để reuse
        for phrase, embedding in zip(phrases, embeddings):
            self.phrase_embeddings[phrase] = embedding
        logger.debug(f"Stored embeddings for {len(self.phrase_embeddings)} phrases")
        
        # STEP 3: Compute similarity matrix
        logger.info("Computing similarity matrix...")
        # Cosine similarity giữa tất cả cặp embeddings
        # Kết quả: matrix NxN với similarity[i][j] = similarity giữa phrase i và j
        similarity_matrix = cosine_similarity(embeddings)
        logger.debug(f"Similarity matrix shape: {similarity_matrix.shape}")
        
        # STEP 4: Find synonym pairs
        synonym_pairs = []
        processed_pairs = set()  # Để tránh duplicate pairs
        
        logger.info("Finding synonym pairs...")
        # Nested loop để kiểm tra tất cả cặp phrases
        for i in range(len(phrases)):
            for j in range(i + 1, len(phrases)):  # j > i để tránh duplicate và self-comparison
                similarity = similarity_matrix[i][j]
                
                # Nếu similarity >= threshold thì coi là synonym
                if similarity >= similarity_threshold:
                    phrase1, phrase2 = phrases[i], phrases[j]
                    
                    # STEP 5: Avoid duplicate pairs
                    # Tạo pair_key sorted để tránh (A,B) và (B,A) đều được thêm
                    pair_key = tuple(sorted([phrase1, phrase2]))
                    if pair_key not in processed_pairs:
                        # Tạo SynonymPair object
                        synonym_pair = SynonymPair(
                            phrase1=phrase1,
                            phrase2=phrase2,
                            similarity_score=float(similarity)
                        )
                        synonym_pairs.append(synonym_pair)
                        processed_pairs.add(pair_key)
                        logger.debug(f"Found synonym pair: {phrase1} ≈ {phrase2} (score: {similarity:.3f})")
        
        logger.info(f"Found {len(synonym_pairs)} synonym pairs with threshold {similarity_threshold}")
        return synonym_pairs
    
    def create_synonym_mapping(self, synonym_pairs: List[SynonymPair] = None) -> Dict[str, str]:
        """
        Create mapping từ synonyms về canonical form (dạng chuẩn)
        
        Args:
            synonym_pairs (List[SynonymPair]): List synonym pairs, nếu None thì dùng self.synonym_pairs
        
        Returns:
            Dict[str, str]: Mapping từ phrase -> canonical_phrase
            
        Algorithm:
            1. Build graph of synonyms (undirected graph)
            2. Find connected components (synonym groups)
            3. Choose canonical form cho mỗi group (shortest phrase)
            4. Create mapping dict
            
        Example:
            Input: [("diego costa", "costa"), ("costa", "diego da silva costa")]
            Output: {"diego costa": "costa", "diego da silva costa": "costa", "costa": "costa"}
        """
        logger.info("Creating synonym mapping...")
        if synonym_pairs is None:
            synonym_pairs = self.synonym_pairs
            
        # STEP 1: Build graph of synonyms
        # Graph represented as adjacency list: {phrase: set_of_connected_phrases}
        synonym_graph = {}
        
        for pair in synonym_pairs:
            # Initialize empty sets if phrases not in graph
            if pair.phrase1 not in synonym_graph:
                synonym_graph[pair.phrase1] = set()
            if pair.phrase2 not in synonym_graph:
                synonym_graph[pair.phrase2] = set()
            
            # Add bidirectional edges (undirected graph)
            synonym_graph[pair.phrase1].add(pair.phrase2)
            synonym_graph[pair.phrase2].add(pair.phrase1)
        
        logger.debug(f"Built synonym graph with {len(synonym_graph)} nodes")
        
        # STEP 2: Find connected components (synonym groups) using DFS
        visited = set()
        synonym_groups = []
        
        def dfs(node, current_group):
            """
            Depth-First Search để tìm connected component
            
            Args:
                node (str): Current node trong DFS
                current_group (set): Set lưu tất cả nodes trong component hiện tại
            """
            if node in visited:
                return
            visited.add(node)
            current_group.add(node)
            
            # Recursive DFS cho tất cả neighbors
            for neighbor in synonym_graph.get(node, set()):
                dfs(neighbor, current_group)
        
        # Tìm tất cả connected components
        for phrase in synonym_graph:
            if phrase not in visited:
                group = set()
                dfs(phrase, group)
                # Chỉ thêm groups có > 1 phrase (tức có synonyms)
                if len(group) > 1:
                    synonym_groups.append(group)
                    logger.debug(f"Found synonym group: {group}")
        
        # STEP 3: Create mapping to canonical forms
        synonym_mapping = {}
        
        for group in synonym_groups:
            # Choose shortest phrase as canonical (assumption: shorter = more common)
            canonical = min(group, key=len)
            
            # Map tất cả phrases trong group về canonical
            for phrase in group:
                synonym_mapping[phrase] = canonical
                logger.debug(f"Mapped {phrase} → {canonical}")
        
        logger.info(f"Created {len(synonym_groups)} synonym groups with {len(synonym_mapping)} mappings")
        return synonym_mapping
    
    def get_phrase_embedding(self, phrase: str) -> np.ndarray:
        """
        Get embedding cho một phrase, sử dụng cache nếu có
        
        Args:
            phrase (str): Phrase cần tính embedding
            
        Returns:
            np.ndarray: Vector embedding của phrase
            
        Note:
            - Sử dụng cache để tránh tính lại embeddings đã có
            - Embedding được normalize bởi sentence-transformers
        """
        # Kiểm tra cache trước
        if phrase in self.phrase_embeddings:
            logger.debug(f"Retrieved cached embedding for phrase: {phrase}")
            return self.phrase_embeddings[phrase]
        else:
            # Tính embedding mới
            logger.debug(f"Computing new embedding for phrase: {phrase}")
            # model.encode() trả về array, lấy element đầu tiên
            embedding = self.model.encode([phrase])[0]
            # Lưu vào cache
            self.phrase_embeddings[phrase] = embedding
            return embedding
    
    def find_similar_phrases(self, target_phrase: str, candidate_phrases: List[str], 
                           top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find top-k phrases most similar to target phrase
        
        Args:
            target_phrase (str): Phrase để tìm similar
            candidate_phrases (List[str]): List phrases để so sánh
            top_k (int): Số lượng top results trả về
            
        Returns:
            List[Tuple[str, float]]: List (phrase, similarity_score) sorted by similarity desc
            
        🚨 BUG ALERT: Dòng similarity calculation có bug!
        """
        logger.info(f"Finding top-{top_k} similar phrases to: {target_phrase}")
        target_embedding = self.get_phrase_embedding(target_phrase)
        
        similarities = []
        for phrase in candidate_phrases:
            if phrase != target_phrase:  # Skip self-comparison
                phrase_embedding = self.get_phrase_embedding(phrase)
                # 🚨 BUG: [2][0] should be [0][0] 
                # cosine_similarity returns 1x1 matrix, not 3x1
                similarity = float(cosine_similarity([target_embedding], [phrase_embedding])[0][0])
                similarities.append((phrase, similarity))
                logger.debug(f"Similarity with {phrase}: {similarity:.3f}")
        
        # Sort by similarity descending (highest similarity first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(f"Found {len(similarities)} similar phrases")
        return similarities[:top_k]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics về synonym detection results
        
        Returns:
            Dict[str, Any]: Statistics dictionary with keys:
                - total_synonym_pairs: Tổng số synonym pairs
                - avg_similarity: Similarity trung bình
                - min_similarity: Similarity thấp nhất
                - max_similarity: Similarity cao nhất  
                - unique_phrases_with_synonyms: Số phrases unique có synonyms
        """
        if not self.synonym_pairs:
            logger.warning("No synonym pairs detected yet")
            return {}
        
        # Extract similarity scores từ tất cả pairs
        similarities = [pair.similarity_score for pair in self.synonym_pairs]
        
        # Calculate statistics
        stats = {
            'total_synonym_pairs': len(self.synonym_pairs),
            'avg_similarity': np.mean(similarities),
            'min_similarity': np.min(similarities),
            'max_similarity': np.max(similarities),
            # Count unique phrases có synonyms (phrase1 + phrase2 từ tất cả pairs)
            'unique_phrases_with_synonyms': len(set([pair.phrase1 for pair in self.synonym_pairs] + 
                                                  [pair.phrase2 for pair in self.synonym_pairs]))
        }
        
        logger.info(f"Synonym detection statistics: {stats}")
        return stats
    
    def save_synonyms_to_file(self, output_path: Path):
        """
        Save synonym pairs to TSV file để review và debug
        
        Args:
            output_path (Path): Path để save file
            
        Output format:
            TSV file với columns: Phrase1, Phrase2, Similarity_Score
        """
        logger.info(f"Saving {len(self.synonym_pairs)} synonym pairs to {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write("Phrase1\tPhrase2\tSimilarity_Score\n")
            # Write data rows
            for pair in self.synonym_pairs:
                f.write(f"{pair.phrase1}\t{pair.phrase2}\t{pair.similarity_score:.4f}\n")
        logger.info("Synonym pairs saved successfully")

# Test function
def test_synonym_detector():
    """
    Test function cho Module 3 - Demo basic functionality
    
    Test case: Chemical/Vietnamese phrases có synonyms rõ ràng
    Expected synonyms:
        - "axít" ≈ "axit" (Vietnamese spelling variants)
        - "kiềm" ≈ "bazơ" (chemical synonyms)  
        - "dung dịch axít" ≈ "dung dịch axit"
        - "pH nhỏ hơn 7" ≈ "pH < 7" (mathematical notation)
    """
    logger.info("Starting synonym detector test")
    detector = SynonymDetector()
    
    # Test phrases with obvious synonyms
    test_phrases = [
        "axít",           # Vietnamese spelling 1
        "axit",           # Vietnamese spelling 2  
        "kiềm",           # Vietnamese
        "bazơ",           # Vietnamese alternative
        "dung dịch axít", # Compound phrase 1
        "dung dịch axit", # Compound phrase 2
        "pH nhỏ hơn 7",   # Text form
        "pH < 7"          # Symbol form
    ]
    
    print("🔗 Testing Synonym Detection...")
    synonym_pairs = detector.detect_synonyms(test_phrases, similarity_threshold=0.8)
    
    print("📊 Synonym Detection Results:")
    for pair in synonym_pairs:
        print(f"  {pair.phrase1} ≈ {pair.phrase2} (score: {pair.similarity_score:.3f})")
    
    # Test mapping creation
    mapping = detector.create_synonym_mapping(synonym_pairs)
    print("\n📋 Synonym Mapping:")
    for original, canonical in mapping.items():
        print(f"  {original} → {canonical}")
    
    logger.info("Synonym detector test completed")
    return synonym_pairs

if __name__ == "__main__":
    test_synonym_detector()
