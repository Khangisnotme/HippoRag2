# Hệ Thống Đánh Giá RAG (Retrieval-Augmented Generation)

## 1. Cấu Trúc Evaluation

Hệ thống đánh giá RAG được chia thành 3 thành phần chính:

### 1.1. Retrieval Evaluation
- Đánh giá khả năng tìm kiếm tài liệu liên quan
- Kiểm tra độ chính xác của việc retrieve
- Phát hiện tài liệu không liên quan
- Xác định thông tin bị thiếu

### 1.2. Generation Evaluation
- Đánh giá chất lượng câu trả lời được sinh ra
- Kiểm tra độ chính xác của thông tin
- Phát hiện thông tin bịa đặt (hallucinations)
- Đánh giá độ đầy đủ của câu trả lời

### 1.3. Tổng Hợp Đánh Giá
- Kết hợp kết quả từ retrieval và generation
- Tạo báo cáo tổng hợp
- Đưa ra khuyến nghị cải thiện
- Tạo biểu đồ trực quan

## 2. Các Chỉ Số Đánh Giá

### 2.1. Retrieval Metrics
- **Relevance Score**: Điểm đánh giá độ liên quan (0-100)
- **Precision**: Tỷ lệ tài liệu liên quan trong số tài liệu retrieve
- **Recall**: Tỷ lệ tài liệu liên quan được retrieve
- **Irrelevant Docs**: Danh sách tài liệu không liên quan
- **Missing Topics**: Các chủ đề/thông tin bị thiếu

### 2.2. Generation Metrics
- **LLM Score**: Điểm đánh giá tổng thể từ LLM (0-100)
- **BLEU Scores**: Đánh giá độ chính xác từ vựng (BLEU-1 đến BLEU-4)
- **Rouge-L**: Đánh giá độ chính xác cấu trúc câu
- **F1 Score**: Đánh giá độ chính xác tổng hợp
- **Missing Information**: Thông tin bị thiếu trong câu trả lời
- **Hallucinations**: Thông tin bịa đặt trong câu trả lời

### 2.3. Detailed Scores
- **Accuracy**: Độ chính xác của thông tin
- **Completeness**: Độ đầy đủ của câu trả lời
- **Relevance**: Độ liên quan với câu hỏi
- **Clarity**: Độ rõ ràng của câu trả lời
- **Consistency**: Tính nhất quán với nguồn

## 3. Các File Chức Năng

### 3.1. evaluator_retrieval.py
- Class `RetrievalEvaluator`: Đánh giá khâu retrieval
- Tính toán precision và recall
- Phát hiện tài liệu không liên quan
- Xác định thông tin bị thiếu

### 3.2. evaluator_generation.py
- Class `GenerationEvaluator`: Đánh giá khâu generation
- Tính toán BLEU, Rouge-L, F1 scores
- Phát hiện hallucinations
- Đánh giá chất lượng ngôn ngữ

### 3.3. evaluator.py
- Class `RAGEvaluator`: Đánh giá tổng hợp
- Kết hợp kết quả từ retrieval và generation
- Tạo báo cáo chi tiết
- Tạo biểu đồ trực quan

### 3.4. test_rag_evaluation.py
- File test toàn bộ hệ thống
- Tạo dữ liệu mẫu
- Chạy các test case
- Hiển thị kết quả đánh giá

## 4. Phân Tích Output Mẫu

### 4.1. Retrieval Output
```python
{
    "relevance_score": 85,
    "retrieved_docs_count": 4,
    "irrelevant_docs": [0, 3],
    "missing_topics": ["ứng dụng cụ thể", "ví dụ thực tế"],
    "precision": 0.50,
    "recall": 0.22
}
```

### 4.2. Generation Output
```python
{
    "llm_score": 85,
    "bleu_1": 0.583,
    "bleu_2": 0.364,
    "bleu_3": 0.200,
    "bleu_4": 0.111,
    "rouge_l": 0.667,
    "f1": 0.667,
    "missing_information": ["chi tiết về ứng dụng"],
    "hallucinations": ["thông tin không có trong nguồn"]
}
```

## 5. Phân Tích Metrics

### 5.1. Metrics Có Thể Thừa
- **BLEU-3 và BLEU-4**: Ít được sử dụng trong thực tế, có thể bỏ
- **Context-based BLEU**: Kém hiệu quả khi không có reference answer

### 5.2. Cách Tính Các Metrics

#### BLEU Score
```python
def _calculate_bleu(generated_tokens, reference_tokens, n):
    # Tạo n-grams
    gen_ngrams = _get_ngrams(generated_tokens, n)
    ref_ngrams = _get_ngrams(reference_tokens, n)
    
    # Đếm matches
    matches = sum(min(gen_counter[ngram], ref_counter[ngram]) 
                 for ngram in gen_counter)
    
    # Tính precision
    precision = matches / len(gen_ngrams)
    
    # Brevity penalty
    bp = exp(1 - len(reference_tokens) / len(generated_tokens))
    
    return bp * precision
```

#### Rouge-L Score
```python
def _calculate_rouge_l(generated_tokens, reference_tokens):
    # Tính LCS length
    lcs_length = _lcs_length(generated_tokens, reference_tokens)
    
    # Tính precision và recall
    precision = lcs_length / len(generated_tokens)
    recall = lcs_length / len(reference_tokens)
    
    # Tính F1
    return 2 * precision * recall / (precision + recall)
```

#### F1 Score
```python
def _calculate_f1(generated_tokens, reference_tokens):
    # Tính intersection
    intersection = set(generated_tokens) & set(reference_tokens)
    
    # Tính precision và recall
    precision = len(intersection) / len(generated_tokens)
    recall = len(intersection) / len(reference_tokens)
    
    # Tính F1
    return 2 * precision * recall / (precision + recall)
```

## 6. Cải Tiến Đề Xuất

1. **Tối Ưu Metrics**:
   - Bỏ BLEU-3 và BLEU-4
   - Thêm ROUGE-1 và ROUGE-2
   - Thêm METEOR score

2. **Cải Thiện Đánh Giá**:
   - Thêm đánh giá ngữ nghĩa
   - Thêm đánh giá tính nhất quán
   - Thêm đánh giá độ tin cậy

3. **Tối Ưu Hiệu Suất**:
   - Cache kết quả đánh giá
   - Parallel processing cho batch evaluation
   - Tối ưu hóa prompts
