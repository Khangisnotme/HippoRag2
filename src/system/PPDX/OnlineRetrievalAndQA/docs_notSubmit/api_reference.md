"""
API Reference - Tài liệu tham khảo API cho OnlineRetrievalAndQA
"""

# API Reference

Tài liệu này cung cấp thông tin chi tiết về các module và API trong hệ thống OnlineRetrievalAndQA.

## Module 1: Dual/Hybrid Retrieval

### `DualRetriever`

```python
from module1_dual_retrieval import DualRetriever, RetrievalResult

retriever = DualRetriever(
    bm25_index_path="path/to/bm25_index",
    embedding_model_name="paraphrase-multilingual-mpnet-base-v2",
    passage_embeddings_path="path/to/passage_embeddings.npy",
    passage_data_path="path/to/passage_data.json",
    triple_data_path="path/to/triple_data.json",
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password",
    bm25_weight=0.5,
    embedding_weight=0.5
)

# Truy xuất passages và triples
result = retriever.retrieve(
    query="Câu hỏi của người dùng?",
    top_k_passages=100,
    top_n_triples=50
)

# Truy cập kết quả
passages = result.raw_passages
triples = result.raw_triples
retrieval_stats = result.retrieval_stats
```

#### Tham số

- `bm25_index_path`: Đường dẫn đến BM25 index
- `embedding_model_name`: Tên model embedding
- `passage_embeddings_path`: Đường dẫn đến file embeddings của passages
- `passage_data_path`: Đường dẫn đến file dữ liệu passages
- `triple_data_path`: Đường dẫn đến file dữ liệu triples
- `neo4j_uri`: URI của Neo4j database
- `neo4j_user`: Username của Neo4j database
- `neo4j_password`: Password của Neo4j database
- `bm25_weight`: Trọng số cho BM25 retrieval (0.0-1.0)
- `embedding_weight`: Trọng số cho embedding retrieval (0.0-1.0)

## Module 2: LLM Triple Filtering

### `TripleFilter`

```python
from module2_triple_filter import TripleFilter, FilteredTripleResult

triple_filter = TripleFilter(
    primary_model="qwen2.5-7b-instruct",
    backup_model="gpt-3.5-turbo",
    primary_provider="huggingface",
    backup_provider="openai",
    openai_api_key="your_openai_api_key",
    max_triples_to_filter=50,
    target_filtered_count=15,
    use_backup_on_failure=True
)

# Lọc triples
result = triple_filter.filter_triples(
    query="Câu hỏi của người dùng?",
    raw_triples=[...],  # Danh sách triples từ retriever
    target_count=15
)

# Truy cập kết quả
filtered_triples = result.filtered_triples
filtering_stats = result.filtering_stats
```

#### Tham số

- `primary_model`: Tên model LLM chính
- `backup_model`: Tên model LLM dự phòng
- `primary_provider`: Provider của model chính (huggingface/openai)
- `backup_provider`: Provider của model dự phòng (huggingface/openai)
- `openai_api_key`: API key của OpenAI
- `max_triples_to_filter`: Số lượng tối đa triples đưa vào LLM để lọc
- `target_filtered_count`: Số lượng triples mục tiêu sau khi lọc
- `use_backup_on_failure`: Có sử dụng model dự phòng khi model chính thất bại không

## Module 3: Triple-based Passage Ranking

### `PassageRanker`

```python
from module3_passage_ranker import PassageRanker, RankedPassageResult

passage_ranker = PassageRanker(
    alpha=0.7,
    min_token_overlap=2,
    use_semantic_matching=True,
    embedding_model_name="paraphrase-multilingual-mpnet-base-v2"
)

# Xếp hạng passages
result = passage_ranker.rank_passages(
    raw_passages=[...],  # Danh sách passages từ retriever
    filtered_triples=[...],  # Danh sách triples đã lọc
    top_p=10
)

# Truy cập kết quả
ranked_passages = result.ranked_passages
ranking_method = result.ranking_method
ranking_time = result.ranking_time
```

