draft ngắn gọn các step cần làm 
1. Dựng DB 
2. Triển xây Graph 
- Từ 1 file excel có 3 cột: doc_id	title	text
+, sử dụng LLMs: Qwen/Qwen2.5-7B-Instruct

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="together",
    api_key="hf_xxxxxxxxxxxxxxxxxxxxxxxx",
)

completion = client.chat.completions.create(
    model="Qwen/Qwen2.5-7B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
)

print(completion.choices[0].message)
```

Sử dụng model này để Open Informatin Extraction để extract ra bộ 3: Triples: Subject Indicate Object -> lưu node Phrase node 

\section{Offline Indexing – Giai đoạn Xây dựng Bộ nhớ}

Trong giai đoạn Offline Indexing, nhiệm vụ chính là xây dựng hệ thống bộ nhớ dài hạn bằng cách tạo ra một Đồ thị Tri thức (Knowledge Graph - KG) từ các tài liệu văn bản. Giai đoạn này đóng vai trò nền tảng cho toàn bộ hệ thống được đề xuất, quyết định chất lượng và hiệu quả của các hoạt động truy xuất trong tương lai. Các module trong giai đoạn này làm việc cùng nhau để trích xuất, xử lý và tổ chức thông tin một cách có cấu trúc, tạo ra một biểu diễn tri thức phong phú và linh hoạt có thể được truy xuất hiệu quả trong giai đoạn Online.

Trong pha offline này, nghiên cứu xây dựng đồ thị gồm 2 node: phrase node and passages node 

2 node: Phrase Node, Passage Node (Phrase node gồm Subject and Object). 
3 Cạnh: Relation Edge (giữa 2 phrase node), synonym edge (giữa 2 phrase node), contain Edge (giữa Passage và Phrase node của nó)

\subsection{Module 1: Phân đoạn Tài liệu}

\subsubsection{Diễn giải chi tiết Module}
Phân đoạn tài liệu là bước đầu tiên và quan trọng trong quá trình xây dựng bộ nhớ, nhằm chia nhỏ tài liệu gốc thành các đoạn ngắn hơn, mỗi đoạn mang một ý nghĩa logic riêng biệt. Hệ thống được đề xuất sử dụng các Mô hình Ngôn ngữ Lớn (LLM), cụ thể là Qwen-1.5B-Instruct, để thực hiện nhiệm vụ này với độ chính xác cao. Quá trình phân đoạn bắt đầu bằng việc LLM phân tích cấu trúc tổng thể của tài liệu, xác định các phần, chương, đoạn và các đơn vị tổ chức khác. Tiếp theo, thay vì chỉ dựa vào dấu chấm câu hoặc số từ cố định, LLM xác định ranh giới dựa trên sự thay đổi chủ đề, ý tưởng hoặc ngữ cảnh. Mỗi đoạn được tạo ra có độ dài vừa đủ để mang một ý nghĩa hoàn chỉnh nhưng không quá dài để gây khó khăn cho việc xử lý tiếp theo. Quan trọng nhất, quá trình này đảm bảo rằng mỗi đoạn vẫn giữ được đủ ngữ cảnh để có thể hiểu độc lập, ngay cả khi được tách khỏi tài liệu gốc.

Phân đoạn tài liệu đóng vai trò quan trọng vì nhiều lý do. Các đoạn có kích thước phù hợp và mạch lạc về mặt ngữ nghĩa giúp quá trình trích xuất triple trong bước tiếp theo hiệu quả hơn. Nó đảm bảo rằng thông tin ngữ cảnh quan trọng không bị mất khi chia nhỏ tài liệu. Các đoạn được phân chia tốt sẽ dễ dàng được truy xuất chính xác hơn khi cần thiết. Việc phân đoạn cũng giúp loại bỏ thông tin thừa hoặc không liên quan, tập trung vào nội dung quan trọng. So với các phương pháp phân đoạn truyền thống dựa trên quy tắc cố định, phương pháp sử dụng LLM của hệ thống được đề xuất mang lại những lợi thế đáng kể. Nó nhận thức được ngữ cảnh và ý nghĩa của văn bản, không chỉ cấu trúc bề mặt, từ đó tạo ra các đoạn có tính mạch lạc cao hơn về mặt ngữ nghĩa. Phương pháp này cũng thích ứng tốt với các loại tài liệu và phong cách viết khác nhau, đồng thời giảm thiểu việc cắt đứt các ý tưởng hoặc khái niệm liên quan. 

\subsubsection{Ví dụ minh họa}
Xét một đoạn văn bản y khoa dài về bệnh tiểu đường:

\begin{quote}
"Bệnh tiểu đường là một rối loạn chuyển hóa mạn tính đặc trưng bởi lượng đường trong máu cao (tăng đường huyết). Có nhiều loại tiểu đường khác nhau, nhưng phổ biến nhất là tiểu đường type 1 và type 2. Tiểu đường type 1 xảy ra khi hệ miễn dịch tấn công và phá hủy các tế bào beta trong tuyến tụy, dẫn đến thiếu hụt insulin. Tiểu đường type 2 bắt đầu với kháng insulin, một tình trạng mà các tế bào không phản ứng đúng với insulin. Metformin thường được sử dụng như liệu pháp đầu tay cho bệnh nhân tiểu đường type 2. Thuốc này hoạt động bằng cách giảm sản xuất glucose ở gan và tăng độ nhạy insulin của các tế bào cơ thể."
\end{quote}

Phương pháp phân đoạn truyền thống có thể đơn giản chia đoạn này thành hai phần dựa trên số câu hoặc số từ. Tuy nhiên, hệ thống được đề xuất sẽ phân tích ngữ nghĩa và tạo ra các đoạn như sau:

\begin{quote}
Đoạn 1: "Bệnh tiểu đường là một rối loạn chuyển hóa mạn tính đặc trưng bởi lượng đường trong máu cao (tăng đường huyết). Có nhiều loại tiểu đường khác nhau, nhưng phổ biến nhất là tiểu đường type 1 và type 2."

Đoạn 2: "Tiểu đường type 1 xảy ra khi hệ miễn dịch tấn công và phá hủy các tế bào beta trong tuyến tụy, dẫn đến thiếu hụt insulin. Tiểu đường type 2 bắt đầu với kháng insulin, một tình trạng mà các tế bào không phản ứng đúng với insulin."

Đoạn 3: "Metformin thường được sử dụng như liệu pháp đầu tay cho bệnh nhân tiểu đường type 2. Thuốc này hoạt động bằng cách giảm sản xuất glucose ở gan và tăng độ nhạy insulin của các tế bào cơ thể."
\end{quote}

Mỗi đoạn đều mang một chủ đề logic riêng biệt: giới thiệu chung về bệnh tiểu đường, các loại tiểu đường, và phương pháp điều trị bằng Metformin.

\subsection{Module 2: OpenIE by LLM (Trích xuất Triple)}

\subsubsection{Diễn giải chi tiết Module}

Mục đích của module này là extract triples 

Trong nghiên cứu này, các paragraph đã đủ đơn giản nên được giữ nguyên. Sau khi có các đoạn paragraph ngắn gọn, ta chuyển đến bước: OpenIE by LLM để extract triples. 

OpenIE là viết tắt của Open Information Ĩntraction, hệ thống sử dụng model Qwen/Qwen2.5-7B-Instructio để trích xuất các triple từ mỗi đoạn văn đã được phân đoạn ở bước trước. Quá trình này chuyển đổi văn bản phi cấu trúc thành kiến thức có cấu trúc có để tích hợp vào đồ thị tri thức. việc lựa chọn model Qwen là đủ dùng vì ... 
Quy trình trích xuất triple bắt đầu bằng việc LLM phân tích ngữ nghĩa của đoạn văn để xác định các sự kiện và mối quan hệ chính. Từ mỗi sự kiện hoặc mối quan hệ, LLM tạo ra các triple có dạng (subject, relation, object). Các triple này sau đó được chuẩn hóa để đảm bảo tính nhất quán và dễ xử lý. Cuối cùng, mỗi triple tạo ra hai Phrase Node (subject và object) và một Relation Edge (có hướng từ subject đến object) trong đồ thị tri thức. Hệ thống sử dụng phương pháp "schema-less open KG", cho phép trích xuất bất kỳ loại quan hệ nào mà không bị giới hạn bởi một schema cố định, khác biệt so với các hệ thống KG truyền thống.

Việc sử dụng LLM để trích xuất triple mang lại nhiều lợi thế. LLM có khả năng hiểu ngữ cảnh và trích xuất các mối quan hệ phức tạp. Phương pháp "schema-less" cho phép biểu diễn đa dạng thông tin và làm cho KG linh hoạt, dễ mở rộng. LLM cũng có thể hiểu và trích xuất các mối quan hệ tinh tế và ngữ cảnh phụ thuộc. So với các phương pháp truyền thống, phương pháp này có độ chính xác cao hơn, khả năng xử lý văn bản phức tạp tốt hơn, không cần quy tắc thủ công và có khả năng thích ứng cao.

\subsubsection{Ví dụ minh họa}
Xét đoạn văn sau về Metformin:

\begin{quote}
"Metformin thường được sử dụng như liệu pháp đầu tay cho bệnh nhân tiểu đường type 2. Thuốc này hoạt động bằng cách giảm sản xuất glucose ở gan và tăng độ nhạy insulin của các tế bào cơ thể. Tác dụng phụ phổ biến bao gồm buồn nôn, tiêu chảy và đau bụng. Trong một số trường hợp hiếm gặp, Metformin có thể gây ra tình trạng nhiễm axit lactic nghiêm trọng."
\end{quote}

Module OpenIE by LLM sẽ trích xuất các triple như: ("Metformin", "được sử dụng cho", "bệnh nhân tiểu đường type 2"), ("Metformin", "hoạt động bằng cách", "giảm sản xuất glucose ở gan"), ("Metformin", "hoạt động bằng cách", "tăng độ nhạy insulin"), ("Metformin", "có tác dụng phụ", "buồn nôn"), ("Metformin", "có tác dụng phụ", "tiêu chảy"), ("Metformin", "có tác dụng phụ", "đau bụng"), ("Metformin", "có thể gây ra", "nhiễm axit lactic"), ("Nhiễm axit lactic", "là", "nghiêm trọng"), và ("Nhiễm axit lactic", "xảy ra trong", "trường hợp hiếm gặp"). Mỗi triple này sẽ tạo ra các node và edge tương ứng trong đồ thị tri thức. Ví dụ, triple đầu tiên sẽ tạo ra hai Phrase Node ("Metformin" và "bệnh nhân tiểu đường type 2") và một Relation Edge "được sử dụng cho" từ node "Metformin" đến node "bệnh nhân tiểu đường type 2".

\subsection{Module 3: Synonym Detection by Embedding}

\subsubsection{Diễn giải chi tiết Module}
Sau khi trích xuất triple, module Synonym Detection sử dụng các kỹ thuật embedding để phát hiện các từ và cụm từ đồng nghĩa trong đồ thị tri thức, giải quyết thách thức về sự đa dạng trong cách diễn đạt cùng một khái niệm. Model embedding được sử dụng ở đây là: sentence-transformers/paraphrase-multilingual-mpnet-base-v2, lý do model đủ khả năng xử lý cho data tiếng việt trong nghiên cứu. 
Quy trình bắt đầu bằng việc tạo embedding cho mỗi Phrase Node, sử dụng các mô hình như Word2Vec, GloVe, hoặc BERT. Sau đó, độ tương đồng cosine giữa các embedding của các Phrase Node khác nhau được tính toán: $\text{similarity}(A, B) = \frac{A \cdot B}{||A|| \cdot ||B||}$. Khi độ tương đồng giữa hai node vượt quá ngưỡng được định nghĩa trước (thường là 0.85-0.95), một Synonym Edge không có hướng được tạo ra để kết nối chúng.

Module này mang lại nhiều lợi ích. Nó khắc phục sự đa dạng ngôn ngữ, giúp hệ thống nhận diện các cách diễn đạt khác nhau của cùng một khái niệm. Nó kết nối thông tin phân tán bằng cách tạo liên kết giữa thông tin tương tự nhau. Điều này cải thiện khả năng truy xuất, tăng độ bao phủ của kết quả. Nó còn có thể hỗ trợ đa ngôn ngữ. So với từ điển đồng nghĩa cố định, phương pháp dựa trên embedding phát hiện mối quan hệ ngữ nghĩa thực tế, có khả năng thích ứng với từ mới, xử lý ngữ cảnh tốt hơn và cho phép điều chỉnh độ chính xác.

\subsubsection{Ví dụ minh họa}
Xét các Phrase Node sau: "Metformin", "Glucophage" (tên thương mại), "tiểu đường type 2", "đái tháo đường type 2", "bệnh tiểu đường loại 2", và "T2DM". Module Synonym Detection tính toán độ tương đồng. Giả sử similarity("Metformin", "Glucophage") = 0.92, similarity("tiểu đường type 2", "đái tháo đường type 2") = 0.95, similarity("tiểu đường type 2", "bệnh tiểu đường loại 2") = 0.91, và similarity("tiểu đường type 2", "T2DM") = 0.88, trong khi similarity("Metformin", "tiểu đường type 2") = 0.45. Với ngưỡng 0.85, hệ thống sẽ tạo Synonym Edge kết nối "Metformin" với "Glucophage", và kết nối "tiểu đường type 2" với "đái tháo đường type 2", "bệnh tiểu đường loại 2", và "T2DM".

(chi tiết hơn ví dụ) 

\subsection{Module 4: Connect Phrase Node with Passage Node}

\subsubsection{Diễn giải chi tiết Module}
Module kết hợp hai loại node trong đồ thị tri thức: Module được thiết kế dựa trên nguyên lý thiết kế Phrase node (mã hóa thưa thớt - sparse coding) và Passage node (mã hóa dày đặc - dense coding). Sự tích hợp này giải quyết sự đánh đổi giữa độ chính xác khái niệm và sự phong phú về ngữ cảnh. Quy trình tích hợp bắt đầu bằng việc tạo Phrase Node cho mỗi subject và object từ các triple, biểu diễn thông tin ở định dạng thưa thớt. Đồng thời, mỗi đoạn văn gốc trở thành một Passage Node, lưu trữ toàn bộ ngữ cảnh. Sau đó, các Context Edge có nhãn "contains" được tạo ra, có hướng từ Passage Node đến Phrase Node. Cuối cùng, cả hai loại node và các cạnh kết nối được tích hợp vào cùng một đồ thị tri thức.

Thiết kế này cân bằng giữa hiệu quả và độ chính xác: mã hóa thưa thớt hiệu quả về lưu trữ và suy luận nhanh, trong khi mã hóa dày đặc bảo toàn ngữ cảnh đầy đủ. Nó khắc phục hạn chế của các phương pháp trước đây vốn tập trung vào thực thể và bỏ qua tín hiệu ngữ cảnh. Sự kết hợp này cải thiện khả năng truy xuất và hỗ trợ suy luận đa cấp độ. So với các phương pháp khác, nó tương đồng với bộ nhớ con người, linh hoạt trong truy vấn, cân bằng tốc độ và độ chính xác, và có khả năng mở rộng.

\subsubsection{Ví dụ minh họa}
Xét đoạn văn: "Metformin thường được sử dụng như liệu pháp đầu tay cho bệnh nhân tiểu đường type 2. Tác dụng phụ phổ biến bao gồm buồn nôn và đau bụng." Từ các triple đã trích xuất: ("Metformin", "được sử dụng cho", "bệnh nhân tiểu đường type 2"), ("Metformin", "có tác dụng phụ", "buồn nôn"), và ("Metformin", "có tác dụng phụ", "đau bụng"). Module Dense-Sparse Integration sẽ tạo ra các Phrase Node ("Metformin", "bệnh nhân tiểu đường type 2", "buồn nôn", "đau bụng"), một Passage Node chứa toàn bộ đoạn văn, và các Context Edge từ Passage Node đến mỗi Phrase Node với nhãn "contains".

\subsection{Tổng kết Giai đoạn Offline Indexing}

Giai đoạn Offline Indexing trong hệ thống được đề xuất tạo ra một đồ thị tri thức phong phú và linh hoạt thông qua bốn module chính: Phân đoạn Tài liệu, OpenIE by LLM, Synonym Detection, và Dense-Sparse Integration. Phân đoạn Tài liệu tạo ra các đoạn văn có ý nghĩa logic. OpenIE by LLM chuyển đổi văn bản thành kiến thức có cấu trúc dưới dạng triple. Synonym Detection kết nối các khái niệm đồng nghĩa. Connect Phrase Node with Passage Node kết hợp thông tin cô đọng và thông tin ngữ cảnh đầy đủ. Kết quả là một đồ thị tri thức toàn diện, sẵn sàng cho việc truy xuất hiệu quả trong giai đoạn Online, hỗ trợ suy luận và truy xuất thông tin phức tạp. Việc mở rộng và tinh chỉnh cho dữ liệu tiếng Việt đã cải thiện đáng kể hiệu suất hệ thống.



=======

1. Dựng DB 
2. Code section offline này trước. 
- Trước khi code tôi muốn hỏi bạn là pha offline này nên chia nhỏ thành các file không hay 1 file? 

Nếu thành 1 file cho gọn cũng oke 
Nếu refactor thành nhiều file thì bạn code theo 4 modules của section 1 

cùng tôi phân tích ưu và nhược của 2 cách trước khi code

----



# 🎯 **DRAFT PLAN - GraphRAG với Neo4j**

## 📋 **QUICK STEPS OVERVIEW**

### **🔧 Step 1: Dựng Database**
```bash
# Docker setup Neo4j
docker-compose up -d neo4j
# Access: http://localhost:7474
```

### **🏗️ Step 2: Offline Pipeline (4 Modules)**
```
Excel (doc_id, title, text) → Module 1-4 → Neo4j Graph
```

---

## 📁 **OFFLINE PIPELINE ARCHITECTURE**

### **📊 Input Data Structure:**
```python
# Excel với 3 cột:
df = pd.read_excel("data.xlsx")
# Columns: ['doc_id', 'title', 'text']
```

### **🧠 LLM Setup (Qwen2.5-7B):**
```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="together", 
    api_key="hf_xxxxxxxxxxxxxxxxxxxxxxxx"
)

