"""
Script Đánh Giá Truy Xuất PPDX

Script này đánh giá kết quả truy xuất từ hệ thống PPDX (Passage Processing and Document Extraction) sử dụng các metrics không xếp hạng.
Script xử lý và so sánh các đoạn văn được truy xuất với các supporting facts thực tế.

Input:
    - File Excel (main_vimqa_dev_300lines.xlsx) chứa:
        - Sheet 'PPDX_result_retrieve_raw' với các cột:
            - 'supporting_facts': Danh sách các tuple chứa ID tài liệu thực tế và vị trí của chúng
                Ví dụ: "[('Diego Maradona', 1), ('Rutherford B. Hayes', 2)]"
            - 'final_passages': Danh sách các dictionary chứa các đoạn văn được truy xuất và metadata
                Ví dụ: "[{'passage_id': 'passage_chunk_Diego Maradona_2_0', ...}]"
    - Vị trí: src/system/eval/input/main_vimqa_dev_300lines.xlsx

Output:
    - File Excel (main_vimqa_dev_300lines_PPDX_non_rank_retrieval_evaluator.xlsx) chứa:
        - Các cột gốc
        - Các cột đã xử lý:
            - processed_supporting_facts: Danh sách ID tài liệu thực tế đã được làm sạch
            - processed_final_passage: Danh sách ID tài liệu truy xuất đã được làm sạch
        - Các metrics đánh giá:
            - Metrics Ma Trận Nhầm Lẫn:
                - true_positive: Số tài liệu liên quan được truy xuất đúng
                - false_positive: Số tài liệu không liên quan được truy xuất sai
                - false_negative: Số tài liệu liên quan bị bỏ sót
                - true_negative: Số tài liệu không liên quan được loại bỏ đúng
                - total_corpus: Tổng số tài liệu duy nhất trong corpus
            - Tỷ Lệ Trúng:
                - hit_rate: Tỷ lệ truy vấn có ít nhất một tài liệu liên quan
            - Metrics Đánh Giá Chính:
                - accuracy: Độ chính xác tổng thể
                - precision: Độ chính xác tại k (k=5)
                - recall_at_k: Độ bao phủ tại k (k=5)
                - f1_score: Điểm F1 tại k (k=5)
    - Vị trí: src/system/eval/retrieval/outputs/main_vimqa_dev_300lines_PPDX_non_rank_retrieval_evaluator.xlsx
    - Dòng cuối chứa các metrics trung bình trên tất cả các truy vấn

Các Hàm Chính:
    - process_supporting_facts(): Trích xuất ID tài liệu từ các tuple supporting facts
    - clean_passage_id(): Loại bỏ tiền tố và hậu tố từ ID đoạn văn
    - process_final_passages(): Trích xuất và làm sạch ID đoạn văn từ các đoạn văn được truy xuất
    - main(): Điều phối quá trình đánh giá

"""

import pandas as pd
import ast
import re
from pathlib import Path
from non_rank_metrics_evaluator import NonRankMetricsEvaluator, RetrievalResult

def process_supporting_facts(supporting_facts_str):
    """
    Process supporting facts string into list of document IDs.
    
    Args:
        supporting_facts_str (str): String representation of list containing supporting facts.
            Example: "[('Diego Maradona', 1), ('Rutherford B. Hayes', 2)]"
    
    Returns:
        list: List of document IDs extracted from supporting facts.
            Example: ['Diego Maradona', 'Rutherford B. Hayes']
    """
    try:
        # Parse the string representation of list into actual list
        facts_list = ast.literal_eval(supporting_facts_str)
        # Extract just the document IDs (first element of each tuple)
        return [fact[0] for fact in facts_list]
    except:
        return []

def clean_passage_id(passage_id):
    """
    Clean passage ID by removing 'passage_chunk_' prefix and trailing numbers.
    
    Args:
        passage_id (str): Original passage ID.
            Example: 'passage_chunk_Diego Maradona_2_0'
    
    Returns:
        str: Cleaned passage ID.
            Example: 'Diego Maradona'
    """
    # Remove 'passage_chunk_' prefix
    cleaned_id = passage_id.replace('passage_chunk_', '')
    # Remove trailing numbers and underscores
    cleaned_id = re.sub(r'_\d+(_\d+)?$', '', cleaned_id)
    return cleaned_id

def process_final_passages(final_passages_str):
    """
    Process final passages string into list of cleaned passage IDs.
    
    Args:
        final_passages_str (str): String representation of list containing passage objects.
            Example: "[{'passage_id': 'passage_chunk_Diego Maradona_2_0', ...}]"
    
    Returns:
        list: List of cleaned passage IDs.
            Example: ['Diego Maradona', 'Rutherford B. Hayes']
    """
    try:
        # Parse the string representation of list into actual list
        passages_list = ast.literal_eval(final_passages_str)
        # Extract passage IDs and clean them
        return [clean_passage_id(passage['passage_id']) for passage in passages_list]
    except:
        return []

