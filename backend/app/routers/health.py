"""Health check API routes."""
from fastapi import APIRouter
from typing import Dict, Any
import logging

from app.connectors.factory import get_connector
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("")
async def health() -> Dict[str, Any]:
    """Application health status."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }

@router.get("/llm")
async def health_llm() -> Dict[str, Any]:
    """Local LLM health status."""
    try:
        connector = get_connector()
        health = await connector.health_check()
        return health
    except Exception as e:
        logger.error(f"LLM health check failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "adapter": settings.LLM_ADAPTER
        }

@router.get("/models")
async def get_models() -> Dict[str, Any]:
    """Get available LLM models."""
    try:
        connector = get_connector()
        models = await connector.list_models()
        active = await connector.get_active_model()
        
        return {
            "models": models,
            "active_model": active,
            "adapter": settings.LLM_ADAPTER,
        }
    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        return {
            "error": str(e),
            "models": []
        }
