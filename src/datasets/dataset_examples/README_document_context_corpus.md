
# 3. Cách xây dựng **hệ thống QA dạng retriever–reader** trên HotpotQA: **định nghĩa rõ các khái niệm: context, document, corpus**

---

## 🧠 Định nghĩa CHUẨN – theo từng tầng:

---

### 🟩 **1. `document` là gì?**

> Một **document** là **một đoạn văn** tương ứng với một tiêu đề (`title`) và danh sách các câu (`sentences`) trong đó.


```json
[
  "Donald Trump",
  [
    "Là chủ tịch kiêm tổng giám đốc của The Trump Organization...",
    "Ông nổi tiếng trên toàn nước Mỹ nhờ sự nghiệp..."
  ]
]
```

→ Đây là **1 document** có:

* `title = "Donald Trump"`
* `paragraph = 2 câu`

✅ **HotpotQA context được chia theo document** như thế này.

---

### 🟦 **2. `context` là gì?**

> `context` là **tập hợp các documents liên quan đến một câu hỏi**.

👉 Trong ví dụ bạn gửi, `context` là danh sách gồm **10 documents**:

```json
"context": [
  ["Charles J. Pedersen", [ ... ]],
  ["Joseph Louis Gay-Lussac", [ ... ]],
  ...
  ["Donald Trump", [ ... ]]
]
```

🔍 Trong đó:

* Có thể có 1–2 đoạn **liên quan trực tiếp đến câu hỏi** (supporting\_facts)
* Các đoạn còn lại là **distractors** – để tăng độ khó & kiểm tra khả năng reasoning

---

### 🟥 **3. `supporting_facts` là gì?**

> Là **(title, sent\_id)** – chỉ định rõ đoạn và câu nào trong `context` là **câu then chốt** để suy luận ra đáp án.

👉 Trong ví dụ:

```json
"supporting_facts": [["Donald Trump", 1]]
```

→ Câu thứ 2 (index 1) trong đoạn `"Donald Trump"` là fact quan trọng nhất.

---

### 🟨 **4. `corpus` là gì?**

> `corpus` là **toàn bộ tập hợp các documents** mà hệ thống **retriever** có thể truy xuất để tìm ra các `context` phù hợp cho một câu hỏi bất kỳ.

---

#### Có 2 dạng phổ biến:

| Kiểu corpus                               | Nội dung gồm                                      | Mục đích                                                               |
| ----------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------- |
| 🧪 **Closed corpus** (Distractor setting) | Chỉ lấy các `context` của HotpotQA dev/train      | Dùng để test mô hình reasoning, kiểm tra phân biệt đoạn nào quan trọng |
| 🌐 **Open corpus** (Fullwiki setting)     | Gồm toàn bộ Wikipedia (\~5M docs) hoặc corpus lớn | Dùng để test retriever như Dense Passage Retrieval, RAG, ColBERT       |


---

## 🎯 Tổng kết trên ví dụ

| Thành phần         | Ý nghĩa cụ thể trong ví dụ bạn gửi                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------- |
| `document`         | Một mục trong `context`, ví dụ: `["Donald Trump", [...]]`                                               |
| `context`          | Danh sách 10 documents: Charles Pedersen, Mike Pence, Donald Trump…                                     |
| `supporting_facts` | Chỉ `("Donald Trump", 1)` là thông tin then chốt để trả lời                                             |
| `corpus`           | Nếu gom 10 đoạn này **+** hàng nghìn đoạn khác từ toàn bộ HotpotQA → thành corpus để retriever tìm kiếm |

---

## 🔧 Mở rộng: Khi triển khai hệ thống QA

* **Reader model** (BERT QA, T5 QA): input là `question + context` → trả về `answer`
* **Retriever model** (BM25, DPR, RAG): input là `question`, output là top-k documents từ **corpus**

