""" OnlineRetrievalAndQA/run_retrieval_pipeline.py 
src/system/PPDX/OnlineRetrievalAndQA/run_retrieval_and_qa_pipeline.py
Xử lý file Excel questions và thêm detailed results từ các modules bao gồm Module 5 (Answer Generation)
"""

import pandas as pd
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
import time
from datetime import datetime
import traceback

# Module imports
from retrieval_pipeline_orchestrator import (
    RetrievalPipelineOrchestrator,
    RetrievalPipelineConfig,
    create_default_pipeline_config
)
from module1_dual_retrieval import RetrievalConfig
from module2_triple_filter import TripleFilterConfig
from module3_passage_ranker import PassageRankerConfig
from module4_context_expander import ContextExpansionConfig
from module5_answer_generator import AnswerGeneratorConfig  # NEW: Module 5 import

# Shared utilities
from utils.utils_shared_general import setup_logger

# Setup logger
logger = setup_logger(__name__, log_file=Path(f"outputs/log/run_retrieval_and_qa_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"))

def standardize_triple_passage_ids(
    filtered_triples: List[Any],
    passage_id_prefix: str = "passage_chunk_",
    triple_id_prefix: str = "chunk_"
) -> List[Any]:
    """
    Chuẩn hóa tiền tố của source_passage_id trong các FilteredTriple để khớp với định dạng passage_id của các passage.

    Args:
        filtered_triples (List[Any]): Danh sách các đối tượng FilteredTriple từ Module 2
        passage_id_prefix (str): Tiền tố mong muốn cho passage_id
        triple_id_prefix (str): Tiền tố hiện tại của source_passage_id trong triples

    Returns:
        List[Any]: Danh sách các đối tượng FilteredTriple đã được chuẩn hóa source_passage_id
    """
    if not filtered_triples:
        return []

    logger.info(f"Standardizing triple source_passage_ids from '{triple_id_prefix}' to '{passage_id_prefix}'...")
    standardized_triples = []
    for triple in filtered_triples:
        if triple.source_passage_id.startswith(triple_id_prefix):
            new_source_passage_id = passage_id_prefix + triple.source_passage_id[len(triple_id_prefix):]
            # Create a new triple with updated ID
            triple_dict = triple.__dict__.copy()
            triple_dict['source_passage_id'] = new_source_passage_id
            standardized_triples.append(type(triple)(**triple_dict))
        else:
            logger.warning(f"Triple ID '{triple.source_passage_id}' does not start with '{triple_id_prefix}'. Keeping as is.")
            standardized_triples.append(triple)
    logger.info(f"Finished standardizing {len(standardized_triples)} triples.")
    return standardized_triples

