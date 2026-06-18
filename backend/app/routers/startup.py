"""Startup API routes."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import logging

from app.modules.startup_manager import StartupManager
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/check")
async def check_startup() -> Dict[str, Any]:
    """Check startup readiness."""
    try:
        checks = {
            "system": await StartupManager.check_system_requirements(),
            "workspace": await StartupManager.prepare_workspace(),
            "llm": await StartupManager.check_llm_connection(),
        }
        return checks
    except Exception as e:
        logger.error(f"Startup check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bootstrap")
async def bootstrap() -> Dict[str, Any]:
    """Bootstrap the application."""
    try:
        result = await StartupManager.bootstrap()
        return result
    except Exception as e:
        logger.error(f"Bootstrap failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
