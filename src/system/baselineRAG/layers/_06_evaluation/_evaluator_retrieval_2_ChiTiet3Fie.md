Báo cáo về việc đánh giá khâu Retrieval trong hệ thống RAG một cách chi tiết, mạch lạc, và đầy đủ bằng tiếng Việt, có sử dụng các thông tin bạn đã cung cấp, bao gồm cả phần giải thích về Accuracy, Precision, Recall@K, F1-Score, và Hit Rate@K, cùng với phân tích về Macro-averaged và Micro-averaged metrics. 

---

# Báo Cáo Chi Tiết: Đánh Giá Toàn Diện Khâu Retrieval trong Hệ Thống RAG

Đánh giá hiệu suất của module **Retrieval** là yếu tố then chốt để đảm bảo một hệ thống **RAG** (Retrieval-Augmented Generation) hoạt động hiệu quả. Một khâu truy xuất kém chất lượng sẽ dẫn đến việc **LLM** (Large Language Model) nhận được thông tin không đầy đủ, không liên quan, hoặc thậm chí sai lệch, từ đó ảnh hưởng nghiêm trọng đến chất lượng câu trả lời cuối cùng.

Việc đánh giá Retrieval cần được thực hiện một cách toàn diện, sử dụng nhiều chỉ số khác nhau để có cái nhìn đa chiều về hiệu suất. Chúng ta sẽ chia các chỉ số này thành ba nhóm chính, mỗi nhóm sẽ đại diện cho một khía cạnh đánh giá quan trọng.

---

## 1. Nhóm Chỉ Số Non-Rank Based Metrics

Nhóm này bao gồm các chỉ số **không quan tâm đến thứ tự xếp hạng cụ thể** của các tài liệu được truy xuất, mà tập trung vào việc có hay không có tài liệu liên quan trong tập kết quả. Đây là những chỉ số cơ bản, dễ hiểu và thường được dùng để có cái nhìn tổng quan về hiệu suất.

### Mục tiêu:
Đánh giá mức độ bao phủ và độ chính xác cơ bản của các tài liệu được truy xuất, không tính đến vị trí của chúng.

### Các chỉ số chính:

* **Accuracy (Độ chính xác tổng thể):**
    * **Ý nghĩa:** Tỷ lệ các dự đoán đúng trên tổng số dự đoán. Trong ngữ cảnh retrieval, nó đo lường tỷ lệ tài liệu được phân loại đúng là liên quan hoặc không liên quan.
    * **Công thức:** $Accuracy = \frac{\text{TP + TN}}{\text{TP + TN + FP + FN}}$
        * **TP (True Positive):** Số tài liệu **liên quan** được hệ thống **truy xuất đúng**.
        * **TN (True Negative):** Số tài liệu **không liên quan** được hệ thống **không truy xuất đúng**.
        * **FP (False Positive):** Số tài liệu **không liên quan** nhưng bị hệ thống **truy xuất sai**.
        * **FN (False Negative):** Số tài liệu **liên quan** nhưng bị hệ thống **bỏ sót (không truy xuất)**.
    * **Lưu ý:** Để tính Accuracy, chúng ta cần biết tổng số tài liệu trong corpus (tổng TN). Chỉ số này có thể gây hiểu lầm trên các tập dữ liệu mất cân bằng lớp (ví dụ: rất ít tài liệu liên quan so với tổng số).

* **Precision (Độ chính xác):**
    * **Ý nghĩa:** Tỷ lệ các tài liệu được truy xuất thực sự liên quan so với tổng số tài liệu mà hệ thống truy xuất. Nó trả lời câu hỏi "Trong số các tài liệu tôi trả về, bao nhiêu phần trăm là **đúng**?".
    * **Công thức:** $Precision = \frac{\text{TP}}{\text{TP + FP}}$
    * **Ứng dụng:** Quan trọng khi bạn muốn giảm thiểu "kết quả sai" (false positives), đảm bảo chất lượng của các tài liệu được hiển thị cho LLM.

