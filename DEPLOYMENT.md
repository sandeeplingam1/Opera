# Opera Deployment Guide

## Local Development

### Backend
```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run
uvicorn opera.backend.main:app --reload
```

### Frontend
```bash
cd opera-frontend
npm install
npm run dev
```

---

## Docker Deployment

### Prerequisites
- Docker & Docker Compose installed
- OpenAI API key

### Quick Start
```bash
# Set environment variables
export OPENAI_API_KEY="your-key-here"

# Build and run
docker-compose up --build

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Production
```bash
# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Cloud Deployment

### Railway.app

1. **Create New Project**
   - Connect your Git repository
   - Railway will auto-detect the Dockerfile

2. **Add Environment Variables**
   ```
   OPENAI_API_KEY=your-key-here
   DATABASE_URL=sqlite:///./data/opera.db
   CHROMA_PERSIST_DIR=./data/chroma_db
   ```

3. **Deploy**
   - Railway auto-deploys on git push
   - Access via generated domain

### Fly.io

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Initialize App**
   ```bash
   fly launch
   ```

3. **Set Secrets**
   ```bash
   fly secrets set OPENAI_API_KEY=your-key-here
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

---

## Environment Variables

### Required
- `OPENAI_API_KEY` - OpenAI API key for LLM and embeddings

### Optional
- `OPENAI_MODEL` - Model name (default: gpt-4o-mini)
- `OPENAI_EMBEDDING_MODEL` - Embedding model (default: text-embedding-3-small)
- `DATABASE_URL` - Database connection string
- `CHROMA_PERSIST_DIR` - ChromaDB storage directory
- `API_HOST` - API server host (default: 0.0.0.0)
- `API_PORT` - API server port (default: 8000)

---

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# Backend
docker-compose logs -f backend

# Frontend
docker-compose logs -f frontend
```

### Database
```bash
# Access SQLite database
docker-compose exec backend sqlite3 /data/opera.db
```

---

## Backup

### Data
```bash
# Backup data volume
docker run --rm -v opera_opera-data:/data -v $(pwd):/backup \
  alpine tar czf /backup/opera-backup.tar.gz /data
```

### Restore
```bash
# Restore data volume
docker run --rm -v opera_opera-data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/opera-backup.tar.gz -C /
```

---

## Troubleshooting

### Backend not starting
- Check OpenAI API key is set
- Verify port 8000 is available
- Check logs: `docker-compose logs backend`

### Frontend can't connect to backend
- Ensure backend is running
- Check `next.config.ts` proxy configuration
- Verify CORS settings

### Database errors
- Ensure data directory has write permissions
- Check DATABASE_URL is correct
- Clear volumes and restart: `docker-compose down -v && docker-compose up`

### ChromaDB issues
- Clear chroma data: `docker volume rm opera_chroma-data`
- Restart ChromaDB: `docker-compose restart chromadb`
