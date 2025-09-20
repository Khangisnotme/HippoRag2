# mẶC ĐỊNH:
python evaluator_generation_for_xlsx.py --start_row 0 --end_row 5

python evaluator_generation_for_xlsx.py --sheet baseline_result_QA_raw --start_row 0 --end_row 10 --batch_size 5 --max_workers 3
python evaluator_generation_for_xlsx.py --sheet PPDX_result_QA_raw --start_row 0 --end_row 10 --batch_size 5 --max_workers 3

# Xử lý 300 dòng với batch size 20 và 5 worker
python evaluator_generation_for_xlsx.py --batch_size 20 --max_workers 10