def main():
    """
    Main function to evaluate retrieval results using non-ranking metrics.
    
    The function:
    1. Reads an Excel file containing retrieval results
    2. Processes supporting facts and final passages
    3. Evaluates the results using various metrics
    4. Saves the evaluation results to a new Excel file
    
    Input Excel file should contain:
    - supporting_facts: Ground truth documents
    - final_passages: Retrieved passages with their metadata
    
    Output Excel file will contain:
    - Original columns
    - Processed columns (cleaned IDs)
    - Evaluation metrics (accuracy, precision, recall, etc.)
    """
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Input and output file paths relative to script directory
    input_file = script_dir.parent / "input" / "main_vimqa_dev_300lines.xlsx"
    output_file = script_dir / "outputs" / "main_vimqa_dev_300lines_PPDX_non_rank_retrieval_evaluator.xlsx"
    
    # Verify input file exists
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read the Excel file
    print(f"Reading Excel file: {input_file}")
    df = pd.read_excel(input_file, sheet_name="PPDX_result_QA_raw")
    
    # Process supporting facts and final passages
    print("Processing data...")
    df['processed_supporting_facts'] = df['supporting_facts'].apply(process_supporting_facts)
    df['processed_final_passage'] = df['final_passages'].apply(process_final_passages)
    
    # Calculate total unique documents in corpus
    all_docs = set()
    for docs in df['processed_supporting_facts']:
        all_docs.update(docs)
    for docs in df['processed_final_passage']:
        all_docs.update(docs)
    total_docs_in_corpus = len(all_docs)
    print(f"Total unique documents in corpus: {total_docs_in_corpus}")
    
    # Initialize evaluator with total corpus size
    evaluator = NonRankMetricsEvaluator(total_docs_in_corpus=total_docs_in_corpus)
    
    # Prepare retrieval results for evaluation
    retrieval_results = []
    for idx, row in df.iterrows():
        result = RetrievalResult(
            query_id=f"query_{idx}",
            retrieved_docs=row['processed_final_passage'],
            relevant_docs=row['processed_supporting_facts'],
            k_value=5  # Using k=5 for evaluation
        )
        retrieval_results.append(result)
    
    # Run evaluation
    print("Running evaluation...")
    evaluation_results = evaluator.evaluate_multiple_queries(retrieval_results)
    
    # Add evaluation metrics to dataframe
    print("Adding evaluation metrics to dataframe...")
    for idx, result in enumerate(evaluation_results['individual_results']):
        # 1. Confusion Matrix Metrics
        df.loc[idx, 'true_positive'] = result['true_positive']
        df.loc[idx, 'false_positive'] = result['false_positive']
        df.loc[idx, 'false_negative'] = result['false_negative']
        df.loc[idx, 'true_negative'] = total_docs_in_corpus - result['relevant_count'] - result['false_positive']
        df.loc[idx, 'total_corpus'] = total_docs_in_corpus
        
        # 2. Hit Rate
        df.loc[idx, 'hit_rate'] = result['hit_rate_single']
        
        # 3. Main Evaluation Metrics
        df.loc[idx, 'accuracy'] = result['accuracy']
        df.loc[idx, 'precision'] = result['precision']
        df.loc[idx, 'recall_at_k'] = result['recall_at_k']
        df.loc[idx, 'f1_score'] = result['f1_score']
    
    # Add average metrics as a new row
    avg_metrics = evaluation_results['average_metrics']
    df.loc[len(df)] = {
        # Main metrics averages
        'accuracy': avg_metrics['macro_accuracy'],
        'precision': avg_metrics['macro_precision'],
        'recall_at_k': avg_metrics['macro_recall'],
        'f1_score': avg_metrics['macro_f1'],
        'hit_rate': avg_metrics['hit_rate_at_k'],
        'total_corpus': total_docs_in_corpus
    }
    
    # Get all columns from the dataframe
    original_columns = df.columns.tolist()
    
    # Add new columns at the end
    new_columns = [
        # Processed columns
        'processed_supporting_facts', 'processed_final_passage',
        # Confusion matrix metrics
        'true_positive', 'true_negative', 'false_positive', 'false_negative',
        'total_corpus',
        # Hit rate
        'hit_rate',
        # Main evaluation metrics
        'accuracy', 'precision', 'recall_at_k', 'f1_score'
    ]
    
    # Combine original columns with new columns
    column_order = original_columns + [col for col in new_columns if col not in original_columns]
    
    # Filter to only include columns that exist
    column_order = [col for col in column_order if col in df.columns]
    df = df[column_order]
    
    # Create outputs directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Save results to new Excel file
    print(f"Saving results to: {output_file}")
    df.to_excel(output_file, index=False)
    
    # Print evaluation summary
    print("\nEvaluation Summary:")
    print(evaluation_results['evaluation_summary'])

if __name__ == "__main__":
    main()
