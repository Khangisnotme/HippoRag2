"""
This module helps generate answers using AI models.
It combines retrieved documents with user questions to create good answers.
"""

from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from openai import OpenAI
import httpx
from dotenv import load_dotenv
import os
import argparse
from huggingface_hub import InferenceClient
import requests

# Load environment variables
load_dotenv()

# Default system prompt
DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the given context. 
If you don't know the answer, say you don't know. 
Use only the information from the context to answer. 
Keep your answers clear and simple."""

# Vietnamese system prompt for Qwen models
VIETNAMESE_SYSTEM_PROMPT = """Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể dựa trên ngữ cảnh được cung cấp."""

class HuggingFaceProvider:
    """Provider for Hugging Face models via Inference API"""
    
    def __init__(self, model_name: str, hf_token: str):
        self.model_name = model_name
        self.hf_token = hf_token
        self.client = InferenceClient(token=hf_token)
        
        # Working models from test results
        self.supported_models = {
            "Qwen/Qwen2.5-1.5B-Instruct": "chat_completion",
            # Add more as they become available
        }
        
        # Check if model is supported
        if model_name not in self.supported_models:
            print(f"⚠️  Warning: {model_name} may not be supported. Using Qwen/Qwen2.5-1.5B-Instruct instead.")
            self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        
        self.method = self.supported_models.get(self.model_name, "chat_completion")
    
    def generate_completion(self, messages: List[Dict], **kwargs):
        """Generate completion using Hugging Face model"""
        try:
            if self.method == "chat_completion":
                response = self.client.chat_completion(
                    messages=messages,
                    model=self.model_name,
                    max_tokens=kwargs.get('max_tokens', 2048),
                    temperature=kwargs.get('temperature', 0.1),
                    stream=False
                )
                return response.choices[0].message.content
            else:
                # Fallback to text generation if needed
                prompt = self._messages_to_prompt(messages)
                response = self.client.text_generation(
                    prompt=prompt,
                    model=self.model_name,
                    max_new_tokens=kwargs.get('max_tokens', 2048),
                    temperature=kwargs.get('temperature', 0.1),
                    return_full_text=False
                )
                return response
                
        except Exception as e:
            return f"Hugging Face API Error: {str(e)}"
    
    def _messages_to_prompt(self, messages: List[Dict]) -> str:
        """Convert messages to single prompt"""
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt = msg["content"] + "\n\n"
            elif msg["role"] == "user":
                prompt += msg["content"]
        return prompt

class AnswerGenerator:
    """
    A class that helps generate answers using OpenAI models or Hugging Face models.
    
    This class can:
    - Combine documents with questions
    - Use OpenAI models or Hugging Face models to generate answers
    - Format answers nicely
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0,
        max_tokens: int = 4096,
        system_prompt: str = None
    ):
        """
        Start the AnswerGenerator with optional model settings.
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Check if it's a Hugging Face model
        self.is_hf_model = any(provider in model_name for provider in 
                              ["Qwen/", "AITeamVN/", "microsoft/", "huggingface/"])
        
        # Check if it's Vietnamese-focused
        self.is_vietnamese = any(keyword in model_name.lower() for keyword in 
                               ["vi-qwen", "vietnamese", "vi_", "vn_"]) or "Qwen" in model_name
        
        # Set appropriate system prompt
        if system_prompt is None:
            self.system_prompt = VIETNAMESE_SYSTEM_PROMPT if self.is_vietnamese else DEFAULT_SYSTEM_PROMPT
        else:
            self.system_prompt = system_prompt
            
        # Initialize appropriate client
        if self.is_hf_model:
            hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
            if not hf_token:
                raise ValueError("HF_TOKEN, HUGGINGFACE_TOKEN, or HUGGINGFACE_API_KEY environment variable is required for Hugging Face models")
            
            self.provider = HuggingFaceProvider(model_name, hf_token)
            print(f"🤖 Using Hugging Face model: {self.provider.model_name}")
        else:
            # Initialize OpenAI client
            if os.getenv("OPENAI_PROXY"):
                http_client = httpx.Client(proxies=os.getenv("OPENAI_PROXY"))
                self.client = OpenAI(
                    http_client=http_client,
                    api_key=os.getenv("OPENAI_API_KEY")
                )
            else:
                self.client = OpenAI(
                    api_key=os.getenv("OPENAI_API_KEY")
                )
            print(f"🤖 Using OpenAI model: {model_name}")
    
    def format_context(self, documents: List[Document]) -> str:
        """Combine documents into a single context string."""
        return "\n\n".join(doc.page_content for doc in documents)
    
    def _create_rag_prompt(self, question: str, context: str) -> str:
        """Create RAG prompt - works for both English and Vietnamese"""
        if self.is_vietnamese:
            template = '''Chú ý các yêu cầu sau:
- Câu trả lời phải chính xác và đầy đủ nếu ngữ cảnh có câu trả lời. 
- Chỉ sử dụng các thông tin có trong ngữ cảnh được cung cấp.
- Chỉ cần từ chối trả lời và không suy luận gì thêm nếu ngữ cảnh không có câu trả lời.
Hãy trả lời câu hỏi dựa trên ngữ cảnh:

### Ngữ cảnh:
{context}

### Câu hỏi:
{question}

### Trả lời:'''
        else:
            template = '''Please follow these requirements:
- Answer must be accurate and complete if the context contains the answer.
- Only use information provided in the context.
- Simply refuse to answer if the context doesn't contain the answer.
Answer the question based on the context:

### Context:
{context}

### Question:
{question}

### Answer:'''
        
        return template.format(context=context, question=question)
    
    def generate_answer(
        self,
        question: str,
        documents: List[Document],
        format_context: bool = True
    ) -> str:
        """Generate an answer using the specified model."""
        if format_context:
            context = self.format_context(documents)
        else:
            context = documents[0].page_content if documents else ""
            
        if self.is_hf_model:
            # Use RAG-specific prompt format for Hugging Face models
            prompt = self._create_rag_prompt(question, context)
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            return self.provider.generate_completion(
                messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
        else:
            # Use OpenAI format
            prompt = f"""Context: {context}

