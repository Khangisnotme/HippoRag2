"""
Quickstart Guide - Hướng dẫn nhanh cho OnlineRetrievalAndQA
"""

# Hướng dẫn nhanh

Tài liệu này cung cấp hướng dẫn nhanh để bắt đầu sử dụng hệ thống OnlineRetrievalAndQA.

## Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/your-organization/OnlineRetrievalAndQA.git
cd OnlineRetrievalAndQA
```

### 2. Cài đặt dependencies

```bash
pip install -r online_requirements.txt
```

### 3. Cấu hình môi trường

Sao chép file `.env.example` thành `.env`:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với các thông tin cấu hình cần thiết:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key

# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Model Configuration
PRIMARY_LLM_MODEL=qwen2.5-7b-instruct
BACKUP_LLM_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=paraphrase-multilingual-mpnet-base-v2
```

## Sử dụng cơ bản

### Chạy Retrieval Pipeline

Để chạy pipeline chỉ bao gồm các bước retrieval (1-3/4):

```bash
python run_retrieval_pipeline.py --config config/pipeline_config.json --queries data/queries.json --output_dir outputs/retrieval_results --enable_expansion False
```

### Chạy Full Pipeline

Để chạy toàn bộ pipeline bao gồm cả retrieval và answer generation (1-5):

```bash
python run_retrieval_and_qa_pipeline.py --config config/pipeline_config.json --queries data/queries.json --output_dir outputs --enable_expansion True
```

## Cấu hình Pipeline

Tạo file cấu hình JSON với cấu trúc sau:

```json
{
  "retriever": {
    "bm25_index_path": "path/to/bm25_index",
    "embedding_model": "paraphrase-multilingual-mpnet-base-v2",
    "passage_embeddings_path": "path/to/passage_embeddings.npy",
    "passage_data_path": "path/to/passage_data.json",
    "triple_data_path": "path/to/triple_data.json",
    "bm25_weight": 0.5,
    "embedding_weight": 0.5
  },
  "filter": {
    "primary_model": "qwen2.5-7b-instruct",
    "backup_model": "gpt-3.5-turbo",
    "primary_provider": "huggingface",
    "backup_provider": "openai",
    "max_triples_to_filter": 50,
    "target_filtered_count": 15
  },
  "ranker": {
    "alpha": 0.7,
    "min_token_overlap": 2,
    "use_semantic_matching": true
  },
  "expander": {
    "expansion_strategy": "balanced",
    "max_expansions": 5
  },
  "generator": {
    "primary_model": "qwen2.5-7b-instruct",
    "backup_model": "gpt-3.5-turbo",
    "primary_provider": "huggingface",
    "backup_provider": "openai",
    "max_answer_length": 500
  },
  "database": {
    "uri": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "password"
  },
  "pipeline": {
    "top_k_passages": 100,
    "top_n_triples": 50,
    "filtered_triple_count": 15,
    "final_passage_count": 10,
    "expansion_limit": 20
  }
}
```

## Định dạng Queries

Queries có thể được cung cấp dưới dạng file JSON hoặc text:

### JSON Format

```json
[
  "Câu hỏi 1?",
  "Câu hỏi 2?",
  "Câu hỏi 3?"
]
```

hoặc

```json
[
  {"query": "Câu hỏi 1?"},
  {"query": "Câu hỏi 2?"},
  {"query": "Câu hỏi 3?"}
]
```

### Text Format

```
Câu hỏi 1?
Câu hỏi 2?
Câu hỏi 3?
```

## Kết quả đầu ra

Kết quả sẽ được lưu trong thư mục đầu ra với cấu trúc sau:

### Retrieval Pipeline

```
outputs/retrieval_results/
├── retrieval_result_1_câu_hỏi_1.json
├── retrieval_result_2_câu_hỏi_2.json
├── all_retrieval_results.json
└── retrieval_stats.json
```

### Full Pipeline

```
outputs/
├── full_result_1_câu_hỏi_1.json
├── full_result_2_câu_hỏi_2.json
├── all_pipeline_results.json
├── pipeline_stats.json
├── retrieval_results/
│   ├── retrieval_1_câu_hỏi_1.json
│   └── retrieval_2_câu_hỏi_2.json
└── final_answers/
    ├── answer_1_câu_hỏi_1.json
    ├── answer_1_câu_hỏi_1.txt
    ├── answer_2_câu_hỏi_2.json
    └── answer_2_câu_hỏi_2.txt
```

## Ví dụ nhanh

### 1. Tạo file queries

```bash
echo '[
  "Các thành phần chính của HippoRAG 2 là gì?",
  "Giải thích cách hoạt động của module Triple Extractor trong HippoRAG 2"
]' > queries.json
```

### 2. Chạy pipeline

```bash
python run_retrieval_and_qa_pipeline.py --config config/pipeline_config.json --queries queries.json --output_dir outputs --enable_expansion True
```

### 3. Xem kết quả

```bash
cat outputs/final_answers/answer_1_các_thành_phần_chính_của_hipporag.txt
```

## Tiếp theo

Xem [API Reference](api_reference.md) để biết thêm chi tiết về các module và cách tùy chỉnh pipeline.