#### Tham số

- `alpha`: Trọng số cho điểm retrieval gốc vs điểm hỗ trợ triple (0.0-1.0)
- `min_token_overlap`: Số lượng token tối thiểu cần trùng lặp
- `use_semantic_matching`: Có sử dụng semantic matching không
- `embedding_model_name`: Tên model embedding cho semantic matching

## Module 4: Context Expansion

### `ContextExpander`

```python
from module4_context_expander import ContextExpander, ExpandedContext

context_expander = ContextExpander(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password",
    expansion_strategy="balanced",
    max_expansions=5,
    embedding_model_name="paraphrase-multilingual-mpnet-base-v2"
)

# Mở rộng context
result = context_expander.expand_context(
    filtered_triples=[...],  # Danh sách triples đã lọc
    original_query="Câu hỏi của người dùng?",
    expansion_limit=20
)

# Truy cập kết quả
expanded_triples = result.expanded_triples
all_triples = result.get_all_triples()
expansion_paths = result.expansion_paths
```

#### Tham số

- `neo4j_uri`: URI của Neo4j database
- `neo4j_user`: Username của Neo4j database
- `neo4j_password`: Password của Neo4j database
- `expansion_strategy`: Chiến lược mở rộng (balanced/subject_focus/object_focus)
- `max_expansions`: Số lượng tối đa expansions cho mỗi triple
- `embedding_model_name`: Tên model embedding cho semantic matching

## Module 5: Answer Generation

### `AnswerGenerator`

```python
from module5_answer_generator import AnswerGenerator, AnswerResult

answer_generator = AnswerGenerator(
    primary_model="qwen2.5-7b-instruct",
    backup_model="gpt-3.5-turbo",
    primary_provider="huggingface",
    backup_provider="openai",
    openai_api_key="your_openai_api_key",
    max_answer_length=500,
    use_backup_on_failure=True
)

# Tạo câu trả lời
result = answer_generator.generate_answer(
    query="Câu hỏi của người dùng?",
    ranked_passages=[...],  # Danh sách passages đã xếp hạng
    filtered_triples=[...],  # Danh sách triples đã lọc
    expanded_context=expanded_context.to_dict()  # Kết quả mở rộng context (tùy chọn)
)

# Truy cập kết quả
answer = result.answer
confidence = result.confidence
supporting_passages = result.supporting_passages
supporting_triples = result.supporting_triples
```

#### Tham số

- `primary_model`: Tên model LLM chính
- `backup_model`: Tên model LLM dự phòng
- `primary_provider`: Provider của model chính (huggingface/openai)
- `backup_provider`: Provider của model dự phòng (huggingface/openai)
- `openai_api_key`: API key của OpenAI
- `max_answer_length`: Độ dài tối đa của câu trả lời
- `use_backup_on_failure`: Có sử dụng model dự phòng khi model chính thất bại không

## Pipeline Orchestrator

### `PipelineOrchestrator`

```python
from online_pipeline_orchestrator import PipelineOrchestrator, PipelineResult

# Tải cấu hình
with open("config/pipeline_config.json", "r") as f:
    config = json.load(f)

# Khởi tạo orchestrator
orchestrator = PipelineOrchestrator(
    config=config,
    enable_expansion=True
)

# Chạy pipeline cho một query
result = orchestrator.run_pipeline(
    query="Câu hỏi của người dùng?"
)

# Chạy pipeline cho nhiều queries
results = orchestrator.run_batch_pipeline(
    queries=["Câu hỏi 1?", "Câu hỏi 2?", "Câu hỏi 3?"]
)

# Lưu kết quả
orchestrator.save_results(
    results=result,  # hoặc results cho batch
    output_dir="outputs"
)

# Lấy thống kê
stats = orchestrator.get_pipeline_statistics()

# Đóng tài nguyên
orchestrator.close()
```