* **Recall@K (Độ phủ / Độ thu hồi tại K):**
    * **Ý nghĩa:** Tỷ lệ các mục liên quan thực sự được truy xuất trong **Top K** kết quả so với tổng số mục liên quan có sẵn trong toàn bộ tập dữ liệu (ground truth). Nó trả lời câu hỏi "Trong tất cả các tài liệu **đúng**, tôi đã tìm được bao nhiêu phần trăm trong Top K?".
    * **Công thức:** $Recall@K = \frac{\text{TP}}{\text{TP + FN}} = \frac{|\text{Relevant} \cap \text{Retrieved@K}|}{|\text{Relevant}|}$
    * **Ứng dụng:** Quan trọng khi bạn muốn đảm bảo không bỏ lỡ các thông tin quan trọng (giảm thiểu "bỏ sót" - false negatives), ví dụ như trong các hệ thống tìm kiếm pháp lý hoặc y tế.

* **F1-Score:**
    * **Ý nghĩa:** Trung bình điều hòa (harmonic mean) của Precision và Recall. F1-Score cung cấp một cái nhìn cân bằng về hiệu suất khi cả Precision và Recall đều quan trọng. Nó đặc biệt hữu ích khi tập dữ liệu bị mất cân bằng.
    * **Công thức:** $F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision + Recall}}$
    * **Ứng dụng:** Hữu ích khi so sánh các hệ thống hoặc mô hình mà không cần phải xem xét riêng lẻ Precision và Recall, đưa ra một chỉ số tổng hợp duy nhất.

* **Hit Rate@K (Tỷ lệ trúng tại K):**
    * **Ý nghĩa:** Tỷ lệ các truy vấn mà hệ thống trả về **ít nhất một mục liên quan** trong Top K kết quả. Nó chỉ quan tâm đến việc có "hit" hay không, không quan tâm số lượng hit.
    * **Công thức:** $HitRate@K = \frac{\text{Số truy vấn có ít nhất 1 hit trong top-K}}{\text{Tổng số truy vấn}}$
    * **Ứng dụng:** Đơn giản, dễ hiểu và thường được sử dụng trong các hệ thống khuyến nghị hoặc các tình huống mà việc có bất kỳ kết quả liên quan nào trong top K là đủ để khởi đầu một trải nghiệm tốt cho người dùng.

### Các phương pháp tính trung bình (Averaging Methods):

Khi đánh giá trên nhiều truy vấn, có hai phương pháp chính để tính trung bình các chỉ số:

* **Macro-averaged (Trung bình Macro):**
    * **Cách tính:** Tính chỉ số cho từng truy vấn độc lập, sau đó lấy trung bình cộng các chỉ số đó.
    * **Ưu điểm:** Mỗi truy vấn có trọng số bằng nhau, không quan tâm đến số lượng tài liệu liên quan của truy vấn đó.
    * **Phù hợp khi:** Các truy vấn có tầm quan trọng như nhau.
    * **Ví dụ:** Nếu có 3 truy vấn với Precision lần lượt là 0.8, 0.6, 0.4. Macro Precision = $(0.8 + 0.6 + 0.4) / 3 = 0.6$.

* **Micro-averaged (Trung bình Micro):**
    * **Cách tính:** Tổng hợp TP, FP, FN từ tất cả các truy vấn, sau đó tính chỉ số trên tổng hợp đó.
    * **Ưu điểm:** Phản ánh hiệu suất tổng thể trên toàn bộ dữ liệu. Các truy vấn có nhiều tài liệu liên quan (hoặc nhiều tài liệu được truy xuất) sẽ có ảnh hưởng lớn hơn đến kết quả cuối cùng.
    * **Phù hợp khi:** Cần đánh giá hiệu suất trên tập dữ liệu lớn và không muốn các truy vấn nhỏ ảnh hưởng quá nhiều đến kết quả.
    * **Ví dụ:**
        * Truy vấn 1: TP=2, FP=1, FN=1
        * Truy vấn 2: TP=3, FP=2, FN=0
        * Truy vấn 3: TP=1, FP=1, FN=2
        * Tổng: TP=6, FP=4, FN=3
        * Micro Precision = $6 / (6+4) = 0.6$.

