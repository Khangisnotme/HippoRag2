import pandas as pd
import ast
from pathlib import Path
from non_rank_metrics_evaluator import NonRankMetricsEvaluator, RetrievalResult

def process_supporting_facts(supporting_facts_str):
    """Process supporting facts string into list of document IDs."""
    try:
        # Parse the string representation of list into actual list
        facts_list = ast.literal_eval(supporting_facts_str)
        # Extract just the document IDs (first element of each tuple)
        return [fact[0] for fact in facts_list]
    except:
        return []

def process_retrieved_docs(title_str):
    """Process retrieved documents string into list of document IDs."""
    try:
        # Parse the string representation of list into actual list
        return ast.literal_eval(title_str)
    except:
        return []

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    
    # Input and output file paths relative to script directory
    input_file = script_dir / "outputs" / "main_vimqa_dev_300lines.xlsx"
    output_file = script_dir / "outputs" / "main_vimqa_dev_300lines_evaluated.xlsx"
    
    # Verify input file exists
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Read the Excel file
    print(f"Reading Excel file: {input_file}")
    df = pd.read_excel(input_file, sheet_name="retrieve")
    
    # Process supporting facts and retrieved documents
    print("Processing data...")
    df['processed_supporting_facts'] = df['supporting_facts'].apply(process_supporting_facts)
    df['processed_retrieved_docs'] = df['title'].apply(process_retrieved_docs)
    
    # Calculate total unique documents in corpus
    all_docs = set()
    for docs in df['processed_retrieved_docs']:
        all_docs.update(docs)
    for docs in df['processed_supporting_facts']:
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
            retrieved_docs=row['processed_retrieved_docs'],
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
    
    # Reorder columns
    column_order = [
        # Original columns
        'supporting_facts', 'title',
        'processed_supporting_facts', 'processed_retrieved_docs',
        # Confusion matrix metrics
        'true_positive', 'true_negative', 'false_positive', 'false_negative',
        'total_corpus',
        # Hit rate
        'hit_rate',
        # Main evaluation metrics
        'accuracy', 'precision', 'recall_at_k', 'f1_score'
    ]
    
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
