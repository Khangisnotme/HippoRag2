"""
Enhanced RAG Pipeline cho VIMQA_dev collection
Hỗ trợ đầy đủ Vector retrieval
"""

import pandas as pd
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import time

# Qdrant imports
from qdrant_client import QdrantClient
from langchain_core.documents import Document

# Setup paths
current_file = Path(__file__)
sys.path.append(str(current_file.parent))

# Create outputs directory if it doesn't exist
outputs_dir = current_file.parent / "outputs"
outputs_dir.mkdir(exist_ok=True)

# Import RAG Pipeline
from pipelineRAG import RAGPipeline

class DocumentLoader:
    """
    Class để load documents từ Qdrant collection
    """
    
    def __init__(self, qdrant_url: str, qdrant_api_key: str):
        """
        Initialize Document Loader
        
        Args:
            qdrant_url: URL của Qdrant server
            qdrant_api_key: API key
        """
        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=30
        )
        print(f"✅ Connected to Qdrant: {qdrant_url}")
    
    def load_documents_from_collection(self, collection_name: str, limit: int = None) -> List[Document]:
        """
        Load documents từ Qdrant collection
        
        Args:
            collection_name: Tên collection
            limit: Giới hạn số documents (None = load tất cả)
            
        Returns:
            List of Document objects
        """
        print(f"📚 Loading documents from collection: {collection_name}")
        
        try:
            # Get collection info
            collection_info = self.qdrant_client.get_collection(collection_name)
            total_vectors = collection_info.vectors_count
            print(f"   Collection has {total_vectors} vectors")
            
            # Determine how many to load
            load_limit = min(limit, total_vectors) if limit else total_vectors
            print(f"   Loading {load_limit} documents...")
            
            documents = []
            batch_size = 100
            offset = 0
            
            while len(documents) < load_limit:
                # Calculate current batch size
                current_batch = min(batch_size, load_limit - len(documents))
                
                print(f"   Loading batch {offset//batch_size + 1}: {len(documents) + 1}-{len(documents) + current_batch}")
                
                # Scroll through collection
                points, next_offset = self.qdrant_client.scroll(
                    collection_name=collection_name,
                    limit=current_batch,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False
                )
                
                if not points:
                    break
                
                # Convert to Document objects
                for point in points:
                    payload = point.payload
                    content = payload.get('page_content', '')
                    
                    if content.strip():  # Only add non-empty documents
                        doc = Document(
                            page_content=content,
                            metadata=payload.get('metadata', {})
                        )
                        documents.append(doc)
                
                offset += current_batch
                
                # Break if no next offset or we have enough documents
                if next_offset is None or len(documents) >= load_limit:
                    break
            
            print(f"✅ Loaded {len(documents)} documents successfully")
            return documents
            
        except Exception as e:
            print(f"❌ Error loading documents: {e}")
            raise

