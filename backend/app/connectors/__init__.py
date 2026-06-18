"""Local LLM Connector - Abstract interface for any local LLM backend."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AdapterType(str, Enum):
    """Supported LLM adapter types."""
    GENERIC = "generic"
    OLLAMA = "ollama"
    CUSTOM = "custom"

@dataclass
class ChatMessage:
    """Chat message structure."""
    role: str  # "user", "assistant", "system"
    content: str

@dataclass
class ConnectorConfig:
    """Connector configuration."""
    adapter_type: AdapterType
    endpoint: str
    model: str
    timeout: int = 300
    context_limit: int = 4096
    keep_alive: int = 300

class LocalLLMConnector(ABC):
    """Abstract base class for local LLM connectors."""
    
    @abstractmethod
    async def send_chat(
        self, 
        messages: List[ChatMessage],
        config: Optional[ConnectorConfig] = None,
        stream: bool = False
    ) -> str:
        """Send a chat request to the local LLM."""
        pass
    
    @abstractmethod
    async def embed_text(
        self,
        items: List[str],
        config: Optional[ConnectorConfig] = None
    ) -> List[List[float]]:
        """Generate embeddings for text items."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check health and readiness of the LLM connector."""
        pass
    
    @abstractmethod
    async def list_models(self) -> List[str]:
        """List available models."""
        pass
    
    @abstractmethod
    async def get_active_model(self) -> str:
        """Get the currently active model."""
        pass
    
    @abstractmethod
    def supports_structured_output(self) -> bool:
        """Check if connector supports structured output."""
        pass
    
    @abstractmethod
    def supports_tool_calls(self) -> bool:
        """Check if connector supports tool/function calling."""
        pass
    
    @abstractmethod
    def get_context_limit(self) -> int:
        """Get the context window limit."""
        pass