def extract_triples(text):
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct",
        messages=[{"role": "user", "content": prompt}]
    )
    return parse_triples(completion.choices[0].message)
```

---

## 🗂️ **CODE STRUCTURE OPTIONS**

### **🎯 Option 1: Single File (offline_pipeline.py)**

#### **✅ Advantages:**
- **Đơn giản**: Tất cả logic trong 1 file, dễ debug
- **Nhanh**: Prototype nhanh, ít config
- **Demo-friendly**: Dễ present cho thesis defense
- **Dependency đơn giản**: Ít import, ít lỗi

#### **❌ Disadvantages:**
- **Khó maintain**: File lớn, khó tìm function
- **Không reusable**: Khó tái sử dụng từng module
- **Testing khó**: Unit test phức tạp
- **Collaboration khó**: Multiple people edit conflict

#### **📝 Structure:**
```python
# offline_pipeline.py (single file)
class OfflinePipeline:
    def __init__(self):
        # Setup connections
        pass
    
    # Module 1: Document Segmentation (already done - keep paragraphs)
    def process_documents(self, df):
        pass
    
    # Module 2: OpenIE Triple Extraction
    def extract_triples_qwen(self, text):
        pass
    
    # Module 3: Synonym Detection
    def detect_synonyms(self, phrases):
        pass
    
    # Module 4: Connect Nodes
    def build_graph(self, documents):
        pass
