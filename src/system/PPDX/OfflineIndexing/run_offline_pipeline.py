"""
File: run_offline_pipeline_hipporag.py - UPDATED with GPT-3.5 Fallback
Description: Main script for running the GraphRAG offline pipeline - HippoRAG 2 Style

HippoRAG 2 Style Features:
- NO canonical mapping of synonyms
- ALL phrase surface forms preserved as separate nodes
- SYNONYM edges connect semantically similar phrases
- Lower similarity threshold (0.8 instead of 0.85) like original paper
- Bidirectional synonym edges for better graph traversal
- GPT-3.5 Turbo fallback for failed HuggingFace API calls

Environment Variables (Recommended):
    HF_API_KEY=your_huggingface_api_key
    OPENAI_API_KEY=your_openai_api_key (optional, for fallback)

Usage:
    # Basic usage (auto-detects API keys from .env)
    python run_offline_pipeline_hipporag.py --excel test/test_data.xlsx
    
    # With explicit keys (optional)
    python run_offline_pipeline_hipporag.py --excel test/test_data.xlsx --api-key YOUR_HF_KEY --openai-key YOUR_OPENAI_KEY
    
    # Disable GPT fallback
    python run_offline_pipeline_hipporag.py --excel test/test_data.xlsx --no-gpt-fallback

Options:
    --excel PATH           Path to Excel file (default: test_data.xlsx)
    --api-key KEY         HuggingFace API key (optional if HF_API_KEY env var set)
    --openai-key KEY      OpenAI API key (optional if OPENAI_API_KEY env var set)
    --no-gpt-fallback     Disable GPT-3.5 fallback (use HF only)
    --clear-graph         Clear existing graph before building
    --synonym-threshold N Synonym detection threshold (default: 0.8)
    --save-results        Save intermediate results
    --log-level LEVEL     Logging level (DEBUG/INFO/WARNING/ERROR)
    --neo4j-uri URI       Neo4j connection URI
    --neo4j-user USER     Neo4j username
    --neo4j-password PASS Neo4j password
"""

from pathlib import Path 
import os
import sys
from dotenv import load_dotenv
import argparse

# Add parent directory to path
parent_dir = Path(__file__).parent
sys.path.append(str(parent_dir))

from pipeline_orchestrator import OfflinePipelineOrchestrator
from utils.utils_general import setup_logging, check_environment, save_pipeline_results

# Load environment variables FIRST
load_dotenv()