class EnhancedVIMQARunner:
    """
    Enhanced VIMQA Runner với full support cho Vector retrieval
    """
    
    def __init__(
        self,
        collection_name: str = "VIMQA_dev",
        retriever_type: str = "vector",
        k: int = 5,
        qdrant_url: str = None,
        qdrant_api_key: str = None
    ):
        """
        Khởi tạo Enhanced VIMQA Runner
        
        Args:
            collection_name: Tên collection trong Qdrant
            retriever_type: Loại retriever (vector)
            k: Số documents retrieve
            qdrant_url: URL Qdrant server
            qdrant_api_key: API key Qdrant
        """
        self.collection_name = collection_name
        self.retriever_type = retriever_type
        self.k = k
        
        # Get Qdrant credentials
        self.qdrant_url = qdrant_url or os.getenv("QDRANT_URL")
        self.qdrant_api_key = qdrant_api_key or os.getenv("QDRANT_API_KEY")
        
        if not self.qdrant_url or not self.qdrant_api_key:
            raise ValueError("Qdrant URL and API key are required")
        
        print(f"🚀 Initializing Enhanced VIMQA Pipeline...")
        print(f"   Collection: {collection_name}")
        print(f"   Retriever: {retriever_type}")
        print(f"   K documents: {k}")
        
        # Initialize RAG Pipeline
        self._initialize_rag_pipeline()
        
        print(f"✅ Enhanced Pipeline initialized successfully!")
    
    def _initialize_rag_pipeline(self):
        """
        Initialize RAG Pipeline với appropriate configuration
        """
        try:
            self.rag_pipeline = RAGPipeline(
                retriever_type=self.retriever_type,
                vector_store_type="qdrant",
                collection_name=self.collection_name,
                k=self.k,
                qdrant_url=self.qdrant_url,
                qdrant_api_key=self.qdrant_api_key
            )
            
        except Exception as e:
            print(f"❌ Error initializing RAG pipeline: {e}")
            raise
    
    def test_retrieval_methods(self, test_query: str = "Quy định về tốc độ tối đa trên đường cao tốc"):
        """
        Test retrieval methods
        
        Args:
            test_query: Query để test
        """
        print(f"\n🧪 Testing retrieval methods with query: '{test_query}'")
        print("="*60)
        
        # Test Vector Search
        print(f"\n1. VECTOR SEARCH:")
        try:
            vector_result = self.rag_pipeline.retriever.retrieve_documents(test_query)
            print(f"   Found: {len(vector_result)} documents")
            if vector_result:
                for i, doc in enumerate(vector_result[:2], 1):
                    print(f"   Doc {i}: {doc.page_content[:80]}...")
        except Exception as e:
            print(f"   ❌ Vector search failed: {e}")
    
    def load_questions_from_excel(
        self, 
        file_path: str, 
        question_column: str = "question", 
        nrows: Optional[int] = None,
        start_row: Optional[int] = None,
        end_row: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Load questions từ file Excel
        
        Args:
            file_path: Đường dẫn file Excel
            question_column: Tên cột chứa câu hỏi
            nrows: Số dòng tối đa để đọc (None = đọc tất cả)
            start_row: Dòng bắt đầu (0-based, None = từ đầu)
            end_row: Dòng kết thúc (0-based, None = đến cuối)
        """
        try:
            print(f"📖 Loading questions from: {file_path}")
            
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path, nrows=nrows)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path, nrows=nrows)
            else:
                raise ValueError("Unsupported file format. Use .xlsx, .xls, or .csv")
            
            # Apply row range if specified
            if start_row is not None or end_row is not None:
                start_idx = start_row if start_row is not None else 0
                end_idx = end_row if end_row is not None else len(df)
                df = df.iloc[start_idx:end_idx]
                print(f"📊 Processing rows {start_idx+1} to {end_idx} (total: {len(df)} rows)")
            
            print(f"✅ Loaded {len(df)} rows")
            print(f"📋 Columns: {list(df.columns)}")
            
            if question_column not in df.columns:
                possible_cols = [col for col in df.columns if 'question' in col.lower() or 'câu hỏi' in col.lower()]
                if possible_cols:
                    question_column = possible_cols[0]
                    print(f"✅ Auto-detected question column: '{question_column}'")
                else:
                    raise ValueError(f"Cannot find question column. Available: {list(df.columns)}")
            
            original_len = len(df)
            df = df[df[question_column].notna() & (df[question_column] != "")]
            print(f"📝 Valid questions: {len(df)}/{original_len}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            raise
    
    def process_questions(
        self, 
        df: pd.DataFrame, 
        question_column: str = "question",
        batch_size: int = 10,
        save_intermediate: bool = True
    ) -> pd.DataFrame:
        """
        Xử lý questions qua RAG pipeline
        """
        results = []
        total_questions = len(df)
        
        print(f"\n🤖 Processing {total_questions} questions with {self.retriever_type} retrieval...")
        print(f"📦 Batch size: {batch_size}")
        
        for i in range(0, total_questions, batch_size):
            batch_end = min(i + batch_size, total_questions)
            batch_df = df.iloc[i:batch_end].copy()
            
            print(f"\n📦 Batch {i//batch_size + 1}/{(total_questions-1)//batch_size + 1}")
            print(f"   Questions {i+1}-{batch_end}/{total_questions}")
            
            batch_results = []
            
            for idx, row in batch_df.iterrows():
                question = row[question_column]
                
                try:
                    print(f"   🔍 Q{idx+1}: {question[:50]}...")
                    start_time = time.time()
                    
                    # Step 1: Retrieve documents first
                    print(f"   📚 Retrieving documents...")
                    retrieval_result = self.rag_pipeline.retriever.retrieve_documents(question)
                    
                    # Extract metadata from retrieved documents
                    sources = []
                    doc_ids = []
                    titles = []
                    excel_rows = []
                    
                    print(f"   📄 Processing documents metadata...")
                    if retrieval_result:
                        print(f"   Found {len(retrieval_result)} documents to process")
                        for doc in retrieval_result:
                            if isinstance(doc, dict):
                                metadata = doc.get('metadata', {})
                            elif hasattr(doc, 'metadata'):
                                metadata = doc.metadata
                            else:
                                metadata = {}
                            
                            source = metadata.get('source', '')
                            doc_id = metadata.get('doc_id', '')
                            title = metadata.get('title', '')
                            excel_row = str(metadata.get('excel_row', ''))
                            
                            print(f"   Document metadata:")
                            print(f"     - Source: {source}")
                            print(f"     - Doc ID: {doc_id}")
                            print(f"     - Title: {title}")
                            print(f"     - Excel Row: {excel_row}")
                            
                            sources.append(source)
                            doc_ids.append(doc_id)
                            titles.append(title)
                            excel_rows.append(excel_row)
                    else:
                        print(f"   ⚠️ No documents found in retrieval result")
                    
                    processing_time = time.time() - start_time
                    
                    # Prepare result row
                    result_row = row.copy()
                    result_row['retrieval_method'] = self.retriever_type
                    result_row['processing_time'] = round(processing_time, 2)
                    
                    # Use metadata from retrieval step
                    result_row['sources'] = str(sources)
                    result_row['doc_id'] = str(doc_ids)
                    result_row['title'] = str(titles)
                    result_row['excel_row'] = str(excel_rows)
                    result_row['num_documents_used'] = len(sources)
                    
                    print(f"   💾 Saving result row with metadata:")
                    print(f"     - Sources: {result_row['sources']}")
                    print(f"     - Doc IDs: {result_row['doc_id']}")
                    print(f"     - Titles: {result_row['title']}")
                    print(f"     - Excel Rows: {result_row['excel_row']}")
                    
                    batch_results.append(result_row)
                    print(f"   ✅ Completed in {processing_time:.2f}s")
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    print(f"   📝 Creating error result row...")
                    
                    result_row = row.copy()
                    result_row['retrieval_method'] = self.retriever_type
                    result_row['processing_time'] = 0
                    result_row['sources'] = str(sources) if 'sources' in locals() else '[]'
                    result_row['doc_id'] = str(doc_ids) if 'doc_ids' in locals() else '[]'
                    result_row['title'] = str(titles) if 'titles' in locals() else '[]'
                    result_row['excel_row'] = str(excel_rows) if 'excel_rows' in locals() else '[]'
                    result_row['num_documents_used'] = len(sources) if 'sources' in locals() else 0
                    result_row['has_error'] = True
                    result_row['error_message'] = str(e)
                    
                    print(f"   💾 Saving error result row with metadata:")
                    print(f"     - Sources: {result_row['sources']}")
                    print(f"     - Doc IDs: {result_row['doc_id']}")
                    print(f"     - Titles: {result_row['title']}")
                    print(f"     - Excel Rows: {result_row['excel_row']}")
                    
                    batch_results.append(result_row)
            
            results.extend(batch_results)
            
            # Save intermediate results
            if save_intermediate and len(results) > 0:
                temp_df = pd.DataFrame(results)
                temp_file = outputs_dir / f"temp_{self.retriever_type}_batch_{i//batch_size + 1}.xlsx"
                temp_df.to_excel(temp_file, index=False)
                print(f"💾 Saved intermediate results to: {temp_file}")
                print(f"📊 Intermediate results shape: {temp_df.shape}")
                print(f"📋 Columns in intermediate results: {list(temp_df.columns)}")
        
        return pd.DataFrame(results)
    
    def save_results(
        self, 
        results_df: pd.DataFrame, 
        output_file: str = None,
        include_metadata: bool = True
    ) -> str:
        """
        Lưu kết quả ra file Excel
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"vimqa_{self.retriever_type}_results_{timestamp}.xlsx"
        
        output_path = outputs_dir / output_file
        
        try:
            print(f"\n💾 Saving results to: {output_path}")
            
            if include_metadata:
                with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                    # Main results
                    results_df.to_excel(writer, sheet_name='Results', index=False)
                    
                    # Metadata
                    metadata = {
                        'run_timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        'collection_name': [self.collection_name],
                        'retriever_type': [self.retriever_type],
                        'k_documents': [self.k],
                        'total_questions': [len(results_df)],
                        'avg_processing_time': [results_df['processing_time'].mean()]
                    }
                    metadata_df = pd.DataFrame(metadata)
                    metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
                    
                    print(f"✅ Saved with metadata")
            else:
                results_df.to_excel(output_path, index=False)
                print(f"✅ Saved results only")
            
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            raise
    
    def run_full_pipeline(
        self,
        input_file: str,
        output_file: str = None,
        question_column: str = "question",
        batch_size: int = 10,
        nrows: Optional[int] = None,
        start_row: Optional[int] = None,
        end_row: Optional[int] = None,
        test_retrieval: bool = True
    ) -> str:
        """
        Chạy full pipeline với testing
        
        Args:
            input_file: Đường dẫn file input
            output_file: Đường dẫn file output (optional)
            question_column: Tên cột chứa câu hỏi
            batch_size: Kích thước batch xử lý
            nrows: Số dòng tối đa để đọc (None = đọc tất cả)
            start_row: Dòng bắt đầu (0-based, None = từ đầu)
            end_row: Dòng kết thúc (0-based, None = đến cuối)
            test_retrieval: Có test retrieval không
        """
        print(f"\n🚀 Starting Enhanced VIMQA Full Pipeline")
        print(f"{'='*60}")
        
        # Test retrieval methods first
        if test_retrieval:
            self.test_retrieval_methods()
        
        # Step 1: Load questions
        df = self.load_questions_from_excel(
            input_file, 
            question_column,
            nrows=nrows,
            start_row=start_row,
            end_row=end_row
        )
        
        # Step 2: Process questions
        results_df = self.process_questions(
            df, 
            question_column=question_column,
            batch_size=batch_size
        )
        
        # Step 3: Save results
        output_path = self.save_results(results_df, output_file)
        
        # Step 4: Summary
        total = len(results_df)
        avg_time = results_df['processing_time'].mean()
        
        print(f"\n🎯 Enhanced Pipeline Summary:")
        print(f"   Retrieval Method: {self.retriever_type.upper()}")
        print(f"   Total questions: {total}")
        print(f"   Avg processing time: {avg_time:.2f}s")
        print(f"   Output file: {output_path}")
        
        return output_path

def main():
    """
    Main function với enhanced argument parsing
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced VIMQA RAG Pipeline with Vector retrieval support")
    parser.add_argument("--input", "-i", required=True, help="Input Excel file path")
    parser.add_argument("--output", "-o", help="Output Excel file path")
    parser.add_argument("--question_column", "-q", default="question", help="Question column name")
    parser.add_argument("--collection", "-c", default="VIMQA_dev", help="Qdrant collection name")
    parser.add_argument("--retriever", "-r", default="vector", 
                       choices=["vector"], 
                       help="Retriever type")
    parser.add_argument("--k", type=int, default=5, help="Number of documents to retrieve")
    parser.add_argument("--batch_size", "-b", type=int, default=10, help="Batch size for processing")
    parser.add_argument("--nrows", "-n", type=int, help="Number of rows to process from start")
    parser.add_argument("--start_row", type=int, help="Start row (0-based, inclusive)")
    parser.add_argument("--end_row", type=int, help="End row (0-based, exclusive)")
    parser.add_argument("--no_test", action="store_true", 
                       help="Skip retrieval testing")
    
    args = parser.parse_args()
    
    try:
        # Initialize enhanced runner
        runner = EnhancedVIMQARunner(
            collection_name=args.collection,
            retriever_type=args.retriever,
            k=args.k
        )
        
        # Run pipeline
        output_file = runner.run_full_pipeline(
            input_file=args.input,
            output_file=args.output,
            question_column=args.question_column,
            batch_size=args.batch_size,
            nrows=args.nrows,
            start_row=args.start_row,
            end_row=args.end_row,
            test_retrieval=not args.no_test
        )
        
        print(f"\n🎉 Enhanced Pipeline completed successfully!")
        print(f"📄 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"\n💥 Enhanced Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("🚀 Enhanced VIMQA RAG Pipeline Runner")
        print("="*50)
        print("\nFeatures:")
        print("✅ Full Vector Search support")
        print("✅ Document loading from Qdrant")
        print("✅ Retrieval method testing")
        print("✅ Enhanced error handling")
        print("✅ Processing time tracking")
        print("✅ Row range selection support")
        
        print("\nExample usage:")
        print("# Vector search with default settings")
        print("python run_pipeline_rag_real_enhanced.py -i questions.xlsx -r vector")
        
        print("\n# Quick test with 5 questions")
        print("python run_pipeline_rag_real_enhanced.py -i questions.xlsx -r vector -n 5")
        
        print("\n# Process specific rows")
        print("python run_pipeline_rag_real_enhanced.py -i questions.xlsx --start_row 10 --end_row 20")
        
        print("\n# Process from specific row to end")
        print("python run_pipeline_rag_real_enhanced.py -i questions.xlsx --start_row 10")
        
        print("\n# Process from start to specific row")
        print("python run_pipeline_rag_real_enhanced.py -i questions.xlsx --end_row 20")
        
    else:
        main()