```

---

### **🏗️ Option 2: Modular Files (4 files)**

#### **✅ Advantages:**
- **Clean architecture**: Mỗi module rõ ràng, dễ maintain
- **Reusable**: Có thể dùng lại từng module
- **Testable**: Unit test cho từng module
- **Scalable**: Dễ extend, optimize từng phần
- **Professional**: Chuẩn software engineering

#### **❌ Disadvantages:**
- **Phức tạp hơn**: Nhiều file, nhiều import
- **Setup time**: Cần design interface giữa modules
- **Debug khó hơn**: Lỗi có thể ở nhiều chỗ

#### **📁 Structure:**
```python
src/offline/
├── __init__.py
├── module1_document_processor.py    # (Simple - keep paragraphs)
├── module2_triple_extractor.py      # OpenIE với Qwen
├── module3_synonym_detector.py      # Embedding similarity
├── module4_graph_builder.py         # Connect nodes
└── pipeline_orchestrator.py        # Coordinate all modules
```

---

## 🤔 **ANALYSIS & RECOMMENDATION**

### **🎓 For Thesis Context:**

| Criteria | Single File | Modular Files |
|----------|-------------|---------------|
| **Demo Simplicity** | ✅ Perfect | ⚠️ Complex |
| **Code Quality** | ⚠️ Acceptable | ✅ Professional |
| **Development Speed** | ✅ Fast | ⚠️ Slower |
| **Maintainability** | ❌ Hard | ✅ Easy |
| **Testing** | ❌ Difficult | ✅ Easy |
| **Thesis Defense** | ✅ Easy to explain | ⚠️ Need architecture explanation |

### **🎯 My Recommendation: HYBRID APPROACH**

```python
# Best of both worlds:
# 1. Start với Single File cho MVP
# 2. Refactor thành Modular sau khi working

