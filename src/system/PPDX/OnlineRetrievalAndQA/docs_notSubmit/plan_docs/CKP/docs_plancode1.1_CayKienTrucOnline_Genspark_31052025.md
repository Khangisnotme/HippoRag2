# toàn bộ file pdf + code của phần Offline + mô tả ngắn gọn luồng Online. + Cây cấu trúc code của phần offline vào => Mục tiêu là ra cấu trúc của phần Online 

----


#### Phương pháp đề xuất (tóm tắt như sau ạ)
```bash
1. Pha offline (y nguyên HippoRAG2)
2. Pha online: 


Luồng xử lý 5 bước - Giai đoạn Online Retrieval & QA:

1. Truy xuất Kép/Lai (Dual/Hybrid Retrieval) : mục đích tận dụng Hybrid Search
Input: Truy vấn người dùng
Xử lý: Truy xuất song song từ 2 nguồn bằng BM25 + Embedding:
Passages: Lấy Top-K passages (50-100) → Raw Passages
Triples: Lấy Top-N triples (20-50) → Raw Triples
Output: Raw Passages + Raw Triples

2. Lọc Triple bằng LLM - mục đích: giữ lại triples phù hợp với truy vấn ban đầu
Input: Raw Triples + truy vấn gốc
Xử lý: LLM (Qwen2.5-7B) đánh giá và chọn facts cốt lõi nhất
Output: Filtered Triples (Top-M, khoảng 10-20 triple chất lượng cao)

3. Xếp hạng lại Passages dựa trên Triples - mục đích lọc bỏ passages nhiễu bằng cách tính score của nó với các triples
Input: Raw Passages + Filtered Triples
Xử lý:
Tính điểm hỗ trợ: đếm số triple mà mỗi passage hỗ trợ
Kết hợp điểm: Score_final = α × Score_retriever + (1-α) × Score_support
Chọn Top-P passages có điểm cao nhất
Output: Final Passages (5-10 passages tốt nhất)

Score_retriever (Điểm truy xuất ban đầu)
Điểm số từ Module 1 (kết hợp BM25 + Embedding)
Phản ánh độ liên quan ngữ nghĩa với truy vấn
Giá trị: thường từ 0-1

Score_support (Điểm hỗ trợ triple)
Đếm số lượng Filtered Triples mà passage đó hỗ trợ
Kiểm tra: passage có chứa cả subject và object của triple không?
Giá trị: số nguyên (0, 1, 2, 3...)

Score_final (Điểm cuối cùng)
Score_final = α × Score_retriever + (1-α) × Score_support

Tham số α (alpha):
α = 0.7-0.8: Ưu tiên độ liên quan ngữ nghĩa
α = 0.5: Cân bằng giữa liên quan và hỗ trợ facts
α < 0.5: Ưu tiên passages được facts hỗ trợ mạnh

Ví dụ nhanh:
Passage A: Score_retriever = 0.85, hỗ trợ 3 triples
Với α = 0.7: Score_final = 0.7×0.85 + 0.3×3 = 1.495
Passage này sẽ được ưu tiên cao vì vừa liên quan vừa được facts xác thực

4. Mở rộng Ngữ cảnh (Tùy chọn) - Mở rộng 1 hop cho Filted Triples (thay vì lan truyền rộng như PPR) 
Input: Filtered Triples
Xử lý: Tìm kiếm 1-hop trên KG để lấy thêm thông tin liên quan
Output: Expanded Context

5. Tạo Câu trả lời
Input: Truy vấn + Final Passages + Filtered Triples + Expanded Context
Xử lý:
Định dạng thành prompt có cấu trúc
Đưa vào LLM mạnh (GPT-4, Gemini Pro...) để tạo câu trả lời
Output: Câu trả lời cuối cùng cho người dùng

Đánh giá tổng quan: Mục đích chính là cải thiện vấn đề Retrieve nhờ vào:
Kết hợp ưu điểm của cả passages (ngữ cảnh phong phú) và triples (facts chính xác) => Bổ sung thông tin.
Lọc Triples => Sau đó dùng Filtered Triples để lọc Passages => Bỏ thông tin dư thừa.
Sử dụng filtered triples lan truyền 1 - hop sang các Phrase Nodes khác => Bổ sung thông tin.
```

# Chi tiết về phần 2: 


