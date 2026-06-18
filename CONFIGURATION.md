# Configuration Template - Standalone Local LLM Workspace

## Quick Configuration Guide

### Option 1: Using Ollama (Recommended)

1. **Install Ollama**
   - Download from https://ollama.ai
   - Run: `ollama serve`

2. **Pull a Model**
   ```bash
   # In another terminal
   ollama pull mistral          # or llama2, neural-chat, etc.
   ```

3. **Configure Application**
   ```env
   LLM_ADAPTER=ollama
   LLM_ENDPOINT=http://localhost:11434
   LLM_MODEL=mistral
   ```

### Option 2: Using Generic REST API

1. **Have your LLM service running**
   - Ensure it has a `/v1/chat/completions` endpoint
   - Ensure it has a `/v1/embeddings` endpoint (if using search)

2. **Configure Application**
   ```env
   LLM_ADAPTER=generic
   LLM_ENDPOINT=http://your-api-server:port
   LLM_MODEL=your-model-name
   ```

### Option 3: Custom Implementation

1. **Create Custom Adapter**
   - See INTEGRATION.md for instructions
   - Implement LocalLLMConnector interface
   - Register in factory.py

2. **Configure Application**
   ```env
   LLM_ADAPTER=custom
   LLM_ENDPOINT=http://localhost:8080
   LLM_MODEL=your-model
   ```

---

## Full Configuration Reference

### Application Settings
```env
# Application name and version
APP_NAME=Standalone Local LLM Workspace
APP_VERSION=0.1.0

# Debug mode (false for production)
DEBUG=false
```

### API Server Configuration
```env
# Host and port for backend API
API_HOST=0.0.0.0
API_PORT=8000

# Full URL for API access
API_BASE_URL=http://localhost:8000
```

### Frontend Configuration
```env
# Frontend port
FRONTEND_PORT=3000

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### LLM Connector Configuration
```env
# Adapter type: generic, ollama, or custom
LLM_ADAPTER=ollama

# Local LLM endpoint (your service URL)
LLM_ENDPOINT=http://localhost:11434

# Model name to use
LLM_MODEL=mistral

# Request timeout in seconds
LLM_TIMEOUT=300

# Context window size (max tokens)
LLM_CONTEXT_LIMIT=4096

# Keep-alive connection timeout
LLM_KEEP_ALIVE=300
```

### Workspace Configuration
```env
# Root workspace directory
WORKSPACE_ROOT=workspace

# Subdirectories (relative to WORKSPACE_ROOT)
# Don't usually need to change these
MODULES_DIR=workspace/modules
INDEXES_DIR=workspace/indexes
MEMORY_DIR=workspace/memory
LOGS_DIR=workspace/logs
PATCHES_DIR=workspace/patches
```

### Feature Flags
```env
# Enable/disable Ollama adapter
ENABLE_OLLAMA_ADAPTER=true

# Enable/disable code review features
ENABLE_CODE_REVIEW=true

# Enable/disable safe patching
ENABLE_SAFE_PATCHING=true

# Enable/disable embeddings
ENABLE_EMBEDDINGS=true
```

---

## Environment Setup Methods

### Method 1: .env File (Recommended)
Create `.env` in project root with your settings:
```env
LLM_ADAPTER=ollama
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=mistral
API_PORT=8000
```

### Method 2: Export Environment Variables
```bash
export LLM_ADAPTER=ollama
export LLM_ENDPOINT=http://localhost:11434
export LLM_MODEL=mistral

./run.sh
```

### Method 3: Docker Environment
```bash
docker run -e LLM_ADAPTER=ollama \
           -e LLM_ENDPOINT=http://ollama:11434 \
           standalone-llm-workspace
```

---

## Available LLM Models

### Ollama Models
```
ollama pull mistral           # 7B - Fast, good quality
ollama pull llama2            # 7B/13B - General purpose
ollama pull neural-chat       # 7B - Conversational
ollama pull openchat          # 7B - Optimized
ollama pull zephyr            # 7B - High quality
ollama pull dolphin-mix       # 7B - Versatile
```

### Model Selection Guide
- **Fast/Light**: mistral, neural-chat (7B models)
- **Accurate**: llama2 13B, zephyr (13B+ models)
- **General**: mistral, llama2 7B
- **Specialized**: dolphin-mix, openchat

---

## Troubleshooting Configuration

### LLM Connection Issues
```bash
# Test connection
curl http://localhost:11434/api/tags    # For Ollama
curl http://localhost:8080/health       # For generic

# Check environment
cat .env | grep LLM

# Verify in logs
tail -f workspace/logs/backend.log
```

### Port Conflicts
```bash
# Check what's using a port
lsof -i :8000      # Check port 8000
lsof -i :3000      # Check port 3000

# Change ports in .env
API_PORT=8001
FRONTEND_PORT=3001
```

### Model Not Available
```bash
# List available models
ollama list

# Pull model
ollama pull mistral

# Update .env
LLM_MODEL=mistral
```

---

## Performance Tuning

### For Better Speed
```env
LLM_MODEL=mistral          # Smaller models are faster
LLM_TIMEOUT=60             # Shorter timeout for quick failures
LLM_CONTEXT_LIMIT=2048     # Smaller context window
```

### For Better Quality
```env
LLM_MODEL=llama2            # Larger models are more accurate
LLM_TIMEOUT=300             # Longer timeout for complex queries
LLM_CONTEXT_LIMIT=4096      # Larger context window
```

---

## Security Configuration

### For Local Development
```env
DEBUG=true
# Default settings fine for local use
```

### For Production
```env
DEBUG=false
API_HOST=127.0.0.1         # Only listen locally
# Use reverse proxy (nginx) for access control
# Enable HTTPS at proxy level
# Implement API key authentication
```

---

## Docker Configuration

### Example docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "3000:3000"
    environment:
      - LLM_ADAPTER=ollama
      - LLM_ENDPOINT=http://ollama:11434
      - LLM_MODEL=mistral
    depends_on:
      - ollama
  
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  ollama_data:
```

---

## Configuration Examples

### Example 1: Ollama with Mistral
```env
LLM_ADAPTER=ollama
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=mistral
DEBUG=false
```

### Example 2: Generic REST API
```env
LLM_ADAPTER=generic
LLM_ENDPOINT=http://192.168.1.100:8080
LLM_MODEL=gpt-3.5-turbo
DEBUG=true
```

### Example 3: Custom Ports
```env
API_PORT=8001
FRONTEND_PORT=3001
LLM_ADAPTER=ollama
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=neural-chat
```

### Example 4: Production Setup
```env
DEBUG=false
API_HOST=127.0.0.1
API_PORT=8000
LLM_ADAPTER=ollama
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=mistral
LLM_TIMEOUT=120
WORKSPACE_ROOT=/var/llm-workspace
```

---

## Validation Checklist

Before running `./run.sh`, verify:
- [ ] Python 3.8+ installed: `python3 --version`
- [ ] Your LLM service is running
- [ ] Network ports 8000 and 3000 are free (or configured)
- [ ] `.env` file has LLM_ENDPOINT configured correctly
- [ ] `workspace/modules/` directory exists (or will be created)
- [ ] Write permissions to `workspace/` directory

---

## Getting Help

- Full documentation: README.md
- API reference: http://localhost:8000/docs (when running)
- Integration guide: INTEGRATION.md
- Build guide: BUILD.md

---

**Keep your LLM local. Keep your data yours.**
