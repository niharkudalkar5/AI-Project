#!/usr/bin/env bash
# Standalone Local LLM Workspace - Startup Script
# This script bootstraps the entire application with system checks, dependency installation, and service startup.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}/frontend"
WORKSPACE_DIR="${PROJECT_DIR}/workspace"

# Default ports
API_PORT=${API_PORT:-8000}
FRONTEND_PORT=${FRONTEND_PORT:-3000}

# LLM Configuration
LLM_ADAPTER=${LLM_ADAPTER:-generic}
LLM_ENDPOINT=${LLM_ENDPOINT:-http://localhost:11434}
LLM_MODEL=${LLM_MODEL:-mistral}

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   Standalone Local LLM Workspace - Startup                   ║"
echo "║   Version: 0.1.0                                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to print progress
progress() {
  echo -e "${BLUE}[▶]${NC} $1"
}

success() {
  echo -e "${GREEN}[✓]${NC} $1"
}

error() {
  echo -e "${RED}[✗]${NC} $1"
}

warning() {
  echo -e "${YELLOW}[⚠]${NC} $1"
}

# Step 1: Check system requirements
progress "Checking system requirements..."

if ! command -v python3 &> /dev/null; then
  error "Python 3 is not installed"
  exit 1
fi
success "Python 3 found: $(python3 --version)"

if ! command -v node &> /dev/null; then
  warning "Node.js not found - frontend setup will be skipped"
  SKIP_FRONTEND=true
else
  success "Node.js found: $(node --version)"
fi

if ! command -v git &> /dev/null; then
  warning "Git not found"
fi

# Step 2: Prepare workspace directories
progress "Preparing workspace directories..."

mkdir -p "${WORKSPACE_DIR}/{modules,indexes,memory,logs,patches}"
success "Workspace directories prepared"

# Step 3: Setup Backend
progress "Setting up Python backend..."

cd "${BACKEND_DIR}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  progress "Creating Python virtual environment..."
  python3 -m venv venv
  success "Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
progress "Installing Python dependencies..."
pip install --quiet --upgrade pip setuptools wheel
pip install --quiet -r requirements.txt
success "Python dependencies installed"

cd "${PROJECT_DIR}"

# Step 4: Setup Frontend (if Node.js is available)
if [ -z "$SKIP_FRONTEND" ]; then
  progress "Setting up React frontend..."
  
  cd "${FRONTEND_DIR}"
  
  if [ ! -d "node_modules" ]; then
    progress "Installing Node.js dependencies..."
    npm install --silent 2>/dev/null || npm install
    success "Node.js dependencies installed"
  fi
  
  cd "${PROJECT_DIR}"
fi

# Step 5: Create .env files if they don't exist
progress "Configuring environment..."

if [ ! -f "${BACKEND_DIR}/.env" ]; then
  cat > "${BACKEND_DIR}/.env" << EOF
# Standalone Local LLM Workspace Configuration
APP_NAME=Standalone Local LLM Workspace
APP_VERSION=0.1.0
DEBUG=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=${API_PORT}
API_BASE_URL=http://localhost:${API_PORT}

# Frontend Configuration
FRONTEND_PORT=${FRONTEND_PORT}
FRONTEND_URL=http://localhost:${FRONTEND_PORT}

# LLM Configuration
LLM_ADAPTER=${LLM_ADAPTER}
LLM_ENDPOINT=${LLM_ENDPOINT}
LLM_MODEL=${LLM_MODEL}
LLM_TIMEOUT=300
LLM_CONTEXT_LIMIT=4096

# Workspace Configuration
WORKSPACE_ROOT=${WORKSPACE_DIR}
EOF
  success "Environment configured"
else
  success "Environment already configured"
fi

# Step 6: Check LLM connectivity
progress "Checking Local LLM connectivity..."

if [ "${LLM_ADAPTER}" = "ollama" ] || [ "${LLM_ADAPTER}" = "generic" ]; then
  if curl -s "${LLM_ENDPOINT}/health" > /dev/null 2>&1 || curl -s "${LLM_ENDPOINT}/api/tags" > /dev/null 2>&1; then
    success "Local LLM is available at ${LLM_ENDPOINT}"
  else
    warning "Local LLM not available at ${LLM_ENDPOINT}"
    warning "Make sure your LLM service is running"
    echo -e "  For Ollama: ${BLUE}ollama serve${NC}"
    echo -e "  For generic: Start your local LLM REST service"
  fi
fi

# Step 7: Start services
echo ""
progress "Starting services..."

# Start backend
progress "Starting backend API (port ${API_PORT})..."
cd "${BACKEND_DIR}"
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port ${API_PORT} > "${WORKSPACE_DIR}/logs/backend.log" 2>&1 &
BACKEND_PID=$!
success "Backend started (PID: ${BACKEND_PID})"

# Wait for backend to be ready
sleep 2

# Start frontend (if Node.js is available)
if [ -z "$SKIP_FRONTEND" ]; then
  progress "Starting frontend (port ${FRONTEND_PORT})..."
  cd "${FRONTEND_DIR}"
  REACT_APP_API_URL="http://localhost:${API_PORT}/api" npm start > "${WORKSPACE_DIR}/logs/frontend.log" 2>&1 &
  FRONTEND_PID=$!
  success "Frontend started (PID: ${FRONTEND_PID})"
fi

cd "${PROJECT_DIR}"

# Step 8: Display final information
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Standalone Local LLM Workspace Started Successfully!        ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}Access the Application:${NC}"
if [ -z "$SKIP_FRONTEND" ]; then
  echo -e "  🌐 Frontend: ${BLUE}http://localhost:${FRONTEND_PORT}${NC}"
fi
echo -e "  📡 Backend API: ${BLUE}http://localhost:${API_PORT}${NC}"
echo -e "  📚 API Docs: ${BLUE}http://localhost:${API_PORT}/docs${NC}"

echo ""
echo -e "${BLUE}Configuration:${NC}"
echo -e "  LLM Adapter: ${YELLOW}${LLM_ADAPTER}${NC}"
echo -e "  LLM Endpoint: ${YELLOW}${LLM_ENDPOINT}${NC}"
echo -e "  LLM Model: ${YELLOW}${LLM_MODEL}${NC}"
echo -e "  Workspace: ${YELLOW}${WORKSPACE_DIR}${NC}"

echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "  Backend: ${YELLOW}${WORKSPACE_DIR}/logs/backend.log${NC}"
if [ -z "$SKIP_FRONTEND" ]; then
  echo -e "  Frontend: ${YELLOW}${WORKSPACE_DIR}/logs/frontend.log${NC}"
fi

echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Copy your repositories to: ${YELLOW}${WORKSPACE_DIR}/modules/${NC}"
echo "  2. Open the web interface and click 'Scan Workspace'"
echo "  3. Select a repository and start asking questions"

echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait for services to run
wait