```tex
\section{Offline Indexing Phase – Building Memory}

In the \textbf{Offline Indexing} phase, the core task is to build a long-term memory system by constructing a \textbf{Knowledge Graph (KG)} from input text documents. This phase is considered the foundation for the entire proposed RAG system, critically impacting the quality and performance of future information retrieval operations (Online phase). The component modules in this phase cooperate closely to systematically and structurally extract, process, and organize information. The goal is to create a rich, diverse, and flexible knowledge representation, ready for efficient querying in the Online phase.

Specifically, in this offline phase, the research focuses on building a knowledge graph comprising two main types of \textbf{nodes}: Phrase Nodes and Passage Nodes.

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \textbf{Nodes:}
        \begin{itemize}[label=\textendash, leftmargin=*]
            \item \texttt{Phrase Node}: Represents core entities or concepts, typically the Subject or Object in an information triple.
            \item \texttt{Passage Node}: Represents an original text passage, containing the full context.
        \end{itemize}
    \item \textbf{Edges:}
        \begin{itemize}[label=\textendash, leftmargin=*]
            \item \texttt{Relation Edge}: A directed edge connecting two \texttt{Phrase Nodes} (from Subject to Object) to represent a relationship or a fact (triple). This edge\'s attributes can store information about the relation type (Predicate).
            \item \texttt{Synonym Edge}: An undirected edge connecting two \texttt{Phrase Nodes} identified as synonymous.
            \item \texttt{Contain Edge}: A directed edge connecting from a \texttt{Passage Node} to the \texttt{Phrase Nodes} (entities/concepts) that the passage contains.
        \end{itemize}
\end{itemize}

Here is a detailed description of each module in the Offline Indexing phase:

\subsection{Module 1: Document Segmentation}

\subsubsection{Detailed Explanation of the Module}

Document segmentation is an essential initial step in the memory building process. The goal of this step is to break down original text documents into shorter \textbf{passages}, where each passage should carry a relatively complete and independent logical meaning. To achieve this with high accuracy, the proposed system leverages the power of \textbf{Large Language Models (LLMs)}, specifically the \textbf{Qwen-1.5B-Instruct} model.

The segmentation process begins with the LLM deeply analyzing the overall structure of the source document. The model identifies structural components such as major sections, chapters, headings, paragraphs, and other text organizational units. A crucial difference compared to traditional methods is that the LLM does not rely solely on surface cues like punctuation or a fixed word count to segment. Instead, it identifies boundaries between passages based on changes in \textbf{topic, flow of ideas, or context} presented in the text. The result is that each generated passage is of moderate length, sufficient to contain a complete meaning, but not too long to complicate subsequent processing steps. An important requirement is that the segmentation process must ensure that each resulting passage retains enough context to be understood relatively independently, even when separated from the original text.

Effective document segmentation plays a foundational role for several reasons. First, appropriately sized and semantically coherent passages facilitate more efficient operation of the triple extraction (OpenIE) module in the next step. Second, it helps ensure that important contextual information is not lost or arbitrarily cut when documents are broken down. Third, well-segmented passages will be more easily indexed and accurately retrieved when users perform queries in the Online phase. Finally, segmentation also helps eliminate noisy or irrelevant information, helping the system focus on core and important content.

Compared to traditional segmentation methods, which often rely on fixed heuristic rules (e.g., sentence breaks, fixed word counts, special characters), the proposed system\'s LLM-based approach offers significant advantages. LLMs have a deep understanding of context and the underlying meaning of text, not just surface structure. This allows for the creation of passages with much higher semantic coherence. Moreover, this method is highly adaptable to various document types, formats, and writing styles without needing to redefine rules. It also significantly minimizes the risk of breaking up ideas, concepts, or logical relationships that are presented continuously in the original text.

\subsubsection{Illustrative Example (Fruit Topic)}

Consider the original text about the benefits of some fruits:

\begin{quote}
"Chuối là một loại trái cây phổ biến, chứa nhiều kali – một khoáng chất quan trọng giúp điều hòa huyết áp và hỗ trợ hoạt động của tim. Ngoài ra, chuối còn cung cấp năng lượng nhanh, thích hợp cho người luyện tập thể thao. Táo là nguồn chất xơ dồi dào, đặc biệt là pectin – một loại chất xơ hoà tan giúp cải thiện tiêu hoá và kiểm soát lượng đường trong máu. Vỏ táo cũng chứa nhiều chất chống oxy hoá, có thể giảm nguy cơ mắc bệnh tim mạch. Cam nổi bật với hàm lượng vitamin C cao, đóng vai trò quan trọng trong việc tăng cường hệ miễn dịch và hỗ trợ hấp thu sắt. Uống nước cam thường xuyên còn giúp cải thiện làn da và giảm mệt mỏi. Một chế độ ăn giàu trái cây không chỉ cung cấp vitamin và khoáng chất thiết yếu, mà còn hỗ trợ phòng chống nhiều bệnh mạn tính như tiểu đường, cao huyết áp và ung thư."
\end{quote}

The Document Segmentation module using LLM will analyze the semantics and identify distinct topics, creating coherent passages as follows:

\begin{quote}
\textbf{Passage 1 (P1):} "Chuối là một loại trái cây phổ biến, chứa nhiều kali – một khoáng chất quan trọng giúp điều hòa huyết áp và hỗ trợ hoạt động của tim. Ngoài ra, chuối còn cung cấp năng lượng nhanh, thích hợp cho người luyện tập thể thao."

\textit{(Topic: Information and benefits of Banana)}
\end{quote}

\begin{quote}
\textbf{Passage 2 (P2):} "Táo là nguồn chất xơ dồi dào, đặc biệt là pectin – một loại chất xơ hoà tan giúp cải thiện tiêu hoá và kiểm soát lượng đường trong máu. Vỏ táo cũng chứa nhiều chất chống oxy hoá, có thể giảm nguy cơ mắc bệnh tim mạch."

\textit{(Topic: Information and benefits of Apple)}
\end{quote}

\begin{quote}
\textbf{Passage 3 (P3):} "Cam nổi bật với hàm lượng vitamin C cao, đóng vai trò quan trọng trong việc tăng cường hệ miễn dịch và hỗ trợ hấp thu sắt. Uống nước cam thường xuyên còn giúp cải thiện làn da và giảm mệt mỏi."

\textit{(Topic: Information and benefits of Orange)}
\end{quote}

\begin{quote}
\textbf{Passage 4 (P4):} "Một chế độ ăn giàu trái cây không chỉ cung cấp vitamin và khoáng chất thiết yếu, mà còn hỗ trợ phòng chống nhiều bệnh mạn tính như tiểu đường, cao huyết áp và ung thư."

\textit{(Topic: General benefits of eating fruit)}
\end{quote}

The result is passages focused on individual fruit types or general benefits, facilitating detailed information extraction and subsequent retrieval.

\subsection{Module 2: OpenIE by LLM (Triple Extraction)}

\subsubsection{Detailed Explanation of the Module}

The main purpose of this module is to perform \textbf{Open Information Extraction (OpenIE)} to extract structured knowledge units, called \textbf{triples}, from the text passages segmented in the previous module. In this research, it is assumed that the segmented passages are simple and coherent enough for direct extraction.

Specifically, the system uses a \textbf{Large Language Model}, such as Qwen or the improved Qwen2.5-7B-Instruct, to perform the OpenIE task. This process aims to transform latent information in unstructured text into a structured, explicit knowledge form, ready for integration into the \textbf{Knowledge Graph (KG)}. The choice of a model like Qwen is considered capable and suitable for this task, balancing performance and computational cost.

The triple extraction process begins with the LLM deeply analyzing the semantics of each passage to identify key events, relationships, and attributes mentioned. For each identified event or relationship, the LLM generates one or more triples in the standard format: \texttt{(subject, relation, object)}. For example, from the sentence "Chuối chứa nhiều kali" (Banana contains a lot of potassium), the LLM can extract the triple \texttt{(Chuối, chứa, Kali)}.

After extraction, these triples often undergo a \textbf{normalization} step to ensure consistency and facilitate subsequent processing. For instance, variations of the same entity or relation can be mapped to a single canonical form. Finally, each extracted and normalized triple contributes to building the KG: the subject and object of the triple will form two \texttt{Phrase Nodes} (if they don\'t already exist), and the relation will create a directed \texttt{Relation Edge} from the subject\'s \texttt{Phrase Node} to the object\'s \texttt{Phrase Node}.

A key characteristic of the proposed system is the application of a \textbf{"schema-less open KG"} construction method. This means the system is not limited by a predefined set of relation types (schema). Instead, it can extract and represent any type of relation that the LLM discovers in the text. This approach offers high flexibility, allowing the KG to represent the diversity and richness of information in the real world, unlike traditional KG systems that often require a rigid schema.

Using LLMs for OpenIE offers significant advantages over rule-based extraction methods or traditional machine learning models. LLMs have a deep contextual understanding, allowing them to extract complex, implicit, or context-dependent relationships more accurately. The "schema-less" approach makes the KG flexible, easily extensible, and capable of integrating information from various sources. LLMs can also better handle complex sentence structures, linguistic variations, and subtle expressions that rule-based methods often miss. Overall, this method promises higher accuracy, better handling of complex text, no longer requiring costly manual rule building, and is highly adaptable to different domains and languages.

\subsubsection{Illustrative Example (Triple Extraction)}

Consider the passages segmented in Module 1:

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \textbf{Từ Passage 1 (Chuối):}
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item \texttt{(Chuối, là loại, trái cây phổ biến)}
        \item \texttt{(Chuối, chứa, Kali)}
        \item \texttt{(Kali, là, khoáng chất quan trọng)}
        \item \texttt{(Kali, giúp, điều hòa huyết áp)}
        \item \texttt{(Kali, hỗ trợ, hoạt động của tim)}
        \item \texttt{(Chuối, cung cấp, năng lượng nhanh)}
        \item \texttt{(Chuối, thích hợp cho, người luyện tập thể thao)}
    \end{itemize}
    \item \textbf{Từ Passage 2 (Táo):}
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item \texttt{(Táo, là nguồn, chất xơ)}
        \item \texttt{(Táo, chứa, Pectin)}
        \item \texttt{(Pectin, là loại, chất xơ hoà tan)}
        \item \texttt{(Pectin, giúp, cải thiện tiêu hoá)}
        \item \texttt{(Pectin, giúp, kiểm soát lượng đường trong máu)}
        \item \texttt{(Vỏ táo, chứa, chất chống oxy hoá)}
        \item \texttt{(Chất chống oxy hoá, có thể giảm nguy cơ, bệnh tim mạch)}
    \end{itemize}
    \item \textbf{Từ Passage 3 (Cam):}
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item \texttt{(Cam, nổi bật với, Vitamin C)}
        \item \texttt{(Vitamin C, đóng vai trò trong, tăng cường hệ miễn dịch)}
        \item \texttt{(Vitamin C, hỗ trợ, hấp thu sắt)}
        \item \texttt{(Uống nước cam, giúp, cải thiện làn da)}
        \item \texttt{(Uống nước cam, giúp, giảm mệt mỏi)}
    \end{itemize}
    \item \textbf{Từ Passage 4 (Lợi ích chung):}
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item \texttt{(Chế độ ăn giàu trái cây, cung cấp, vitamin)}
        \item \texttt{(Chế độ ăn giàu trái cây, cung cấp, khoáng chất)}
        \item \texttt{(Chế độ ăn giàu trái cây, hỗ trợ phòng chống, bệnh mạn tính)}
    \end{itemize}
\end{itemize}

Each of these triples will be used to create \texttt{Phrase Nodes} (e.g., "Chuối", "Kali", "Táo", "Pectin", "Cam", "Vitamin C") and \texttt{Relation Edges} (e.g., "chứa", "giúp", "là nguồn", "hỗ trợ") in the KG.


\subsection{Module 3: Synonym Detection by Embedding}

\subsubsection{Detailed Explanation of the Module}

After triples have been extracted and corresponding \texttt{Phrase Nodes} created in the knowledge graph, a challenge arises from linguistic variability: the same concept or entity can be referred to by multiple names or phrases in different parts of the document or across different documents. The \textbf{Synonym Detection} module is designed to address this problem by employing \textbf{word/sentence embedding techniques}.

The objective of this module is to automatically identify \texttt{Phrase Nodes} in the knowledge graph that represent the same concept (i.e., they are synonymous) and create \textbf{links (\texttt{Synonym Edge})} between them. The proposed system uses a powerful embedding model, for instance, \texttt{sentence-transformers/paraphrase-multilingual-mpnet-base-v2}, chosen for its effective processing of Vietnamese data and multilingual support, which is suitable for the research scope.

The operation process of this module is as follows:

\begin{enumerate}[label=\arabic*.]
    \item \textbf{Generate Embeddings:} First, the system creates an \textbf{embedding vector} (a dense numerical representation) for each \texttt{Phrase Node} in the knowledge graph. This vector is generated by feeding the text of the \texttt{Phrase Node} (e.g., "Chuối", "Táo", "Vitamin C") into the chosen embedding model (\texttt{paraphrase-multilingual-mpnet-base-v2}). This embedding vector encodes the semantic meaning of the phrase.
    \item \textbf{Calculate Similarity:} Next, the system calculates the \textbf{semantic similarity} between different pairs of \texttt{Phrase Nodes} by measuring the distance or angle between their embedding vectors. A common measure is \textbf{cosine similarity}, calculated using the formula:
    \begin{equation}
    \label{eq:cosine_similarity}
    \text{similarity}(A, B) = \frac{A \cdot B}{\|A\| \cdot \|B\|}
    \end{equation}
    Where A and B are the embedding vectors of the two \texttt{Phrase Nodes}. The cosine similarity value ranges from [-1, 1], with values closer to 1 indicating high semantic similarity.
    \item \textbf{Create Synonym Edges:} Finally, the system sets a predefined \textbf{similarity threshold} (e.g., 0.85, 0.9, or 0.95, depending on the accuracy requirements). If the cosine similarity between two \texttt{Phrase Nodes} exceeds this threshold, the system creates an \textbf{undirected \texttt{Synonym Edge}} to connect these two nodes in the knowledge graph. This edge indicates that the two nodes are considered synonymous within the system\'s context.
\end{enumerate}

Integrating the Synonym Detection module offers several significant benefits. First, it helps \textbf{overcome linguistic diversity}, allowing the system to recognize and link different expressions of the same concept. Second, it \textbf{connects scattered information} in the knowledge graph by creating logical links between similar pieces of information represented by different phrases. This directly \textbf{improves information retrieval capabilities}, increasing the recall of search results, as a query for one term can automatically expand to include synonymous terms. Furthermore, the use of multilingual embedding models like \texttt{paraphrase-multilingual-mpnet-base-v2} also opens up \textbf{multilingual processing capabilities}, allowing for the linking of similar concepts expressed in different languages (e.g., "Táo" and "Apple").

\subsubsection{Illustrative Example (Synonym)}

Suppose the KG contains the following \texttt{Phrase Nodes} with their embeddings:
\begin{itemize}[label=\textbullet, leftmargin=*]
    \item Node 1: "Táo" (Embedding Vector A)
    \item Node 2: "Apple" (Embedding Vector B)
    \item Node 3: "Chất xơ" (Embedding Vector C)
    \item Node 4: "Fiber" (Embedding Vector D)
    \item Node 5: "Chuối" (Embedding Vector E)
\end{itemize}

Calculating cosine similarity:
\begin{itemize}[label=\textbullet, leftmargin=*]
    \item similarity(A, B) = 0.96 (High similarity)
    \item similarity(C, D) = 0.94 (High similarity)
    \item similarity(A, E) = 0.15 (Low similarity)
    \item similarity(C, E) = 0.20 (Low similarity)
\end{itemize}

With a threshold of 0.9, the system creates:
\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \texttt{Synonym Edge} between "Táo" and "Apple".
    \item \texttt{Synonym Edge} between "Chất xơ" and "Fiber".
\end{itemize}

\subsection{Module 4: Dense-Sparse Integration}

\subsubsection{Detailed Explanation of the Module}

The final module in the Offline Indexing phase is \textbf{Knowledge Graph Integration (Dense-Sparse Integration)}. This module does not perform additional complex processing but focuses on \textbf{completing the structure} of the Knowledge Graph (KG) by ensuring all components created from previous modules (Passage Nodes, Phrase Nodes, Relation Edges, Synonym Edges) are logically and fully connected. In particular, this module emphasizes creating \textbf{\texttt{Contain Edge}s} to clearly link the full context (\texttt{Passage Node}) with the core concepts (\texttt{Phrase Node}) it contains.

The main process of this module includes:

\begin{enumerate}[label=\arabic*.]
    \item \textbf{Validate Existing Nodes and Edges:} The system re-checks all created components:
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item \texttt{Passage Nodes}: Representing text passages from Module 1.
        \item \texttt{Phrase Nodes}: Representing entities/concepts from Module 2.
        \item \texttt{Relation Edges}: Represent the relationships between subject and object entities as extracted in Module 2. 
        \item \texttt{Synonym Edges}: Linking synonymous Phrase Nodes from Module 3.
    \end{itemize}
    \item \textbf{Create Contain Edges:} This is the core step of this module. For each \texttt{Passage Node} $P$ and each \texttt{Phrase Node} $ph$ appearing in the original text of $P$ (usually the subject or object of triples extracted from $P$), the system will create a \textbf{directed \texttt{Contain Edge}} from $P$ to $ph$. This edge represents the "contains" or "mentions" relationship, directly linking the broad context of the passage with the specific concepts within it.
    \item \textbf{Finalize and Store KG:} Once all \texttt{Contain Edge}s have been created, the KG structure is considered complete. This graph is then stored and indexed (e.g., using a graph database like Neo4j or graph libraries like NetworkX combined with efficient storage methods) to be ready for fast querying in the Online phase.
\end{enumerate}

The creation of \texttt{Contain Edge}s provides important benefits. \textbf{Link Context and Concepts:} It creates a clear bridge between the full text representation (\texttt{Passage Node}) and the structured knowledge representation (\texttt{Phrase Nodes} and \texttt{Relation Edges}), allowing the system to easily transition between these two forms of information during retrieval and reasoning. \textbf{Support Diverse Retrieval:} When querying, the system can start from a Phrase Node (concept) and easily find all Passage Nodes (contexts) containing that concept via reverse \texttt{Contain Edge}s, or vice versa. \textbf{Foundation for Graph Algorithms:} The complete KG structure with diverse node and edge types provides a solid foundation for applying more complex graph algorithms (if needed) such as label propagation, node clustering, or variations of PageRank (like PPR in original HippoRAG) for deeper analysis and reasoning on the graph.


At the end of Module 4, the Offline Indexing phase is complete, resulting in a rich and well-structured Knowledge Graph, ready to serve complex information retrieval requests in the Online phase.

\subsubsection{Illustrative Example (KG Integration)}

Consider the components available from previous modules:

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \texttt{Passage Nodes}: P1 (Chuối), P2 (Táo), P3 (Cam), P4 (Lợi ích chung).
    \item \texttt{Phrase Nodes}: "Chuối", "Kali", "Táo", "Pectin", "Chất xơ", "Cam", "Vitamin C", "Apple", "Fiber", ...
    \item \texttt{Relation Edges}: \texttt{(Chuối, chứa, Kali)}, \texttt{(Táo, là nguồn, chất xơ)}, ...
    \item \texttt{Synonym Edges}: \texttt{(Táo, Apple)}, \texttt{(Chất xơ, Fiber)}, ...
\end{itemize}

Module 4 will focus on creating \texttt{Contain Edge}s:

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item From P1 (Chuối): Create \texttt{Contain Edge}s to "Chuối", "Kali", "điều hòa huyết áp", "hoạt động của tim", "năng lượng nhanh", "người luyện tập thể thao".
    \item From P2 (Táo): Create \texttt{Contain Edge}s to "Táo", "chất xơ", "Pectin", "cải thiện tiêu hoá", "kiểm soát lượng đường trong máu", "Vỏ táo", "chất chống oxy hoá", "bệnh tim mạch".
    \item From P3 (Cam): Create \texttt{Contain Edge}s to "Cam", "Vitamin C", "hệ miễn dịch", "hấp thu sắt", "cải thiện làn da", "giảm mệt mỏi".
    \item From P4 (Lợi ích chung): Create \texttt{Contain Edge}s to "Chế độ ăn giàu trái cây", "vitamin", "khoáng chất", "bệnh mạn tính".
\end{itemize}

Upon completion, the KG will have a complete structure, tightly linking passages and the concepts/facts contained within them, ready for the Online phase.

\section{Online Retrieval \& QA Phase – Proposed Method}

After building the Knowledge Graph (KG) and indexing the text corpus in the Offline phase, the system transitions to the Online phase to process user queries and generate answers. The main goal of this phase is to efficiently retrieve the most relevant information from both the KG and the text corpus, then synthesize it into a high-quality context to provide to the Large Language Model (LLM) for generating the final answer. The proposed method focuses on combining information from passages and triples, using core facts to refine and filter passages, while avoiding the complexity of extensive graph propagation algorithms like PPR.

\hrulefill % Using hrulefill instead of --- for a horizontal line

\subsection{Module 1: Dual/Hybrid Retrieval}

\subsubsection{Detailed Module Explanation}

The first module in the Online phase acts as the gateway for user queries, performing the initial information retrieval from two main data sources prepared in the Offline phase: the Passage Store and the Knowledge Graph (KG). The objective of this module is to collect a set of potential candidates, including both text passages and information triples, that are likely to contain information relevant to the query.

To achieve good coverage and leverage the strengths of different retrieval methods, this module implements a \textbf{dual (dual retrieval)} or \textbf{hybrid (hybrid retrieval)} strategy. Specifically:

\begin{enumerate}[label=\arabic*.]
    \item \textbf{Passage Retrieval:} The system uses a hybrid approach combining:
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item \textbf{BM25 (Best Matching 25):} A classic yet effective keyword-based retrieval algorithm that focuses on the frequency and inverse document frequency of terms in the query and passages. BM25 is strong at finding passages that contain the exact terms in the query.
        \item \textbf{Embedding-based Retrieval:} Uses a sentence embedding model (e.g., \texttt{sentence-transformers/paraphrase-multilingual-mpnet-base-v2} as chosen in the Offline phase) to convert both the query and passages into dense vectors. The system then searches for passages whose embedding vectors are closest to the query\'s embedding vector (typically using cosine similarity). This method is strong at finding passages that are semantically related, even if they do not contain the exact keywords in the query.
        \item \textbf{Combination (Hybrid):} Scores from BM25 and embedding similarity are combined to create a final ranking for the passages. The system selects the Top-K passages with the highest combined scores (e.g., K=20-50) as output, referred to as \texttt{Raw Passages}.
    \end{itemize}

    \item \textbf{Triple Retrieval:} Similar to passage retrieval, the system also applies a hybrid approach to retrieve triples from the KG:
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item \textbf{BM25:} Applies BM25 on the textual representation of triples (e.g., concatenating subject, relation, object into a string) to find triples that match keywords in the query.
        \item \textbf{Embedding-based Retrieval:} Generates embedding vectors for the query and for the textual representation of the triples. Searches for triples with embeddings closest to the query\'s embedding.
        \item \textbf{Combination (Hybrid):} Combines scores from BM25 and embeddings to rank the triples. The system selects the Top-N triples with the highest scores (e.g., N=20-50) as output, referred to as \texttt{Raw Triples}.
    \end{itemize}
\end{enumerate}

Using a dual/hybrid retrieval method for both passages and triples offers significant benefits. It combines BM25\'s precise keyword matching capability with the deeper semantic understanding of embedding models, helping the system avoid missing important information, regardless of how it is expressed. The output of this module is two initial sets of candidates (\texttt{Raw Passages} and \texttt{Raw Triples}), laying the groundwork for subsequent filtering and refinement steps.

\subsubsection{Example Illustration (Retrieval)}

Suppose the user queries: "What are the benefits of apples for digestion?"

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \textbf{Passage Retrieval (Top-K=50):}
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item BM25 might return Passage 2 (P2 - containing "Táo", "chất xơ", "pectin", "cải thiện tiêu hoá") with a high BM25 score.
        \item Embedding retrieval might return P2 with a high cosine similarity score (e.g., 0.90) due to strong semantic relevance. It could also return Passage 4 (P4 - discussing general benefits, including disease prevention) with a lower score (e.g., 0.75).
        \item Passage 1 (P1 - Chuối) and Passage 3 (P3 - Cam) would have low scores from both methods.
        \item After combining scores, the system selects the top 50 \texttt{Raw Passages}. P2 will almost certainly be in a very high position, P4 might appear in a lower position, while P1 and P3 might be excluded or ranked very low.
    \end{itemize}
    \item \textbf{Triple Retrieval (Top-N=50):}
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item BM25 might find triples like \texttt{(Táo, là nguồn, chất xơ)}, \texttt{(Pectin, giúp, cải thiện tiêu hoá)}, \texttt{(Táo, chứa, Pectin)}.
        \item Embedding retrieval would also prioritize these triples due to semantic relevance. It could also find \texttt{(Chất xơ, hỗ trợ, tiêu hóa khỏe mạnh)} (if it exists in the KG and has a close embedding).
        \item Triples about bananas or oranges like \texttt{(Chuối, chứa, Kali)}, \texttt{(Cam, nổi bật với, Vitamin C)} would have much lower scores.
        \item Combining scores, the system selects the 50 most relevant \texttt{Raw Triples}, mainly focusing on apples, pectin, and digestion.
    \end{itemize}
\end{itemize}

The result is two lists: \texttt{Raw Passages} (primarily P2) and \texttt{Raw Triples} (focused on apples and digestion), ready for Modules 2 and 3.

\hrulefill % Using hrulefill instead of --- for a horizontal line

\subsection{Module 2: Filter Triples using LLM}

\subsubsection{Detailed Module Explanation}

After collecting a large initial set of candidate triples (\texttt{Raw Triples}) from Module 1, the next step is to refine this set to retain only the core, reliable, and most directly relevant facts to the user\'s query. Module 2 performs this crucial task by using a Large Language Model (LLM) as an intelligent filter.

The main goal of this module is to transform the list of \texttt{Raw Triples} (which may contain noise, irrelevant information, or low-level facts) into a smaller, higher-quality set called \texttt{Filtered Triples}. This set will serve as the "gold standard" or "core facts" for subsequent processing steps, especially in ranking and filtering passages.

The operation of Module 2 is as follows:

\begin{enumerate}[label=\arabic*.]
    \item \textbf{Prepare Input for LLM:} The system gathers the retrieved \texttt{Raw Triples} and the original user query. This information is formatted into a clear prompt for the LLM.
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item The prompt asks the LLM to evaluate the relevance of each triple to the query and select the Top-M most important triples from the input list.
        \item \textbf{Detailed Prompt Example:}
        
        \begin{tcolorbox}[
            colback=gray!5!white,
            colframe=gray!75!black,
            title=LLM Prompt Example,
            fonttitle=\bfseries,
            sharp corners,
            boxrule=0.5pt,
            ]
        \begin{verbatim}
You are an information analysis expert. Based on the following question:
Question: "[ORIGINAL USER QUERY]"

Please review the list of facts (triples) below:
[LIST OF RAW TRIPLES, ONE TRIPLE PER LINE, E.G., (Subject, Relation, Object)]

Your task is to select the Top [M] most directly relevant and important facts (triples) 
to answer the question above. Only return the selected facts, one fact per line, 
maintaining the (Subject, Relation, Object) format.

Selected facts:
        \end{verbatim}
        \end{tcolorbox}
        
        Where `[ORIGINAL USER QUERY]`, `[LIST OF RAW TRIPLES]`, and `[M]` will be replaced with actual values.
    \end{itemize}

    \item \textbf{Execute Filtering with LLM:} The prompt is sent to the LLM (in this study, \texttt{Qwen2.5-7B-Instruct}, deployed via Inference Providers). The LLM will semantically analyze the query and each triple in the \texttt{Raw Triples} list.
    
    LLM will use its language understanding and reasoning capabilities to identify which triples provide the most direct, accurate, and useful information for answering the query. At the same time, it can eliminate irrelevant, redundant, or overly general or misleading triples.

    \item \textbf{Collect Results:} The system receives the results returned by the LLM, which is the list of filtered triples (\texttt{Filtered Triples}). The number of triples in this list is usually significantly smaller than the original \texttt{Raw Triples} (e.g., M=10-20).
\end{enumerate}

Using Large Language Models (LLMs) as triple filters offers several advantages over simpler rule-based or threshold-based filtering methods. Firstly, LLMs have a deep contextual understanding, allowing the model to recognize the true intent behind the query and assess the semantic relevance of each triple more subtly. Secondly, LLMs offer high flexibility, as there is no need to predefine rigid filtering rules, and they can adapt to various query types and application domains. Finally, thanks to their strong reasoning capabilities, LLMs can eliminate noisy information and retain truly important facts, thereby creating a high-quality, semantically rich set of \texttt{Filtered Triples} that serves well for subsequent processing steps.

The \texttt{Filtered Triples} result plays a crucial role in directing and enhancing the quality of subsequent processing steps in the pipeline, preventing the redundancy of information irrelevant to the query.

\subsubsection{Example Illustration (Triple Filtering)}

Continuing with the query: "What are the benefits of apples for digestion?"

Assume \texttt{Raw Triples} (Top-N=50) contains triples such as:

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \texttt{(Táo, là nguồn, chất xơ)} - Very relevant
    \item \texttt{(Pectin, giúp, cải thiện tiêu hoá)} - Very relevant
    \item \texttt{(Táo, chứa, Pectin)} - Very relevant
    \item \texttt{(Chất xơ, hỗ trợ, tiêu hóa khỏe mạnh)} - Relevant
    \item \texttt{(Vỏ táo, chứa, chất chống oxy hoá)} - Less relevant to digestion
    \item \texttt{(Táo, thuộc loại, Trái cây ôn đới)} - Not relevant
    \item \texttt{(Chuối, chứa, Kali)} - Not relevant
    \item \texttt{(Cam, nổi bật với, Vitamin C)} - Not relevant
    \item \texttt{(Pectin, là loại, chất xơ hoà tan)} - Relevant, supplementary information
    \item ... (and other triples)
\end{itemize}

Using the prompt example above with M=5, the LLM (Qwen2.5-7B) will analyze and select the triples most relevant to the "digestive benefits" of apples. The resulting \texttt{Filtered Triples} might be:

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \texttt{(Táo, là nguồn, chất xơ)}
    \item \texttt{(Pectin, giúp, cải thiện tiêu hoá)}
    \item \texttt{(Táo, chứa, Pectin)}
    \item \texttt{(Chất xơ, hỗ trợ, tiêu hóa khỏe mạnh)}
    \item \texttt{(Pectin, là loại, chất xơ hoà tan)}
\end{itemize}

The LLM has eliminated triples about apple peel, fruit type, bananas, oranges, and retained the core facts about apples, fiber, pectin, and their role in digestion. This set of \texttt{Filtered Triples} will be used in Module 3.

\hrulefill % Using hrulefill instead of --- for a horizontal line

\subsection{Module 3: Rank Passages based on Filtered Triples}

\subsubsection{Detailed Module Explanation}

This module is the core innovation of the proposed retrieval method. Instead of relying solely on direct query-passage similarity (like standard RAG) or complex graph propagation (like HippoRAG), this module re-ranks the initially retrieved \texttt{Raw Passages} based on their relevance to the high-quality \texttt{Filtered Triples} identified in Module 2.

The goal is to prioritize passages that not only match the query keywords or semantics but also strongly support the core facts deemed most important by the LLM filter. This approach aims to improve the precision and relevance of the final context provided to the LLM for answer generation.

The process is as follows:

\begin{enumerate}[label=\arabic*.]
    \item \textbf{Input:} The module receives the list of \texttt{Raw Passages} (from Module 1) and the list of \texttt{Filtered Triples} (from Module 2).
    \item \textbf{Calculate Passage-Triple Relevance Score:} For each passage $P$ in \texttt{Raw Passages} and each triple $T$ in \texttt{Filtered Triples}, the system calculates a relevance score, denoted as $Score(P, T)$. This score measures how well passage $P$ supports or contains the information represented by triple $T$. Several methods can be used for this calculation:
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item \textbf{Simple Co-occurrence:} Check if the subject, relation, and object of triple $T$ (or their synonyms) appear within passage $P$. A higher count of matching components leads to a higher score.
        \item \textbf{Embedding Similarity:} Calculate the cosine similarity between the embedding of passage $P$ and the embedding of the textual representation of triple $T$. Higher similarity indicates stronger relevance.
        \item \textbf{LLM-based Assessment (More Advanced):} Use an LLM to directly assess the relevance between passage $P$ and triple $T$. This is more accurate but computationally expensive.
        \item \textbf{Hybrid Approach (Recommended):} Combine co-occurrence checks with embedding similarity for a balanced approach.
    \end{itemize}
    \item \textbf{Calculate Aggregate Passage Score:} For each passage $P$, calculate an aggregate score based on its relevance to \textit{all} \texttt{Filtered Triples}. A simple way is to sum the individual relevance scores: $AggregateScore(P) = \sum_{T \in \text{Filtered Triples}} Score(P, T)$. More sophisticated aggregation methods (e.g., weighted sum, maximum score) can also be used.
    \item \textbf{Re-rank Passages:} Re-sort the \texttt{Raw Passages} based on their $AggregateScore(P)$ in descending order. This new ranking prioritizes passages that align best with the core facts.
    \item \textbf{Select Top-P Passages:} Select the top P passages from the re-ranked list (e.g., P=5-10) to form the final set of \texttt{Ranked Passages}. This set represents the most relevant and factually supported context retrieved by the system.
\end{enumerate}

This triple-based passage ranking method offers several advantages. It leverages the structured knowledge (triples) filtered by the LLM to refine the selection of unstructured text (passages). This helps ensure that the retrieved context is not only topically relevant but also factually aligned with the most important aspects of the query. Compared to standard RAG, it adds a layer of factual grounding. Compared to complex graph methods like PPR, it is computationally simpler while still incorporating graph-derived information (triples) into the ranking process.

\subsubsection{Example Illustration (Passage Ranking)}

Continuing with the query and previous results:

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \texttt{Raw Passages}: Assume P2 (Apple passage) and P4 (General benefits passage) are highly ranked initially.
    \item \texttt{Filtered Triples}: \texttt{(Táo, là nguồn, chất xơ)}, \texttt{(Pectin, giúp, cải thiện tiêu hoá)}, \texttt{(Táo, chứa, Pectin)}, \texttt{(Chất xơ, hỗ trợ, tiêu hóa khỏe mạnh)}, \texttt{(Pectin, là loại, chất xơ hoà tan)}.
\end{itemize}

Calculating relevance scores (using a simplified co-occurrence + embedding method):

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \textbf{Passage P2 (Apple):} Contains "Táo", "chất xơ", "Pectin", "cải thiện tiêu hoá". It strongly supports most of the \texttt{Filtered Triples}. Let\'s assume $AggregateScore(P2) = 4.5$.
    \item \textbf{Passage P4 (General Benefits):} Mentions "chất xơ" and "bệnh mạn tính" but not specifically "Táo" or "Pectin" or "cải thiện tiêu hoá". It weakly supports only one or two triples (e.g., the one about fiber). Let\'s assume $AggregateScore(P4) = 1.2$.
    \item Other passages (e.g., P1-Banana, P3-Orange) would likely have scores near 0.
\end{itemize}

Re-ranking based on these scores: P2 will be ranked much higher than P4.

Selecting Top-P=3 passages: The system will likely select P2 as the top passage, potentially followed by other less relevant passages if P2\'s score is significantly higher than others. The final \texttt{Ranked Passages} set will be highly focused on the apple passage that directly addresses the query based on the filtered facts.

\subsection{Module 4: Generate Answer using LLM}

\subsubsection{Detailed Module Explanation}

This is the final module in the Online phase, responsible for synthesizing the retrieved information and generating a coherent, comprehensive, and accurate answer to the user\'s original query. It leverages the power of a Large Language Model (LLM), often referred to as the "Generator" or "Reader" in RAG terminology.

The process involves:

\begin{enumerate}[label=\arabic*.]
    \item \textbf{Prepare Context and Prompt:} The system gathers the final set of \texttt{Ranked Passages} obtained from Module 3. This set represents the most relevant and factually supported context found by the retrieval pipeline. This context is then combined with the original user query to construct a detailed prompt for the Generator LLM.
    \begin{itemize}[label=\textendash, leftmargin=*]
        \item The prompt typically instructs the LLM to answer the query based \textit{only} on the provided context passages.
        \item It might also include instructions to synthesize information from multiple passages if necessary, cite sources (passage IDs), and maintain a specific tone or format.
        \item \textbf{Detailed Prompt Example:}
        
        \begin{tcolorbox}[
            colback=blue!5!white,
            colframe=blue!75!black,
            title=Generator LLM Prompt Example,
            fonttitle=\bfseries,
            sharp corners,
            boxrule=0.5pt,
            ]
        \begin{verbatim}
Based *only* on the following context passages, please answer the question below. 
Synthesize information if needed and cite the passage number(s) (e.g., [P1], [P2]) 
that support your answer.

Context Passages:
[CONTEXT FROM RANKED PASSAGES - E.g., Passage P2 content here]
[CONTEXT FROM RANKED PASSAGES - E.g., Passage Px content here]
...

Question: "[ORIGINAL USER QUERY]"

Answer:
        \end{verbatim}
        \end{tcolorbox}
        
        Where `[CONTEXT FROM RANKED PASSAGES]` and `[ORIGINAL USER QUERY]` are replaced with the actual retrieved context and the user\'s question.
    \end{itemize}
    \item \textbf{Execute Answer Generation:} The constructed prompt is sent to the Generator LLM (e.g., GPT-4, Claude 3, or another powerful model suitable for generation tasks). The LLM reads the query and the provided context, understands the relationships between them, synthesizes the relevant information, and generates a natural language answer.
    \item \textbf{Post-process and Return Answer:} The raw answer generated by the LLM might undergo minor post-processing (e.g., formatting, citation checking) before being presented to the user as the final result.
\end{enumerate}

The quality of the final answer heavily depends on two factors: the quality of the retrieved context (\texttt{Ranked Passages}) and the capabilities of the Generator LLM. By using the proposed retrieval pipeline (Modules 1-3) that filters triples and ranks passages based on these core facts, the system aims to provide a highly relevant and factually grounded context to the Generator LLM, thereby reducing the likelihood of hallucinations or irrelevant information in the final answer.

\subsubsection{Example Illustration (Answer Generation)}

Continuing with the query: "What are the benefits of apples for digestion?"

\begin{itemize}[label=\textbullet, leftmargin=*]
    \item \texttt{Ranked Passages}: Assume the top passage is P2: "Táo là nguồn chất xơ dồi dào, đặc biệt là pectin – một loại chất xơ hoà tan giúp cải thiện tiêu hoá và kiểm soát lượng đường trong máu. Vỏ táo cũng chứa nhiều chất chống oxy hoá, có thể giảm nguy cơ mắc bệnh tim mạch."
    \item \textbf{Prompt Sent to Generator LLM:} (Using the template above)
    
    \begin{tcolorbox}[
        colback=blue!5!white,
        colframe=blue!75!black,
        title=Filled Generator Prompt,
        fonttitle=\bfseries,
        sharp corners,
        boxrule=0.5pt,
        ]
    \begin{verbatim}
Based *only* on the following context passages, please answer the question below. 
Synthesize information if needed and cite the passage number(s) (e.g., [P1], [P2]) 
that support your answer.

Context Passages:
[P2] Táo là nguồn chất xơ dồi dào, đặc biệt là pectin – một loại chất xơ hoà tan 
giúp cải thiện tiêu hoá và kiểm soát lượng đường trong máu. Vỏ táo cũng chứa 
nhiều chất chống oxy hoá, có thể giảm nguy cơ mắc bệnh tim mạch.

Question: "What are the benefits of apples for digestion?"

Answer:
    \end{verbatim}
    \end{tcolorbox}

    \item \textbf{Generated Answer (Example):}
    
    \begin{quote}
    "Táo có lợi cho tiêu hóa chủ yếu do chúng là nguồn chất xơ dồi dào, đặc biệt là pectin. Pectin là một loại chất xơ hòa tan giúp cải thiện tiêu hóa [P2]."
    
    \textit{(Apples benefit digestion mainly because they are a rich source of dietary fiber, especially pectin. Pectin is a type of soluble fiber that helps improve digestion [P2].)}
    \end{quote}
\end{itemize}

This answer directly addresses the query using only the information provided in the relevant passage P2, demonstrating the effectiveness of the RAG pipeline in generating contextually grounded responses.

```


