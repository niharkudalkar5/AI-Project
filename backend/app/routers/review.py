"""Code review API routes."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from app.modules.code_reviewer import CodeReviewer

router = APIRouter()
logger = logging.getLogger(__name__)

reviewer = CodeReviewer()

class ReviewRequest(BaseModel):
    """Code review request."""
    code: str
    language: str = "python"
    context: Optional[str] = None

@router.post("/code")
async def review_code(request: ReviewRequest) -> Dict[str, Any]:
    """Review provided code."""
    try:
        result = await reviewer.review_code(
            request.code,
            language=request.language,
            context=request.context or ""
        )
        return result
    except Exception as e:
        logger.error(f"Code review failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