# Phase 1: Single file prototype
offline_pipeline.py  # All-in-one working version

# Phase 2: Refactor when stable  
src/offline/
├── module1_document_processor.py
├── module2_triple_extractor.py  
├── module3_synonym_detector.py
├── module4_graph_builder.py
└── pipeline.py  # Orchestrator
```

---

## 💡 **CONCRETE RECOMMENDATION**

### **🚀 Start with Option 1 (Single File) because:**

1. **Thesis timeline**: Cần working prototype nhanh
2. **Demo requirements**: Dễ present và explain
3. **Less complexity**: Focus vào algorithms, không phải architecture
4. **Faster iteration**: Debug và test nhanh hơn

### **📝 Implementation Plan:**

```python
# offline_pipeline.py
class GraphRAGOffline:
    def __init__(self):
        self.neo4j = Neo4jManager()
        self.qwen_client = InferenceClient()
        self.embedder = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    def run_pipeline(self, excel_file_path):
        """Main pipeline execution"""
        # Load data
        df = pd.read_excel(excel_file_path)
        
        # Module 1: Keep paragraphs as-is (simple)
        documents = self._prepare_documents(df)
        
        # Module 2: Extract triples with Qwen
        all_triples = self._extract_all_triples(documents)
        
        # Module 3: Detect synonyms
        synonym_mapping = self._detect_synonyms(all_triples)
        
        # Module 4: Build Neo4j graph
        self._build_graph(documents, all_triples, synonym_mapping)
        
        print("✅ Offline pipeline completed!")
    
    def _extract_all_triples(self, documents):
        """Module 2: OpenIE Triple Extraction"""
        all_triples = []
        for doc in documents:
            triples = self._extract_triples_qwen(doc['text'])
            all_triples.extend(triples)
        return all_triples
    
    def _extract_triples_qwen(self, text):
        """Use Qwen2.5-7B for OpenIE"""
        prompt = f"""
        Trích xuất tất cả các mối quan hệ từ đoạn văn sau dưới dạng (chủ thể, quan hệ, đối tượng).
        
        Đoạn văn: {text}
        
        Chỉ trả về các triple theo định dạng:
        (subject1, predicate1, object1)
        (subject2, predicate2, object2)
        """
        
        completion = self.qwen_client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        
        return self._parse_triples(completion.choices[0].message.content)
    
    # ... other methods