class DetailedPipelineProcessor(RetrievalPipelineOrchestrator):
    """Extended Pipeline Processor để capture detailed outputs từ mỗi module bao gồm Module 5"""

    def __init__(self, config: Optional[RetrievalPipelineConfig] = None, **kwargs):
        super().__init__(config, **kwargs)
        self.detailed_results = {}
        # Initialize answer_generator if enabled
        if self.config and self.config.enable_answer_generation:
            from module5_answer_generator import AnswerGenerator, AnswerGeneratorConfig
            self.answer_generator = AnswerGenerator(AnswerGeneratorConfig())
        else:
            self.answer_generator = None

    def process_single_query_detailed(self, query: str, query_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process query và capture detailed info từ mỗi module

        Returns:
            Dict với detailed breakdown từ tất cả modules bao gồm Module 5
        """
        if query_id is None:
            query_id = f"Q_{int(time.time() * 1000)}"

        logger.info(f"🔍 Processing detailed query: {query_id}")
        logger.info(f"📝 Query: '{query}'")

        detailed_result = {
            'query_id': query_id,
            'query': query,
            'processing_time': 0,
            'success': False,
            'error': None,
            'module1_results': {},
            'module2_results': {},
            'module3_results': {},
            'module4_results': {},
            'module5_results': {},  # NEW: Module 5 results
            'final_results': {
                'final_passages': [],
                'final_triples': [],
                'overall_stats': {
                    'total_passages_retrieved': 0,
                    'total_triples_filtered': 0,
                    'high_relevance_triples': 0,
                    'final_triples_count': 0,
                    'avg_final_passage_score': 0,
                    'avg_triple_relevance': 0,
                    'answer_generated': False,
                    'answer_quality_score': 0,
                    'answer_confidence_score': 0,
                    'answer_generation_time': 0,
                    'answer_llm_provider': 'N/A'
                }
            }
        }

        start_time = time.time()

        try:
            # Validate query
            if not query or len(query.strip()) < 2:
                raise ValueError("Query quá ngắn hoặc rỗng")

            # Module 1: Dual Retrieval
            logger.info("📊 Module 1: Dual Retrieval...")
            retrieval_result = self.dual_retriever.retrieve_dual(
                query,
                top_k_passages=self.config.dual_retrieval_config.max_passages,
                top_n_triples=self.config.dual_retrieval_config.max_triples
            )
            detailed_result['module1_results'] = self._extract_module1_details(retrieval_result)

            # Module 2: Triple Filtering
            logger.info("🤖 Module 2: Triple Filtering...")
            filtering_result = self.triple_filter.filter_triples(query, retrieval_result.raw_triples)
            detailed_result['module2_results'] = self._extract_module2_details(filtering_result)

            # Standardize triple passage IDs before Module 3
            logger.info("🔄 Standardizing triple passage IDs...")
            standardized_triples = standardize_triple_passage_ids(
                filtering_result.filtered_triples,
                passage_id_prefix="passage_chunk_",
                triple_id_prefix="chunk_"
            )

            # Module 3: Passage Ranking
            logger.info("🏆 Module 3: Passage Ranking...")
            ranking_result = self.passage_ranker.rank_passages(
                retrieval_result.raw_passages,
                standardized_triples,  # Use standardized triples
                query
            )
            detailed_result['module3_results'] = self._extract_module3_details(ranking_result)

            # Module 4: Context Expansion (nếu enabled)
            expansion_result = None
            if self.config.enable_context_expansion:
                logger.info("🔗 Module 4: Context Expansion...")
                expansion_result = self.context_expander.expand_context(
                    standardized_triples, query  # Use standardized triples
                )
                detailed_result['module4_results'] = self._extract_module4_details(expansion_result)

            # NEW: Module 5: Answer Generation (nếu enabled)
            answer_result = None
            if self.config.enable_answer_generation and self.answer_generator:
                logger.info("💬 Module 5: Answer Generation...")
                answer_result = self.answer_generator.generate_answer(
                    query=query,
                    ranked_passages=ranking_result.ranked_passages,
                    filtered_triples=standardized_triples,
                    expanded_context=expansion_result
                )
                detailed_result['module5_results'] = self._extract_module5_details(answer_result)

            # Final Results
            detailed_result['final_results'] = self._extract_final_results(ranking_result, filtering_result, answer_result)  # NEW parameter

            detailed_result['processing_time'] = time.time() - start_time
            detailed_result['success'] = True

            logger.info(f"✅ Query {query_id} processed successfully in {detailed_result['processing_time']:.2f}s")

        except Exception as e:
            error_msg = str(e)
            detailed_result['error'] = error_msg
            detailed_result['processing_time'] = time.time() - start_time

            logger.error(f"❌ Error processing query {query_id}: {error_msg}")
            logger.error(f"❌ Traceback: {traceback.format_exc()}")

        return detailed_result

    def _extract_module1_details(self, retrieval_result) -> Dict[str, Any]:
        """Extract detailed info từ Module 1"""
        # Top passages
        top_passages = []
        for passage in retrieval_result.raw_passages:
            top_passages.append({
                'passage_id': passage.item_id,
                'bm25_score': round(passage.bm25_score, 3),
                'embedding_score': round(passage.embedding_score, 3),
                'hybrid_score': round(passage.hybrid_score, 3),
                'text_preview': passage.text[:100] + ('...' if len(passage.text) > 100 else ''),
                'text_length': len(passage.text),
                'title': passage.metadata.get('title', ''),
                'rank': passage.metadata.get('rank', 0)
            })

        # Top triples
        top_triples = []
        for triple in retrieval_result.raw_triples:
            top_triples.append({
                'triple_id': triple.item_id,
                'subject': triple.metadata.get('subject', ''),
                'predicate': triple.metadata.get('predicate', ''),
                'object': triple.metadata.get('object', ''),
                'bm25_score': round(triple.bm25_score, 3),
                'embedding_score': round(triple.embedding_score, 3),
                'hybrid_score': round(triple.hybrid_score, 3),
                'confidence': triple.metadata.get('confidence', 0),
                'source_passage_id': triple.metadata.get('source_passage_id', ''),
                'rank': triple.metadata.get('rank', 0)
            })

        # Statistics
        passage_scores = [p.hybrid_score for p in retrieval_result.raw_passages]
        triple_scores = [t.hybrid_score for t in retrieval_result.raw_triples]

        stats = {
            'passages_count': len(retrieval_result.raw_passages),
            'triples_count': len(retrieval_result.raw_triples),
            'avg_passage_score': round(sum(passage_scores) / len(passage_scores), 3) if passage_scores else 0,
            'avg_triple_score': round(sum(triple_scores) / len(triple_scores), 3) if triple_scores else 0,
            'max_passage_score': round(max(passage_scores), 3) if passage_scores else 0,
            'max_triple_score': round(max(triple_scores), 3) if triple_scores else 0,
            'retrieval_time': retrieval_result.retrieval_time
        }

        return {
            'top_passages': top_passages,
            'top_triples': top_triples,
            'stats': stats
        }

    def _extract_module2_details(self, filtering_result) -> Dict[str, Any]:
        """Extract detailed info từ Module 2"""
        # Filtered triples
        filtered_triples = []
        for triple in filtering_result.filtered_triples:
            filtered_triples.append({
                'triple_id': triple.triple_id,
                'subject': triple.subject,
                'predicate': triple.predicate,
                'object': triple.object,
                'relevance_score': round(triple.query_relevance_score, 3),
                'relevance_level': triple.relevance_level.value,
                'confidence_score': round(triple.confidence_score, 3),
                'quality_score': round(triple.get_quality_score(), 3),
                'original_hybrid_retrieval_score': round(triple.original_hybrid_retrieval_score, 3),
                'source_passage_id': triple.source_passage_id,
                'explanation': triple.llm_explanation[:150] + ('...' if len(triple.llm_explanation) > 150 else '')
            })

        # Statistics
        relevance_scores = [t.query_relevance_score for t in filtering_result.filtered_triples]
        relevance_distribution = filtering_result.get_relevance_distribution()

        stats = {
            'original_count': filtering_result.original_count,
            'filtered_count': filtering_result.filtered_count,
            'filtering_efficiency': round(filtering_result.get_filtering_efficiency(), 3),
            'avg_relevance_score': round(sum(relevance_scores) / len(relevance_scores), 3) if relevance_scores else 0,
            'max_relevance_score': round(max(relevance_scores), 3) if relevance_scores else 0,
            'relevance_distribution': relevance_distribution,
            'filtering_time': filtering_result.filtering_time
        }

        return {
            'filtered_triples': filtered_triples,
            'stats': stats
        }

    def _extract_module3_details(self, ranking_result) -> Dict[str, Any]:
        """Extract detailed info từ Module 3"""
        # Ranked passages
        ranked_passages = []
        for passage in ranking_result.ranked_passages:
            ranked_passages.append({
                'passage_id': passage.passage_id,
                'rank': passage.rank,
                'final_score': round(passage.final_score, 3),
                'hybrid_retrieval_score': round(passage.hybrid_retrieval_score, 3),
                'support_score': round(passage.support_score, 3),
                'supporting_triples_count': passage.supporting_triples_count,
                'supporting_triples': passage.supporting_triples[:10],  # Top 10 supporting triples
                'text_preview': passage.original_text[:100] + ('...' if len(passage.original_text) > 100 else ''),
                'text_length': len(passage.original_text),
                'score_breakdown': passage.score_breakdown,
                'has_strong_support': passage.has_strong_support()
            })

        # Statistics
        final_scores = [p.final_score for p in ranking_result.ranked_passages]
        support_distribution = ranking_result.get_support_distribution()

        stats = {
            'original_passage_count': ranking_result.original_passage_count,
            'final_passage_count': ranking_result.final_passage_count,
            'ranking_efficiency': round(ranking_result.get_ranking_efficiency(), 3),
            'avg_final_score': round(sum(final_scores) / len(final_scores), 3) if final_scores else 0,
            'max_final_score': round(max(final_scores), 3) if final_scores else 0,
            'support_distribution': support_distribution,
            'ranking_time': ranking_result.ranking_time
        }

        return {
            'ranked_passages': ranked_passages,
            'stats': stats
        }

    def _extract_module4_details(self, expansion_result) -> Dict[str, Any]:
        """Extract detailed info từ Module 4"""
        if not expansion_result:
            return {'expanded_contexts': [], 'stats': {}}

        # Expanded contexts
        expanded_contexts = []
        for context in expansion_result.expanded_contexts:
            expanded_contexts.append({
                'context_id': context.context_id,
                'context_type': context.context_type,
                'source_triple_id': context.source_triple_id,
                'expansion_path': context.expansion_path,
                'relevance_score': round(context.relevance_score, 3),
                'relevance_level': context.relevance_level.value,
                'distance_from_source': context.distance_from_source,
                'text_preview': context.context_text[:100] + ('...' if len(context.context_text) > 100 else ''),
                'supporting_evidence': context.supporting_evidence
            })

        # Statistics
        relevance_scores = [c.relevance_score for c in expansion_result.expanded_contexts]
        relevance_distribution = expansion_result.get_relevance_distribution()

        stats = {
            'source_triples_count': expansion_result.source_triples_count,
            'expanded_contexts_count': expansion_result.expanded_contexts_count,
            'expansion_efficiency': round(expansion_result.get_expansion_efficiency(), 3),
            'avg_relevance_score': round(sum(relevance_scores) / len(relevance_scores), 3) if relevance_scores else 0,
            'max_relevance_score': round(max(relevance_scores), 3) if relevance_scores else 0,
            'relevance_distribution': relevance_distribution,
            'expansion_time': expansion_result.expansion_time
        }

        return {
            'expanded_contexts': expanded_contexts,
            'stats': stats
        }

    def _extract_module5_details(self, answer_result) -> Dict[str, Any]:
        """NEW: Extract detailed info từ Module 5 (Answer Generation)"""
        if not answer_result:
            return {'answer_details': None, 'stats': {}}

        details = {
            'ai_answer': answer_result.ai_answer,
            'query': answer_result.query,
            'quality_score': round(answer_result.quality_score, 3),
            'quality_level': answer_result.quality_level.value,
            'confidence_score': round(answer_result.confidence_score, 3),
            'supporting_passages_ids': answer_result.supporting_passages,
            'supporting_triples_ids': answer_result.supporting_triples,
            'generation_time': round(answer_result.generation_time, 3),
            'llm_provider': answer_result.llm_provider,
            'generation_metadata': answer_result.generation_metadata,
            'prompt_used': answer_result.generation_metadata.get('prompt', '')  # Extract prompt for easier access
        }

        stats = {
            'quality_score': round(answer_result.quality_score, 3),
            'confidence_score': round(answer_result.confidence_score, 3),
            'generation_time': round(answer_result.generation_time, 3),
            'llm_provider': answer_result.llm_provider,
            'prompt_tokens': answer_result.generation_metadata.get('prompt_tokens', 0),
            'response_tokens': answer_result.generation_metadata.get('response_tokens', 0),
            'cache_hit': answer_result.generation_metadata.get('cache_hit', False)
        }

        return {
            'answer_details': details,
            'stats': stats
        }

    def _extract_final_results(self, ranking_result, filtering_result, answer_result=None) -> Dict[str, Any]:  # NEW parameter
        """Extract final consolidated results"""
        # Final passages (top-ranked)
        final_passages = []
        for passage in ranking_result.ranked_passages[:10]:  # Top 10
            final_passages.append({
                'passage_id': passage.passage_id,
                'rank': passage.rank,
                'final_score': round(passage.final_score, 3),
                'text_preview': passage.original_text[:150] + ('...' if len(passage.original_text) > 150 else ''),
                'supporting_triples_count': passage.supporting_triples_count
            })

        # Final triples (ALL filtered triples, not just high relevance)
        final_triples = []
        for triple in filtering_result.filtered_triples[:15]:  # Top 15 filtered triples
            final_triples.append({
                'triple_id': triple.triple_id,
                'subject': triple.subject,
                'predicate': triple.predicate,
                'object': triple.object,
                'relevance_score': round(triple.query_relevance_score, 3),
                'relevance_level': triple.relevance_level.value,
                'source_passage_id': triple.source_passage_id
            })

        # Count high relevance triples for stats
        high_relevance_triples = [t for t in filtering_result.filtered_triples if t.query_relevance_score >= 0.7]

        # Overall stats
        overall_stats = {
            'total_passages_retrieved': len(ranking_result.ranked_passages),
            'total_triples_filtered': len(filtering_result.filtered_triples),
            'high_relevance_triples': len(high_relevance_triples),
            'final_triples_count': len(final_triples),
            'avg_final_passage_score': round(sum(p.final_score for p in ranking_result.ranked_passages) / len(ranking_result.ranked_passages), 3) if ranking_result.ranked_passages else 0,
            'avg_triple_relevance': round(sum(t.query_relevance_score for t in filtering_result.filtered_triples) / len(filtering_result.filtered_triples), 3) if filtering_result.filtered_triples else 0
        }

        # NEW: Add answer generation stats to overall stats
        if answer_result:
            overall_stats.update({
                'answer_generated': True,
                'answer_quality_score': round(answer_result.quality_score, 3),
                'answer_confidence_score': round(answer_result.confidence_score, 3),
                'answer_generation_time': round(answer_result.generation_time, 3),
                'answer_llm_provider': answer_result.llm_provider
            })
        else:
            overall_stats.update({
                'answer_generated': False,
                'answer_quality_score': 0,
                'answer_confidence_score': 0,
                'answer_generation_time': 0,
                'answer_llm_provider': 'N/A'
            })

        return {
            'final_passages': final_passages,
            'final_triples': final_triples,
            'overall_stats': overall_stats
        }

def process_excel_file(input_path: Path, output_path: Path,
                      top_k_passages: int = 10,
                      top_n_triples: int = 20,
                      enable_context_expansion: bool = False,
                      enable_answer_generation: bool = True,  # NEW parameter, default True
                      start_row: int = None,
                      end_row: int = None) -> None:
    """
    Process Excel file với questions và thêm detailed results

    Args:
        input_path (Path): Path to input Excel file
        output_path (Path): Path to output Excel file
        top_k_passages (int): Number of top passages to retrieve
        top_n_triples (int): Number of top triples to retrieve
        enable_context_expansion (bool): Enable Module 4
        enable_answer_generation (bool): Enable Module 5 (NEW)
        start_row (int): Start row number (1-based, None for beginning)
        end_row (int): End row number (1-based, None for end)
    """
    logger.info(f"🚀 Starting Excel processing...")
    logger.info(f"   📥 Input: {input_path}")
    logger.info(f"   📤 Output: {output_path}")
    logger.info(f"   📊 Parameters: top_k={top_k_passages}, top_n={top_n_triples}, expansion={enable_context_expansion}, answer_gen={enable_answer_generation}")

    # Load Excel file
    try:
        df = pd.read_excel(input_path)
        logger.info(f"✅ Loaded Excel file với {len(df)} rows")
    except Exception as e:
        logger.error(f"❌ Error loading Excel file: {e}")
        raise

    # Validate columns
    if 'question' not in df.columns:
        raise ValueError("Excel file phải có cột 'question'")

    # Apply row filtering if specified
    original_length = len(df)
    if start_row is not None or end_row is not None:
        # Convert to 0-based indexing
        start_idx = (start_row - 1) if start_row is not None else 0
        end_idx = end_row if end_row is not None else len(df)

        # Validate row numbers
        if start_idx < 0:
            start_idx = 0
        if end_idx > len(df):
            end_idx = len(df)
        if start_idx >= end_idx:
            raise ValueError(f"Invalid row range: start_row ({start_row}) >= end_row ({end_row})")

        # Filter DataFrame but keep original indices
        df_to_process = df.iloc[start_idx:end_idx].copy()
        logger.info(f"📊 Processing rows {start_idx+1} to {end_idx} ({len(df_to_process)} rows) out of {original_length} total rows")

        # Create a copy of original DataFrame for output
        df_output = df.copy()
    else:
        df_to_process = df.copy()
        df_output = df.copy()
        logger.info(f"📊 Processing all {len(df)} rows")

    # Create memory-optimized config
    config = create_default_pipeline_config()
    # CRITICAL: Limit data size to avoid memory issues
    config.dual_retrieval_config.max_passages = min(top_k_passages, 5)  # Max 5 passages
    config.dual_retrieval_config.max_triples = min(top_n_triples, 10)   # Max 10 triples
    config.dual_retrieval_config.embedding_model = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    config.dual_retrieval_config.batch_size = 4  # Very small batch
    config.enable_context_expansion = enable_context_expansion
    config.enable_answer_generation = enable_answer_generation  # NEW
    config.max_final_passages = min(top_k_passages, 5)

    # Initialize processor
    processor = DetailedPipelineProcessor(config)

    # Create new columns for results
    new_columns = [
        'module1_top_passages', 'module1_top_triples', 'module1_stats',
        'module2_filtered_triples', 'module2_stats',
        'module3_ranked_passages', 'module3_stats',
        'final_passages', 'final_triples', 'final_stats',
        'processing_time', 'success', 'error'
    ]

    if enable_context_expansion:
        new_columns.extend(['module4_expanded_contexts', 'module4_stats'])

    # NEW: Add Module 5 columns
    if enable_answer_generation:
        new_columns.extend([
            'ai_answer',
            'prompt_used',
            'quality_score',
            'quality_level',
            'confidence_score',
            'generation_time',
            'llm_provider',
            'supporting_passages_ids',
            'supporting_triples_ids',
            'generation_metadata_json',
            'module5_stats'
        ])

    # Initialize new columns in output DataFrame
    for col in new_columns:
        df_output[col] = None

    logger.info(f"📊 Processing {len(df_to_process)} questions...")

    # Process each question in the filtered range
    for idx, row in df_to_process.iterrows():
        question = row.get('question', '').strip()
        row_number = idx + 1  # 1-based row number for display

        if not question:
            logger.warning(f"⚠️ Row {row_number}: Empty question, skipping...")
            df_output.at[idx, 'success'] = False
            df_output.at[idx, 'error'] = "Empty question"
            continue

        # Calculate position in processing
        current_pos = list(df_to_process.index).index(idx) + 1
        total_to_process = len(df_to_process)

        logger.info(f"🔍 Processing row {row_number} ({current_pos}/{total_to_process}): '{question[:50]}{'...' if len(question) > 50 else ''}'")

        try:
            # Process question
            result = processor.process_single_query_detailed(question, f"Q_{row_number:03d}")

            # Fill results into output DataFrame
            df_output.at[idx, 'module1_top_passages'] = json.dumps(result['module1_results']['top_passages'], ensure_ascii=False, indent=2)
            df_output.at[idx, 'module1_top_triples'] = json.dumps(result['module1_results']['top_triples'], ensure_ascii=False, indent=2)
            df_output.at[idx, 'module1_stats'] = json.dumps(result['module1_results']['stats'], ensure_ascii=False, indent=2)

            df_output.at[idx, 'module2_filtered_triples'] = json.dumps(result['module2_results']['filtered_triples'], ensure_ascii=False, indent=2)
            df_output.at[idx, 'module2_stats'] = json.dumps(result['module2_results']['stats'], ensure_ascii=False, indent=2)

            df_output.at[idx, 'module3_ranked_passages'] = json.dumps(result['module3_results']['ranked_passages'], ensure_ascii=False, indent=2)
            df_output.at[idx, 'module3_stats'] = json.dumps(result['module3_results']['stats'], ensure_ascii=False, indent=2)

            if enable_context_expansion and result['module4_results']:
                df_output.at[idx, 'module4_expanded_contexts'] = json.dumps(result['module4_results']['expanded_contexts'], ensure_ascii=False, indent=2)
                df_output.at[idx, 'module4_stats'] = json.dumps(result['module4_results']['stats'], ensure_ascii=False, indent=2)

            # NEW: Fill Module 5 results
            if enable_answer_generation and result['module5_results'] and result['module5_results']['answer_details']:
                answer_details = result['module5_results']['answer_details']
                df_output.at[idx, 'ai_answer'] = answer_details.get('ai_answer', '')
                df_output.at[idx, 'prompt_used'] = answer_details.get('prompt_used', '')
                df_output.at[idx, 'quality_score'] = answer_details.get('quality_score', 0.0)
                df_output.at[idx, 'quality_level'] = answer_details.get('quality_level', '')
                df_output.at[idx, 'confidence_score'] = answer_details.get('confidence_score', 0.0)
                df_output.at[idx, 'generation_time'] = answer_details.get('generation_time', 0.0)
                df_output.at[idx, 'llm_provider'] = answer_details.get('llm_provider', '')
                df_output.at[idx, 'supporting_passages_ids'] = ', '.join(answer_details.get('supporting_passages_ids', []))
                df_output.at[idx, 'supporting_triples_ids'] = ', '.join(answer_details.get('supporting_triples_ids', []))
                df_output.at[idx, 'generation_metadata_json'] = json.dumps(answer_details.get('generation_metadata', {}), ensure_ascii=False, indent=2)
                df_output.at[idx, 'module5_stats'] = json.dumps(result['module5_results']['stats'], ensure_ascii=False, indent=2)
            elif enable_answer_generation:  # Feature enabled but no answer generated
                df_output.at[idx, 'ai_answer'] = "No answer generated"
                df_output.at[idx, 'prompt_used'] = ""
                df_output.at[idx, 'quality_score'] = 0.0
                df_output.at[idx, 'quality_level'] = "N/A"
                df_output.at[idx, 'confidence_score'] = 0.0
                df_output.at[idx, 'generation_time'] = 0.0
                df_output.at[idx, 'llm_provider'] = "N/A"
                df_output.at[idx, 'supporting_passages_ids'] = ""
                df_output.at[idx, 'supporting_triples_ids'] = ""
                df_output.at[idx, 'generation_metadata_json'] = json.dumps({}, ensure_ascii=False)
                df_output.at[idx, 'module5_stats'] = json.dumps({}, ensure_ascii=False)

            df_output.at[idx, 'final_passages'] = json.dumps(result['final_results']['final_passages'], ensure_ascii=False, indent=2)
            df_output.at[idx, 'final_triples'] = json.dumps(result['final_results']['final_triples'], ensure_ascii=False, indent=2)
            df_output.at[idx, 'final_stats'] = json.dumps(result['final_results']['overall_stats'], ensure_ascii=False, indent=2)

            df_output.at[idx, 'processing_time'] = round(result['processing_time'], 2)
            df_output.at[idx, 'success'] = result['success']
            df_output.at[idx, 'error'] = result.get('error', '')

            logger.info(f"   ✅ Row {row_number} processed successfully in {result['processing_time']:.2f}s")

        except Exception as e:
            error_msg = str(e)
            logger.error(f"   ❌ Row {row_number} failed: {error_msg}")

            df_output.at[idx, 'success'] = False
            df_output.at[idx, 'error'] = error_msg
            df_output.at[idx, 'processing_time'] = 0

            # Fill empty JSON for failed rows
            empty_json = json.dumps([], ensure_ascii=False)
            empty_stats = json.dumps({}, ensure_ascii=False)

            for col in new_columns:
                if col not in ['processing_time', 'success', 'error']:
                    if col in ['ai_answer']:
                        df_output.at[idx, col] = "ERROR"
                    elif col in ['quality_score', 'confidence_score', 'generation_time']:
                        df_output.at[idx, col] = 0.0
                    elif col in ['quality_level', 'llm_provider']:
                        df_output.at[idx, col] = "ERROR"
                    elif col in ['prompt_used', 'supporting_passages_ids', 'supporting_triples_ids']:
                        df_output.at[idx, col] = ""
                    elif 'stats' in col or 'metadata' in col:
                        df_output.at[idx, col] = empty_stats
                    else:
                        df_output.at[idx, col] = empty_json

    # Close processor
    processor.close()

    # Save output Excel
    try:
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save with formatting
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_output.to_excel(writer, sheet_name='Results', index=False)

            # Apply basic formatting
            worksheet = writer.sheets['Results']

            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter

                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass

                adjusted_width = min(max_length + 2, 100)  # Max width 100
                worksheet.column_dimensions[column_letter].width = adjusted_width

        logger.info(f"✅ Results saved to: {output_path}")

        # Log summary statistics
        processed_rows = df_to_process.index.tolist()
        success_count = df_output.loc[processed_rows, 'success'].sum()
        total_time = df_output.loc[processed_rows, 'processing_time'].sum()
        successful_times = df_output.loc[(df_output.index.isin(processed_rows)) & (df_output['success'] == True), 'processing_time']
        avg_time = successful_times.mean() if len(successful_times) > 0 else 0

        # NEW: Calculate answer generation statistics
        if enable_answer_generation:
            successful_answers = df_output.loc[(df_output.index.isin(processed_rows)) & (df_output['success'] == True) & (df_output['ai_answer'].notna()) & (df_output['ai_answer'] != "No answer generated") & (df_output['ai_answer'] != "ERROR"), 'ai_answer']
            answer_generation_rate = len(successful_answers) / success_count * 100 if success_count > 0 else 0
            
            # Calculate average quality and confidence scores for successful answers
            quality_scores = df_output.loc[(df_output.index.isin(processed_rows)) & (df_output['success'] == True) & (df_output['quality_score'] > 0), 'quality_score']
            confidence_scores = df_output.loc[(df_output.index.isin(processed_rows)) & (df_output['success'] == True) & (df_output['confidence_score'] > 0), 'confidence_score']
            generation_times = df_output.loc[(df_output.index.isin(processed_rows)) & (df_output['success'] == True) & (df_output['generation_time'] > 0), 'generation_time']

        logger.info(f"📊 PROCESSING SUMMARY:")
        logger.info(f"   📋 Processed rows: {len(df_to_process)} out of {original_length} total")
        if start_row is not None or end_row is not None:
            actual_start = min(processed_rows) + 1 if processed_rows else 0
            actual_end = max(processed_rows) + 1 if processed_rows else 0
            logger.info(f"   📊 Row range: {actual_start} to {actual_end}")
        logger.info(f"   ✅ Successful: {success_count}/{len(df_to_process)} ({success_count/len(df_to_process)*100:.1f}%)")
        logger.info(f"   ❌ Failed: {len(df_to_process) - success_count}")
        logger.info(f"   ⏱️ Total time: {total_time:.2f}s")
        logger.info(f"   ⏱️ Average time per question: {avg_time:.2f}s")

        # NEW: Log answer generation summary
        if enable_answer_generation:
            logger.info(f"💬 ANSWER GENERATION SUMMARY:")
            logger.info(f"   📝 Answers generated: {len(successful_answers)}/{success_count} ({answer_generation_rate:.1f}%)")
            if len(quality_scores) > 0:
                logger.info(f"   🎯 Average quality score: {quality_scores.mean():.3f}")
                logger.info(f"   🔍 Average confidence score: {confidence_scores.mean():.3f}")
                logger.info(f"   ⏱️ Average generation time: {generation_times.mean():.2f}s")

    except Exception as e:
        logger.error(f"❌ Error saving Excel file: {e}")
        raise

def main():
    """Main function với command line arguments"""
    parser = argparse.ArgumentParser(description="Run retrieval pipeline on Excel file with questions")

    parser.add_argument("--excel_input", type=str, required=True,
                       help="Path to input Excel file với cột 'question'")
    parser.add_argument("--excel_output", type=str,
                       help="Path to output Excel file (default: add _results suffix)")
    parser.add_argument("--top_k", "-k", type=int, default=10,
                       help="Number of top passages to retrieve (default: 10)")
    parser.add_argument("--top_n", "-n", type=int, default=20,
                       help="Number of top triples to retrieve (default: 20)")
    parser.add_argument("--enable_expansion", action="store_true",
                       help="Enable Module 4 - Context Expansion")
    parser.add_argument("--enable_answer_generation", action="store_true", default=True,  # NEW argument
                       help="Enable Module 5 - Answer Generation (default: True)")
    parser.add_argument("--disable_answer_generation", action="store_true",  # NEW argument for explicit disable
                       help="Disable Module 5 - Answer Generation")
    parser.add_argument("--start_row", type=int,
                       help="Start row number (1-based, inclusive)")
    parser.add_argument("--end_row", type=int,
                       help="End row number (1-based, inclusive)")

    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.excel_input)
    if not input_path.exists():
        print(f"❌ Input file not found: {input_path}")
        return

    # Generate output path
    if args.excel_output:
        output_path = Path(args.excel_output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_results{input_path.suffix}"

    # Validate row arguments
    if args.start_row is not None and args.start_row < 1:
        print(f"❌ start_row must be >= 1, got {args.start_row}")
        return

    if args.end_row is not None and args.end_row < 1:
        print(f"❌ end_row must be >= 1, got {args.end_row}")
        return

    if args.start_row is not None and args.end_row is not None and args.start_row > args.end_row:
        print(f"❌ start_row ({args.start_row}) cannot be greater than end_row ({args.end_row})")
        return

    # Handle answer generation flag logic (NEW)
    enable_answer_gen = True  # Default
    if args.disable_answer_generation:
        enable_answer_gen = False
    elif args.enable_answer_generation:
        enable_answer_gen = True

    # Show configuration info
    print(f"🚀 Starting Excel processing with configuration:")
    print(f"   📥 Input: {input_path}")
    print(f"   📤 Output: {output_path}")
    print(f"   📊 Top passages: {args.top_k}")
    print(f"   📊 Top triples: {args.top_n}")
    print(f"   🔗 Context expansion: {'Enabled' if args.enable_expansion else 'Disabled'}")
    print(f"   💬 Answer generation: {'Enabled' if enable_answer_gen else 'Disabled'}")  # NEW

    # Show row range info
    if args.start_row is not None or args.end_row is not None:
        start_info = f"row {args.start_row}" if args.start_row else "beginning"
        end_info = f"row {args.end_row}" if args.end_row else "end"
        print(f"   📊 Row range: from {start_info} to {end_info}")

    # Run processing
    try:
        process_excel_file(
            input_path=input_path,
            output_path=output_path,
            top_k_passages=args.top_k,
            top_n_triples=args.top_n,
            enable_context_expansion=args.enable_expansion,
            enable_answer_generation=enable_answer_gen,  # NEW parameter
            start_row=args.start_row,
            end_row=args.end_row
        )
        print(f"🎉 Processing completed successfully!")
        print(f"📤 Results saved to: {output_path}")

        # NEW: Show output columns info
        print(f"\n📋 Output includes:")
        print(f"   📊 Module 1-3 results (passages, triples, rankings)")
        if args.enable_expansion:
            print(f"   🔗 Module 4 results (context expansion)")
        if enable_answer_gen:
            print(f"   💬 Module 5 results (answer generation):")
            print(f"      - ai_answer: Generated answer")
            print(f"      - prompt_used: Full prompt sent to LLM")
            print(f"      - quality_score: Answer quality (0-1)")
            print(f"      - quality_level: Quality category")
            print(f"      - confidence_score: Answer confidence (0-1)")
            print(f"      - generation_time: Time to generate answer")
            print(f"      - llm_provider: LLM provider used")
            print(f"      - supporting_passages_ids: Supporting passage IDs")
            print(f"      - supporting_triples_ids: Supporting triple IDs")
            print(f"      - generation_metadata_json: Full generation metadata")

    except Exception as e:
        print(f"❌ Processing failed: {e}")
        logger.exception("Processing error:")

if __name__ == "__main__":
    main()
