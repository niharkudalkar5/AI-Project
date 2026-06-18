"""Chat API routes."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from app.modules.chat_orchestrator import ChatOrchestrator

router = APIRouter()
logger = logging.getLogger(__name__)

# Global orchestrator instance
orchestrator = ChatOrchestrator()

class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    context: Optional[str] = None
    intent: str = "chat"  # chat, review, modify, build

@router.post("")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    """Send a chat message."""
    try:
        result = await orchestrator.process_message(
            request.message,
            context=request.context,
            intent=request.intent
        )
        return result
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def chat_stream(request: ChatRequest) -> Dict[str, Any]:
    """Send a chat message with streaming."""
    # Streaming implementation - simplified version
    try:
        result = await orchestrator.process_message(
            request.message,
            context=request.context,
            intent=request.intent
        )
        return result
    except Exception as e:
        logger.error(f"Stream chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history() -> Dict[str, Any]:
    """Get chat history."""
    return {
        "history": orchestrator.get_history(),
        "count": len(orchestrator.get_history())
    }

@router.post("/clear-history")
async def clear_history() -> Dict[str, Any]:
    """Clear chat history."""
    orchestrator.clear_history()
    return {"status": "cleared"}
