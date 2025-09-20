"""
RAG Pipeline - Kết hợp retrieval và generation để trả lời câu hỏi
"""

from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Setup paths
current_file = Path(__file__)

sys.path.append(str(current_file.parent.parent))

# Import các module đã có
from layers._04_retrieval.retriever import DocumentRetriever
from layers._05_generation.generator import AnswerGenerator

# Load environment variables
load_dotenv()

# Default system prompts
DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the given context. 
If you don't know the answer, say you don't know. 
Use only the information from the context to answer. 
Keep your answers clear and simple."""

VIETNAMESE_SYSTEM_PROMPT = """Bạn là một trợ lý AI hữu ích, trả lời câu hỏi dựa trên thông tin được cung cấp. 
Nếu bạn không biết câu trả lời, hãy nói bạn không biết. 
Chỉ sử dụng thông tin từ context để trả lời. 
Giữ câu trả lời rõ ràng và đơn giản."""

class RAGPipeline:
    """
    Pipeline RAG hoàn chỉnh: Input -> Retrieval -> Generation -> Output
    """
    
    def __init__(
        self,
        # Retriever parameters
        retriever_type: str = "vector",
        vector_store_type: str = "qdrant",
        documents: Optional[List[Document]] = None,
        embeddings_model = None,
        hybrid_weights: List[float] = [0.5, 0.5],
        k: int = 5,
        
        # Vector store parameters
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None,
        collection_name: str = "VIMQA_dev",
        
        # Generator parameters
        generator_model: str = "gpt-4o-mini",
        temperature: float = 0,
        max_tokens: int = 4096,
        system_prompt: Optional[str] = None
    ):
        """
        Khởi tạo RAG Pipeline
        
        Args:
            retriever_type: Loại retriever ("vector", "bm25", "hybrid", "compression")
            vector_store_type: Loại vector store ("qdrant")
            documents: List documents cho BM25 và hybrid
            embeddings_model: Model embedding
            hybrid_weights: Trọng số cho hybrid search [vector_weight, bm25_weight]
            k: Số lượng documents trả về
            qdrant_url: URL Qdrant server
            qdrant_api_key: API key Qdrant
            collection_name: Tên collection
            generator_model: Model OpenAI hoặc Hugging Face
            temperature: Độ sáng tạo của model
            max_tokens: Số token tối đa
            system_prompt: System prompt tùy chỉnh
        """
        
        # Khởi tạo embeddings model nếu chưa có
        if embeddings_model is None:
            self.embeddings_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
            )
        else:
            self.embeddings_model = embeddings_model
        
        # Store documents for later use
        self.documents = documents or []
        
        # Khởi tạo Document Retriever
        self.retriever = DocumentRetriever(
            retriever_type=retriever_type,
            vector_store_type=vector_store_type,
            documents=self.documents,
            embeddings_model=self.embeddings_model,
            hybrid_weights=hybrid_weights,
            k=k,
            qdrant_url=qdrant_url or os.getenv("QDRANT_URL"),
            qdrant_api_key=qdrant_api_key or os.getenv("QDRANT_API_KEY"),
            collection_name=collection_name
        )
        
        # Determine if using Hugging Face model
        self.is_hf_model = any(provider in generator_model for provider in 
                              ["Qwen/", "AITeamVN/", "microsoft/", "huggingface/"])
        
        # Determine if Vietnamese-focused model
        self.is_vietnamese = any(keyword in generator_model.lower() for keyword in 
                               ["vi-qwen", "vietnamese", "vi_", "vn_"]) or "Qwen" in generator_model
        
        # Set appropriate system prompt
        if system_prompt is None:
            self.system_prompt = VIETNAMESE_SYSTEM_PROMPT if self.is_vietnamese else DEFAULT_SYSTEM_PROMPT
        else:
            self.system_prompt = system_prompt
        
        # Khởi tạo Answer Generator
        self.generator = AnswerGenerator(
            model_name=generator_model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=self.system_prompt
        )
        
        # Fix: Add documents to vector store if using vector retriever
        if self.documents and retriever_type in ["vector", "hybrid"]:
            self._ensure_documents_indexed()
        
        print(f"RAG Pipeline initialized with:")
        print(f"  - Retriever: {retriever_type}")
        print(f"  - Vector Store: {vector_store_type}")
        print(f"  - Generator: {generator_model}")
        print(f"  - Model Type: {'Hugging Face' if self.is_hf_model else 'OpenAI'}")
        print(f"  - Language: {'Vietnamese' if self.is_vietnamese else 'English'}")
        print(f"  - K documents: {k}")
        print(f"  - Documents loaded: {len(self.documents)}")
    
    def _ensure_documents_indexed(self):
        """
        Đảm bảo documents đã được index vào vector store
        """
        try:
            if hasattr(self.retriever, 'vector_store') and self.retriever.vector_store:
                # Try to get collection info
                try:
                    collection_info = self.retriever.vector_store.get_collection_info()
                    if collection_info and collection_info.get('vectors_count', 0) == 0:
                        print(f"📝 Indexing {len(self.documents)} documents to vector store...")
                        self.retriever.vector_store.add_documents(self.documents)
                        print(f"✅ Documents indexed successfully")
                    else:
                        print(f"📚 Vector store already contains documents")
                except:
                    # If can't get collection info, try to add documents anyway
                    print(f"📝 Attempting to index {len(self.documents)} documents...")
                    if self.documents:
                        self.retriever.vector_store.add_documents(self.documents)
                        print(f"✅ Documents added to vector store")
        except Exception as e:
            print(f"⚠️  Warning: Could not verify/index documents: {e}")
            print(f"    This might be okay if documents are already indexed")
    
    def query(
        self, 
        question: str,
        return_sources: bool = True,
        return_documents: bool = False
    ) -> Dict[str, Any]:
        """
        Xử lý câu hỏi qua pipeline RAG hoàn chỉnh
        
        Args:
            question: Câu hỏi của user
            return_sources: Có trả về sources không
            return_documents: Có trả về raw documents không
            
        Returns:
            Dictionary chứa answer và thông tin bổ sung
        """
        
        print(f"\n🔍 Retrieving documents for: '{question}'")
        
        # Bước 1: Retrieve documents
        try:
            documents = self.retriever.retrieve_documents(question)
            print(f"✅ Found {len(documents)} relevant documents")
            
            # Debug: Print document contents if found
            if len(documents) > 0:
                print("📄 Retrieved documents preview:")
                for i, doc in enumerate(documents[:2]):  # Show first 2 docs
                    content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
                    print(f"   {i+1}. {content_preview}")
            else:
                print("⚠️  No documents found, trying fallback...")
                # Fallback: use original documents if retrieval fails
                if self.documents:
                    documents = self.documents[:self.retriever.k]
                    print(f"📚 Using fallback documents: {len(documents)}")
                    
        except Exception as e:
            print(f"❌ Retrieval failed: {e}")
            # Fallback to original documents
            if self.documents:
                documents = self.documents[:self.retriever.k]
                print(f"📚 Using fallback documents: {len(documents)}")
            else:
                return {
                    "question": question,
                    "answer": "Xin lỗi, không thể tìm kiếm tài liệu liên quan.",
                    "error": str(e),
                    "num_documents_used": 0
                }
        
        # Bước 2: Generate answer
        print(f"🤖 Generating answer...")
        try:
            if return_sources:
                result = self.generator.generate_answer_with_sources(question, documents)
                answer = result["answer"]
                sources = result["sources"]
            else:
                answer = self.generator.generate_answer(question, documents)
                sources = []
                
            print(f"✅ Answer generated successfully")
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            print(f"    Error details: {type(e).__name__}: {str(e)}")
            return {
                "question": question,
                "answer": "Xin lỗi, không thể tạo câu trả lời.",
                "error": str(e),
                "num_documents_used": len(documents) if 'documents' in locals() else 0
            }
        
        # Prepare result
        result = {
            "question": question,
            "answer": answer,
            "num_documents_used": len(documents)
        }
        
        if return_sources:
            result["sources"] = sources
            
        if return_documents:
            result["documents"] = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in documents
            ]
        
        return result
    
    def batch_query(self, questions: List[str]) -> List[Dict[str, Any]]:
        """
        Xử lý nhiều câu hỏi cùng lúc
        
        Args:
            questions: List các câu hỏi
            
        Returns:
            List các kết quả
        """
        results = []
        for i, question in enumerate(questions, 1):
            print(f"\n📝 Processing question {i}/{len(questions)}")
            result = self.query(question)
            results.append(result)
            
        return results
    
    def add_documents(self, new_documents: List[Document]):
        """
        Thêm documents mới vào hệ thống
        
        Args:
            new_documents: List documents mới
        """
        try:
            # Add to local storage
            self.documents.extend(new_documents)
            
            if hasattr(self.retriever, 'vector_store') and self.retriever.vector_store:
                # Thêm vào vector store
                self.retriever.vector_store.add_documents(new_documents)
                print(f"✅ Added {len(new_documents)} documents to vector store")
                
            # Cập nhật documents cho BM25 nếu cần
            if hasattr(self.retriever, 'documents') and self.retriever.documents is not None:
                self.retriever.documents.extend(new_documents)
                # Reinitialize BM25 retriever if needed
                if hasattr(self.retriever.retriever, 'bm25_retriever'):
                    self.retriever._initialize_retriever()
                print(f"✅ Updated BM25 index with {len(new_documents)} new documents")
                
        except Exception as e:
            print(f"❌ Failed to add documents: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Lấy thông tin về hệ thống RAG
        """
        return {
            "retriever_type": self.retriever.retriever_type,
            "vector_store_type": self.retriever.vector_store_type,
            "generator_model": self.generator.model_name,
            "k_documents": self.retriever.k,
            "temperature": self.generator.temperature,
            "collection_name": getattr(self.retriever.vector_store, 'collection_name', 'N/A'),
            "total_documents": len(self.documents)
        }

