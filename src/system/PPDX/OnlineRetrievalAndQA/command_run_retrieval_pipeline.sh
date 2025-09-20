#!/bin/bash

# ======================================================
# Command Examples for Running Retrieval Pipeline
# ======================================================

# Main run 
python run_retrieval_pipeline.py --excel_input input.xlsx --excel_output results.xlsx --batch_size 5

# Process queries in larger batches
python run_retrieval_pipeline.py --excel_input qa_pairs_vimqa_dev_300.xlsx --excel_output results.xlsx --start_row 10 --end_row 20  --batch_size 10