* **Sự khác biệt chính:**
    * **Macro-averaged:** Mỗi truy vấn có trọng số bằng nhau, không quan tâm đến số lượng tài liệu liên quan/được truy xuất.
    * **Micro-averaged:** Các truy vấn với nhiều tài liệu liên quan/được truy xuất sẽ có ảnh hưởng lớn hơn đến kết quả cuối cùng.

### Ví dụ về Đánh giá kết quả của Non-Rank Metrics:

Giả sử chúng ta có 3 truy vấn và đang đánh giá với $K=5$, và tổng số tài liệu trong corpus là 100.

* **Truy vấn 1 (Q1):**
    * **Tài liệu liên quan (ground truth):** `[doc1, doc3, doc6]`
    * **Tài liệu truy xuất (Top 5):** `[doc1, doc2, doc3, doc4, doc5]`
    * **Tính toán:**
        * TP = 2 (`doc1`, `doc3`)
        * FP = 3 (`doc2`, `doc4`, `doc5`)
        * FN = 1 (`doc6`)
        * Precision = $2 / (2+3) = 0.4$
        * Recall@5 = $2 / (2+1) = 0.667$
        * F1-Score = $2 \times (0.4 \times 0.667) / (0.4 + 0.667) \approx 0.500$
        * Hit Rate (cho Q1) = 1 (có hit)
        * TN (ước lượng): `100 - (2+3+1)` (total docs - TP - FP - FN) = `100 - 6 = 94`
        * Accuracy = $(2 + 94) / 100 = 0.96$

* **Truy vấn 2 (Q2):**
    * **Tài liệu liên quan (ground truth):** `[doc11, doc12]`
    * **Tài liệu truy xuất (Top 5):** `[doc7, doc8, doc9, doc10, doc_X]`
    * **Tính toán:**
        * TP = 0
        * FP = 5 (`doc7`, `doc8`, `doc9`, `doc10`, `doc_X`)
        * FN = 2 (`doc11`, `doc12`)
        * Precision = $0 / 5 = 0.0$
        * Recall@5 = $0 / 2 = 0.0$
        * F1-Score = $0.0$
        * Hit Rate (cho Q2) = 0 (không có hit)
        * TN (ước lượng): `100 - (0+5+2)` = `93`
        * Accuracy = $(0 + 93) / 100 = 0.93$

* **Truy vấn 3 (Q3):**
    * **Tài liệu liên quan (ground truth):** `[doc13, doc14]`
    * **Tài liệu truy xuất (Top 5):** `[doc13, doc14, doc15, doc16, doc17]`
    * **Tính toán:**
        * TP = 2 (`doc13`, `doc14`)
        * FP = 3 (`doc15`, `doc16`, `doc17`)
        * FN = 0
        * Precision = $2 / (2+3) = 0.4$
        * Recall@5 = $2 / (2+0) = 1.0$
        * F1-Score = $2 \times (0.4 \times 1.0) / (0.4 + 1.0) \approx 0.571$
        * Hit Rate (cho Q3) = 1 (có hit)
        * TN (ước lượng): `100 - (2+3+0)` = `95`
        * Accuracy = $(2 + 95) / 100 = 0.97$

**Tổng kết trung bình (trên 3 truy vấn):**