def create_rag_pipeline(
    documents: Optional[List[Document]] = None,
    retriever_type: str = "bm25",  # Changed default to BM25 for reliability
    generator_model: str = "gpt-4o-mini"
) -> RAGPipeline:
    """
    Factory function để tạo RAG pipeline đơn giản
    
    Args:
        documents: Documents để index
        retriever_type: Loại retriever
        generator_model: Model generator
        
    Returns:
        RAGPipeline instance
    """
    return RAGPipeline(
        retriever_type=retriever_type,
        documents=documents,
        generator_model=generator_model
    )

if __name__ == "__main__":
    """
    Demo và test RAG Pipeline
    """
    from langchain_core.documents import Document
    
    # Tạo sample documents
    sample_docs = [
        Document(
            page_content="RAG (Retrieval-Augmented Generation) là một kỹ thuật kết hợp việc tìm kiếm thông tin liên quan với việc tạo sinh ngôn ngữ. RAG giúp cải thiện độ chính xác của các mô hình ngôn ngữ lớn.",
            metadata={"source": "rag_intro.txt", "doc_id": "RAG_1", "title": "Giới thiệu RAG", "excel_row": 1}
        ),
        Document(
            page_content="Vector search sử dụng embeddings để tìm kiếm tài liệu tương tự về mặt ngữ nghĩa. Nó hiệu quả hơn keyword search trong nhiều trường hợp.",
            metadata={"source": "vector_search.txt", "doc_id": "VEC_1", "title": "Vector Search", "excel_row": 2}
        ),
        Document(
            page_content="OpenAI GPT-4 là một mô hình ngôn ngữ lớn có khả năng hiểu và tạo sinh văn bản một cách tự nhiên. Nó được sử dụng trong nhiều ứng dụng AI.",
            metadata={"source": "gpt4_info.txt", "doc_id": "GPT4_1", "title": "GPT-4", "excel_row": 3}
        ),
        Document(
            page_content="Python là ngôn ngữ lập trình phổ biến trong AI và machine learning. Các thư viện như LangChain giúp xây dựng ứng dụng AI dễ dàng hơn.",
            metadata={"source": "python_ai.txt", "doc_id": "PY_1", "title": "Python & AI", "excel_row": 4}
        )
    ]
    
    print("🚀 Testing RAG Pipeline...")
    
    # Test 1: BM25 retriever (more reliable for testing)
    print("\n" + "="*50)
    print("TEST 1: BM25 Retriever + GPT-4o-mini")
    print("="*50)
    try:
        rag = RAGPipeline(
            retriever_type="bm25",
            documents=sample_docs,
            k=3
        )
        
        # Test single query
        result = rag.query("RAG là gì?")
        print(f"\n📋 Question: {result['question']}")
        print(f"💡 Answer: {result['answer']}")
        print(f"📚 Sources: {result.get('sources', [])}")
        print(f"📄 Documents used: {result['num_documents_used']}")
        
    except Exception as e:
        print(f"❌ BM25 test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Vector retriever
    print("\n" + "="*50)
    print("TEST 2: Vector Retriever")
    print("="*50)
    try:
        rag_vector = RAGPipeline(
            retriever_type="vector",
            documents=sample_docs,
            k=2,
            collection_name="VIMQA_dev"  # Use unique collection name
        )
        
        result = rag_vector.query("Vector search hoạt động như thế nào?")
        print(f"\n📋 Question: {result['question']}")
        print(f"💡 Answer: {result['answer']}")
        print(f"📚 Sources: {result.get('sources', [])}")
        
    except Exception as e:
        print(f"❌ Vector test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Batch queries (only if BM25 test passed)
    print("\n" + "="*50)
    print("TEST 3: Batch Queries")
    print("="*50)
    try:
        if 'rag' in locals():
            questions = [
                "Python có ưu điểm gì trong AI?",
                "GPT-4 là gì?"
            ]
            
            results = rag.batch_query(questions)
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['question']}")
                if 'error' not in result:
                    print(f"   Answer: {result['answer'][:100]}...")
                else:
                    print(f"   Error: {result['error']}")
                    
    except Exception as e:
        print(f"❌ Batch test failed: {e}")
    
    # Test 4: System info
    print("\n" + "="*50)
    print("TEST 4: System Information")
    print("="*50)
    try:
        if 'rag' in locals():
            info = rag.get_system_info()
            print("🔧 System Configuration:")
            for key, value in info.items():
                print(f"   {key}: {value}")
                
    except Exception as e:
        print(f"❌ System info test failed: {e}")
    
    # Test 5: Simple functional test
    print("\n" + "="*50)
    print("TEST 5: Simple Functional Test")
    print("="*50)
    try:
        simple_rag = create_rag_pipeline(documents=sample_docs, retriever_type="bm25")
        result = simple_rag.query("Python có gì hay?", return_documents=True)
        
        print(f"\n📋 Question: {result['question']}")
        if 'error' not in result:
            print(f"💡 Answer: {result['answer']}")
            print(f"📄 Documents used: {result['num_documents_used']}")
            
            if result.get('documents'):
                print("\n📑 Retrieved documents:")
                for i, doc in enumerate(result['documents'], 1):
                    print(f"   {i}. {doc['content'][:50]}...")
        else:
            print(f"❌ Error: {result['error']}")
        
    except Exception as e:
        print(f"❌ Simple test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ RAG Pipeline testing completed!")
