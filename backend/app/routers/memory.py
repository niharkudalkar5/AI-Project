"""Memory API routes."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging

from app.modules.memory_manager import MemoryManager
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

memory_manager = MemoryManager(settings.MEMORY_DIR)

@router.get("/{session_id}")
async def get_session(session_id: str) -> Dict[str, Any]:
    """Get a session from memory."""
    try:
        session = memory_manager.load_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session
    except Exception as e:
        logger.error(f"Failed to get session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{session_id}")
async def save_session(session_id: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
    """Save a session to memory."""
    try:
        success = memory_manager.save_session(session_id, session_data)
        return {
            "saved": success,
            "session_id": session_id
        }
    except Exception as e:
        logger.error(f"Failed to save session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def list_sessions() -> Dict[str, Any]:
    """List all sessions."""
    try:
        sessions = memory_manager.list_sessions()
        return {
            "sessions": sessions,
            "count": len(sessions)
        }
    except Exception as e:
        logger.error(f"Failed to list sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{session_id}")
async def delete_session(session_id: str) -> Dict[str, Any]:
    """Delete a session."""
    try:
        success = memory_manager.delete_session(session_id)
        return {
            "deleted": success,
            "session_id": session_id
        }
    except Exception as e:
        logger.error(f"Failed to delete session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