* **Macro-averaged Metrics:**
    * **Macro Precision:** $(0.4 + 0.0 + 0.4) / 3 \approx \mathbf{0.267}$
    * **Macro Recall@5:** $(0.667 + 0.0 + 1.0) / 3 \approx \mathbf{0.556}$
    * **Macro F1-Score:** $(0.500 + 0.0 + 0.571) / 3 \approx \mathbf{0.357}$
    * **Macro Accuracy:** $(0.96 + 0.93 + 0.97) / 3 \approx \mathbf{0.953}$

* **Micro-averaged Metrics:**
    * **Tổng TP:** $2 + 0 + 2 = 4$
    * **Tổng FP:** $3 + 5 + 3 = 11$
    * **Tổng FN:** $1 + 2 + 0 = 3$
    * **Micro Precision:** $4 / (4+11) = 4/15 \approx \mathbf{0.267}$
    * **Micro Recall:** $4 / (4+3) = 4/7 \approx \mathbf{0.571}$
    * **Micro F1-Score:** $2 \times (0.267 \times 0.571) / (0.267 + 0.571) \approx \mathbf{0.364}$

* **Hit Rate@5 cho toàn bộ tập truy vấn:**
    * Số truy vấn có hit: 2 (Q1, Q3)
    * Tổng số truy vấn: 3
    * **Hit Rate@5:** $2 / 3 \approx \mathbf{0.667}$

### Đánh giá chất lượng từ các chỉ số Non-Rank:

* **Hit Rate (0.667):** TỐT (60-80% truy vấn có kết quả liên quan). Điều này có nghĩa là hệ thống của bạn khá tốt trong việc đảm bảo hầu hết các truy vấn đều nhận được ít nhất một tài liệu hữu ích.
* **Precision (Macro 0.267 / Micro 0.267):** THẤP (nhiều kết quả không liên quan). Chỉ số này cho thấy, trong số các tài liệu hệ thống trả về, một phần lớn trong số đó không thực sự hữu ích. Điều này có thể làm nhiễu LLM hoặc gây mất thời gian xử lý.
* **Recall (Macro 0.556 / Micro 0.571):** TRUNG BÌNH. Hệ thống của bạn tìm được hơn một nửa số tài liệu liên quan có thể có. Có chỗ để cải thiện để không bỏ sót các thông tin quan trọng.

---

## 2. Nhóm Chỉ Số Rank-Based Metrics

Nhóm này bao gồm các chỉ số **quan tâm đến thứ tự xếp hạng** của các tài liệu được truy xuất. Các chỉ số này đánh giá cao hơn những hệ thống có khả năng đặt các tài liệu liên quan ở vị trí cao trong danh sách kết quả.

### Mục tiêu:
Đánh giá chất lượng của danh sách xếp hạng tài liệu, phản ánh trải nghiệm người dùng khi các kết quả tốt nhất nên xuất hiện ở đầu.

### Các chỉ số chính:

* **Mean Reciprocal Rank (MRR):**
    * **Ý nghĩa:** Trung bình của nghịch đảo thứ hạng của **kết quả liên quan đầu tiên** được tìm thấy. MRR tập trung vào việc hệ thống có nhanh chóng tìm ra câu trả lời đúng nhất hay không.
    * **Công thức:** $MRR = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{\text{rank}_i}$, trong đó $\text{rank}_i$ là thứ hạng của tài liệu liên quan đầu tiên cho truy vấn thứ $i$. Nếu không tìm thấy tài liệu liên quan nào, giá trị đó là 0.
    * **Ứng dụng:** Rất hữu ích trong các ứng dụng hỏi đáp (QA) hoặc các tình huống mà người dùng chỉ cần tìm một kết quả "đúng" duy nhất và quan tâm đến việc nó xuất hiện ở vị trí nào (càng cao càng tốt).

