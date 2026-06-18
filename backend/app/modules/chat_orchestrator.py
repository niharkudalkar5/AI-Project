"""Chat Orchestrator module."""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.connectors import ChatMessage
from app.connectors.factory import get_connector

logger = logging.getLogger(__name__)

class ChatOrchestrator:
    """Manages chat interactions and intent routing."""
    
    def __init__(self):
        """Initialize the chat orchestrator."""
        self.connector = get_connector()
        self.conversation_history: List[Dict[str, Any]] = []
    
    async def process_message(
        self,
        user_message: str,
        context: Optional[str] = None,
        intent: str = "chat"
    ) -> Dict[str, Any]:
        """
        Process a user message and generate response.
        
        Args:
            user_message: The user's input message
            context: Optional context about current repository or file
            intent: Type of intent (chat, review, modify, build)
            
        Returns:
            Response dictionary with content and metadata
        """
        try:
            # Build prompt with context
            system_prompt = self._build_system_prompt(intent)
            if context:
                full_message = f"Context: {context}\n\n{user_message}"
            else:
                full_message = user_message
            
            # Prepare messages
            messages = [
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=full_message),
            ]
            
            # Get response from LLM
            response = await self.connector.send_chat(messages)
            
            # Store in history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "intent": intent,
                "user_message": user_message,
                "response": response,
                "context": context
            })
            
            return {
                "success": True,
                "response": response,
                "intent": intent,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Chat processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "intent": intent
            }
    
    def _build_system_prompt(self, intent: str) -> str:
        """Build system prompt based on intent."""
        prompts = {
            "chat": "You are a helpful AI assistant for code analysis and development.",
            "review": "You are an expert code reviewer. Analyze the provided code and give structured feedback.",
            "modify": "You are a code generation AI. Generate clean, well-documented code changes.",
            "build": "You are a build system assistant. Help debug build issues and optimize builds.",
        }
        return prompts.get(intent, prompts["chat"])
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
