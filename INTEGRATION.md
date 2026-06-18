# API Integration Guide

## Local LLM Connector Interface

All adapters must implement:

```python
class LocalLLMConnector(ABC):
    async def send_chat(
        self, 
        messages: List[ChatMessage],
        config: Optional[ConnectorConfig] = None,
        stream: bool = False
    ) -> str:
        """Send a chat request to the local LLM."""
        pass
    
    async def embed_text(
        self,
        items: List[str],
        config: Optional[ConnectorConfig] = None
    ) -> List[List[float]]:
        """Generate embeddings for text items."""
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health and readiness of the LLM connector."""
        pass
    
    async def list_models(self) -> List[str]:
        """List available models."""
        pass
    
    async def get_active_model(self) -> str:
        """Get the currently active model."""
        pass
    
    def supports_structured_output(self) -> bool:
        """Check if connector supports structured output."""
        pass
    
    def supports_tool_calls(self) -> bool:
        """Check if connector supports tool/function calling."""
        pass
    
    def get_context_limit(self) -> int:
        """Get the context window limit."""
        pass
```

## Example: Adding Ollama Support

The Ollama adapter is already included. Configuration:

```env
LLM_ADAPTER=ollama
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=mistral
```

## Example: Adding Custom REST API

```python
# backend/app/connectors/adapters/custom_rest_adapter.py

import aiohttp
from app.connectors import LocalLLMConnector, ChatMessage, ConnectorConfig

class CustomRestAdapter(LocalLLMConnector):
    def __init__(self, config: ConnectorConfig):
        self.config = config
        self.endpoint = config.endpoint
        self.model = config.model
    
    async def send_chat(self, messages, config=None, stream=False):
        config = config or self.config
        
        # Your implementation here
        payload = {
            "model": config.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{config.endpoint}/chat", json=payload) as resp:
                data = await resp.json()
                return data.get("response", "")
    
    # ... implement other methods ...
```

Register in factory:

```python
# backend/app/connectors/factory.py

from app.connectors.adapters.custom_rest_adapter import CustomRestAdapter

class ConnectorFactory:
    _adapters = {
        AdapterType.CUSTOM_REST: CustomRestAdapter,
        # ... others ...
    }
```

## REST API Usage

### Chat Request
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What does this function do?",
    "context": "Repository: my-project",
    "intent": "chat"
  }'
```

### Code Review Request
```bash
curl -X POST http://localhost:8000/api/review/code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def foo():\n    pass",
    "language": "python",
    "context": "utility function"
  }'
```

### Workspace Scan
```bash
curl -X POST http://localhost:8000/api/workspace/scan
```

### Get Health Status
```bash
curl http://localhost:8000/api/health/llm
```

## WebSocket Support (Future)

For streaming responses, WebSocket support can be added:

```python
from fastapi import WebSocket

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    # Implement streaming chat
```

## Tool Execution

Tools can be registered and executed:

```python
@router.post("/tools/execute")
async def execute_tool(tool_name: str, params: Dict[str, Any]):
    # Safe tool execution with sandboxing
    pass
```

---

For more information, see the full API documentation at `/docs` when the application is running.
