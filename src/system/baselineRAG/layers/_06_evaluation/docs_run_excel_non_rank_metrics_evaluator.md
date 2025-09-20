@run_excel_non_rank_metrics_evaluator.py 

File này kế thừa tinh hoa từ file @non_rank_metrics_evaluator.py 
src\system\baselineRAG\layers\_06_evaluation\run_excel_non_rank_metrics_evaluator.py


- Đọc file src\system\baselineRAG\layers\_06_evaluation\outputs\main_vimqa_dev_300lines.xlsx

- copy file này ra thành 1 file mới có tên ... gì đó ở trong cùng thư mục với file gốc luôn 
- Chạy đánh giá với input là 
+, sheet: retrieve
+, 1 cột: supporting_facts : [['Diego Maradona', 0], ['Rutherford B. Hayes', 0]]  => cần tiền xử lý ra cột: processed_supporting_facts:  (để mà về đúng định dạng như cột title để mà đánh giá)  

+, cột: title là cột hệ thống RAG truy vấn ra 

['Diego Maradona']
['Cao nguyên Lâm Viên', 'Cao nguyên Lâm Viên', 'Khu dự trữ sinh quyển Langbiang', 'Ngọc Linh liên sơn', 'Ngọc Linh liên sơn']
['Billie Eilish', 'Black Eyes (EP)', 'When We All Fall Asleep, Where Do We Go?', 'The Sweet Escape', 'The Sweet Escape']


+, các kết quả chỉ số đánh giá được trả ra thì bạn tạo thêm các cột mới nhé 