# Cây cấu trúc của dự án: 

```bash 
graphrag-thesis/
├── 📖 README.md
├── 📋 requirements.txt  
├── 🌍 .env.example
│
├── 📁 src/
│   ├── 📁 DB/
│   │   └── 🐳 docker-compose.yml
│   │
│   └── 📁 OfflineIndexing/
│       ├── 📋 offline_indexing_requirements.txt
│       │
│       ├── 📄 module1_chunking.py
│       ├── 🧠 module2_triple_extractor.py  
│       ├── 🔗 module3_synonym_detector.py
│       ├── 🏗️ module4_graph_builder.py
│       ├── 🎯 pipeline_orchestrator.py
│       ├── 🚀 run_offline_pipeline.py
│       │
│       ├── 📁 utils/
│       │   ├── 🔧 utils_general.py
│       │   ├── 📊 utils_excel_documents.py
│       │   └── 🗃️ utils_neo4j.py
│       │
│       └── 📁 test/
│           ├── 📊 test_data.py
│           ├── 🧪 test_offline_pipeline.py
│           └── 🔍 test_query_functions.py
│
└── 📁 OnlineRetrievalAndQA
```



-----


# Sau 1 hồi lâu làm với Genspark để tinh chỉnh từng module, từng phần kiến trúc xem cái nào cần cái nào không 

