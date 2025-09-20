Tôi sẽ giải thích cách hoạt động của dotenv khi có nhiều file .env trong dự án:

1. **Cách dotenv hoạt động với nhiều file .env:**

- Khi sử dụng `load_dotenv()`, dotenv sẽ tìm kiếm file .env theo thứ tự sau:
  1. Đầu tiên tìm trong thư mục hiện tại (current directory)
  2. Sau đó tìm trong các thư mục cha (parent directories)
  3. Nếu không tìm thấy, sẽ tìm trong thư mục home của user

- Nếu có nhiều file .env, dotenv sẽ load file đầu tiên tìm thấy và bỏ qua các file khác

2. **Cách xử lý nhiều file .env:**

```python
from dotenv import load_dotenv
import os

# Cách 1: Load file .env cụ thể
load_dotenv(".env.development")  # Load file .env.development
load_dotenv(".env.production")   # Load file .env.production

# Cách 2: Load nhiều file theo thứ tự ưu tiên
load_dotenv(".env.local", override=True)     # Load và ghi đè
load_dotenv(".env.development", override=True) 
load_dotenv(".env", override=True)
```

3. **Best practices khi sử dụng nhiều file .env:**

- Tạo các file .env riêng cho từng môi trường:
  ```
  .env                # File mặc định
  .env.development    # Cho môi trường development
  .env.production     # Cho môi trường production
  .env.local         # Cho cấu hình local (không commit lên git)
  ```

- Trong file `.gitignore`, thêm:
  ```
  .env
  .env.local
  .env.*
  !.env.example
  ```

4. **Ví dụ cụ thể trong dự án của bạn:**

```python
# Trong file run_offline_pipeline.py
from dotenv import load_dotenv
import os

# Load các file .env theo thứ tự ưu tiên
load_dotenv(".env.local", override=True)     # Cấu hình local
load_dotenv(".env.development", override=True) # Cấu hình development
load_dotenv(".env", override=True)           # File mặc định

# Lấy giá trị từ biến môi trường
api_key = os.getenv("HF_API_KEY")
neo4j_uri = os.getenv("NEO4J_URI")
```

5. **Lưu ý quan trọng:**

- Tham số `override=True` cho phép ghi đè giá trị từ các file .env trước đó
- Nên tạo file `.env.example` làm template và commit lên git
- Các file .env thực tế nên được thêm vào `.gitignore`
- Nên có comment rõ ràng trong code về thứ tự load các file .env
- Kiểm tra kỹ các biến môi trường trước khi sử dụng

6. **Ví dụ về nội dung các file .env:**

```bash
# .env.example
HF_API_KEY=your_api_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here

# .env.development
HF_API_KEY=dev_api_key
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=dev_password

# .env.production
HF_API_KEY=prod_api_key
NEO4J_URI=bolt://prod-server:7687
NEO4J_USER=prod_user
NEO4J_PASSWORD=prod_password
```

7. **Xử lý lỗi:**

```python
from dotenv import load_dotenv
import os
import sys

def load_environment():
    """Load environment variables with error handling"""
    try:
        # Load các file .env
        load_dotenv(".env.local", override=True)
        load_dotenv(".env.development", override=True)
        load_dotenv(".env", override=True)
        
        # Kiểm tra các biến bắt buộc
        required_vars = ["HF_API_KEY", "NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"❌ Missing required environment variables: {missing_vars}")
            print("Please check your .env files")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error loading environment: {e}")
        sys.exit(1)
```

Với cách tổ chức này, bạn có thể dễ dàng quản lý các cấu hình khác nhau cho các môi trường khác nhau, đồng thời đảm bảo an toàn cho các thông tin nhạy cảm.