```

---

## ⏱️ **DEVELOPMENT TIMELINE**

### **Week 1: Single File MVP**
- ✅ Basic pipeline working
- ✅ All 4 modules implemented
- ✅ Neo4j integration
- ✅ Demo ready

### **Week 2-3: Optimization & Testing**
- ✅ Performance tuning
- ✅ Error handling
- ✅ Quality evaluation

### **Week 4: Optional Refactoring**
- 🔄 Split into modules if needed
- 🔄 Add advanced features

---

## 🤝 **DECISION**

**Let's go with Single File approach first!** 

**Reasons:**
1. ⚡ **Speed**: Get working system faster
2. 🎯 **Focus**: Concentrate on algorithms, not architecture  
3. 🎓 **Thesis-friendly**: Easier to demonstrate and explain
4. 🔄 **Flexible**: Can refactor later if needed

**Ready to code the single file `offline_pipeline.py`?** 

I'll implement all 4 modules in one clean, well-documented file that's easy to understand and demo! 🚀


----

```bash
file pipeline.py sẽ để phần test nhỏ ở main rồi nhỉ 
Thế sẽ cần 1 file run_... gì đó nữa: file này sẽ đọc file excel từ .xslx ở cùng thư mục offline luôn 

(file gồm 3 cột: doc_id	title	text  ) 

