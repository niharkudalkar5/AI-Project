"""Generic local LLM adapter."""
import aiohttp
import json
import logging
from typing import List, Dict, Any, Optional

from app.connectors import LocalLLMConnector, ChatMessage, ConnectorConfig, AdapterType

logger = logging.getLogger(__name__)

class GenericAdapter(LocalLLMConnector):
    """Generic REST-based local LLM adapter."""
    
    def __init__(self, config: ConnectorConfig):
        """Initialize the generic adapter."""
        self.config = config
        self.endpoint = config.endpoint
        self.model = config.model
        self.timeout = aiohttp.ClientTimeout(total=config.timeout)
        
    async def send_chat(
        self,
        messages: List[ChatMessage],
        config: Optional[ConnectorConfig] = None,
        stream: bool = False
    ) -> str:
        """Send a chat request to the local LLM."""
        config = config or self.config
        
        payload = {
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "model": config.model,
            "stream": stream
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{config.endpoint}/v1/chat/completions",
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    else:
                        logger.error(f"API error: {response.status}")
                        return f"Error: {response.status}"
        except Exception as e:
            logger.error(f"Chat request failed: {e}")
            return f"Error: {str(e)}"
    
    async def embed_text(
        self,
        items: List[str],
        config: Optional[ConnectorConfig] = None
    ) -> List[List[float]]:
        """Generate embeddings for text items."""
        config = config or self.config
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{config.endpoint}/v1/embeddings",
                    json={"input": items, "model": config.model}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        embeddings = [item["embedding"] for item in data.get("data", [])]
                        return embeddings
                    else:
                        logger.error(f"Embeddings API error: {response.status}")
                        return []
        except Exception as e:
            logger.error(f"Embedding request failed: {e}")
            return []
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health and readiness of the LLM connector."""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.config.endpoint}/health") as response:
                    if response.status == 200:
                        return {
                            "status": "healthy",
                            "endpoint": self.config.endpoint,
                            "adapter": "generic"
                        }
                    else:
                        return {"status": "unhealthy", "error": f"HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def list_models(self) -> List[str]:
        """List available models."""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.config.endpoint}/v1/models") as response:
                    if response.status == 200:
                        data = await response.json()
                        return [m.get("id") for m in data.get("data", [])]
                    return []
        except Exception as e:
            logger.error(f"List models failed: {e}")
            return []
    
    async def get_active_model(self) -> str:
        """Get the currently active model."""
        return self.config.model
    
    def supports_structured_output(self) -> bool:
        """Check if connector supports structured output."""
        return False
    
    def supports_tool_calls(self) -> bool:
        """Check if connector supports tool/function calling."""
        return False
    
    def get_context_limit(self) -> int:
        """Get the context window limit."""
        return self.config.context_limit
