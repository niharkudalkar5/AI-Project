# Quick Start Guide

## 5-Minute Setup

### Step 1: Verify Prerequisites
```bash
# Check Python
python3 --version  # Requires 3.8+

# Check Node.js (optional)
node --version     # Requires 14+ for frontend
```

### Step 2: Start the Application
```bash
cd /workspaces/AI-Project
./run.sh
```

The script will automatically:
- ✓ Create workspace directories
- ✓ Install Python dependencies
- ✓ Install Node.js dependencies (if available)
- ✓ Configure environment
- ✓ Check LLM connectivity
- ✓ Start backend API (port 8000)
- ✓ Start frontend UI (port 3000)

### Step 3: Access the Application
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Adding Your First Repository

### 1. Copy a Repository
```bash
# Create a test repository or copy an existing one
cp -r ~/my-project /workspaces/AI-Project/workspace/modules/

# Or clone one
cd /workspaces/AI-Project/workspace/modules/
git clone https://github.com/torvalds/linux.git linux
```

### 2. Scan in the UI
Click **"🔄 Scan Workspace"** in the web interface.

### 3. Start Chatting
- Select your repository from the left panel
- Type a question in the chat input
- Select an intent (Chat, Review, Modify, or Build)
- Click Send

## Common Tasks

### Change LLM Model
Edit `.env`:
```env
LLM_MODEL=neural-chat  # or llama2, mistral, etc.
```
Restart the application.

### Use Different LLM Backend
Edit `.env`:
```env
LLM_ADAPTER=ollama
LLM_ENDPOINT=http://your-api:port
```

### View Logs
```bash
# Backend logs
tail -f workspace/logs/backend.log

# Frontend logs
tail -f workspace/logs/frontend.log
```

### Stop the Application
```bash
# Press Ctrl+C in the terminal where run.sh is running
# Or in another terminal:
pkill -f "uvicorn"
pkill -f "npm start"
```

## Troubleshooting

### "LLM not available" message
Make sure your local LLM is running:
```bash
# For Ollama
ollama serve

# In another terminal
ollama pull mistral
```

### Port already in use
Change ports in `.env`:
```env
API_PORT=8001
FRONTEND_PORT=3001
```

### Dependencies not installed
```bash
# Reinstall Python dependencies
cd backend
pip install --force-reinstall -r requirements.txt

# Reinstall Node dependencies
cd ../frontend
rm -rf node_modules package-lock.json
npm install
```

## API Quick Reference

### Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "intent": "chat"}'
```

### Review Code
```bash
curl -X POST http://localhost:8000/api/review/code \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"hello\")", "language": "python"}'
```

### Scan Workspace
```bash
curl -X POST http://localhost:8000/api/workspace/scan
```

### Health Check
```bash
curl http://localhost:8000/api/health/llm
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read the docs**: Check README.md for complete documentation
3. **Add custom tools**: See INTEGRATION.md for extending
4. **Deploy**: See BUILD.md for production deployment

## Getting Help

- **API Docs**: http://localhost:8000/docs (interactive)
- **Full Documentation**: README.md
- **Integration Guide**: INTEGRATION.md
- **Build Guide**: BUILD.md
- **Logs**: workspace/logs/

---

Happy coding! 🚀
