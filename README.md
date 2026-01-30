# Opera - Personal Intelligence OS

Opera is a personal intelligence operating system that continuously constructs a structured model of you (memories, preferences, goals, skills) and uses that model to reason, plan, and act.

## Architecture

```
┌─────────────────────────────────────────────┐
│          Frontend (Next.js)                 │
│  • Chat Interface                           │
│  • Memory Browser                           │
│  • Timeline View                            │
└──────────────────┬──────────────────────────┘
                   │ HTTP/WebSocket
┌──────────────────▼──────────────────────────┐
│       Backend (FastAPI + Python)            │
│  ┌────────────────────────────────────────┐ │
│  │  Intelligence Layer                    │ │
│  │  • LLM Reasoning (OpenAI)             │ │
│  │  • Intent Derivation                   │ │
│  │  • Plan Generation                     │ │
│  └────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────┐ │
│  │  Memory Layer                          │ │
│  │  • Vector Search (ChromaDB)           │ │
│  │  • Embeddings (OpenAI)                │ │
│  │  • SQL Storage (SQLite/PostgreSQL)    │ │
│  └────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────┐ │
│  │  Tool Execution                        │ │
│  │  • 9+ Tools (File, Memory, Web)      │ │
│  │  • Permission System                   │ │
│  │  • Safety Checks                       │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Features

### ✅ Implemented
- **LLM-Powered Reasoning**: Intent derivation and plan generation
- **Vector Search**: Semantic memory retrieval with ChromaDB
- **Tool Execution**: 9 tools with permission-based safety
- **Memory Taxonomy**: 5 types (episodic, semantic, preference, goal, skill)
- **Beautiful UI**: Modern Next.js frontend with dark mode
- **Chat Interface**: Conversational AI with real-time planning
- **Memory Browser**: Filter, search, and explore memories

### 🚧 Roadmap
- **Data Ingestion**: Gmail, Calendar, Document uploads
- **Proactive Intelligence**: Background reasoning, notifications
- **Multi-user**: Authentication and data isolation
- **Production**: Docker deployment, monitoring

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key

### Setup

1. **Backend**
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastapi sqlmodel uvicorn openai chromadb python-dotenv requests beautifulsoup4

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run backend
uvicorn opera.backend.main:app --reload
```

2. **Frontend**
```bash
cd opera-frontend
npm install
npm run dev
```

3. **Access**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Endpoints

### Memory
- `POST /memory` - Store a memory
- `GET /memory` - List memories
- `POST /search/semantic` - Semantic search

### Reasoning
- `POST /intent/derive` - Derive intent from user input
- `POST /plan/generate` - Generate execution plan
- `POST /action/preview` - Preview action effects

### Execution
- `POST /execute/plan` - Execute a plan
- `GET /execute/tools` - List available tools

## Memory Types

1. **Episodic** - Events that happened
2. **Semantic** - Facts you know
3. **Preference** - Likes, dislikes, biases
4. **Goal** - What you're trying to achieve
5. **Skill** - Capabilities and competencies

## Development

### Project Structure
```
opera/
├── backend/
│   ├── api/          # FastAPI endpoints
│   ├── models/       # Pydantic/SQLModel schemas
│   ├── services/     # Business logic
│   └── tools/        # Executable tools
├── frontend/
│   └── src/
│       ├── app/      # Next.js pages
│       ├── components/ # React components
│       └── lib/      # API client
└── tests/           # Unit tests
```

### Running Tests
```bash
python3 -m unittest discover tests
```

## License

MIT

## Contributing

Opera is in active development. Contributions welcome!
