"""
===============================================================================
GLOBAL IT KNOWLEDGE HUB — FASTAPI WEB APPLICATION (main.py)
===============================================================================
This is the primary application server for Global IT Knowledge Hub:
- Implements the `/api/chat` grounded retrieval-augmented generation (RAG) pipeline
- Serves the frontend single-page application and static assets
- Provides `/api/companies` for dynamic tabs and category dropdowns
- Provides `/api/health` for monitoring cloud connection status

===============================================================================
✏️ HOW TO MODIFY THIS FILE:
===============================================================================
1. TO CHANGE THE MAXIMUM QUESTION LENGTH:
   - Modify `MAX_QUESTION_LENGTH` below (default is 1,500 characters).

2. TO ENABLE CROSS-ORIGIN REQUESTS (CORS) FOR AN EXTERNAL FRONTEND:
   - Adjust the `origins` list inside the CORSMiddleware configuration.

3. TO RUN ON A DIFFERENT HOST OR PORT:
   - Modify the `config.DEFAULT_HOST` or `config.DEFAULT_PORT` in `config.py`
     or run with: `uvicorn main:app --host 0.0.0.0 --port 3000`
===============================================================================
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import config
import companies
import data_seed
import azure_search
import foundry_ai


# -----------------------------------------------------------------------------
# Base Directories
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


# -----------------------------------------------------------------------------
# FastAPI App Initialization
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Global IT Knowledge Hub",
    description="Official enterprise IT knowledge search and grounded AI question answering.",
    version="1.0.0"
)


# =============================================================================
# ✏️ MODIFY HERE: CORS Settings (if calling API from a separate frontend domain)
# =============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Request & Response Data Models
# =============================================================================
# ✏️ MODIFY HERE: Maximum question length restriction
MAX_QUESTION_LENGTH = 1500


class ChatRequest(BaseModel):
    """Payload sent by the frontend search form."""
    question: str = Field(..., description="The user's query up to 1,500 characters")
    company: str = Field(default="all", description="Selected company tab ID, e.g. 'Microsoft', 'AWS', or 'all'")
    category: str = Field(default="All Categories", description="Selected category filter name")


class SourceDocumentResponse(BaseModel):
    """Schema for individual official source citations."""
    company: str
    category: str
    title: str
    url: str
    updatedAt: str
    content: Optional[str] = None


class ChatResponse(BaseModel):
    """Response returned to the user containing the answer and official references."""
    answer: str
    sources: List[SourceDocumentResponse]
    mode: Optional[str] = None


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/api/companies")
def get_companies_and_categories():
    """
    Returns the company tabs and knowledge categories for frontend rendering.
    """
    return {
        "companies": companies.COMPANIES,
        "categories": companies.CATEGORIES
    }


@app.get("/api/health")
def get_health_status():
    """
    Returns configuration and operational status of Azure AI services.
    """
    return config.get_status_summary()


@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    """
    Core Grounded Question-Answering Endpoint:
    1. Validates the question length (<= 1500 characters)
    2. Searches Azure AI Search (or local index) filtered by company and category
    3. Feeds official source context to Azure AI Foundry model
    4. Returns grounded answer with direct links to official documents
    """
    question = payload.question.strip() if payload.question else ""

    # Input validation
    if not question or len(question) > MAX_QUESTION_LENGTH:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"Enter a question of up to {MAX_QUESTION_LENGTH:,} characters."}
        )

    try:
        # Step 1: Retrieve relevant documents from Azure AI Search (or local index)
        sources = azure_search.search_documents(
            query=question,
            company=payload.company,
            category=payload.category,
            top=5
        )

        # Step 2: Handle empty search results gracefully
        if not sources:
            return ChatResponse(
                answer=(
                    "I couldn't find a matching document in the current official-source library. "
                    "Try another company or topic. This does not mean the company has no such policy."
                ),
                sources=[]
            )

        # Step 3: Call Azure AI Foundry (or local grounded synthesis)
        answer = foundry_ai.answer_question(
            question=question,
            company=payload.company,
            sources=sources
        )

        # Step 4: Format and return sanitized source records
        formatted_sources = [
            SourceDocumentResponse(
                company=s.get("company", "Unknown"),
                category=s.get("category", "General"),
                title=s.get("title", "Official Publication"),
                url=s.get("url", "#"),
                updatedAt=s.get("updatedAt", "N/A"),
                content=s.get("content", "")
            )
            for s in sources
        ]

        mode = "Azure Cloud" if config.is_azure_foundry_configured() else "Local Grounded Engine"
        return ChatResponse(answer=answer, sources=formatted_sources, mode=mode)

    except Exception as e:
        print(f"[API Error] Exception in /api/chat: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Unable to process the question. Check the server configuration."}
        )


@app.post("/api/seed")
def seed_endpoint():
    """
    Triggers index creation and uploads official seed documents to Azure AI Search.
    Can be called directly from an admin portal or curl command.
    """
    try:
        index_res = azure_search.create_or_update_index()
        docs_res = azure_search.upload_documents(data_seed.INITIAL_DOCUMENTS)
        return {
            "index_result": index_res,
            "upload_result": docs_res,
            "documents_count": len(data_seed.INITIAL_DOCUMENTS)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Seeding failed: {str(e)}"
        )


# =============================================================================
# Frontend Static Files & Single-Page Application Serving
# =============================================================================

# Mount the static directory for CSS, JS, and image assets
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def serve_index():
    """Serves the primary Single-Page Application interface."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse({"message": "Global IT Knowledge Hub API is running. UI not found in static/."})


# =============================================================================
# Standalone CLI Entrypoint
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    print("===============================================================")
    print(f"[*] Starting Global IT Knowledge Hub on http://{config.DEFAULT_HOST}:{config.DEFAULT_PORT}")
    print(f"[*] Search Engine: {'Azure AI Search' if config.is_azure_search_configured() else 'Local Grounded Index'}")
    print(f"[*] AI Inference:  {'Azure AI Foundry' if config.is_azure_foundry_configured() else 'Local Grounded Synthesis'}")
    print("===============================================================")
    uvicorn.run(
        "main:app",
        host=config.DEFAULT_HOST,
        port=config.DEFAULT_PORT,
        reload=True
    )
