# Build & Deployment

## Development Environment Setup

### Automatic Setup (Recommended)

```bash
chmod +x run.sh
./run.sh
```

### Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
REACT_APP_API_URL=http://localhost:8000/api npm start
```

## Building for Production

### Backend Build
```bash
cd backend

# Build Docker image
docker build -t standalone-llm-workspace:latest .

# Or use setuptools
python setup.py sdist bdist_wheel
```

### Frontend Build
```bash
cd frontend

# Create production build
npm run build

# Output in: frontend/build/
```

## Docker Deployment

### Dockerfile (Backend)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY backend/app ./app

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile (Frontend)

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY frontend/package*.json ./

RUN npm ci

COPY frontend ./

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - LLM_ADAPTER=ollama
      - LLM_ENDPOINT=http://ollama:11434
      - LLM_MODEL=mistral
    volumes:
      - ./workspace:/app/workspace
    depends_on:
      - ollama

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://localhost:8000/api

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  ollama_data:
```

Run with:
```bash
docker-compose up
```

## Testing

### Backend Tests
```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=app
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# With coverage
npm test -- --coverage
```

## Performance Tuning

### Backend
- Use async/await for I/O operations
- Implement caching for frequent queries
- Batch process embeddings
- Connection pooling for LLM requests

### Frontend
- Code splitting for large components
- Lazy loading of route components
- Memoization of expensive computations
- Virtual scrolling for large lists

## Monitoring

### Logs

Backend logs in: `workspace/logs/backend.log`
Frontend logs in: `workspace/logs/frontend.log`

### Health Monitoring

```bash
# Check application health
curl http://localhost:8000/api/health

# Check LLM connection
curl http://localhost:8000/api/health/llm

# Check available models
curl http://localhost:8000/api/health/models
```

### Metrics Collection

Add Prometheus metrics:

```python
from prometheus_client import Counter, Histogram

chat_requests = Counter('chat_requests_total', 'Total chat requests')
chat_duration = Histogram('chat_duration_seconds', 'Chat request duration')
```

## Scaling Considerations

1. **Horizontal Scaling**: Load balance multiple API instances
2. **Caching**: Redis for session/index caching
3. **Message Queue**: Celery/RabbitMQ for async tasks
4. **Database**: PostgreSQL for persistent storage
5. **Search**: Elasticsearch for advanced indexing

---

For more information on deployment strategies, see the main README.md
