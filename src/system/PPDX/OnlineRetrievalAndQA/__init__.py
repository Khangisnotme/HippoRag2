"""
Online Retrieval and QA Pipeline Package
"""

from pathlib import Path

# Package version
__version__ = "1.0.0"

# Package root directory
PACKAGE_ROOT = Path(__file__).parent

# Export main classes
from .retrieval_pipeline_orchestrator import PipelineOrchestrator, PipelineResult
from .module1_dual_retrieval import DualRetriever, RetrievalResult
from .module2_triple_filter import TripleFilter, FilteredTripleResult
from .module3_passage_ranker import PassageRanker, RankedPassageResult
from .module4_context_expander import ContextExpander, ExpandedContext
from .module5_answer_generator import AnswerGenerator, AnswerResult 