def main():
    """Main function with GPT-3.5 fallback support"""
    parser = argparse.ArgumentParser(description="Run GraphRAG Offline Pipeline (HippoRAG 2 Style with GPT Fallback)")
    parser.add_argument("--excel", type=str, default="test_data.xlsx", 
                       help="Path to Excel file")
    parser.add_argument("--api-key", type=str, default=None,
                       help="HuggingFace API key (optional if HF_API_KEY env var set)")
    parser.add_argument("--openai-key", type=str, default=None,
                       help="OpenAI API key for GPT-3.5 fallback (optional if OPENAI_API_KEY env var set)")
    parser.add_argument("--no-gpt-fallback", action="store_true", default=False,
                       help="Disable GPT-3.5 fallback (use HuggingFace only)")
    parser.add_argument("--clear-graph", action="store_true", default=True,
                       help="Clear existing graph before building")
    parser.add_argument("--synonym-threshold", type=float, default=0.8,
                       help="Synonym detection threshold (HippoRAG 2 style: 0.8)")
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
    
    # Setup logging with fixed path handling
    excel_path = Path(args.excel)
    log_filename = f"offline_pipeline_hipporag_{excel_path.stem}.log"
    log_file = Path("logs") / log_filename
    log_file.parent.mkdir(exist_ok=True)
    setup_logging(args.log_level, log_file)
    
    print("="*60)
    print("GraphRAG Offline Pipeline - HippoRAG 2 Style + GPT Fallback")
    print("="*60)
    print("Features:")
    print("- No canonical synonym mapping")
    print("- All phrase surface forms preserved")
    print("- Synonym edges connect similar phrases")
    print("- Lower similarity threshold (0.8)")
    print("- Bidirectional synonym connectivity")
    print("- GPT-3.5 Turbo fallback for API failures")
    print("="*60)
    
    # Check environment
    if not check_environment():
        print("Environment check failed. Please fix issues and try again.")
        return 1
    
    # Get API keys - AUTO-DETECT from environment or use arguments
    hf_api_key = args.api_key or os.getenv("HF_API_KEY")
    openai_api_key = args.openai_key or os.getenv("OPENAI_API_KEY")
    
    # Validate HuggingFace API key (required)
    if not hf_api_key:
        print("❌ HuggingFace API key required!")
        print("Options:")
        print("1. Set HF_API_KEY environment variable in .env file")
        print("2. Use --api-key argument")
        print("3. Get your API key from: https://huggingface.co/settings/tokens")
        return 1
    
    # Determine GPT fallback configuration
    enable_gpt_fallback = not args.no_gpt_fallback and openai_api_key is not None
    
    # Display API configuration
    print(f"🔑 API Configuration:")
    print(f"   HuggingFace: {'✅ Set' if hf_api_key else '❌ Missing'}")
    print(f"   OpenAI GPT-3.5: {'✅ Set' if openai_api_key else '❌ Missing'}")
    print(f"   Fallback Mode: {'✅ Enabled' if enable_gpt_fallback else '❌ Disabled'}")
    
    if not enable_gpt_fallback:
        if args.no_gpt_fallback:
            print("   ℹ️  GPT fallback manually disabled")
        else:
            print("   ⚠️  GPT fallback disabled (no OPENAI_API_KEY)")
            print("   💡 Set OPENAI_API_KEY in .env to enable fallback")
    print()
    
    # Validate Excel file
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
        print(f"🔗 Synonym threshold: {args.synonym_threshold} (HippoRAG 2 style)")
        print(f"🗃️ Clear existing graph: {args.clear_graph}")
        print(f"🌐 Neo4j URI: {args.neo4j_uri}")
        print(f"🎯 Pipeline style: HippoRAG 2 (no canonical mapping)")
        print(f"🤖 Extraction: HuggingFace + {'GPT-3.5 fallback' if enable_gpt_fallback else 'No fallback'}")
        print()
        
        orchestrator = OfflinePipelineOrchestrator(
            huggingface_api_key=hf_api_key,
            openai_api_key=openai_api_key,
            enable_gpt_fallback=enable_gpt_fallback,
            neo4j_uri=args.neo4j_uri,
            neo4j_user=args.neo4j_user,
            neo4j_password=args.neo4j_password
        )
        
        # Run pipeline (HippoRAG 2 style with fallback)
        results = orchestrator.run_complete_pipeline(
            excel_file_path=excel_path,
            clear_existing_graph=args.clear_graph,
            synonym_threshold=args.synonym_threshold,
            save_intermediate_results=args.save_results
        )
        
        # Save results
        if args.save_results:
            results_file = excel_path.parent / f"pipeline_results_hipporag_{excel_path.stem}.json"
            save_pipeline_results(results, results_file)
            print(f"💾 Results saved to: {results_file}")
        
        print()
        print("="*60)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY (HippoRAG 2 Style)")
        print("="*60)
        print("🌐 Access Neo4j Browser: http://localhost:7474")
        print("   Username: neo4j")
        print(f"   Password: {args.neo4j_password}")
        print()
        print("📈 Extraction Statistics:")
        if 'triples' in results and 'extraction_stats' in results['triples']:
            stats = results['triples']['extraction_stats']
            print(f"   HuggingFace successful: {stats.get('hf_success', 0)}")
            print(f"   HuggingFace failed: {stats.get('hf_failed', 0)}")
            print(f"   GPT-3.5 fallback used: {stats.get('gpt_success', 0)}")
            print(f"   Total failures: {stats.get('gpt_failed', 0)}")
        print()
        print("🏗️ HippoRAG 2 Graph Structure:")
        print("   - Passage nodes: Document chunks with embeddings")
        print("   - Phrase nodes: All surface forms preserved")
        print("   - RELATION edges: Semantic relationships")
        print("   - SYNONYM edges: Similarity connections")
        print("   - CONTAINS edges: Passage -> Phrase relationships")
        print()
        print("📝 Query Examples:")
        print("   1. Find synonyms: MATCH (p1:Phrase)-[:SYNONYM]-(p2:Phrase) RETURN p1, p2")
        print("   2. Explore relations: MATCH (p1:Phrase)-[:RELATION]-(p2:Phrase) RETURN p1, p2")
        print("   3. Find passages: MATCH (passage:Passage)-[:CONTAINS]->(phrase:Phrase) RETURN passage, phrase")
        print("   4. Check extraction methods: MATCH ()-[r:RELATION]->() RETURN r.extraction_method, count(*)")
        print()
        print("🚀 Next steps:")
        print("   1. Explore graph in Neo4j Browser")
        print("   2. Run Personalized PageRank queries")
        print("   3. Test semantic search capabilities")
        print("   4. Check intermediate results in output files")
        print("   5. Verify all passages have CONTAINS edges")
        print("="*60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️ Pipeline interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)