* **Mean Average Precision (MAP):**
    * **Ý nghĩa:** Trung bình của Average Precision (AP) trên một tập hợp các truy vấn. AP tính toán Precision tại mỗi điểm mà một mục liên quan được tìm thấy và lấy trung bình. MAP đánh giá chất lượng của danh sách xếp hạng trên nhiều truy vấn, ưu tiên các hệ thống đặt các mục liên quan lên vị trí cao hơn.
    * **Công thức (AP cho một truy vấn):** $\sum_{k=1}^{n} (P(k) \times \text{rel}(k)) / (\text{Số tài liệu liên quan})$, trong đó $P(k)$ là precision tại k (tỷ lệ tài liệu liên quan trong top k), $\text{rel}(k)$ là 1 nếu tài liệu tại k liên quan, 0 nếu không.
    * **Công thức (MAP):** $MAP = \frac{1}{N} \sum_{i=1}^{N} AP_i$, trong đó $AP_i$ là Average Precision cho truy vấn thứ $i$.
    * **Ứng dụng:** Một trong những chỉ số mạnh mẽ và được sử dụng rộng rãi nhất để đánh giá các hệ thống tìm kiếm và xếp hạng, vì nó có tính đến thứ hạng của các mục liên quan. Một hệ thống có MAP cao là một hệ thống tốt trong việc đưa các kết quả liên quan lên đầu.

* **Normalized Discounted Cumulative Gain (NDCG@K):**
    * **Ý nghĩa:** Đánh giá chất lượng của danh sách xếp hạng, đặc biệt hữu ích khi các mục có các **mức độ liên quan khác nhau** (graded relevance, ví dụ: 0 = không liên quan, 1 = liên quan ít, 2 = liên quan vừa, 3 = rất liên quan). NDCG cho điểm cao hơn cho các mục có mức độ liên quan cao được xếp hạng ở các vị trí đầu.
    * **Công thức (DCG):** $DCG_k = \sum_{i=1}^{k} \frac{rel_i}{\log_2(i+1)}$, trong đó $rel_i$ là mức độ liên quan của tài liệu ở vị trí $i$.
    * **Công thức (IDCG):** $IDCG_k$ là DCG lý tưởng (tài liệu liên quan nhất ở đầu, được sắp xếp theo mức độ liên quan giảm dần).
    * **Công thức (NDCG):** $NDCG_k = \frac{DCG_k}{IDCG_k}$
    * **Ứng dụng:** Chỉ số hàng đầu cho các hệ thống tìm kiếm và khuyến nghị hiện đại, nơi mà việc phân biệt mức độ liên quan và thứ tự của các kết quả là cực kỳ quan trọng đối với trải nghiệm người dùng.

---

## 3. Nhóm Chỉ Số Đánh Giá Bằng LLMs

Với sự phát triển của các mô hình ngôn ngữ lớn, việc sử dụng LLM để đánh giá khâu retrieval ngày càng trở nên phổ biến. Phương pháp này tận dụng khả năng hiểu ngữ nghĩa sâu sắc của LLM để đưa ra những đánh giá chất lượng cao mà không cần đến ground truth được gán nhãn thủ công phức tạp.

### Mục tiêu:
Đánh giá chất lượng ngữ cảnh được truy xuất từ góc độ hiểu biết của LLM, tập trung vào độ liên quan, tính đầy đủ và khả năng trả lời câu hỏi.

### Các chỉ số chính:

* **Context Relevance (Độ liên quan của ngữ cảnh):**
    * **Ý nghĩa:** LLM đánh giá mức độ liên quan của từng tài liệu (hoặc toàn bộ tập hợp tài liệu) được truy xuất đối với câu hỏi ban đầu. Điểm số thường được xếp hạng trên thang điểm (ví dụ: 0-100).
    * **Cách thức:** Gửi câu hỏi và các tài liệu truy xuất cho LLM và yêu cầu nó đánh giá xem các tài liệu đó có giúp trả lời câu hỏi hay không, và mức độ liên quan là bao nhiêu.
    * **Ứng dụng:** Đảm bảo rằng LLM không bị "nhiễu" bởi quá nhiều thông tin không liên quan, giúp nó tập trung vào các thông tin chính xác. Đây là một chỉ số quan trọng trong các framework đánh giá RAG hiện đại như RAGAs.

