#!/bin/bash

# ======================================================
# Command Examples for Running Retrieval Pipeline
# ======================================================

# Version đầu chưa có primary_model và batch_size
python run_retrieval_and_qa_pipeline.py --excel_input qa_pairs_vimqa_dev_300.xlsx --excel_output results.xlsx --start_row 0 --end_row 10 


python run_retrieval_and_qa_pipeline.py --excel_input qa_pairs_vimqa_dev_300.xlsx --excel_output results.xlsx --start_row 1 --end_row 11
