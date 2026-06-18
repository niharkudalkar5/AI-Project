"""Startup Manager module."""
import os
import logging
import asyncio
from typing import Dict, Any
from pathlib import Path

from app.config import settings
from app.connectors.factory import get_connector

logger = logging.getLogger(__name__)

class StartupManager:
    """Manages application startup and initialization."""
    
    @staticmethod
    async def check_system_requirements() -> Dict[str, Any]:
        """Check system dependencies."""
        checks = {
            "python": True,
            "git": os.system("which git > /dev/null 2>&1") == 0,
            "node": os.system("which node > /dev/null 2>&1") == 0,
        }
        return checks
    
    @staticmethod
    async def prepare_workspace() -> Dict[str, Any]:
        """Prepare workspace directories."""
        dirs = [
            settings.MODULES_DIR,
            settings.INDEXES_DIR,
            settings.MEMORY_DIR,
            settings.LOGS_DIR,
            settings.PATCHES_DIR,
        ]
        
        results = {}
        for dir_path in dirs:
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                results[dir_path] = "ready"
                logger.info(f"Workspace directory ready: {dir_path}")
            except Exception as e:
                results[dir_path] = f"error: {str(e)}"
                logger.error(f"Failed to create workspace directory {dir_path}: {e}")
        
        return results
    
    @staticmethod
    async def check_llm_connection() -> Dict[str, Any]:
        """Check local LLM connection."""
        try:
            connector = get_connector()
            health = await connector.health_check()
            models = await connector.list_models()
            
            return {
                "connected": health.get("status") == "healthy",
                "health": health,
                "models": models,
                "active_model": await connector.get_active_model(),
                "adapter": settings.LLM_ADAPTER,
                "context_limit": connector.get_context_limit(),
                "supports_structured": connector.supports_structured_output(),
                "supports_tools": connector.supports_tool_calls(),
            }
        except Exception as e:
            logger.error(f"LLM connection check failed: {e}")
            return {
                "connected": False,
                "error": str(e),
                "adapter": settings.LLM_ADAPTER,
            }
    
    @staticmethod
    async def bootstrap() -> Dict[str, Any]:
        """Full bootstrap process."""
        progress = {}
        
        # Check system requirements
        progress["system_check"] = await StartupManager.check_system_requirements()
        logger.info("✓ System requirements checked")
        
        # Prepare workspace
        progress["workspace"] = await StartupManager.prepare_workspace()
        logger.info("✓ Workspace prepared")
        
        # Check LLM connection
        progress["llm_connection"] = await StartupManager.check_llm_connection()
        if progress["llm_connection"]["connected"]:
            logger.info("✓ Local LLM connected")
        else:
            logger.warning("⚠ Local LLM not available")
        
        progress["status"] = "ready"
        return progress