## Cây kiến trúc ver 1.

```bash
📁 OnlineRetrievalAndQA/                      # 🌐 ONLINE PHASE
├── 📋 online_requirements.txt                # Dependencies for online phase
│
├── 🔍 module1_dual_retrieval.py              # Bước 1: Dual/Hybrid Retrieval
├── 🤖 module2_triple_filter.py               # Bước 2: LLM Triple Filtering  
├── 📊 module3_passage_ranker.py              # Bước 3: Triple-based Passage Ranking
├── 🎯 module4_context_expander.py            # Bước 4: 1-hop Context Expansion (Optional)
├── 🗣️ module5_answer_generator.py            # Bước 5: Final Answer Generation
│
├── 🎯 online_pipeline_orchestrator.py        # Pipeline Logic Coordinator (Core orchestration)
│
├── 🔍 run_retrieval_pipeline.py              # Run Retrieval Only (Steps 1-3/4)
│                                             # Args: --enable_expansion True/False
├── 🌐 run_retrieval_and_qa_pipeline.py       # Run Full Pipeline (Steps 1-5)
│                                             # Args: --enable_expansion True/False
│
├── 📁 utils/                                 # 🔧 UTILS BY MODULE
│   ├── 📁 module1_utils/                     # 🔍 Dual Retrieval Utils
│   │   ├── 🔤 utils_bm25.py                  # BM25 implementation
│   │   ├── 🧠 utils_embedding.py             # Dense retrieval utilities
│   │   └── 🎭 utils_hybrid_scoring.py        # Score combination methods
│   │
│   ├── 📁 module2_utils/                     # 🤖 Triple Filter Utils
│   │   ├── 🤖 utils_llm_filter.py            # LLM filtering utilities
│   │   └── 📝 utils_filter_prompts.py        # Triple filtering prompts
│   │
│   ├── 📁 module3_utils/                     # 📊 Passage Ranker Utils
│   │   ├── 📈 utils_ranking.py               # Ranking algorithms
│   │   └── 🎯 utils_relevance.py             # Relevance calculation
│   │
│   ├── 📁 module4_utils/                     # 🎯 Context Expander Utils
│   │   ├── 🔗 utils_graph_query.py           # Neo4j/KG query utilities
│   │   └── 🔄 utils_expansion.py             # 1-hop expansion logic
│   │
│   ├── 📁 module5_utils/                     # 🗣️ Answer Generator Utils
│   │   ├── 🤖 utils_llm_generator.py         # LLM generation utilities
│   │   ├── 📝 utils_answer_prompts.py        # Answer generation prompts
│   │   └── 🎨 utils_formatting.py            # Response formatting
│   │
│   └── 📁 shared_utils/                      # 🔧 Shared Utilities
│       ├── 🔧 utils_general.py               # General online utilities
│       ├── 📊 utils_logging.py               # Logging utilities
│       └── ⚙️ utils_config.py                # Configuration management
│
└── 📁 test/                                  # 🧪 TESTING
    ├── 🧪 test_dual_retrieval.py             # Test Module 1
    ├── 🤖 test_triple_filter.py              # Test Module 2  
    ├── 📊 test_passage_ranker.py             # Test Module 3
    ├── 🎯 test_context_expander.py           # Test Module 4
    ├── 🗣️ test_answer_generator.py           # Test Module 5
    ├── 🔍 test_retrieval_pipeline.py         # Test retrieval only
    ├── 🌐 test_full_pipeline.py              # Test full pipeline
    ├── 🎯 test_queries.json                  # Sample test queries
    └── 📊 test_expected_results.json         # Expected outputs

```