#### Tham số

- `config`: Cấu hình pipeline dưới dạng dictionary
- `enable_expansion`: Có bật context expansion không

## Utils

### `utils_shared_general`

```python
from utils.utils_shared_general import (
    setup_logging,
    load_json,
    save_json,
    load_env_variables,
    generate_unique_id,
    clean_text,
    normalize_query,
    create_timestamp_dir,
    get_file_paths,
    chunk_list,
    time_function,
    retry
)

# Thiết lập logging
logger = setup_logging(
    log_file="logs/pipeline.log",
    level=logging.INFO,
    console=True
)

# Tải/lưu JSON
data = load_json("path/to/file.json")
save_json(data, "path/to/output.json", indent=2)

# Tải biến môi trường
env_vars = load_env_variables(".env")

# Tạo ID duy nhất
unique_id = generate_unique_id(prefix="query", length=8)

# Làm sạch và chuẩn hóa query
cleaned_text = clean_text("Text   with  extra   spaces!")
normalized_query = normalize_query("Câu Hỏi Của Người Dùng?")

# Tạo thư mục với timestamp
output_dir = create_timestamp_dir("outputs", prefix="run")

# Lấy danh sách file
files = get_file_paths("data", pattern="*.json", recursive=True)

# Chia danh sách thành các phần
chunks = chunk_list([1, 2, 3, 4, 5], chunk_size=2)  # [[1, 2], [3, 4], [5]]

# Decorator đo thời gian
@time_function
def my_function():
    pass

# Decorator thử lại
@retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,))
def my_function():
    pass
```

## Script Pipeline

### `run_retrieval_pipeline.py`

```bash
python run_retrieval_pipeline.py --config config/pipeline_config.json --queries data/queries.json --output_dir outputs/retrieval_results --enable_expansion False
```

### `run_retrieval_and_qa_pipeline.py`

```bash
python run_retrieval_and_qa_pipeline.py --config config/pipeline_config.json --queries data/queries.json --output_dir outputs --enable_expansion True
```

## Định dạng dữ liệu

### Passage

```json
{
  "id": "passage_123",
  "text": "Nội dung passage...",
  "source": "document_456",
  "metadata": {
    "title": "Tiêu đề",
    "page": 42,
    "section": "Phần 3"
  }
}
```

### Triple

```json
{
  "id": "triple_789",
  "subject": "HippoRAG 2",
  "predicate": "sử dụng",
  "object": "graph-based retrieval",
  "confidence": 0.95,
  "source_id": "passage_123"
}
```

### Filtered Triple

```json
{
  "id": "triple_789",
  "subject": "HippoRAG 2",
  "predicate": "sử dụng",
  "object": "graph-based retrieval",
  "confidence": 0.95,
  "source_id": "passage_123",
  "llm_relevance_score": 0.87,
  "llm_reasoning": "Triple này trực tiếp liên quan đến câu hỏi về cách hoạt động của HippoRAG 2"
}
```

### Ranked Passage

```json
{
  "id": "passage_123",
  "text": "Nội dung passage...",
  "source": "document_456",
  "metadata": {
    "title": "Tiêu đề",
    "page": 42,
    "section": "Phần 3"
  },
  "original_hybrid_retrieval_score": 0.75,
  "triple_support_score": 0.82,
  "final_ranking_score": 0.77,
  "supported_triples": ["triple_789", "triple_456"],
  "coverage_ratio": 0.67
}
```

### Answer Result

```json
{
  "answer": "HippoRAG 2 sử dụng graph-based retrieval để cải thiện độ chính xác...",
  "confidence": 0.85,
  "supporting_passages": [...],
  "supporting_triples": [...],
  "generation_time": 2.34,
  "model_used": "qwen2.5-7b-instruct",
  "metadata": {
    "prompt_tokens": 1024,
    "response_tokens": 256
  }
}
```
