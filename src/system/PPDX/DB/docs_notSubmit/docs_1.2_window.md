
**Bước 2: Tạo thư mục lưu trữ dữ liệu (Persistent Volume)**

Chúng ta sẽ tạo các thư mục trên ổ đĩa của bạn để Neo4j lưu trữ dữ liệu bền vững.

Ví dụ, bạn có thể tạo trong thư mục `C:\Users\YourUser\neo4j-data` (thay `YourUser` bằng tên người dùng Windows của bạn) hoặc một ổ đĩa khác như `D:\neo4j-data`.

Chạy các lệnh sau trong PowerShell:
```powershell
mkdir C:\neo4j-data\data
mkdir C:\neo4j-data\logs
mkdir C:\neo4j-data\import
mkdir C:\neo4j-data\conf
```
*(Bạn có thể thay `C:\neo4j-data` bằng đường dẫn bạn muốn)*

**Bước 3: Chạy Neo4j Container bằng lệnh `docker run`**

Bây giờ chúng ta sẽ chạy Neo4j bằng lệnh `docker run`. Điều chỉnh cú pháp đường dẫn cho Windows:

```powershell
docker run `
    --name my-neo4j-graphrag `
    -p 7474:7474 `
    -p 7687:7687 `
    -v C:/neo4j-data/data:/data `
    -v C:/neo4j-data/logs:/logs `
    -v C:/neo4j-data/import:/var/lib/neo4j/import `
    -v C:/neo4j-data/conf:/var/lib/neo4j/conf `
    -e NEO4J_AUTH=neo4j/your_super_secret_password `
    --env NEO4J_ACCEPT_LICENSE_AGREEMENT=yes `
    -d neo4j:latest
```

**Giải thích các điểm khác biệt cho Windows:**

