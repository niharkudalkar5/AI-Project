"""Workspace API routes."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from app.modules.workspace_mapper import WorkspaceMapper
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

mapper = WorkspaceMapper(settings.WORKSPACE_ROOT)

@router.post("/scan")
async def scan_workspace() -> Dict[str, Any]:
    """Scan the workspace for modules."""
    try:
        result = await mapper.scan_modules()
        return result
    except Exception as e:
        logger.error(f"Workspace scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/repos")
async def get_repositories() -> Dict[str, Any]:
    """Get registered repositories."""
    try:
        repos = mapper.get_registered_modules()
        return {
            "repositories": repos,
            "count": len(repos)
        }
    except Exception as e:
        logger.error(f"Failed to get repositories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/repos/{repo_name}")
async def get_repository(repo_name: str) -> Dict[str, Any]:
    """Get details of a specific repository."""
    try:
        repo = mapper.get_module(repo_name)
        if not repo:
            raise HTTPException(status_code=404, detail="Repository not found")
        return repo
    except Exception as e:
        logger.error(f"Failed to get repository: {e}")
        raise HTTPException(status_code=500, detail=str(e))
