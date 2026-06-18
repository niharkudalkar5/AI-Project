"""Ollama-compatible local LLM adapter."""
import aiohttp
import json
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator

from app.connectors import LocalLLMConnector, ChatMessage, ConnectorConfig, AdapterType

logger = logging.getLogger(__name__)

class OllamaAdapter(LocalLLMConnector):
    """Ollama-compatible local LLM adapter."""
    
    def __init__(self, config: ConnectorConfig):
        """Initialize the Ollama adapter."""
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
        """Send a chat request to Ollama."""
        config = config or self.config
        
        payload = {
            "model": config.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "stream": stream
        }
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    f"{config.endpoint}/api/chat",
                    json=payload
                ) as response:
                    if response.status == 200:
                        if stream:
                            # Handle streaming response
                            result = ""
                            async for line in response.content:
                                if line:
                                    data = json.loads(line.decode())
                                    result += data.get("message", {}).get("content", "")
                            return result
                        else:
                            data = await response.json()
                            return data.get("message", {}).get("content", "")
                    else:
                        logger.error(f"Ollama API error: {response.status}")
                        return f"Error: {response.status}"
        except Exception as e:
            logger.error(f"Ollama chat request failed: {e}")
            return f"Error: {str(e)}"
    
    async def embed_text(
        self,
        items: List[str],
        config: Optional[ConnectorConfig] = None
    ) -> List[List[float]]:
        """Generate embeddings using Ollama."""
        config = config or self.config
        embeddings = []
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                for item in items:
                    payload = {"model": config.model, "prompt": item}
                    async with session.post(
                        f"{config.endpoint}/api/embeddings",
                        json=payload
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            embeddings.append(data.get("embedding", []))
                        else:
                            logger.warning(f"Embeddings error for item: {response.status}")
                            embeddings.append([])
            return embeddings
        except Exception as e:
            logger.error(f"Ollama embeddings request failed: {e}")
            return [[] for _ in items]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health and readiness of Ollama."""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.config.endpoint}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        models = data.get("models", [])
                        return {
                            "status": "healthy",
                            "endpoint": self.config.endpoint,
                            "adapter": "ollama",
                            "available_models": len(models),
                            "active_model": self.config.model
                        }
                    else:
                        return {"status": "unhealthy", "error": f"HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def list_models(self) -> List[str]:
        """List available Ollama models."""
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(f"{self.config.endpoint}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        return [m.get("name") for m in data.get("models", [])]
                    return []
        except Exception as e:
            logger.error(f"List Ollama models failed: {e}")
            return []
    
    async def get_active_model(self) -> str:
        """Get the currently active model."""
        return self.config.model
    
    def supports_structured_output(self) -> bool:
        """Check if Ollama supports structured output."""
        return True
    
    def supports_tool_calls(self) -> bool:
        """Check if Ollama supports tool/function calling."""
        return True
    
    def get_context_limit(self) -> int:
        """Get the context window limit."""
        return self.config.context_limit