* **Context Sufficiency (Tính đầy đủ của ngữ cảnh):**
    * **Ý nghĩa:** LLM đánh giá xem các tài liệu được truy xuất có đủ thông tin để LLM có thể trả lời câu hỏi một cách đầy đủ và chính xác hay không.
    * **Cách thức:** Gửi câu hỏi, các tài liệu truy xuất, và câu trả lời lý tưởng (nếu có) cho LLM và yêu cầu nó đánh giá mức độ đầy đủ của ngữ cảnh.
    * **Ứng dụng:** Đảm bảo rằng retrieval không chỉ tìm được tài liệu liên quan mà còn đủ thông tin để LLM tạo ra câu trả lời chất lượng cao.

* **Faithfulness (Tính chân thực / Trung thực):**
    * **Ý nghĩa:** LLM đánh giá mức độ trung thực của câu trả lời được tạo ra so với các tài liệu ngữ cảnh được cung cấp. Mặc dù đây là chỉ số của generation, nó phụ thuộc trực tiếp vào chất lượng của retrieval (nếu ngữ cảnh sai lệch, câu trả lời khó trung thực).
    * **Cách thức:** LLM so sánh từng fact trong câu trả lời với các tài liệu truy xuất để xác minh tính chính xác.
    * **Ứng dụng:** Giảm thiểu "hallucination" (LLM tự bịa thông tin) bằng cách đảm bảo thông tin trong câu trả lời luôn được hỗ trợ bởi ngữ cảnh.

* **Answer Relevance (Độ liên quan của câu trả lời):**
    * **Ý nghĩa:** LLM đánh giá mức độ liên quan của câu trả lời được tạo ra đối với câu hỏi ban đầu.
    * **Cách thức:** LLM nhận câu hỏi và câu trả lời, sau đó đánh giá xem câu trả lời có trực tiếp giải quyết câu hỏi hay không.
    * **Ứng dụng:** Đảm bảo LLM không đi lạc đề, cung cấp câu trả lời đúng trọng tâm.

---

## Cấu Trúc File Excel để Quản Lý Dữ Liệu Đánh Giá (`retrieve_evaluation_data.xlsx`)

Để kết nối dữ liệu từ các file Python và quản lý quá trình đánh giá một cách hiệu quả, việc sử dụng một file Excel là rất tiện lợi. File này sẽ là trung tâm cho việc nhập liệu và quản lý các cặp (Query, Retrieved Docs, Relevant Docs).

### Cấu trúc Sheet chính: `Evaluation_Data`

| Cột ID Truy Vấn (Query ID) | Câu Hỏi (Query Text) | Tài Liệu Được Truy Xuất (Retrieved Document IDs) | Tài Liệu Liên Quan Thực Tế (Relevant Document IDs) | Top K (Ví dụ) |
| :------------------------- | :------------------- | :--------------------------------------------- | :--------------------------------------------- | :------------ |
| Q1                         | Hỏi về lịch sử Việt Nam | `doc_lichsu_1;doc_nghethuat_A;doc_lichsu_2`   | `doc_lichsu_1;doc_lichsu_2;doc_lichsu_3`      | 5             |
| Q2                         | Nguyên lý RAG là gì?   | `doc_rag_A;doc_llm_B;doc_rag_C;doc_IR_D`     | `doc_rag_A;doc_rag_C`                        | 10            |
| Q3                         | Ẩm thực Hà Nội          | `doc_pho_HN;doc_chagio_SG;doc_bunthang_HN`     | `doc_pho_HN;doc_bunthang_HN`                   | 3             |
| ...                        | ...                  | ...                                          | ...                                          | ...           |

### Mô tả các cột:

