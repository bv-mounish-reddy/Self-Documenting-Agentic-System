"""
FastAPI backend for the Self-Documentation Agent System.
Exposes the code documentation workflow as REST API endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add project root to path to import main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main workflow
import logging

# We'll import workflow functions lazily to avoid import-time failures
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("backend")
logging.basicConfig(level=logging.INFO)


# NOTE: `main.py` provides `run_documentation_workflow` as the callable

# Initialize FastAPI app
app = FastAPI(
    title="Self-Documentation Agent API",
    description="API for code documentation and analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class CodeAnalysisRequest(BaseModel):
    """Request model for code analysis"""
    code: str

class CodeAnalysisResponse(BaseModel):
    """Response model for code analysis"""
    status: str
    documented_code: str
    analysis: str
    libraries: list
    issues: list

@app.on_event("startup")
async def startup_event():
    """Initialize environment on startup"""
    logger.info("Backend startup: environment loaded from .env (if present)")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Self-Documentation Agent API",
        "version": "1.0.0"
    }

@app.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(request: CodeAnalysisRequest) -> CodeAnalysisResponse:
    """
    Analyze and document provided Python code.
    
    Args:
        request: CodeAnalysisRequest containing the code to analyze
        
    Returns:
        CodeAnalysisResponse with documented code and analysis results
        
    Raises:
        HTTPException: If code analysis fails
    """
    logger.info("Received analyze request; starting workflow")
    try:
        # Lazy import to provide clearer errors if main.py changes
        from main import run_documentation_workflow

        # Run the workflow (this will call setup_environment inside main if needed)
        result = run_documentation_workflow(request.code)

        logger.info("Workflow completed; preparing response")

        return CodeAnalysisResponse(
            status="success",
            documented_code=result.get("documented_code", ""),
            analysis="\n".join(result.get("test_results", [])),
            libraries=result.get("libraries_used", []),
            issues=result.get("issues_found", [])
        )
    except ImportError as ie:
        logger.exception("Import error while loading workflow from main.py")
        raise HTTPException(status_code=500, detail=f"Server misconfiguration: {ie}")
    except Exception as e:
        logger.exception("Error during code analysis")
        raise HTTPException(status_code=400, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "api": "Self-Documentation Agent",
        "ready": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