Question: {question}

Answer:"""
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
    
    def generate_answer_with_sources(
        self,
        question: str,
        documents: List[Document]
    ) -> Dict[str, Any]:
        """Generate an answer with source information and extra metadata fields."""
        answer = self.generate_answer(question, documents)
        
        # Extract sources and extra metadata from document metadata
        sources = []
        doc_ids = []
        titles = []
        excel_rows = []
        for doc in documents:
            meta = doc.metadata
            if "source" in meta:
                sources.append(meta["source"])
            doc_ids.append(meta.get("doc_id", ""))
            titles.append(meta.get("title", ""))
            excel_rows.append(meta.get("excel_row", ""))
        return {
            "answer": answer,
            "sources": list(set(sources)),  # Remove duplicates
            "doc_id": doc_ids,
            "title": titles,
            "excel_row": excel_rows
        }

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="RAG Answer Generator with multiple model support")
    parser.add_argument(
        "--model", 
        type=str, 
        default="gpt-4o-mini",
        help="Model to use (e.g., gpt-4o-mini, gpt-4, Qwen/Qwen2.5-1.5B-Instruct)"
    )
    parser.add_argument(
        "--temperature", 
        type=float, 
        default=0.0,
        help="Temperature for text generation (0.0 to 1.0)"
    )
    parser.add_argument(
        "--max-tokens", 
        type=int, 
        default=4096,
        help="Maximum number of tokens in response"
    )
    parser.add_argument(
        "--question", 
        type=str,
        help="Question to ask (for quick testing)"
    )
    parser.add_argument(
        "--language", 
        type=str, 
        choices=["en", "vi"], 
        default="auto",
        help="Language mode (en=English, vi=Vietnamese, auto=detect from model)"
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    """
    Usage examples:
    python answer_generator.py --model gpt-4o-mini --question "What is RAG?"
    python answer_generator.py --model Qwen/Qwen2.5-1.5B-Instruct --question "RAG là gì?"
    python answer_generator.py --model Qwen/Qwen2.5-1.5B-Instruct --language vi
    """
    from langchain_core.documents import Document
    
    # Parse command line arguments
    args = parse_arguments()
    
    print(f"Using model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Max tokens: {args.max_tokens}")
    
    # Create sample documents based on model/language
    if "Qwen" in args.model or args.language == "vi":
        # Vietnamese documents
        sample_docs = [
            Document(
                page_content="Machine Learning (Học máy) là một nhánh của trí tuệ nhân tạo (AI) cho phép máy tính học hỏi và cải thiện hiệu suất từ dữ liệu mà không cần được lập trình cụ thể cho từng tác vụ.",
                metadata={"source": "ml_definition_vi"}
            ),
            Document(
                page_content="Machine Learning sử dụng các thuật toán để phân tích dữ liệu, tìm ra các mẫu (pattern), và đưa ra dự đoán hoặc quyết định mà không cần can thiệp trực tiếp của con người.",
                metadata={"source": "ml_process_vi"}
            ),
            Document(
                page_content="RAG (Retrieval-Augmented Generation) là kỹ thuật kết hợp việc truy xuất thông tin từ cơ sở dữ liệu với mô hình ngôn ngữ để tạo ra câu trả lời chính xác hơn.",
                metadata={"source": "rag_definition_vi"}
            )
        ]
        default_question = "Machine learning là gì?"
    else:
        # English documents
        sample_docs = [
            Document(
                page_content="Machine Learning is a subset of artificial intelligence that enables computers to learn and improve from data without being explicitly programmed for each task.",
                metadata={"source": "ml_definition"}
            ),
            Document(
                page_content="Machine Learning algorithms analyze data, identify patterns, and make predictions or decisions without direct human intervention.",
                metadata={"source": "ml_process"}
            ),
            Document(
                page_content="RAG (Retrieval-Augmented Generation) combines information retrieval with language model generation to provide more accurate answers.",
                metadata={"source": "rag_definition"}
            )
        ]
        default_question = "What is machine learning?"
    
    # Use provided question or default
    question = args.question if args.question else default_question
    
    # Test basic answer generation
    print(f"\nTesting basic answer generation with question: '{question}'")
    try:
        answer_gen = AnswerGenerator(
            model_name=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
        answer = answer_gen.generate_answer(question, sample_docs)
        print(f"\nGenerated answer:\n{answer}")
    except Exception as e:
        print(f"Basic generation test failed: {e}")
    
    # Test answer with sources
    print(f"\n" + "="*50)
    try:
        result = answer_gen.generate_answer_with_sources(question, sample_docs)
        print(f"Answer with sources:\n{result['answer']}")
        print(f"\nSources: {result['sources']}")
    except Exception as e:
        print(f"Source generation test failed: {e}")
    
    # Show available models
    print(f"\n" + "="*50)
    print("✅ Tested working models:")
    print("- Qwen/Qwen2.5-1.5B-Instruct (Vietnamese support, free)")
    print("- gpt-4o-mini, gpt-4o, gpt-4, gpt-3.5-turbo (OpenAI, paid)")
    
    print(f"\nUsage examples:")
    print("python answer_generator.py --model Qwen/Qwen2.5-1.5B-Instruct --question 'Machine learning là gì?'")
    print("python answer_generator.py --model gpt-4o-mini --question 'What is machine learning?'")
    print("python answer_generator.py --model Qwen/Qwen2.5-1.5B-Instruct --temperature 0.1 --max-tokens 2048")
