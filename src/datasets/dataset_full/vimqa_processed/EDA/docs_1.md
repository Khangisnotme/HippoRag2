
## Báo cáo về Output và Quy trình Tính toán trong VIMQA Dataset Analysis Tool

### Mục tiêu của công cụ

Công cụ `VIMQAAnalyzer` được thiết kế để phân tích chi tiết 300 câu hỏi đầu tiên của dataset VIMQA, cung cấp các thống kê về độ dài câu hỏi/câu trả lời, phân loại câu hỏi, domain, loại suy luận đa bước, và đánh giá sự phù hợp với mô hình RAG-KG. Các kết quả này được xuất ra dưới dạng báo cáo Markdown, file JSON và biểu đồ hình ảnh.

### I. Các loại Output được tạo ra

Công cụ này tạo ra ba loại output chính:

1.  **Báo cáo Markdown (.md):** Một file báo cáo chi tiết, dễ đọc, tổng hợp tất cả các kết quả phân tích dưới dạng văn bản có cấu trúc. Đây là output trực tiếp mà người dùng có thể đọc để hiểu về dataset.
2.  **File JSON (.json):** Một file chứa toàn bộ kết quả phân tích dưới dạng cấu trúc dữ liệu JSON, tiện lợi cho việc xử lý tự động hoặc tích hợp với các hệ thống khác.
3.  **Biểu đồ hình ảnh (.png):** Một file ảnh chứa 4 biểu đồ tổng hợp, giúp trực quan hóa các phân bố chính của dữ liệu.

### II. Chi tiết Output và Quy trình Tính toán

Chúng ta sẽ đi sâu vào từng phần của output và giải thích cách công cụ tính toán chúng.

#### A. Báo cáo Markdown và File JSON

Cả hai output này chứa cùng các thông tin phân tích, nhưng khác nhau về định dạng. Dưới đây là các phần chính của báo cáo và cách chúng được tính toán:

1.  **Tóm tắt chung (Summary)**
    * **Tổng số câu hỏi phân tích:** `len(self.subset_300)`
        * **Cách tính:** Đơn giản là đếm số lượng phần tử trong danh sách `self.subset_300`, vốn đã được cắt chỉ lấy 300 câu hỏi đầu tiên từ file JSON gốc.
    * **Độ dài câu hỏi trung bình:** `np.mean(question_lengths)`
        * **Cách tính:** Tính độ dài (số từ) của mỗi câu hỏi (`len(item['question'].split())`), thu thập vào danh sách `question_lengths`, sau đó dùng `numpy.mean()` để tính trung bình.
    * **Độ dài câu trả lời trung bình:** `np.mean(answer_lengths)`
        * **Cách tính:** Tương tự như câu hỏi, tính độ dài (số từ) của mỗi câu trả lời (`len(item['answer'].split())`), thu thập vào danh sách `answer_lengths`, sau đó dùng `numpy.mean()` để tính trung bình.
    * **Số supporting facts trung bình:** `np.mean(supporting_facts_counts)`
        * **Cách tính:** Đếm số `supporting_facts` cho mỗi câu hỏi (`len(item['supporting_facts'])`), thu thập vào danh sách `supporting_facts_counts`, sau đó dùng `numpy.mean()` để tính trung bình.
    * **Số title unique:** `len(set(all_titles))`
        * **Cách tính:** Thu thập tất cả các "titles" từ trường `context` của tất cả các câu hỏi vào danh sách `all_titles`. Sau đó, tạo một `set` từ danh sách này để loại bỏ các bản sao và đếm số lượng phần tử trong `set`.

2.  **Phân bố loại câu hỏi (Question Type Distribution)**
    * **Output:** Bảng hiển thị số lượng và tỷ lệ phần trăm của mỗi loại câu hỏi (Yes/No, Other, When, Where, What, Who, Why, How, How many/much).
    * **Cách tính:**
        * Sử dụng phương thức `self.classify_question_type(question)`: Hàm này nhận một chuỗi câu hỏi và áp dụng một bộ quy tắc dựa trên từ khóa và cấu trúc để phân loại. Ví dụ:
            * `"phải không"` hoặc `"đúng không"` -> `Yes/No`
            * Bắt đầu bằng `"ai "` -> `Who`
            * Bắt đầu bằng `"khi nào"` hoặc chứa `"ngày nào"` -> `When`
            * Và tương tự cho `What`, `Where`, `Why`, `How`, `How many/much`.
            * Nếu không khớp với bất kỳ loại nào trên, sẽ là `Other`.
        * Kết quả phân loại của mỗi câu hỏi được đưa vào `collections.Counter` để đếm số lần xuất hiện của mỗi loại.
        * Tỷ lệ được tính bằng cách chia số lượng của từng loại cho tổng số câu hỏi.

