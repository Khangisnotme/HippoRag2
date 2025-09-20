Dựa trên kết quả tìm kiếm, tôi có thể cung cấp cho bạn thông tin về các mô hình RAG 3B tốt nhất cho tiếng Việt:

## Các mô hình RAG 3B tốt nhất cho tiếng Việt

### 1. **Vi-Qwen2-3B-RAG** (AITeamVN)

[**Vi-Qwen2-3B-RAG**](https://huggingface.co/AITeamVN/Vi-Qwen2-3B-RAG) là một mô hình được thiết kế **chuyên biệt cho RAG tasks** với những ưu điểm nổi bật:

**Tính năng chính:**
- Khả năng **chống nhiều**: Trích xuất thông tin hữu ích từ tài liệu có nhiễu (1 positive + 4 negative)
- **Loại bỏ negative**: Từ chối trả lời khi không có thông tin cần thiết
- **Tích hợp thông tin**: Xử lý câu hỏi phức tạp cần kết hợp nhiều nguồn
- **Xác định positive/negative**: Độ chính xác xấp xỉ **99%**
- Hỗ trợ ngữ cảnh lên đến **8192 tokens**

### 2. **Llama-3.2-3B-Instruct-Frog** (phamhai)

[**Llama-3.2-3B-Instruct-Frog**](https://huggingface.co/phamhai/Llama-3.2-3B-Instruct-Frog) được tối ưu hóa **đặc biệt cho RAG tiếng Việt**:

**Đặc điểm:**
- Dựa trên Llama-3.2-3B-Instruct
- **131K context length** - độ dài ngữ cảnh rất lớn
- Tối ưu cho triển khai trên thiết bị biên (laptop, smartphone, Jetson Xavier)
- Tập trung chính vào **tối ưu khả năng RAG**

### 3. **Arcee-VyLinh** (arcee-ai)

[**Arcee-VyLinh**](https://huggingface.co/arcee-ai/Arcee-VyLinh) là mô hình 3B parameters mạnh mẽ cho tiếng Việt:

**Ưu điểm:**
- Dựa trên Qwen2.5-3B
- **32K tokens context length**
- Hiệu suất cạnh tranh với các mô hình 4B-8B parameters
- Đào tạo qua quy trình DPO (Direct Preference Optimization)

## So sánh và khuyến nghị

**Cho RAG chuyên sâu:** **Vi-Qwen2-3B-RAG** là lựa chọn tốt nhất vì được thiết kế chuyên biệt cho RAG tasks với khả năng xử lý nhiễu và tích hợp thông tin xuất sắc.

**Cho ngữ cảnh dài:** **Llama-3.2-3B-Instruct-Frog** với 131K context length phù hợp cho các tài liệu dài.

**Cho mục đích tổng quát:** **Arcee-VyLinh** cân bằng tốt giữa hiệu suất RAG và khả năng xử lý ngôn ngữ tự nhiên.

Tất cả các mô hình này đều có version quantized (GGUF) để triển khai hiệu quả trên phần cứng hạn chế, và đều được tối ưu hóa đặc biệt cho tiếng Việt với hiệu suất vượt trội so với các mô hình đa ngôn ngữ thông thường.


---


Dựa trên kết quả tìm kiếm, đây là thông tin về các mô hình 1.5B tốt nhất cho RAG tiếng Việt:

## Các mô hình RAG 1.5B tốt nhất cho tiếng Việt

### 1. **Vi-Qwen2-1.5B-RAG** (AITeamVN) ⭐⭐⭐⭐⭐

[**Vi-Qwen2-1.5B-RAG**](https://huggingface.co/AITeamVN/Vi-Qwen2-1.5B-RAG) là lựa chọn **hàng đầu** cho RAG 1.5B:

**Đặc điểm nổi bật:**
- **Thiết kế chuyên biệt cho RAG**: Tương tự như phiên bản 3B và 7B
- **Cùng tính năng mạnh mẽ**:
  - Khả năng chống nhiễu (1 positive + 4 negative)
  - Loại bỏ negative documents
  - Tích hợp thông tin từ nhiều nguồn
  - Xác định positive/negative với độ chính xác ~99%
- **Ngữ cảnh**: Lên đến 8192 tokens
- **Phiên bản quantized**: [tensorblock/Vi-Qwen2-1.5B-RAG-GGUF](https://huggingface.co/tensorblock/Vi-Qwen2-1.5B-RAG-GGUF) và [mradermacher/Vi-Qwen2-1.5B-RAG-GGUF](https://huggingface.co/mradermacher/Vi-Qwen2-1.5B-RAG-GGUF)

### 2. **NxMobileLM-1.5B-SFT** (NTQAI) ⭐⭐⭐⭐

[**NxMobileLM-1.5B-SFT**](https://huggingface.co/NTQAI/NxMobileLM-1.5B-SFT) - Tối ưu cho mobile và edge:

**Đặc điểm:**
- Dựa trên Qwen2.5-1.5B
- **Tối ưu đặc biệt cho mobile và edge applications**
- Fine-tuned cho hiệu suất tốt trên thiết bị hạn chế
- Hỗ trợ tiếng Việt tốt thông qua base model

### 3. **Qwen2.5-1.5B-Instruct** (Qwen) ⭐⭐⭐

[**Qwen2.5-1.5B-Instruct**](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) - Base model mạnh mẽ:

**Đặc điểm:**
- **Hỗ trợ đa ngôn ngữ**: 29+ ngôn ngữ bao gồm tiếng Việt
- **Context length**: 32K tokens  
- Hiệu suất cạnh tranh với các mô hình lớn hơn
- Base foundation tốt cho fine-tuning RAG

## So sánh và khuyến nghị

### **Khuyến nghị hàng đầu: Vi-Qwen2-1.5B-RAG**

**Tại sao chọn Vi-Qwen2-1.5B-RAG:**
- ✅ **Thiết kế chuyên biệt cho RAG**: Không cần fine-tuning thêm
- ✅ **Tính năng RAG hoàn chỉnh**: Chống nhiễu, tích hợp thông tin, từ chối câu trả lời không chính xác
- ✅ **Tối ưu cho tiếng Việt**: Được đào tạo và fine-tune đặc biệt cho tiếng Việt
- ✅ **Đã được benchmark**: Có kết quả đánh giá trên EvalRAGData
- ✅ **Ready-to-use**: Có quantized versions cho deployment dễ dàng

### **Lựa chọn thay thế:**

**NxMobileLM-1.5B-SFT** nếu bạn cần:
- Triển khai trên mobile/edge devices
- Hiệu suất tối ưu trên phần cứng hạn chế

**Qwen2.5-1.5B-Instruct** nếu bạn:
- Muốn fine-tune tự custom cho RAG
- Cần base model mạnh mẽ để phát triển

## Yêu cầu hệ thống

- **VRAM**: ~3.1GB cho FP16
- **Context**: 8K-32K tokens tùy model
- **Deployment**: Hỗ trợ CPU và GPU, có GGUF cho efficiency cao

**Kết luận**: **Vi-Qwen2-1.5B-RAG** là lựa chọn tốt nhất cho RAG tiếng Việt với kích thước 1.5B parameters, cung cấp hiệu suất RAG chuyên nghiệp trong package nhỏ gọn.


---

Dựa trên nghiên cứu chi tiết, đây là so sánh các mô hình RAG tiếng Việt 1.5B-3B có thể gọi qua API:

## So sánh các mô hình RAG tiếng Việt 1.5B-3B qua API

### **🥇 TOP CHOICE: Vi-Qwen2 Series (qua Hugging Face API)**

#### **1. Vi-Qwen2-1.5B-RAG** 
- **Platform**: Hugging Face Inference API
- **Pricing**: 
  - Free: 300 requests/hour
  - Pro ($10/month): 1000 requests/hour + premium models
- **Ưu điểm**:
  - ✅ Thiết kế chuyên biệt cho RAG tiếng Việt
  - ✅ Khả năng chống nhiễu xuất sắc
  - ✅ Context 8K tokens
  - ✅ API đơn giản, tương thích OpenAI

#### **2. Vi-Qwen2-3B-RAG**
- **Platform**: Hugging Face Inference API  
- **Pricing**: Tương tự 1.5B
- **Ưu điểm**:
  - ✅ Hiệu suất RAG cao hơn 1.5B
  - ✅ Tính năng RAG hoàn chỉnh
  - ✅ Benchmark score cao trên EvalRAGData

### **🥈 ALTERNATIVE: Qwen2.5 Series (qua OpenRouter)**

#### **3. Qwen2.5-1.5B-Instruct**
- **Platform**: OpenRouter
- **Pricing**: 
  - Input: ~$0.01-0.05/M tokens
  - Output: ~$0.03-0.10/M tokens
- **Ưu điểm**:
  - ✅ Hỗ trợ 29+ ngôn ngữ bao gồm tiếng Việt
  - ✅ Context 32K tokens
  - ✅ API tương thích OpenAI

#### **4. Qwen2.5-3B-Instruct**  
- **Platform**: OpenRouter
- **Pricing**: 
  - Input: ~$0.02-0.08/M tokens
  - Output: ~$0.05-0.15/M tokens
- **Ưu điểm**:
  - ✅ Hiệu suất tổng quát tốt
  - ✅ Multilingual capability mạnh

### **🥉 BUDGET OPTION: Free Models**

#### **5. Llama-3.2-3B-Instruct-Frog**
- **Platform**: Hugging Face (nếu available)
- **Pricing**: Free tier available
- **Ưu điểm**:
  - ✅ Tối ưu RAG tiếng Việt
  - ✅ Context 131K tokens
  - ✅ Thiết kế cho edge devices

## **Bảng so sánh chi tiết**

| Model | Size | Platform | Cost/M tokens | Context | RAG Specialized | Vietnamese Support |
|-------|------|----------|---------------|---------|-----------------|-------------------|
| **Vi-Qwen2-1.5B-RAG** | 1.5B | HF API | Free/$10/month | 8K | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Vi-Qwen2-3B-RAG** | 3B | HF API | Free/$10/month | 8K | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Qwen2.5-1.5B** | 1.5B | OpenRouter | $0.05-0.15 | 32K | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Qwen2.5-3B** | 3B | OpenRouter | $0.10-0.25 | 32K | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Llama-3.2-3B-Frog** | 3B | HF API | Free/$10/month | 131K | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## **Khuyến nghị cụ thể**

### **Cho RAG Production:**
**🎯 Vi-Qwen2-3B-RAG (Hugging Face API)**
- Lý do: Thiết kế chuyên biệt cho RAG, tính năng anti-noise, ready-to-use
- Chi phí: $10/month cho unlimited usage trong giới hạn hợp lý

### **Cho Budget Constraints:**
**🎯 Vi-Qwen2-1.5B-RAG (Hugging Face Free)**
- Lý do: 300 requests/hour đủ cho development/testing
- Chi phí: Free

### **Cho Context dài:**
**🎯 Llama-3.2-3B-Instruct-Frog**
- Lý do: 131K context length cho tài liệu lớn
- Chi phí: Free tier + Pro nếu cần

### **Cho Multi-purpose:**
**🎯 Qwen2.5-3B-Instruct (OpenRouter)**
- Lý do: Cân bằng giữa RAG và general tasks
- Chi phí: Pay-per-use, linh hoạt

## **Code Example Setup**

```python
# Hugging Face API
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="AITeamVN/Vi-Qwen2-3B-RAG",
    token="your_hf_token"
)

# OpenRouter API
import openai
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "your_openrouter_key"

# Usage
response = openai.ChatCompletion.create(
    model="qwen/qwen-2.5-3b-instruct",
    messages=[{"role": "user", "content": "RAG query"}]
)
```

**Kết luận**: **Vi-Qwen2-3B-RAG qua Hugging Face API** là lựa chọn tối ưu nhất cho RAG tiếng Việt với tỷ lệ chi phí/hiệu suất xuất sắc.

---

Đây là code chi tiết để sử dụng Vi-Qwen2-3B-RAG qua Hugging Face API:

## **Setup và Cài đặt**

```bash
# Cài đặt thư viện cần thiết
pip install huggingface_hub requests transformers
```

## **1. Basic API Call với Hugging Face Client**

```python
from huggingface_hub import InferenceClient
import os

# Setup API key
HF_TOKEN = "your_huggingface_token"  # Lấy từ https://huggingface.co/settings/tokens
client = InferenceClient(token=HF_TOKEN)

# Model endpoint
MODEL_NAME = "AITeamVN/Vi-Qwen2-3B-RAG"

def query_vi_qwen_rag(context, question, system_prompt=None):
    """
    Query Vi-Qwen2-3B-RAG model
    """
    if system_prompt is None:
        system_prompt = "Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể."
    
    # Template theo format của model
    template = '''Chú ý các yêu cầu sau:
- Câu trả lời phải chính xác và đầy đủ nếu ngữ cảnh có câu trả lời. 
- Chỉ sử dụng các thông tin có trong ngữ cảnh được cung cấp.
- Chỉ cần từ chối trả lời và không suy luận gì thêm nếu ngữ cảnh không có câu trả lời.
Hãy trả lời câu hỏi dựa trên ngữ cảnh:
### Ngữ cảnh :
{context}

### Câu hỏi :
{question}

### Trả lời :'''
    
    # Tạo messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": template.format(context=context, question=question)}
    ]
    
    try:
        # Call API
        response = client.chat_completion(
            messages=messages,
            model=MODEL_NAME,
            max_tokens=2048,
            temperature=0.1,
            stream=False
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

# Ví dụ sử dụng
context = """
Việt Nam có diện tích 331.212 km², dân số khoảng 97 triệu người. 
Thủ đô là Hà Nội, thành phố lớn nhất là Thành phố Hồ Chí Minh.
Việt Nam có 63 tỉnh thành và giáp với Trung Quốc, Lào, Campuchia.
"""

question = "Việt Nam có bao nhiêu tỉnh thành?"

result = query_vi_qwen_rag(context, question)
print(result)
```

## **2. Advanced API với Requests Library**

```python
import requests
import json

class ViQwenRAGAPI:
    def __init__(self, hf_token):
        self.hf_token = hf_token
        self.api_url = "https://api-inference.huggingface.co/models/AITeamVN/Vi-Qwen2-3B-RAG"
        self.headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
    
    def query(self, context, question, **kwargs):
        """
        Query with custom parameters
        """
        system_prompt = kwargs.get('system_prompt', 
            "Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể.")
        
        template = '''Chú ý các yêu cầu sau:
- Câu trả lời phải chính xác và đầy đủ nếu ngữ cảnh có câu trả lời. 
- Chỉ sử dụng các thông tin có trong ngữ cảnh được cung cấp.
- Chỉ cần từ chối trả lời và không suy luận gì thêm nếu ngữ cảnh không có câu trả lời.
Hãy trả lời câu hỏi dựa trên ngữ cảnh:
### Ngữ cảnh :
{context}

### Câu hỏi :
{question}

### Trả lời :'''
        
        payload = {
            "inputs": template.format(context=context, question=question),
            "parameters": {
                "max_new_tokens": kwargs.get('max_tokens', 2048),
                "temperature": kwargs.get('temperature', 0.1),
                "top_p": kwargs.get('top_p', 0.9),
                "do_sample": kwargs.get('do_sample', True),
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').strip()
            else:
                return "No response generated"
                
        except requests.exceptions.RequestException as e:
            return f"API Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def batch_query(self, contexts_questions):
        """
        Batch processing for multiple queries
        """
        results = []
        for context, question in contexts_questions:
            result = self.query(context, question)
            results.append({
                'context': context[:100] + "..." if len(context) > 100 else context,
                'question': question,
                'answer': result
            })
        return results

# Sử dụng
api = ViQwenRAGAPI("your_hf_token")

# Single query
context = """
RAG (Retrieval-Augmented Generation) là kỹ thuật kết hợp giữa việc truy xuất thông tin 
và mô hình ngôn ngữ lớn để tạo ra câu trả lời chính xác hơn. RAG giúp mô hình AI 
truy cập thông tin từ cơ sở dữ liệu bên ngoài thay vì chỉ dựa vào kiến thức đã học.
"""

question = "RAG là gì và có ích lợi gì?"
answer = api.query(context, question, temperature=0.05)
print(f"Câu hỏi: {question}")
print(f"Trả lời: {answer}")
```

## **3. Streaming Response cho Real-time**

```python
import sseclient
import requests
import json

class ViQwenRAGStreaming:
    def __init__(self, hf_token):
        self.hf_token = hf_token
        self.api_url = "https://api-inference.huggingface.co/models/AITeamVN/Vi-Qwen2-3B-RAG"
        self.headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
    
    def stream_query(self, context, question, **kwargs):
        """
        Streaming response for real-time output
        """
        template = '''Chú ý các yêu cầu sau:
- Câu trả lời phải chính xác và đầy đủ nếu ngữ cảnh có câu trả lời. 
- Chỉ sử dụng các thông tin có trong ngữ cảnh được cung cấp.
- Chỉ cần từ chối trả lời và không suy luận gì thêm nếu ngữ cảnh không có câu trả lời.
Hãy trả lời câu hỏi dựa trên ngữ cảnh:
### Ngữ cảnh :
{context}

### Câu hỏi :
{question}

### Trả lời :'''
        
        payload = {
            "inputs": template.format(context=context, question=question),
            "parameters": {
                "max_new_tokens": kwargs.get('max_tokens', 2048),
                "temperature": kwargs.get('temperature', 0.1),
                "stream": True
            }
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json=payload, 
                stream=True
            )
            response.raise_for_status()
            
            # Process streaming response
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'token' in data:
                            yield data['token']['text']
                    except:
                        continue
                        
        except Exception as e:
            yield f"Streaming error: {str(e)}"

# Sử dụng streaming
streaming_api = ViQwenRAGStreaming("your_hf_token")

context = "Hà Nội là thủ đô của Việt Nam, có diện tích 3.359 km² và dân số khoảng 8 triệu người."
question = "Hà Nội có diện tích bao nhiêu?"

print("Streaming response:")
full_response = ""
for token in streaming_api.stream_query(context, question):
    print(token, end="", flush=True)
    full_response += token
print("\n\nFull response:", full_response)
```

## **4. RAG Pipeline hoàn chỉnh**

```python
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class VietnameseRAGPipeline:
    def __init__(self, hf_token, embedding_model="dangvantuan/vietnamese-embedding"):
        self.api = ViQwenRAGAPI(hf_token)
        self.embedder = SentenceTransformer(embedding_model)
        self.documents = []
        self.document_embeddings = None
        self.index = None
    
    def add_documents(self, documents):
        """
        Add documents to the knowledge base
        """
        self.documents.extend(documents)
        
        # Create embeddings
        embeddings = self.embedder.encode(documents)
        
        if self.document_embeddings is None:
            self.document_embeddings = embeddings
        else:
            self.document_embeddings = np.vstack([self.document_embeddings, embeddings])
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.document_embeddings)
        self.index.add(self.document_embeddings.astype('float32'))
    
    def retrieve_context(self, question, top_k=3):
        """
        Retrieve relevant documents for the question
        """
        if self.index is None:
            return ""
        
        # Encode question
        question_embedding = self.embedder.encode([question])
        faiss.normalize_L2(question_embedding)
        
        # Search
        scores, indices = self.index.search(question_embedding.astype('float32'), top_k)
        
        # Get relevant documents
        relevant_docs = []
        for i, idx in enumerate(indices[0]):
            if scores[0][i] > 0.3:  # Threshold for relevance
                relevant_docs.append(self.documents[idx])
        
        return "\n\n".join(relevant_docs)
    
    def answer_question(self, question, **kwargs):
        """
        Complete RAG pipeline: retrieve + generate
        """
        # Retrieve relevant context
        context = self.retrieve_context(question, top_k=kwargs.get('top_k', 3))
        
        if not context.strip():
            return "Xin lỗi, tôi không tìm thấy thông tin liên quan để trả lời câu hỏi này."
        
        # Generate answer
        answer = self.api.query(context, question, **kwargs)
        
        return {
            'question': question,
            'context': context,
            'answer': answer,
            'context_length': len(context.split())
        }

# Sử dụng RAG Pipeline
rag = VietnameseRAGPipeline("your_hf_token")

# Add knowledge base
documents = [
    "Việt Nam có 63 tỉnh thành, bao gồm 58 tỉnh và 5 thành phố trực thuộc trung ương.",
    "Thủ đô Hà Nội có diện tích 3.359 km² và dân số khoảng 8 triệu người.",
    "Thành phố Hồ Chí Minh là thành phố lớn nhất Việt Nam với dân số khoảng 9 triệu người.",
    "Việt Nam xuất khẩu chủ yếu gạo, cà phê, cao su và hải sản.",
    "Đồng Việt Nam (VND) là đơn vị tiền tệ chính thức của Việt Nam."
]

rag.add_documents(documents)

# Query
result = rag.answer_question("Việt Nam có bao nhiêu tỉnh thành?")
print(f"Câu hỏi: {result['question']}")
print(f"Context: {result['context']}")
print(f"Trả lời: {result['answer']}")
```

## **5. Error Handling và Rate Limiting**

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    """
    Rate limiting decorator for API calls
    """
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

class RobustViQwenRAG:
    def __init__(self, hf_token, max_retries=3):
        self.api = ViQwenRAGAPI(hf_token)
        self.max_retries = max_retries
    
    @rate_limit(calls_per_minute=50)  # Stay under rate limit
    def safe_query(self, context, question, **kwargs):
        """
        Query with retry logic and error handling
        """
        for attempt in range(self.max_retries):
            try:
                result = self.api.query(context, question, **kwargs)
                
                # Check if result indicates an error
                if result.startswith("Error:") or result.startswith("API Error:"):
                    if attempt == self.max_retries - 1:
                        return result
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                
                return result
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"Failed after {self.max_retries} attempts: {str(e)}"
                time.sleep(2 ** attempt)
        
        return "Maximum retries exceeded"

# Sử dụng
robust_api = RobustViQwenRAG("your_hf_token")
result = robust_api.safe_query(context, question)
print(result)
```

## **Setup Token Hugging Face**

1. Truy cập: https://huggingface.co/settings/tokens
2. Tạo token mới với quyền "Read"
3. Copy token và thay thế vào code

## **Rate Limits**

- **Free**: 300 requests/hour
- **Pro ($10/month)**: 1000 requests/hour + premium models
- **Enterprise**: Custom limits

Với code này bạn có thể tích hợp Vi-Qwen2-3B-RAG vào ứng dụng một cách hiệu quả và robust!


---


Đây là code đã được sửa đổi để tích hợp Vi-Qwen2-3B-RAG vào class AnswerGenerator hiện tại:

```python
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

# Vietnamese system prompt for Vi-Qwen2 models
VIETNAMESE_SYSTEM_PROMPT = """Bạn là một trợ lí Tiếng Việt nhiệt tình và trung thực. Hãy luôn trả lời một cách hữu ích nhất có thể."""

class ViQwenRAGProvider:
    """Provider for Vi-Qwen2-RAG models via Hugging Face API"""
    
    def __init__(self, model_name: str, hf_token: str):
        self.model_name = model_name
        self.hf_token = hf_token
        self.client = InferenceClient(token=hf_token)
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json"
        }
    
    def generate_completion(self, messages: List[Dict], **kwargs):
        """Generate completion using Vi-Qwen2-RAG model"""
        try:
            # Try using chat completion first
            response = self.client.chat_completion(
                messages=messages,
                model=self.model_name,
                max_tokens=kwargs.get('max_tokens', 2048),
                temperature=kwargs.get('temperature', 0.1),
                stream=False
            )
            return response.choices[0].message.content
        except:
            # Fallback to direct API call
            return self._direct_api_call(messages, **kwargs)
    
    def _direct_api_call(self, messages: List[Dict], **kwargs):
        """Direct API call as fallback"""
        # Combine messages into single prompt
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt = msg["content"] + "\n\n"
            elif msg["role"] == "user":
                prompt += msg["content"]
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": kwargs.get('max_tokens', 2048),
                "temperature": kwargs.get('temperature', 0.1),
                "top_p": kwargs.get('top_p', 0.9),
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '').strip()
            else:
                return "No response generated"
                
        except Exception as e:
            return f"API Error: {str(e)}"

class AnswerGenerator:
    """
    A class that helps generate answers using OpenAI models or Vi-Qwen2-RAG.
    
    This class can:
    - Combine documents with questions
    - Use OpenAI models or Vi-Qwen2-RAG to generate answers
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
        
        Args:
            model_name: Name of the model to use (OpenAI or Vi-Qwen2-RAG)
            temperature: How creative the answers should be (0.0 to 1.0)
            max_tokens: Maximum number of tokens in the response
            system_prompt: System prompt to guide the model's behavior
            
        Example:
            >>> generator = AnswerGenerator(model_name="gpt-4")
            >>> answer = generator.generate_answer("What is RAG?", documents)
            >>> 
            >>> # For Vietnamese RAG
            >>> generator = AnswerGenerator(model_name="AITeamVN/Vi-Qwen2-3B-RAG")
            >>> answer = generator.generate_answer("RAG là gì?", documents)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Check if it's a Vi-Qwen2 model
        self.is_vi_qwen = "Vi-Qwen2" in model_name or "vi-qwen2" in model_name.lower()
        
        # Set appropriate system prompt
        if system_prompt is None:
            self.system_prompt = VIETNAMESE_SYSTEM_PROMPT if self.is_vi_qwen else DEFAULT_SYSTEM_PROMPT
        else:
            self.system_prompt = system_prompt
            
        # Initialize appropriate client
        if self.is_vi_qwen:
            hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
            if not hf_token:
                raise ValueError("HF_TOKEN or HUGGINGFACE_TOKEN environment variable is required for Vi-Qwen2 models")
            self.provider = ViQwenRAGProvider(model_name, hf_token)
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
    
    def format_context(self, documents: List[Document]) -> str:
        """
        Combine documents into a single context string.
        
        Args:
            documents: List of documents to combine
            
        Returns:
            Combined context as a string
        """
        return "\n\n".join(doc.page_content for doc in documents)
    
    def _create_vi_qwen_prompt(self, question: str, context: str) -> str:
        """Create RAG prompt for Vi-Qwen2 models"""
        template = '''Chú ý các yêu cầu sau:
- Câu trả lời phải chính xác và đầy đủ nếu ngữ cảnh có câu trả lời. 
- Chỉ sử dụng các thông tin có trong ngữ cảnh được cung cấp.
- Chỉ cần từ chối trả lời và không suy luận gì thêm nếu ngữ cảnh không có câu trả lời.
Hãy trả lời câu hỏi dựa trên ngữ cảnh:
### Ngữ cảnh :
{context}

### Câu hỏi :
{question}

### Trả lời :'''
        
        return template.format(context=context, question=question)
    
    def generate_answer(
        self,
        question: str,
        documents: List[Document],
        format_context: bool = True
    ) -> str:
        """
        Generate an answer using the specified model.
        
        Args:
            question: The question to answer
            documents: List of relevant documents
            format_context: Whether to format the context (default: True)
            
        Returns:
            The generated answer
            
        Example:
            >>> answer = generator.generate_answer("What is RAG?", documents)
            >>> print(f"Generated answer: {answer}")
        """
        if format_context:
            context = self.format_context(documents)
        else:
            context = documents[0].page_content if documents else ""
            
        if self.is_vi_qwen:
            # Use Vi-Qwen2-RAG specific prompt format
            prompt = self._create_vi_qwen_prompt(question, context)
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
        """
        Generate an answer with source information.
        
        Args:
            question: The question to answer
            documents: List of relevant documents
            
        Returns:
            Dictionary with answer and sources
        """
        answer = self.generate_answer(question, documents)
        
        # Extract sources from document metadata
        sources = []
        for doc in documents:
            if "source" in doc.metadata:
                sources.append(doc.metadata["source"])
                
        return {
            "answer": answer,
            "sources": list(set(sources))  # Remove duplicates
        }

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="RAG Answer Generator with multiple model support")
    parser.add_argument(
        "--model", 
        type=str, 
        default="gpt-4o-mini",
        help="Model to use (e.g., gpt-4o-mini, gpt-4, AITeamVN/Vi-Qwen2-3B-RAG, AITeamVN/Vi-Qwen2-1.5B-RAG)"
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
    This part runs when you run this file directly.
    It shows examples of how to use the AnswerGenerator class.
    
    Usage examples:
    python answer_generator.py --model gpt-4o-mini --question "What is RAG?"
    python answer_generator.py --model AITeamVN/Vi-Qwen2-3B-RAG --question "RAG là gì?"
    python answer_generator.py --model AITeamVN/Vi-Qwen2-1.5B-RAG --temperature 0.1
    """
    from langchain_core.documents import Document
    
    # Parse command line arguments
    args = parse_arguments()
    
    print(f"Using model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Max tokens: {args.max_tokens}")
    
    # Create sample documents
    if "Vi-Qwen2" in args.model or args.language == "vi":
        # Vietnamese documents
        sample_docs = [
            Document(
                page_content="RAG là viết tắt của Retrieval-Augmented Generation. Đây là kỹ thuật kết hợp việc truy xuất tài liệu liên quan với việc tạo sinh ngôn ngữ tự nhiên.",
                metadata={"source": "test1_vi"}
            ),
            Document(
                page_content="RAG giúp các mô hình ngôn ngữ cung cấp câu trả lời chính xác và cập nhật hơn bằng cách sử dụng kiến thức từ bên ngoài.",
                metadata={"source": "test2_vi"}
            )
        ]
        default_question = "RAG là gì và có lợi ích gì?"
    else:
        # English documents
        sample_docs = [
            Document(
                page_content="RAG stands for Retrieval-Augmented Generation. It combines retrieval of relevant documents with language model generation.",
                metadata={"source": "test1"}
            ),
            Document(
                page_content="RAG helps language models provide more accurate and up-to-date answers by using external knowledge.",
                metadata={"source": "test2"}
            )
        ]
        default_question = "What is RAG?"
    
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
        print(f"Generated answer: {answer}")
    except Exception as e:
        print(f"Basic generation test failed: {e}")
    
    # Test answer with sources
    print(f"\nTesting answer with sources...")
    try:
        result = answer_gen.generate_answer_with_sources(question, sample_docs)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
    except Exception as e:
        print(f"Source generation test failed: {e}")
    
    # Show available models
    print(f"\nAvailable models:")
    print("OpenAI models: gpt-4o-mini, gpt-4o, gpt-4, gpt-3.5-turbo")
    print("Vietnamese RAG models: AITeamVN/Vi-Qwen2-1.5B-RAG, AITeamVN/Vi-Qwen2-3B-RAG")
    
    # Show usage examples
    print(f"\nUsage examples:")
    print("python answer_generator.py --model gpt-4o-mini --question 'What is machine learning?'")
    print("python answer_generator.py --model AITeamVN/Vi-Qwen2-3B-RAG --question 'Machine learning là gì?'")
    print("python answer_generator.py --model AITeamVN/Vi-Qwen2-1.5B-RAG --temperature 0.1 --max-tokens 2048")
```

## **Environment Variables cần thiết**

Tạo file `.env`:

```bash
# For OpenAI models
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_PROXY=http://your_proxy:port  # Optional

# For Vi-Qwen2 models (required when using Vietnamese models)
HF_TOKEN=your_huggingface_token_here
# or
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

## **Cách sử dụng từ command line:**

```bash
# Sử dụng GPT-4o-mini (mặc định)
python answer_generator.py

# Sử dụng GPT-4o-mini với câu hỏi cụ thể
python answer_generator.py --model gpt-4o-mini --question "What is RAG?"

# Sử dụng Vi-Qwen2-3B-RAG cho tiếng Việt
python answer_generator.py --model AITeamVN/Vi-Qwen2-3B-RAG --question "RAG là gì?"

# Sử dụng Vi-Qwen2-1.5B-RAG với tham số tùy chỉnh
python answer_generator.py --model AITeamVN/Vi-Qwen2-1.5B-RAG --temperature 0.1 --max-tokens 2048

# Sử dụng GPT-4 với nhiệt độ cao hơn
python answer_generator.py --model gpt-4 --temperature 0.5 --question "Explain quantum computing"
```

## **Cách sử dụng trong code khác:**

```python
from answer_generator import AnswerGenerator

# Sử dụng Vi-Qwen2-3B-RAG
generator = AnswerGenerator(model_name="AITeamVN/Vi-Qwen2-3B-RAG")
answer = generator.generate_answer("RAG là gì?", documents)

# Sử dụng GPT-4o-mini
generator = AnswerGenerator(model_name="gpt-4o-mini")
answer = generator.generate_answer("What is RAG?", documents)
```

## **Tính năng chính:**

1. **Tự động phát hiện model**: Code tự động nhận biết model Vi-Qwen2 và sử dụng prompt format phù hợp
2. **Command line arguments**: Dễ dàng thay đổi model và tham số từ terminal
3. **Multilingual support**: Tự động chọn ngôn ngữ phù hợp với model
4. **Error handling**: Xử lý lỗi robust cho cả OpenAI và Hugging Face API
5. **Fallback mechanism**: Có cơ chế dự phòng khi API chính gặp lỗi

Code này giữ nguyên structure gốc nhưng thêm khả năng sử dụng Vi-Qwen2-RAG models qua command line arguments!