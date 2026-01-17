from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from dotenv import load_dotenv
from app.chat import router as chat_router

load_dotenv()

app = FastAPI(
    title="Department AI Backend",
    description="FastAPI backend with LangGraph, MCP, and RAG",
    version="0.1.0"
)

# Include chat router
app.include_router(chat_router)

# CORS middleware for iframe embedding
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # host-site
        "http://localhost:3001",  # frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "service": "Department AI Backend",
        "status": "running",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "chat": "/api/chat (coming soon)",
            "workflows": "/api/workflows (coming soon)",
            "rag": "/api/rag (coming soon)"
        }
    }

@app.get("/health")
async def health_check(x_mock_user: Optional[str] = Header(None)):
    """Health check endpoint with optional mock user authentication"""
    return {
        "status": "healthy",
        "auth_mode": "development" if x_mock_user else "production",
        "authenticated_user": x_mock_user or "anonymous",
        "services": {
            "database": "not_connected",
            "vector_store": "not_initialized",
            "openai": "not_configured",
            "mcp_servers": "not_connected"
        }
    }

@app.get("/api/config")
async def get_config():
    """Return current configuration (safe subset)"""
    return {
        "openai_base_url": os.getenv("OPENAI_BASE_URL", "not_configured"),
        "openai_model": os.getenv("OPENAI_MODEL", "not_configured"),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