3.  **Phân bố Domain (Domain Distribution)**
    * **Output:** Bảng hiển thị số lượng và tỷ lệ phần trăm của mỗi domain (Khác, Thể thao, Chính trị/Lịch sử, Khoa học/Công nghệ, Giải trí/Nghệ thuật, Địa lý/Tự nhiên, Giải thưởng, Nhân vật).
    * **Cách tính:**
        * Sử dụng phương thức `self.classify_domain(title)`: Hàm này nhận một chuỗi `title` (tên bài viết/tài liệu) và áp dụng các quy tắc dựa trên từ khóa có trong `title` để phân loại domain. Ví dụ:
            * Chứa `"f.c."`, `"bóng đá"`, `"champions league"` -> `Thể thao`
            * Chứa `"tổng thống"`, `"chiến tranh"` -> `Chính trị/Lịch sử`
            * Chứa `"nhiệt kế"`, `"hóa học"` -> `Khoa học/Công nghệ`
            * Và tương tự cho các domain khác.
            * Nếu không khớp, hoặc chỉ là các từ đơn giản, sẽ được phân loại là `Khác` hoặc `Nhân vật` (nếu `title` ngắn và không chứa chữ cái viết thường).
        * Phương thức `self.get_question_domain(item)` được dùng để xác định domain chính của một *câu hỏi*. Nó duyệt qua các `supporting_facts` của câu hỏi, phân loại domain cho từng `title` trong `supporting_facts`, sau đó chọn domain xuất hiện nhiều nhất.
        * `collections.Counter` lại được sử dụng để đếm số lượng câu hỏi thuộc mỗi domain.

4.  **Phân bố Multi-hop Reasoning (Multi-hop Reasoning Distribution)**
    * **Output:** Bảng hiển thị số lượng và tỷ lệ phần trăm của các loại reasoning (Single-hop, Bridge entity (2-hop), Multiple properties (2-hop), Complex (3+ hop)).
    * **Cách tính:**
        * Sử dụng phương thức `self.analyze_multihop_type(item)`: Hàm này dựa vào số lượng `supporting_facts` và tính duy nhất của các `title` trong `supporting_facts` để phân loại:
            * `num_facts == 1`: `Single-hop`
            * `num_facts == 2` và `len(set([fact[0] for fact in facts])) == 2` (hai fact từ hai title khác nhau): `Bridge entity (2-hop)`
            * `num_facts == 2` và `len(set([fact[0] for fact in facts])) == 1` (hai fact từ cùng một title): `Multiple properties (2-hop)`
            * `num_facts >= 3`: `Complex (3+ hop)`
        * `collections.Counter` được dùng để đếm số lượng mỗi loại reasoning.

5.  **Sự phù hợp với RAG-KG (Suitability for RAG-KG)**
    * **Output:** Điểm số (ví dụ: 7.6/10), đánh giá (Phù hợp), và các tỷ lệ liên quan.
    * **Cách tính:** Đây là một chỉ số tổng hợp được tính toán dựa trên một công thức riêng:
        * `bridge_entity_ratio`: Tỷ lệ các câu hỏi thuộc loại `Bridge entity (2-hop)` trên tổng số câu hỏi.
        * `multihop_ratio`: Tỷ lệ các câu hỏi có từ 2 `supporting_facts` trở lên (bao gồm cả 2-hop và 3+ hop).
        * `domain_diversity`: Số lượng các domain duy nhất được tìm thấy trong dataset.
        * `suitability_score`: Được tính theo công thức có trọng số:
            `($bridge\_entity\_ratio * 4 + multihop\_ratio * 3 + min(domain\_diversity / 5, 1) * 2 + 1$) / 10 * 10`
            * `Bridge entity reasoning` được gán trọng số cao nhất (4) vì nó là một điểm mạnh của KG trong RAG.
            * `Multi-hop reasoning` cũng có trọng số cao (3).
            * `Domain diversity` có trọng số 2 (chuẩn hóa về 1 nếu có 5 domain trở lên).
            * Cộng thêm 1 điểm cơ bản.
            * Tổng điểm được chuẩn hóa về thang 10.
        * `assessment`: Dựa trên `suitability_score` để đưa ra đánh giá (`Rất phù hợp`, `Phù hợp`, `Trung bình`).

