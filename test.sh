#!/usr/bin/env bash
# Test the application locally

echo "Testing Standalone Local LLM Workspace..."

# Test backend health
echo "Testing backend health..."
curl -s http://localhost:8000/api/health | python3 -m json.tool || echo "Backend not responding"

# Test LLM connection
echo ""
echo "Testing LLM connection..."
curl -s http://localhost:8000/api/health/llm | python3 -m json.tool || echo "LLM not responding"

# Test workspace scan
echo ""
echo "Testing workspace scan..."
curl -s -X POST http://localhost:8000/api/workspace/scan | python3 -m json.tool || echo "Scan failed"

# Test chat
echo ""
echo "Testing chat endpoint..."
curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "intent": "chat"}' | python3 -m json.tool || echo "Chat failed"

echo ""
echo "Tests completed!"
