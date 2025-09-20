cd system/PPDX/OnlineRetrievalAndQA/web_demo/
python3 app.py



Bước 2: Mở browser
Vào http://localhost:8000
KHÔNG mở file index.html trực tiếp
Server sẽ tự động serve trang web
🔍 Tại sao không mở file index.html trực tiếp?
❌ File trực tiếp: file:///path/to/index.html - Không có API backend
✅ Qua server: http://localhost:8000 - Có đầy đủ API + WebSocket
📋 Workflow hoàn chỉnh:
Terminal: python .\app.py → Server chạy
Browser: http://localhost:8000 → UI hiển thị
Test: Nhập câu hỏi → PPDX xử lý thật
Stop: Ctrl+C trong terminal → Dừng server