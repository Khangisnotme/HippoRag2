Tuyệt vời! Dựng Neo4j bằng Docker là một lựa chọn rất hợp lý. Dưới đây là các bước chi tiết để bạn có thể bắt đầu ngay:

**Mục tiêu:**
* Chạy một instance Neo4j trong Docker container.
* Thiết lập để dữ liệu Neo4j được lưu trữ bền vững (persistent) trên máy tính của bạn, không bị mất khi container bị xóa hoặc dừng.
* Cấu hình cổng để có thể truy cập Neo4j Browser và các ứng dụng khác.

---

### Bước 1: Đảm bảo Docker đã được cài đặt

Nếu bạn chưa cài Docker, hãy cài đặt nó trước:
* **Docker Desktop (Windows/macOS):** Truy cập [Docker Desktop](https://www.docker.com/products/docker-desktop) và tải về bản cài đặt.
* **Docker Engine (Linux):** Thực hiện theo hướng dẫn cài đặt trên trang web của Docker cho bản phân phối Linux của bạn (ví dụ: [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)).

Sau khi cài đặt, mở Terminal (hoặc Command Prompt/PowerShell trên Windows) và chạy lệnh sau để kiểm tra xem Docker đã hoạt động chưa:
```bash
docker --version
docker compose version # (Nếu bạn dùng docker compose)
```
Nếu các lệnh trả về phiên bản, Docker đã sẵn sàng.

---

### Bước 2: Tạo thư mục lưu trữ dữ liệu (Persistent Volume)

Để đảm bảo dữ liệu Neo4j của bạn không bị mất khi container bị xóa hoặc dừng, chúng ta sẽ ánh xạ một thư mục trên máy tính của bạn vào trong container.

Tạo một thư mục riêng biệt cho Neo4j. Ví dụ, trên Linux/macOS:
```bash
mkdir -p $HOME/neo4j-data/data
mkdir -p $HOME/neo4j-data/logs
mkdir -p $HOME/neo4j-data/import
mkdir -p $HOME/neo4j-data/conf # Tùy chọn, nếu bạn muốn chỉnh sửa cấu hình
```
Trên Windows, bạn có thể tạo thư mục tương tự, ví dụ: `C:\neo4j-data\data`, `C:\neo4j-data\logs`, v.v.

---

### Bước 3: Chạy Neo4j Container bằng lệnh `docker run`

Bây giờ chúng ta sẽ chạy Neo4j bằng lệnh `docker run`. Đây là lệnh bạn sẽ sử dụng:

```bash
docker run \
    --name my-neo4j-graphrag \
    -p 7474:7474 -p 7687:7687 \
    -v $HOME/neo4j-data/data:/data \
    -v $HOME/neo4j-data/logs:/logs \
    -v $HOME/neo4j-data/import:/var/lib/neo4j/import \
    -v $HOME/neo4j-data/conf:/var/lib/neo4j/conf \
    -e NEO4J_AUTH=neo4j/your_super_secret_password \
    --env NEO4J_ACCEPT_LICENSE_AGREEMENT=yes \
    -d neo4j:latest
```

**Giải thích chi tiết các tùy chọn:**

* `docker run`: Lệnh để chạy một container mới.
* `--name my-neo4j-graphrag`: Đặt tên cho container của bạn là `my-neo4j-graphrag`. Tên này giúp bạn dễ dàng tham chiếu đến container sau này (ví dụ: để dừng, khởi động lại, xóa).
* `-p 7474:7474`: Ánh xạ cổng 7474 của container ra cổng 7474 của máy tính host. Cổng này dùng cho **Neo4j Browser** (giao diện web).
* `-p 7687:7687`: Ánh xạ cổng 7687 của container ra cổng 7687 của máy tính host. Cổng này dùng cho **giao thức Bolt**, là giao thức mặc định mà các driver lập trình (như Python driver) sử dụng để kết nối với Neo4j.
* `-v $HOME/neo4j-data/data:/data`: Ánh xạ (mount) thư mục `$HOME/neo4j-data/data` trên máy tính host của bạn tới thư mục `/data` bên trong container. Đây là nơi Neo4j lưu trữ các file database thực tế. **Rất quan trọng để dữ liệu không bị mất!**
    * **Lưu ý:**
        * Trên Linux/macOS: `$HOME` là một biến môi trường trỏ đến thư mục người dùng của bạn.
        * Trên Windows: Bạn cần thay `$HOME/neo4j-data/data` bằng đường dẫn tuyệt đối như `C:\neo4j-data\data` hoặc `/c/neo4j-data/data` (nếu dùng Git Bash/WSL).
* `-v $HOME/neo4j-data/logs:/logs`: Ánh xạ thư mục logs.
* `-v $HOME/neo4j-data/import:/var/lib/neo4j/import`: Ánh xạ thư mục `import`. Đây là nơi bạn sẽ đặt các file CSV/JSON nếu bạn muốn import dữ liệu lớn vào Neo4j bằng lệnh `LOAD CSV` hoặc `apoc.load.json`.
* `-v $HOME/neo4j-data/conf:/var/lib/neo4j/conf`: (Tùy chọn) Ánh xạ thư mục cấu hình. Điều này cho phép bạn chỉnh sửa file `neo4j.conf` của Neo4j từ máy tính host.
* `-e NEO4J_AUTH=neo4j/your_super_secret_password`: Thiết lập tên người dùng mặc định là `neo4j` và mật khẩu ban đầu. **THAY THẾ `your_super_secret_password` bằng một mật khẩu mạnh và an toàn mà bạn sẽ nhớ!**
* `--env NEO4J_ACCEPT_LICENSE_AGREEMENT=yes`: Đồng ý với các điều khoản cấp phép của Neo4j. Điều này là cần thiết để container khởi động mà không bị chặn.
* `-d neo4j:latest`: Chạy container ở chế độ nền (detached mode), và sử dụng image `neo4j` với tag `latest` (phiên bản ổn định mới nhất). Bạn có thể thay `latest` bằng một phiên bản cụ thể, ví dụ: `neo4j:5.12.0`.

---

### Bước 4: Kiểm tra Container đang chạy

Sau khi chạy lệnh trên, bạn có thể kiểm tra xem container đã khởi động thành công chưa:
```bash
docker ps
```
Bạn sẽ thấy một dòng tương tự như sau (tên container sẽ là `my-neo4j-graphrag`):
```
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                                                                     NAMES
a1b2c3d4e5f6   neo4j:latest   "tini -g -- /docker-e…"   10 seconds ago   Up 8 seconds    0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp, 7473/tcp, 7484/tcp   my-neo4j-graphrag
```
Nếu cột `STATUS` hiển thị `Up ... seconds`, container của bạn đã chạy thành công.

---

### Bước 5: Truy cập Neo4j Browser

Mở trình duyệt web của bạn và truy cập địa chỉ:
`http://localhost:7474/`

Bạn sẽ thấy giao diện đăng nhập của Neo4j Browser.
* **Username:** `neo4j`
* **Password:** Mật khẩu bạn đã đặt trong lệnh `docker run` (`your_super_secret_password`).

Khi đăng nhập lần đầu, Neo4j có thể yêu cầu bạn đổi mật khẩu. Hãy đổi thành một mật khẩu mới và ghi nhớ nó.

---

### Bước 6: Chạy thử Cypher Query

Trong Neo4j Browser, bạn có thể chạy một Cypher query đơn giản để kiểm tra:
```cypher
CREATE (n:TestNode {name: 'Hello Neo4j Docker!'}) RETURN n
```
Sau đó:
```cypher
MATCH (n:TestNode) RETURN n
```
Bạn sẽ thấy node `Hello Neo4j Docker!` xuất hiện.

---

### Các lệnh Docker hữu ích khác:

* **Dừng container:**
    ```bash
    docker stop my-neo4j-graphrag
    ```
* **Khởi động lại container đã dừng:**
    ```bash
    docker start my-neo4j-graphrag
    ```
* **Xem logs của container:**
    ```bash
    docker logs my-neo4j-graphrag
    ```
* **Xóa container (khi không cần nữa, nhưng dữ liệu vẫn còn trong volume):**
    ```bash
    docker rm my-neo4j-graphrag
    ```
* **Xóa container và volume (xóa sạch sẽ mọi thứ, kể cả dữ liệu):**
    ```bash
    docker rm -v my-neo4j-graphrag
    ```
    *Cẩn thận với lệnh này, hãy chắc chắn bạn muốn xóa hết dữ liệu.*

Bạn đã sẵn sàng để bắt đầu xây dựng GraphRAG của mình với Neo4j chạy trong Docker!