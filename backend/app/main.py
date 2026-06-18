"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.routers import startup, health, chat, workspace, search, review, repo, memory

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Configured LLM Adapter: {settings.LLM_ADAPTER}")
    logger.info(f"Workspace Root: {settings.WORKSPACE_ROOT}")
    yield
    logger.info("Shutting down application")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Standalone Local LLM Workspace for Code Analysis and Generation",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(startup.router, prefix="/api/startup", tags=["Startup"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(workspace.router, prefix="/api/workspace", tags=["Workspace"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(review.router, prefix="/api/review", tags=["Review"])
app.include_router(repo.router, prefix="/api/repo", tags=["Repository"])
app.include_router(memory.router, prefix="/api/memory", tags=["Memory"])

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info"
    )
