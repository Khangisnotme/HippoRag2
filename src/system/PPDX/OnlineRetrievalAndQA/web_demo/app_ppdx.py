#!/usr/bin/env python3
"""
PPDX Web Demo - Simple Real Integration (HTTP only)

Version này sẽ:

✅ No WebSocket bugs
✅ Real PPDX integration
✅ HTTP-only (đơn giản hơn)
✅ Same functionality nhưng không có real-time updates
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import real PPDX modules
try:
    from retrieval_pipeline_orchestrator import create_default_pipeline_config
    from run_retrieval_and_qa_pipeline import DetailedPipelineProcessor
    
    PPDX_AVAILABLE = True
    print("✅ Real PPDX modules loaded successfully")
    
except ImportError as e:
    print(f"❌ Failed to import PPDX modules: {e}")
    PPDX_AVAILABLE = False

# FastAPI app
app = FastAPI(title="PPDX Web Demo - Simple Real")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
pipeline_processor = None

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    max_passages: int = 10
    max_triples: int = 20
    enable_answer_generation: bool = True
    enable_context_expansion: bool = False

def initialize_ppdx():
    """Initialize real PPDX pipeline"""
    global pipeline_processor
    
    if not PPDX_AVAILABLE:
        return False
    
    try:
        print("🔄 Initializing PPDX pipeline...")
        
        config = create_default_pipeline_config()
        config.dual_retrieval_config.max_passages = 5
        config.dual_retrieval_config.max_triples = 10
        config.dual_retrieval_config.embedding_model = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
        config.dual_retrieval_config.batch_size = 4
        config.enable_context_expansion = False
        config.enable_answer_generation = True
        config.max_final_passages = 5
        
        pipeline_processor = DetailedPipelineProcessor(config)
        
        print("✅ Real PPDX pipeline initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize PPDX: {e}")
        return False

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main UI"""
    html_file = current_dir / "index.html"
    if html_file.exists():
        with open(html_file, "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    else:
        return HTMLResponse("<h1>❌ index.html not found</h1>")

@app.get("/api/health")
async def check_system_health():
    """Check system status"""
    global pipeline_processor
    
    if not pipeline_processor and PPDX_AVAILABLE:
        init_success = initialize_ppdx()
        return {
            "neo4j": "connected" if init_success else "error",
            "vector_db": "ready" if init_success else "error",
            "llm_service": "available" if init_success else "error",
            "ppdx_loaded": init_success
        }
    
    return {
        "neo4j": "connected" if pipeline_processor else "error",
        "vector_db": "ready" if pipeline_processor else "error",
        "llm_service": "available" if pipeline_processor else "error",
        "ppdx_loaded": pipeline_processor is not None
    }

@app.post("/api/process")
async def process_question(request: QuestionRequest):
    """Process question using real PPDX"""
    global pipeline_processor
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Initialize if needed
    if not pipeline_processor:
        print("🔄 First request - initializing PPDX...")
        if not initialize_ppdx():
            raise HTTPException(status_code=503, detail="PPDX system not available")
    
    try:
        print(f"🔍 Processing with real PPDX: {request.question[:50]}...")
        start_time = time.time()
        
        # Configure pipeline
        if hasattr(pipeline_processor.config, 'dual_retrieval_config'):
            pipeline_processor.config.dual_retrieval_config.max_passages = min(request.max_passages, 5)
            pipeline_processor.config.dual_retrieval_config.max_triples = min(request.max_triples, 10)
        
        pipeline_processor.config.enable_answer_generation = request.enable_answer_generation
        pipeline_processor.config.enable_context_expansion = request.enable_context_expansion
        
        # Process question
        result = pipeline_processor.process_single_query_detailed(
            query=request.question,
            query_id=f"WEB_{int(time.time() * 1000)}"
        )
        
        processing_time = time.time() - start_time
        print(f"✅ Real PPDX processing completed in {processing_time:.2f}s")
        
        return result
        
    except Exception as e:
        print(f"❌ Real PPDX processing failed: {e}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting PPDX Web Demo (Simple Real Integration)...")
    print("📡 Server will be available at: http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