Oke, chốt cây kiến trúc này nhé, mô tả chi tiết từng file. 


#### Đánh giá cây kiến trúc OnlineRetrievalAndQA🎯 **Overall Assessment: EXCELLENT** ⭐⭐⭐⭐⭐

Cây kiến trúc này rất **ổn và professional**! Đây là một thiết kế **clean, modular, và scalable**.

---

#### ✅ **Điểm mạnh:**

#### **1. 🏗️ Clear Module Separation**
- 5 modules tương ứng 5 bước rõ ràng
- Mỗi module có responsibility riêng biệt
- Easy to understand và maintain

#### **2. 🎯 Smart Entry Points**
- `run_retrieval_pipeline.py` - Perfect cho research/debugging
- `run_retrieval_and_qa_pipeline.py` - Perfect cho production
- `online_pipeline_orchestrator.py` - Good separation of concerns

#### **3. 🔧 Well-Organized Utils**
- Utils chia theo module → **High cohesion, low coupling**
- `shared_utils/` cho common functionality
- Clear naming convention

#### **4. 🧪 Comprehensive Testing**
- Individual module tests
- Pipeline-level integration tests
- Test data structure thoughtful

#### **5. 📦 Logical Grouping**
```
Core Logic (modules) → Utils (supporting) → Tests (validation) → Entry Points (execution)
```

