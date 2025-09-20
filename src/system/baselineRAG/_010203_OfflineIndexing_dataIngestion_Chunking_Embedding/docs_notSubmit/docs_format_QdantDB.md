Dựa vào hình ảnh, định dạng được lưu trữ có thể được phân tích ngắn gọn như sau:

**1. Cấu trúc dữ liệu chính:**

Dữ liệu được lưu trữ theo từng "Point" (Điểm). Mỗi điểm có vẻ như đại diện cho một bản ghi hoặc một mục dữ liệu riêng lẻ.

**2. Các trường dữ liệu của một "Point":**

* **Payload:** Trường này hiện đang trống trong hình ảnh, nhưng có thể dùng để lưu trữ dữ liệu chính hoặc nội dung liên quan trực tiếp đến điểm đó.
* **metadata (siêu dữ liệu):** Đây là một đối tượng JSON chứa các thông tin mô tả về bản ghi. Trong ví dụ này, nó bao gồm:
    * `source`: Đường dẫn đến nguồn gốc của dữ liệu (`"src\\dataset\\dataset_full\\vimqa_processed\\corpus_v_"`).
    * `doc_id`: ID của tài liệu (`"PH_0"`).
    * `title`: Tiêu đề của tài liệu (`"PH"`).
    * `excel_row`: Số hàng trong file Excel gốc (`1`).
* **page_content (nội dung trang):** Trường này chứa nội dung văn bản chính của bản ghi. Trong ví dụ là: "Các dung dịch nước có giá trị pH nhỏ hơn 7 được coi là tính axit, trong khi các giá trị pH lớn hơn 7 được coi là tính kiềm."
* **Vectors (Vector):** Đây là một trường quan trọng, hiển thị các vector nhúng (embedding vectors) của dữ liệu.
    * `Default vector`: Vector mặc định.
    * `Length`: Chiều dài của vector (ở đây là `768`), cho thấy đây có thể là một vector nhúng được tạo ra từ mô hình học máy (ví dụ: Sentence-BERT, OpenAI embeddings, v.v.) để biểu diễn ngữ nghĩa của `page_content`.

**3. Giao diện quản lý:**

* **Tìm kiếm:** Có thanh "Find similar by ID or filter by payload key:value pair" cho phép tìm kiếm và lọc dữ liệu.
* **Thao tác trên điểm:** Có các biểu tượng để chỉnh sửa, xóa và sao chép điểm.
* **Điều hướng:** Các tab "POINTS", "INFO", "SEARCH QUALITY", "SNAPSHOTS", "VISUALIZE", "GRAPH" cho thấy đây là một hệ thống quản lý cơ sở dữ liệu vector hoặc một nền tảng quản lý dữ liệu có khả năng tìm kiếm ngữ nghĩa.

**Tóm lại:**

Định dạng lưu trữ được thiết kế để chứa các bản ghi dữ liệu có cấu trúc, bao gồm nội dung chính, siêu dữ liệu mô tả và đặc biệt là các vector nhúng (embedding vectors). Việc sử dụng vector nhúng cho thấy hệ thống này có khả năng thực hiện các tác vụ tìm kiếm ngữ nghĩa (semantic search) hoặc tìm kiếm sự tương đồng giữa các bản ghi dựa trên ý nghĩa của chúng, thay vì chỉ tìm kiếm từ khóa truyền thống. Đây là một định dạng thường thấy trong các cơ sở dữ liệu vector hoặc các hệ thống quản lý tri thức.


---

# Payload: 

```bash
payload được sử dụng, nó có thể chứa:

Toàn bộ đối tượng JSON/XML: Nếu dữ liệu của bạn có cấu trúc phức tạp và bạn muốn lưu trữ nó nguyên vẹn.
Các trường dữ liệu không nằm trong metadata hoặc page_content: Ví dụ, nếu bạn có nhiều thuộc tính khác nhau không thuộc loại siêu dữ liệu mà là dữ liệu gốc của bản ghi.
Dữ liệu thô: Dữ liệu chưa qua xử lý, có thể là một chuỗi văn bản dài, một đoạn code, hoặc bất kỳ dữ liệu nào khác mà bạn muốn gắn liền với điểm đó.
Trong trường hợp của hình ảnh, việc page_content và metadata được điền đầy đủ cho thấy dữ liệu đã được tổ chức và lưu trữ một cách có chủ đích, và trường payload có thể không cần thiết hoặc được dành cho các trường hợp sử dụng khác.
```