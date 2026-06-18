# Standalone Local LLM Workspace

A complete, production-ready local AI workspace for code analysis, generation, review, and management. This is a **standalone application** that connects to any local LLM backend through a pluggable adapter architecture.

## Overview

The Standalone Local LLM Workspace enables developers to:

- **Chat** with a local LLM about code and projects
- **Analyze** repositories with automatic scanning and indexing
- **Review** code with AI-powered suggestions
- **Generate** code changes with safe approval workflows
- **Execute** builds and tests with full logging
- **Manage** session memory locally
- **Integrate** with any local LLM backend (Ollama-compatible or custom)

### Key Features

✅ **Standalone Architecture** - Not dependent on any single LLM vendor  
✅ **Local LLM Connector** - Pluggable adapter pattern for Ollama, generic REST, or custom backends  
✅ **Workspace Mapping** - Auto-discover and index modules/repositories  
✅ **Code Review** - AI-powered code analysis and suggestions  
✅ **Safe Patching** - Generate patches with approval workflows  
✅ **Build Integration** - Run tests and builds with logging  
✅ **Local Memory** - Store sessions and summaries locally  
✅ **User-Friendly UI** - Modern React interface with status visibility  
✅ **Progress Tracking** - Visual startup progress and connection status  
✅ **Comprehensive Logging** - All operations logged locally  

## Architecture

### Core Modules

| Module | Purpose |
|--------|---------|
| **Startup Manager** | Environment validation, workspace prep, service startup |
| **Chat Orchestrator** | Request routing, intent classification, memory management |
| **Local LLM Connector** | Unified interface to any LLM backend |
| **Workspace Mapper** | Module/repository discovery and registration |
| **Repository Scanner** | Project analysis, tech stack detection |
| **Code Reviewer** | AI-powered code analysis |
| **Patch Manager** | Safe code modifications with approvals |
| **Memory Manager** | Session storage and reuse |

### Local LLM Connector Adapters

The connector uses an adapter pattern supporting:

1. **Generic Adapter** - REST-based local LLM endpoints
2. **Ollama Adapter** - Ollama-compatible backends
3. **Custom Adapter** - Extensible for other providers

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+ (optional, for frontend)
- A local LLM service (Ollama or compatible REST API)

### Quick Start

```bash
# 1. Make the startup script executable
chmod +x run.sh

# 2. Run the startup script
./run.sh

# 3. Open in browser
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
REACT_APP_API_URL=http://localhost:8000/api npm start
```

## Configuration

### Environment Variables

```env
# LLM Configuration
LLM_ADAPTER=ollama              # generic, ollama, custom
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=mistral

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0

# Frontend Configuration
FRONTEND_PORT=3000

# Workspace
WORKSPACE_ROOT=workspace
```

### LLM Setup

#### Using Ollama

```bash
# Install from https://ollama.ai
ollama serve
# In another terminal:
ollama pull mistral
```

Configure `.env`:
```env
LLM_ADAPTER=ollama
LLM_ENDPOINT=http://localhost:11434
LLM_MODEL=mistral
```

#### Using Generic REST API

```env
LLM_ADAPTER=generic
LLM_ENDPOINT=http://your-api:port
LLM_MODEL=your-model
```

## Usage

### 1. Add Repositories

```bash
cp -r ~/my-project workspace/modules/my-project
cp -r ~/another-repo workspace/modules/another-repo
```

### 2. Scan Workspace

Click **"🔄 Scan Workspace"** in the UI to discover modules.

### 3. Select Repository

Choose from the left panel to make it active.

### 4. Chat with AI

Use different intent modes:
- **Chat** - General questions
- **Review** - Code analysis
- **Modify** - Request changes
- **Build** - Troubleshooting

### 5. Review & Apply Patches

AI generates patches → Review → Approve → Apply

## API Endpoints

### Health & Status
```
GET  /api/health              # App health
GET  /api/health/llm          # LLM status
GET  /api/health/models       # Available models
```

### Chat
```
POST /api/chat                # Send message
POST /api/chat/stream         # Stream response
GET  /api/chat/history        # Conversation history
```

### Workspace
```
POST /api/workspace/scan      # Scan modules
GET  /api/workspace/repos     # List repositories
GET  /api/workspace/repos/{name}
```

### Code Review
```
POST /api/review/code         # Review code
```

### Repository
```
POST /api/repo/modify         # Request modification
POST /api/repo/apply-patch    # Apply patch
POST /api/repo/run-tests      # Run tests
POST /api/repo/run-build      # Run build
```

### Memory
```
GET  /api/memory              # List sessions
GET  /api/memory/{session_id}
POST /api/memory/{session_id}
DELETE /api/memory/{session_id}
```

Full docs: http://localhost:8000/docs

## Workspace Structure

```
workspace/
├── modules/        # Your repositories
├── indexes/        # Vector indexes
├── memory/         # Session history
├── logs/           # Application logs
└── patches/        # Patch files
```

## Project Structure

```
AI-Project/
├── backend/
│   ├── app/
│   │   ├── connectors/      # LLM adapter layer
│   │   ├── modules/         # Core business logic
│   │   ├── routers/         # API endpoints
│   │   ├── config.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── workspace/               # Runtime workspace
├── run.sh                   # Startup script
└── README.md                # This file
```

## Troubleshooting

### Backend Issues
```bash
# Check Python
python3 --version

# Run directly
cd backend && source venv/bin/activate
python -m app.main
```

### LLM Connection
```bash
# Check if running
curl http://localhost:11434/health

# For Ollama
ollama serve
```

### Frontend Issues
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Check Logs
```bash
tail -f workspace/logs/backend.log
tail -f workspace/logs/frontend.log
```

## Extending

### Custom LLM Adapter

Create in `backend/app/connectors/adapters/`:

```python
from app.connectors import LocalLLMConnector

class CustomAdapter(LocalLLMConnector):
    async def send_chat(self, messages, config=None, stream=False):
        # Implement chat
        pass
    # ... implement other methods ...
```

Register in `backend/app/connectors/factory.py`.

## Security

- ✓ Local execution only
- ✓ Sandboxed tool execution
- ✓ Human approval workflows
- ✓ Comprehensive audit logs
- ✓ No cloud dependencies
- ✓ Offline operation

## License

MIT License

## Support

1. Check troubleshooting section
2. Review logs in `workspace/logs/`
3. Check API docs at `/docs`

---

**Keep your code local, keep your data yours.**