* **Cột ID Truy Vấn (Query ID):** ID duy nhất cho mỗi truy vấn. Giúp theo dõi và phân tích kết quả từng truy vấn.
* **Câu Hỏi (Query Text):** Nội dung câu hỏi mà người dùng gửi đến hệ thống RAG.
* **Tài Liệu Được Truy Xuất (Retrieved Document IDs):**
    * Danh sách các ID tài liệu mà hệ thống Retrieval của bạn đã trả về cho câu hỏi này.
    * **Định dạng:** Các ID nên được phân tách bằng một ký tự cố định (ví dụ: `;` hoặc `,`) để dễ dàng đọc và phân tích bằng Python. **Thứ tự của các ID trong danh sách này là quan trọng**, vì nó phản ánh thứ hạng truy xuất của hệ thống (doc đầu tiên là rank 1, v.v.).
    * Ví dụ: `doc_lichsu_1;doc_nghethuat_A;doc_lichsu_2`
* **Tài Liệu Liên Quan Thực Tế (Relevant Document IDs):**
    * Danh sách các ID tài liệu mà bạn (hoặc chuyên gia) xác định là **thực sự liên quan** đến câu hỏi đó (ground truth). Đây là "đáp án" để so sánh với kết quả truy xuất.
    * **Định dạng:** Tương tự, các ID nên được phân tách bằng một ký tự cố định. **Thứ tự của các ID trong danh sách này không quan trọng**, vì chúng ta chỉ quan tâm đến sự tồn tại của chúng.
    * Ví dụ: `doc_lichsu_1;doc_lichsu_2;doc_lichsu_3`
* **Top K (Ví dụ):** Giá trị `K` bạn muốn sử dụng để đánh giá các chỉ số `@K` cho truy vấn đó. Bạn có thể để trống nếu muốn sử dụng K mặc định, hoặc chỉ định riêng cho từng truy vấn.

### Các Sheet phụ (tùy chọn):

* **`Corpus_Document_IDs`:** Một sheet chứa danh sách tất cả các ID tài liệu duy nhất trong toàn bộ corpus của bạn. Điều này hữu ích để tính toán **True Negatives** và **Accuracy** một cách chính xác.
* **`LLM_Relevance_Scores`:** Nếu bạn thực hiện đánh giá bằng LLM, bạn có thể tạo một sheet để lưu trữ các điểm số relevance, sufficiency, faithfulness do LLM đánh giá cho từng cặp (câu hỏi, tài liệu truy xuất, câu trả lời).

---

## Quy trình Đánh giá Tổng thể:

1.  **Chuẩn bị Dữ liệu:** Điền file `retrieve_evaluation_data.xlsx` với các truy vấn, tài liệu được truy xuất và tài liệu liên quan thực tế. Đảm bảo dữ liệu được định dạng đúng.
2.  **Chạy Đánh giá Non-Rank:** Sử dụng module đánh giá Non-Rank (`metrics_non_rank.py`) để đọc dữ liệu từ Excel, tính toán Precision@K, Recall@K, F1-Score, Accuracy và Hit Rate@K.
3.  **Chạy Đánh giá Rank-Based:** Sử dụng module đánh giá Rank-Based (`metrics_rank.py`) để đọc dữ liệu từ Excel, tính toán MRR, MAP và NDCG@K.
4.  **Chạy Đánh giá LLM-based (Nếu có):** Sử dụng module đánh giá LLM-based (`metrics_llm_based.py`) để gọi LLM và thu thập các điểm số liên quan.
5.  **Tổng hợp Báo cáo:** Kết hợp kết quả từ ba nhóm đánh giá vào một báo cáo tổng thể, bao gồm cả phân tích chi tiết và các đề xuất cải thiện.

Bằng cách sử dụng phương pháp đánh giá toàn diện này, bạn sẽ có cái nhìn sâu sắc về hiệu suất của module Retrieval trong hệ thống RAG của mình, từ đó đưa ra các quyết định sáng suốt để tối ưu hóa và cải thiện hệ thống.

