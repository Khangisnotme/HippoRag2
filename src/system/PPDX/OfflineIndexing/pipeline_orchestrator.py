"""
pipeline_orchestrator.py
Pipeline Orchestrator - HippoRAG 2 Style with GPT-3.5 Fallback
Bỏ canonical mapping, chỉ dùng synonym edges như HippoRAG 2
Added GPT-3.5 Turbo fallback for robust triple extraction
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
    """Orchestrate toàn bộ offline pipeline - HippoRAG 2 style with GPT fallback"""
    
    def __init__(self, 
                 huggingface_api_key: str,
                 openai_api_key: Optional[str] = None,
                 enable_gpt_fallback: bool = True,
                 neo4j_uri: str = "bolt://localhost:7687",
                 neo4j_user: str = "neo4j", 
                 neo4j_password: str = "graphrag123"):
        """
        Initialize pipeline với required configurations + GPT fallback
        
        Args:
            huggingface_api_key (str): HuggingFace API key (primary)
            openai_api_key (str, optional): OpenAI API key (fallback)
            enable_gpt_fallback (bool): Enable GPT-3.5 fallback
            neo4j_uri (str): Neo4j connection URI
            neo4j_user (str): Neo4j username
            neo4j_password (str): Neo4j password
        """
        self.huggingface_api_key = huggingface_api_key
        self.openai_api_key = openai_api_key
        self.enable_gpt_fallback = enable_gpt_fallback
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        
        # Initialize processors
        self.excel_processor = ExcelDocumentProcessor()
        self.chunk_processor = ChunkProcessor()
        
        # Initialize triple extractor with fallback support
        self.triple_extractor = TripleExtractor(
            huggingface_api_key=huggingface_api_key,
            openai_api_key=openai_api_key,
            enable_gpt_fallback=enable_gpt_fallback
        )
        
        self.synonym_detector = SynonymDetector()
        self.graph_builder = None  # Initialize later
        
        # Statistics
        self.pipeline_stats = {}
        
        # Log configuration
        logger.info(f"Initialized pipeline with GPT fallback: {enable_gpt_fallback}")
        if enable_gpt_fallback and openai_api_key:
            logger.info("GPT-3.5 Turbo fallback enabled")
        elif enable_gpt_fallback and not openai_api_key:
            logger.warning("GPT fallback requested but no OpenAI API key provided")
        
    def run_complete_pipeline(self, 
                            excel_file_path: Path,
                            clear_existing_graph: bool = True,
                            synonym_threshold: float = 0.8,  # Lower threshold like HippoRAG 2
                            save_intermediate_results: bool = True) -> Dict[str, Any]:
        """Run complete offline pipeline - HippoRAG 2 style with robust extraction"""
        start_time = time.time()
        logger.info("Starting complete offline pipeline (HippoRAG 2 style with GPT fallback)...")
        
        try:
            # Step 0: Load documents from Excel
            logger.info("Step 0: Loading documents from Excel...")
            documents = self.excel_processor.load_and_process_excel(excel_file_path)
            excel_stats = self.excel_processor.get_statistics()
            
            # Step 1: Process chunks
            logger.info("Step 1: Processing chunks...")
            chunks = self.chunk_processor.process_documents(documents)
            chunk_stats = self.chunk_processor.get_statistics()
            
            # Step 2: Extract triples (with fallback)
            logger.info("Step 2: Extracting triples (with GPT fallback support)...")
            triples = self.triple_extractor.extract_triples_from_chunks(chunks)
            triple_stats = self.triple_extractor.get_statistics()
            
            # Log extraction success
            if 'extraction_stats' in triple_stats:
                stats = triple_stats['extraction_stats']
                logger.info(f"Triple extraction summary:")
                logger.info(f"  HF successful: {stats['hf_success']}/{stats['total_chunks']}")
                logger.info(f"  GPT fallback used: {stats['gpt_success']}/{stats['hf_failed']}")
                logger.info(f"  Total failures: {stats['gpt_failed']}")
            
            # Step 3: Detect synonyms (NO canonical mapping)
            logger.info("Step 3: Detecting synonyms (no canonical mapping)...")
            synonym_pairs = self.synonym_detector.detect_synonyms_from_triples(
                triples, synonym_threshold
            )
            # NOTE: NO synonym_mapping creation here!
            synonym_stats = self.synonym_detector.get_statistics()
            
            # Step 4: Build Knowledge Graph (HippoRAG 2 style)
            logger.info("Step 4: Building Knowledge Graph (HippoRAG 2 style)...")
            self.graph_builder = GraphBuilder(
                self.neo4j_uri, self.neo4j_user, self.neo4j_password
            )
            
            if clear_existing_graph:
                self.graph_builder.clear_database()
            
            # Build graph WITHOUT canonical mapping
            self.graph_builder.build_graph_hipporag_style(chunks, triples, synonym_pairs)
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
                'pipeline_style': 'HippoRAG_2_with_GPT_Fallback',
                'canonical_mapping': False,
                'gpt_fallback_enabled': self.enable_gpt_fallback,
                'excel_processing': excel_stats,
                'chunking': chunk_stats,
                'triples': triple_stats,
                'synonyms': synonym_stats,
                'graph': graph_stats,
                'settings': {
                    'synonym_threshold': synonym_threshold,
                    'clear_existing_graph': clear_existing_graph,
                    'enable_gpt_fallback': self.enable_gpt_fallback
                }
            }
            
            logger.info(f"Pipeline completed successfully in {pipeline_duration:.2f} seconds")
            self._print_final_summary()
            
            return self.pipeline_stats
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
        
        finally:
            if self.graph_builder:
                self.graph_builder.close()
    
    def _save_intermediate_results(self, output_dir: Path, triples, synonym_pairs):
        """Save intermediate results for inspection"""
        output_dir = Path(output_dir)
        
        # Save triples with extraction method info
        triples_file = output_dir / "extracted_triples_with_methods.tsv"
        self.triple_extractor.save_triples_to_file(triples_file)
        logger.info(f"Saved triples with extraction methods to {triples_file}")
        
        # Save synonyms
        synonyms_file = output_dir / "detected_synonyms.tsv"
        self.synonym_detector.save_synonyms_to_file(synonyms_file)
        logger.info(f"Saved synonyms to {synonyms_file}")
    
    def _print_final_summary(self):
        """Print final pipeline summary with GPT fallback stats"""
        stats = self.pipeline_stats
        
        print("\n" + "="*60)
        print("OFFLINE PIPELINE SUMMARY (HippoRAG 2 Style + GPT Fallback)")
        print("="*60)
        print(f"Execution Time: {stats['execution_time']:.2f} seconds")
        print(f"Input File: {stats['input_file']}")
        print(f"Pipeline Style: {stats['pipeline_style']}")
        print(f"Canonical Mapping: {stats['canonical_mapping']}")
        print(f"GPT Fallback: {stats['gpt_fallback_enabled']}")
        print()
        
        print("EXCEL PROCESSING:")
        print(f"   Documents Loaded: {stats['excel_processing']['total_documents']}")
        print(f"   Avg Length: {stats['excel_processing']['avg_text_length']:.1f} chars")
        print()
        
        print("CHUNKING:")
        print(f"   Total Chunks: {stats['chunking']['total_chunks']}")
        print(f"   Avg Chunk Length: {stats['chunking']['avg_chunk_length']:.1f} chars")
        print(f"   Method: {stats['chunking']['chunking_method']}")
        print()
        
        print("TRIPLES (ROBUST EXTRACTION):")
        print(f"   Total: {stats['triples']['total_triples']}")
        print(f"   Unique Subjects: {stats['triples']['unique_subjects']}")
        print(f"   Unique Predicates: {stats['triples']['unique_predicates']}")
        print(f"   Unique Objects: {stats['triples']['unique_objects']}")
        
        # Extraction method breakdown
        if 'qwen_triples' in stats['triples']:
            print(f"   Qwen Extracted: {stats['triples']['qwen_triples']}")
        if 'gpt35_triples' in stats['triples']:
            print(f"   GPT-3.5 Extracted: {stats['triples']['gpt35_triples']}")
        
        # Success rates
        if 'extraction_stats' in stats['triples']:
            extraction = stats['triples']['extraction_stats']
            total_chunks = extraction.get('total_chunks', 1)
            hf_success = extraction.get('hf_success', 0)
            gpt_success = extraction.get('gpt_success', 0)
            hf_failed = extraction.get('hf_failed', 0)
            gpt_failed = extraction.get('gpt_failed', 0)
            
            print(f"   HF Success Rate: {hf_success/total_chunks:.1%} ({hf_success}/{total_chunks})")
            if hf_failed > 0:
                print(f"   GPT Fallback Success: {gpt_success}/{hf_failed} failures rescued")
            print(f"   Total Failures: {gpt_failed}")
            
            # Success indicator
            if gpt_failed == 0:
                print("   ✅ All chunks successfully processed!")
            elif gpt_failed < total_chunks * 0.1:
                print("   ✅ High success rate achieved with fallback")
            else:
                print("   ⚠️  Some chunks still failed - check API limits")
        print()
        
        print("SYNONYMS (HippoRAG 2 Style):")
        print(f"   Synonym Pairs: {stats['synonyms']['total_synonym_pairs']}")
        if stats['synonyms']['total_synonym_pairs'] > 0:
            print(f"   Avg Similarity: {stats['synonyms']['avg_similarity']:.3f}")
        print(f"   Threshold Used: {stats['settings']['synonym_threshold']}")
        print("   NOTE: No canonical mapping - all phrase variants preserved")
        print()
        
        print("KNOWLEDGE GRAPH:")
        print(f"   Total Nodes: {stats['graph']['total_nodes']}")
        print(f"   Total Edges: {stats['graph']['total_edges']}")
        
        # Print node types
        for node_type, count in stats['graph']['nodes'].items():
            print(f"   {node_type} Nodes: {count}")
        
        # Print edge types
        for edge_type, count in stats['graph']['edges'].items():
            print(f"   {edge_type} Edges: {count}")
        print()
        
        print("HIPPORAG 2 + GPT FALLBACK FEATURES:")
        print("   - All phrase surface forms preserved")
        print("   - Synonym edges connect similar phrases")
        print("   - No information loss from canonical mapping")
        print("   - Robust extraction with GPT-3.5 fallback")
        print("   - Higher completion rate despite API failures")
        print("   - Ready for Personalized PageRank traversal")
        print("="*60)
        print("Pipeline completed successfully!")
        print("Access Neo4j Browser: http://localhost:7474")
        print("="*60)

# Test function
def test_pipeline_orchestrator():
    """Test complete pipeline with GPT fallback"""
    print("Testing Complete Pipeline (HippoRAG 2 Style + GPT Fallback)...")
    
    # Note: Requires actual API keys
    hf_api_key = "your_huggingface_api_key_here"
    openai_api_key = "your_openai_api_key_here"
    
    if hf_api_key == "your_huggingface_api_key_here":
        print("Please set your actual API keys to test")
        return
    
    try:
        orchestrator = OfflinePipelineOrchestrator(
            huggingface_api_key=hf_api_key,
            openai_api_key=openai_api_key,
            enable_gpt_fallback=True
        )
        
        # Test file path
        test_file = Path("test_data.xlsx")
        
        if test_file.exists():
            stats = orchestrator.run_complete_pipeline(test_file)
            print("Pipeline test completed!")
        else:
            print("Test file not found. Run test_data.py first.")
            
    except Exception as e:
        print(f"Pipeline test failed: {e}")

if __name__ == "__main__":
    test_pipeline_orchestrator()