"""Connector factory and registry."""
from typing import Optional
import logging

from app.connectors import LocalLLMConnector, ConnectorConfig, AdapterType
from app.connectors.adapters.generic_adapter import GenericAdapter
from app.connectors.adapters.ollama_adapter import OllamaAdapter
from app.config import settings

logger = logging.getLogger(__name__)

class ConnectorFactory:
    """Factory for creating LLM connectors based on adapter type."""
    
    _adapters = {
        AdapterType.GENERIC: GenericAdapter,
        AdapterType.OLLAMA: OllamaAdapter,
    }
    
    @classmethod
    def create_connector(
        cls,
        adapter_type: Optional[str] = None,
        config: Optional[ConnectorConfig] = None
    ) -> LocalLLMConnector:
        """
        Create a connector instance.
        
        Args:
            adapter_type: Type of adapter (generic, ollama, custom)
            config: Connector configuration
            
        Returns:
            LocalLLMConnector instance
        """
        adapter_type = adapter_type or settings.LLM_ADAPTER
        
        if config is None:
            config = ConnectorConfig(
                adapter_type=AdapterType(adapter_type),
                endpoint=settings.LLM_ENDPOINT,
                model=settings.LLM_MODEL,
                timeout=settings.LLM_TIMEOUT,
                context_limit=settings.LLM_CONTEXT_LIMIT
            )
        
        try:
            adapter_class = cls._adapters.get(AdapterType(adapter_type))
            if not adapter_class:
                raise ValueError(f"Unknown adapter type: {adapter_type}")
            
            logger.info(f"Creating connector with adapter: {adapter_type}")
            return adapter_class(config)
        except Exception as e:
            logger.error(f"Failed to create connector: {e}")
            raise

# Global connector instance
_connector: Optional[LocalLLMConnector] = None

def get_connector() -> LocalLLMConnector:
    """Get or create the global connector instance."""
    global _connector
    if _connector is None:
        _connector = ConnectorFactory.create_connector()
    return _connector

def set_connector(connector: LocalLLMConnector):
    """Set the global connector instance."""
    global _connector
    _connector = connector