example: 
doc_id PH_0	
title PH	
text Các dung dịch nước có giá trị pH nhỏ hơn 7 được coi là có tính axít , trong khi các giá trị pH lớn hơn 7 được coi là có tính kiềm .

====
Yourr task: 
1. Hướng dẫn chi tiết cách dựng Neo4DB đã 
2. Coding các phần 

src/offline/
├── module1_document_processor.py    # (Simple - keep paragraphs)
├── module2_triple_extractor.py      # OpenIE với Qwen
├── module3_synonym_detector.py      # Embedding similarity
├── module4_graph_builder.py         # Connect nodes
└── pipeline_orchestrator.py        # Coordinate all modules
xlsx.py

Dùng pathlib cho tất cả đồng bộ 


```


Lẽ ra nên viết: để nó vẽ ra kiến trúc trước 

thành ra kết quả như này 

```bash
graphrag-thesis/
├── 🐳 docker-compose.yml              # Neo4j database setup
├── 📋 requirements.txt                # Python dependencies
├── 🌍 .env.example                    # Environment config template
├── 📖 README.md                       # Quick start guide
│
├── 📁 src/offline/                    # 🧠 CORE PIPELINE MODULES
│   ├── 📄 module1_document_processor.py    # 📖 Excel → Documents
│   ├── 🧠 module2_triple_extractor.py      # 🤖 Qwen → Triples  
│   ├── 🔗 module3_synonym_detector.py      # 🎯 Embedding → Synonyms
│   ├── 🏗️ module4_graph_builder.py         # 📊 Neo4j Graph Builder
│   ├── 🎯 pipeline_orchestrator.py         # 🎼 Coordinate All Modules
│   ├── 🔧 utils.py                         # 🛠️ Helper Functions
│   └── 📊 test_data.py                     # 🧪 Generate Test Excel
│
├── 🚀 run_offline_pipeline.py         # 🎬 MAIN EXECUTION SCRIPT
├── 🧪 test_offline_pipeline.py        # ✅ Test Complete Pipeline  
└── 🔍 test_query_functions.py         # 🔎 Verify Graph Functions
```