6.  **Top 10 titles phổ biến (Top 10 Popular Titles)**
    * **Output:** Bảng tên các title và số lần chúng xuất hiện.
    * **Cách tính:**
        * Thu thập tất cả các `title` từ trường `context` của mọi câu hỏi vào một danh sách `all_titles`.
        * Sử dụng `collections.Counter` trên danh sách này để đếm tần suất xuất hiện của mỗi `title`.
        * Sắp xếp kết quả và lấy 10 `title` xuất hiện nhiều nhất.

7.  **Ví dụ minh họa (Examples)**
    * **Output:** 3 ví dụ câu hỏi hoàn chỉnh với câu hỏi, câu trả lời, supporting facts, loại câu hỏi, loại reasoning và domain.
    * **Cách tính:** Đơn giản là lấy 3 mục đầu tiên từ `self.subset_300` và trích xuất các thông tin liên quan, đồng thời gọi các hàm phân loại đã xây dựng (`classify_question_type`, `analyze_multihop_type`, `get_question_domain`) để bổ sung thông tin phân tích cho mỗi ví dụ.

#### B. Biểu đồ hình ảnh (.png)

File PNG chứa 4 biểu đồ được tạo bằng Matplotlib và Seaborn:

1.  **Phân bố loại câu hỏi (Pie Chart):**
    * **Cách tính:** Sử dụng dữ liệu từ `Counter(self.classify_question_type(item['question']) for item in self.subset_300)`. Biểu đồ hình tròn trực quan hóa tỷ lệ phần trăm của từng loại câu hỏi.
2.  **Phân bố domain (Pie Chart):**
    * **Cách tính:** Sử dụng dữ liệu từ `Counter(self.get_question_domain(item) for item in self.subset_300)`. Biểu đồ hình tròn trực quan hóa tỷ lệ phần trăm của từng domain.
3.  **Phân bố số supporting facts (Bar Chart):**
    * **Cách tính:** Đếm số `supporting_facts` cho mỗi câu hỏi (`len(item['supporting_facts'])`), sau đó sử dụng `Counter` để tổng hợp số lượng câu hỏi có cùng số lượng `supporting_facts`. Biểu đồ cột hiển thị tần suất của các số `supporting_facts` khác nhau.
4.  **Phân bố độ dài câu hỏi (Histogram):**
    * **Cách tính:** Thu thập độ dài (số từ) của tất cả các câu hỏi vào một danh sách. Biểu đồ histogram hiển thị phân bố tần suất của các độ dài câu hỏi.

---

### Tóm tắt quy trình chung

Quá trình phân tích của công cụ đi theo các bước chính sau:

1.  **Tải dữ liệu:** Đọc file JSON và lấy 300 câu hỏi đầu tiên.
2.  **Phân tích cơ bản:** Tính toán các thống kê như độ dài trung bình, số `supporting_facts` trung bình.
3.  **Phân loại & Đếm:**
    * Với mỗi câu hỏi, áp dụng các hàm phân loại (`classify_question_type`, `get_question_domain`, `analyze_multihop_type`) để gán nhãn cho nó.
    * Sử dụng `collections.Counter` để đếm số lượng các câu hỏi thuộc mỗi nhãn, tạo ra các phân bố.
4.  **Tổng hợp & Đánh giá:** Tổng hợp các tỷ lệ và số liệu để tính điểm phù hợp RAG-KG.
5.  **Trực quan hóa:** Dùng Matplotlib để vẽ biểu đồ từ các phân bố đã tính toán.
6.  **Xuất báo cáo:** Định dạng và ghi các kết quả vào file Markdown và JSON để người dùng dễ dàng truy cập và sử dụng.

Công cụ này đã được thiết kế một cách có hệ thống để cung cấp một cái nhìn toàn diện về dataset VIMQA dựa trên các đặc điểm quan trọng cho các ứng dụng QA, đặc biệt là những ứng dụng liên quan đến Retrieval-Augmented Generation và Knowledge Graphs.