---

#### 🟡 **Minor Suggestions (Optional):**

##### **1. 📋 Configuration**
Consider adding:
```bash
├── 📁 configs/
│   ├── ⚙️ retrieval_config.yaml
│   ├── 🤖 llm_config.yaml
│   └── 🗃️ database_config.yaml
```

##### **2. 📊 Output/Results**
Consider adding:
```bash
├── 📁 outputs/
│   ├── 📁 intermediate_results/
│   └── 📁 final_answers/
```

#### **3. 📝 Documentation**
Consider adding:
```bash
├── 📖 README.md
├── 📚 docs/
│   ├── 🚀 quickstart.md
│   └── 🔧 api_reference.md
```

---

## 🚀 **Architecture Strengths:**

| Aspect | Rating | Comment |
|--------|--------|---------|
| **Modularity** | ⭐⭐⭐⭐⭐ | Perfect separation of concerns |
| **Scalability** | ⭐⭐⭐⭐⭐ | Easy to add new modules/utils |
| **Maintainability** | ⭐⭐⭐⭐⭐ | Clear structure, easy to debug |
| **Testability** | ⭐⭐⭐⭐⭐ | Comprehensive test coverage |
| **Usability** | ⭐⭐⭐⭐⭐ | Multiple entry points for different use cases |