* **Dấu ` (backtick):** Trong PowerShell, dấu backtick (`` ` ``) được dùng để xuống dòng lệnh mà không thực thi ngay. Nếu bạn gõ trên một dòng duy nhất, bạn không cần dùng nó.
* **Đường dẫn Volume (`-v`):**
    * **Cú pháp:** `C:/your/path:/container/path`
    * Bạn cần sử dụng **dấu sổ phải (`/`)** thay vì dấu sổ trái (`\`) cho đường dẫn Windows khi ánh xạ volume trong Docker.
    * **Thay thế `C:/neo4j-data`** bằng đường dẫn bạn đã tạo ở Bước 2. Ví dụ: `C:/Users/YourUser/neo4j-data`.
* **Mật khẩu:** Thay thế `your_super_secret_password` bằng một mật khẩu mạnh và an toàn mà bạn sẽ nhớ.

**Ví dụ thực tế (nếu bạn tạo thư mục ở `C:\Users\Teo\neo4j-data`):**
```powershell
docker run `
    --name my-neo4j-graphrag `
    -p 7474:7474 `
    -p 7687:7687 `
    -v C:/Users/Teo/neo4j-data/data:/data `
    -v C:/Users/Teo/neo4j-data/logs:/logs `
    -v C:/Users/Teo/neo4j-data/import:/var/lib/neo4j/import `
    -v C:/Users/Teo/neo4j-data/conf:/var/lib/neo4j/conf `
    -e NEO4J_AUTH=neo4j/MySecurePassword123 `
    --env NEO4J_ACCEPT_LICENSE_AGREEMENT=yes `
    -d neo4j:latest
```

**Bước 4: Kiểm tra Container đang chạy**

Trong cùng cửa sổ PowerShell, chạy lệnh sau:
```powershell
docker ps
```
Bạn sẽ thấy container có tên `my-neo4j-graphrag` đang chạy với trạng thái `Up ... seconds`.

**Bước 5: Truy cập Neo4j Browser**

Mở trình duyệt web của bạn và truy cập địa chỉ:
`http://localhost:7474/`

Đăng nhập thành công với: neo4j/your_super_secret_password

----

## Đã đăng nhập thành công vào neo4j@neo4j://localhost:7687/neo4j - Neo4j Browser. Nhưng: localhost:7687 vẫn chưa có gì 



Bạn đã kết nối thành công vào Neo4j Browser qua địa chỉ `neo4j@neo4j://localhost:7687/neo4j`, điều này rất tốt! Điều đó có nghĩa là Docker container của bạn đang chạy Neo4j và cổng Bolt (7687) đã được ánh xạ chính xác.

Tuy nhiên, bạn nói "localhost:7687 vẫn chưa có gì" - có thể bạn đang mong đợi một giao diện web trực quan hiển thị thông tin như bạn thấy trên các trang web thông thường.

**Hãy làm rõ điều này:**

1.  **Cổng `7687` (Bolt) KHÔNG PHẢI là cổng trình duyệt web.**
    * Cổng `7687` là cổng dành cho giao thức **Bolt**. Đây là giao thức nhị phân (binary protocol) mà các thư viện driver (ví dụ: `neo4j` driver trong Python, Java, Node.js) sử dụng để kết nối và tương tác với cơ sở dữ liệu Neo4j.
    * Khi bạn truy cập `localhost:7687` trực tiếp trong trình duyệt web, bạn sẽ không thấy bất kỳ giao diện nào (hoặc thấy thông báo lỗi "Kết nối bị từ chối" hoặc "Trang không thể truy cập" hoặc một chuỗi ký tự lạ), vì trình duyệt không hiểu giao thức Bolt.

2.  **Cổng `7474` (HTTP) MỚI LÀ CỔNG CỦA NEO4J BROWSER.**
    * Khi bạn chạy lệnh `docker run`, chúng ta đã ánh xạ cổng `7474` của container ra cổng `7474` của máy host.
    * Để truy cập giao diện đồ họa của Neo4j (Neo4j Browser), bạn cần mở trình duyệt web và truy cập địa chỉ:
        `http://localhost:7474/`

**Tóm lại:**

* Việc bạn có thể đăng nhập thành công vào `neo4j@neo4j://localhost:7687/neo4j` qua Neo4j Browser **đã chứng tỏ Neo4j của bạn đang chạy tốt và có thể kết nối được.** Neo4j Browser đang sử dụng giao thức Bolt (qua cổng 7687) để nói chuyện với database và hiển thị giao diện cho bạn.
* Bạn không nên truy cập `localhost:7687` trực tiếp trong trình duyệt web.

---
# Test: 

**Các bước bạn cần làm bây giờ:**

1.  **Mở Neo4j Browser:**
    * Nếu bạn chưa mở, hãy mở trình duyệt web của bạn (Chrome, Firefox, Edge, Safari, v.v.).
    * Nhập địa chỉ sau vào thanh địa chỉ:
        `http://localhost:7474/`
    * Bạn sẽ thấy trang đăng nhập của Neo4j Browser.
    * Đăng nhập bằng username `neo4j` và mật khẩu bạn đã đặt (và đổi nếu được yêu cầu).

2.  **Chạy thử Cypher Query để tạo dữ liệu:**
    Sau khi đăng nhập vào Neo4j Browser (qua cổng 7474), bạn sẽ thấy một giao diện có ô nhập lệnh ở phía trên cùng. Hãy nhập các lệnh Cypher sau để tạo một vài nút và mối quan hệ để bạn có thể thấy dữ liệu:

    * **Tạo một số node:**
        ```cypher
        CREATE (p:Person {name: 'Alice', age: 30})
        CREATE (m:Movie {title: 'The Matrix', released: 1999})
        CREATE (d:Director {name: 'Lana Wachowski'})
        RETURN p, m, d
        ```
    * **Tạo mối quan hệ:**
        ```cypher
        MATCH (p:Person {name: 'Alice'}), (m:Movie {title: 'The Matrix'})
        CREATE (p)-[:LIKES]->(m)
        RETURN p, m
        ```
    * **Tạo thêm mối quan hệ:**
        ```cypher
        MATCH (m:Movie {title: 'The Matrix'}), (d:Director {name: 'Lana Wachowski'})
        CREATE (d)-[:DIRECTED]->(m)
        RETURN m, d
        ```
    * **Xem toàn bộ đồ thị (hoặc một phần):**
        ```cypher
        MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25
        ```
        Bạn cũng có thể nhấp vào biểu tượng graph (hình tròn có các đường nối) bên cạnh kết quả trả về để xem dạng đồ thị trực quan.

Sau khi thực hiện các lệnh Cypher này, bạn sẽ thấy dữ liệu được tạo và hiển thị trong Neo4j Browser, xác nhận rằng database của bạn đã hoạt động bình thường.
