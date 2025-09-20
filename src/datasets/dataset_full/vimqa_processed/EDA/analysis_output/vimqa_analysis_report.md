# Báo cáo phân tích Dataset VIMQA - 300 câu đầu tiên

**Ngày tạo:** 2025-06-07 04:26:35
**File dữ liệu:** vimqa_dev_300_vi.json

## Tóm tắt

- **Tổng số câu hỏi phân tích:** 300
- **Độ dài câu hỏi trung bình:** 13.2 từ
- **Độ dài câu trả lời trung bình:** 4.6 từ
- **Số supporting facts trung bình:** 1.7
- **Số title unique:** 1431

## Phân bố loại câu hỏi

| Loại câu hỏi | Số lượng | Tỷ lệ |
|--------------|----------|-------|
| Other | 163 | 54.3% |
| Yes/No | 98 | 32.7% |
| When | 16 | 5.3% |
| Where | 10 | 3.3% |
| What | 10 | 3.3% |
| Who | 3 | 1.0% |

## Phân bố domain

| Domain | Số lượng | Tỷ lệ |
|--------|----------|-------|
| Khác | 277 | 92.3% |
| Thể thao | 14 | 4.7% |
| Chính trị/Lịch sử | 4 | 1.3% |
| Khoa học/Công nghệ | 1 | 0.3% |
| Địa lý/Tự nhiên | 1 | 0.3% |
| Nhân vật | 1 | 0.3% |
| Giải trí/Nghệ thuật | 1 | 0.3% |
| Giải thưởng | 1 | 0.3% |

## Phân bố Multi-hop Reasoning

| Loại reasoning | Số lượng | Tỷ lệ |
|----------------|----------|-------|
| Bridge entity (2-hop) | 190 | 63.3% |
| Single-hop | 97 | 32.3% |
| Complex (3+ hop) | 10 | 3.3% |
| Multiple properties (2-hop) | 3 | 1.0% |

## Sự phù hợp với RAG-KG

- **Điểm phù hợp:** 7.6/10
- **Đánh giá:** Phù hợp
- **Tỷ lệ bridge entity reasoning:** 63.3%
- **Tỷ lệ multi-hop reasoning:** 67.7%
- **Số domain khác nhau:** 8

## Top 10 titles phổ biến

| Title | Số lần xuất hiện |
|-------|------------------|
| Danh sách Tổng thống Hoa Kỳ | 60 |
| Thảo My | 54 |
| PH | 35 |
| Nhiệt kế | 35 |
| Cô gái lắm chiêu | 25 |
| Queens Park Rangers F.C. | 19 |
| Hải cẩu | 18 |
| Nhà Chu | 17 |
| Chelsea F.C. | 15 |
| UEFA Champions League | 14 |

## Ví dụ minh họa

### Ví dụ 1
- **Câu hỏi:** Diego Maradona nhỏ tuổi hơn Rutherford B. Hayes phải không?
- **Câu trả lời:** đúng
- **Supporting facts:** [['Diego Maradona', 0], ['Rutherford B. Hayes', 0]]
- **Loại câu hỏi:** Yes/No
- **Loại reasoning:** Bridge entity (2-hop)
- **Domain:** Khác

### Ví dụ 2
- **Câu hỏi:** Tên núi Lang Biang ở Lạc Dương, Lâm Đồng được giải thích bằng huyền thoại nào
- **Câu trả lời:** chàng K’lang và nàng H'biang
- **Supporting facts:** [['Đỉnh Langbiang', 13]]
- **Loại câu hỏi:** Other
- **Loại reasoning:** Single-hop
- **Domain:** Khác

### Ví dụ 3
- **Câu hỏi:** Album phòng thu đầu tay của Billie Eilish được phát hành vào ngày nào?
- **Câu trả lời:** ngày 29 tháng 3 năm 2019 
- **Supporting facts:** [['Billie Eilish', 4], ['When We All Fall Asleep, Where Do We Go?', 2]]
- **Loại câu hỏi:** When
- **Loại reasoning:** Bridge entity (2-hop)
- **Domain:** Khác