---


## Cây kiến trúc ver 2 - bổ sung Output/Results - bổ sung readme và docs

```bash
📁 OnlineRetrievalAndQA/                      # 🌐 ONLINE PHASE
├── 📋 online_requirements.txt                # Dependencies for online phase
│
├── 🔍 module1_dual_retrieval.py              # Bước 1: Dual/Hybrid Retrieval
├── 🤖 module2_triple_filter.py               # Bước 2: LLM Triple Filtering  
├── 📊 module3_passage_ranker.py              # Bước 3: Triple-based Passage Ranking
├── 🎯 module4_context_expander.py            # Bước 4: 1-hop Context Expansion (Optional)
├── 🗣️ module5_answer_generator.py            # Bước 5: Final Answer Generation
│
├── 🎯 online_pipeline_orchestrator.py        # Pipeline Logic Coordinator (Core orchestration)
│
├── 🔍 run_retrieval_pipeline.py              # Run Retrieval Only (Steps 1-3/4)
│                                             # Args: --enable_expansion True/False
├── 🌐 run_retrieval_and_qa_pipeline.py       # Run Full Pipeline (Steps 1-5)
│                                             # Args: --enable_expansion True/False
│
├── 📁 utils/                                 # 🔧 UTILS BY MODULE
│   ├── 📁 module1_utils/                     # 🔍 Dual Retrieval Utils
│   │   ├── 🔤 utils_bm25.py                  # BM25 implementation
│   │   ├── 🧠 utils_embedding.py             # Dense retrieval utilities
│   │   └── 🎭 utils_hybrid_scoring.py        # Score combination methods
│   │
│   ├── 📁 module2_utils/                     # 🤖 Triple Filter Utils
│   │   ├── 🤖 utils_llm_filter.py            # LLM filtering utilities
│   │   └── 📝 utils_filter_prompts.py        # Triple filtering prompts
│   │
│   ├── 📁 module3_utils/                     # 📊 Passage Ranker Utils
│   │   ├── 📈 utils_ranking.py               # Ranking algorithms
│   │   └── 🎯 utils_relevance.py             # Relevance calculation
│   │
│   ├── 📁 module4_utils/                     # 🎯 Context Expander Utils
│   │   ├── 🔗 utils_graph_query.py           # Neo4j/KG query utilities
│   │   └── 🔄 utils_expansion.py             # 1-hop expansion logic
│   │
│   ├── 📁 module5_utils/                     # 🗣️ Answer Generator Utils
│   │   ├── 🤖 utils_llm_generator.py         # LLM generation utilities
│   │   ├── 📝 utils_answer_prompts.py        # Answer generation prompts
│   │   └── 🎨 utils_formatting.py            # Response formatting
│   │
│   └── 📁 shared_utils/                      # 🔧 Shared Utilities
│       ├── 🔧 utils_general.py               # General online utilities
│       ├── 📊 utils_logging.py               # Logging utilities
│       └── ⚙️ utils_config.py                # Configuration management
│
└── 📁 test/                                  # 🧪 TESTING
    ├── 🧪 test_dual_retrieval.py             # Test Module 1
    ├── 🤖 test_triple_filter.py              # Test Module 2  
    ├── 📊 test_passage_ranker.py             # Test Module 3
    ├── 🎯 test_context_expander.py           # Test Module 4
    ├── 🗣️ test_answer_generator.py           # Test Module 5
    ├── 🔍 test_retrieval_pipeline.py         # Test retrieval only
    ├── 🌐 test_full_pipeline.py              # Test full pipeline
    ├── 🎯 test_queries.json                  # Sample test queries
    └── 📊 test_expected_results.json         # Expected outputs
├── 📖 README.md
├── 📚 docs/
│   ├── 🚀 quickstart.md
│   └── 🔧 api_reference.md
├── 📁 outputs/
│   ├── 📁 retrieval_results/
│   └── 📁 final_answers/
├── 📁 configs/
│   └── ⚙️ config.yaml
```