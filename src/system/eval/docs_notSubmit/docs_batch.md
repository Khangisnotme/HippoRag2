📊 Tổng số dòng trong sheet: 300
▶️ Đánh giá 300 dòng từ sheet 'baseline_result_QA_raw' (từ dòng 0 đến 300)      
✅ Đã mapping cột: answer -> reference_answer, ai_answer -> generated_answer    
🔄 Xây dựng document mapping từ supporting_facts...
📚 Đã tạo 390 documents từ supporting_facts
🚀 Chuẩn bị batch processing...
📦 Chia thành 15 batch (mỗi batch 20 dòng)
⚡ Sử dụng 10 worker song song
🔄 Batch 1 bắt đầu (Thread 23032) - 20 dòng
🔄 Batch 2 bắt đầu (Thread 21712) - 20 dòng
🔄 Batch 3 bắt đầu (Thread 24928) - 20 dòng
🔄 Batch 4 bắt đầu (Thread 25612) - 20 dòng
🔄 Batch 5 bắt đầu (Thread 25644) - 20 dòng
🔄 Batch 6 bắt đầu (Thread 27760) - 20 dòng
🔄 Batch 7 bắt đầu (Thread 21228) - 20 dòng
🔄 Batch 8 bắt đầu (Thread 28260) - 20 dòng
D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\.venv\Lib\site-packages\langchain\__init__.py:30: UserWarning: Importing verbose from langchain root module is no longer supported. Please use langchain.globals.set_verbose() / langchain.globals.get_verbose() instead.
  warnings.warn(
🔄 Batch 9 bắt đầu (Thread 28504) - 20 dòng
🔄 Batch 10 bắt đầu (Thread 16432) - 20 dòng


===

Dựa trên log và source code, tôi có thể giải thích cơ chế **batch_size** và **max_workers** hiện tại:

## 🔧 Cơ chế hiện tại

### **Batch Size** 
- **Giá trị**: 20 dòng/batch (được set trong lệnh chạy)
- **Chức năng**: Chia 300 dòng thành 15 batch, mỗi batch xử lý 20 dòng
- **Mục đích**: Giảm tải memory và tăng khả năng kiểm soát tiến độ

### **Max Workers**
- **Giá trị**: 10 workers song song 
- **Chức năng**: Tối đa 10 thread có thể chạy đồng thời
- **Hiện trạng**: 10 batch đầu tiên chạy ngay, 5 batch còn lại đợi queue

## 📊 Phân tích từ log

```
📦 Chia thành 15 batch (mỗi batch 20 dòng)
⚡ Sử dụng 10 worker song song
🔄 Batch 1-10 bắt đầu ngay (Thread IDs khác nhau)
```

## ⚙️ Cơ chế hoạt động

### **ThreadPoolExecutor Logic**:
```python
with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
    # Submit 15 batch → 10 chạy ngay, 5 đợi
    future_to_batch = {
        executor.submit(self._process_batch, batch_data, doc_map, batch_id, progress_tracker): batch_id 
        for batch_id, batch_data in enumerate(batches)
    }
```

### **Batch Processing**:
1. **Mỗi batch** → **1 thread riêng** → **1 GenerationEvaluator riêng**
2. **Thread-safe**: Mỗi worker có evaluator độc lập
3. **Progress tracking**: Thread-safe với `Lock()`

## 🎯 Tối ưu hóa khuyến nghị

### **Tăng hiệu suất**:
```bash
# Tăng batch size, giảm overhead
--batch_size 50 --max_workers 8

# Hoặc giảm batch size nếu memory hạn chế  
--batch_size 10 --max_workers 15
```

### **Cân bằng tài nguyên**:
- **Batch size lớn**: Ít overhead, nhiều memory
- **Max workers cao**: Tăng concurrency, tốn CPU/API calls
- **Sweet spot**: `batch_size=20-50, max_workers=5-10`

## 🚀 Hiệu quả hiện tại

Với 300 dòng, setup hiện tại:
- ✅ **Tốt**: Tận dụng được 10 cores/threads
- ✅ **Ổn định**: Batch size 20 không quá tải memory
- ⚠️ **Có thể tối ưu**: Có thể tăng batch_size lên 30-50 để giảm overhead

Bạn có muốn tôi đề xuất cấu hình tối ưu cho dataset cụ thể không?