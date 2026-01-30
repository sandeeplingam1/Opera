"""HTTP API for memory operations.

This router exposes endpoints to create and retrieve memory items. It uses
FastAPI and depends on the memory store service.
"""

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..models.memory import MemoryItem
from ..services.memory_store import add_memory, get_session, list_memories, init_db


router = APIRouter()


@router.on_event("startup")
def on_startup() -> None:
    """Ensure database tables exist on application startup."""
    init_db()


@router.post("/memory", response_model=MemoryItem)
def create_memory(item: MemoryItem) -> MemoryItem:
    """Create and persist a new memory item with embedding generation."""
    from ..services.embeddings import EmbeddingService
    from ..services.vector_store import VectorStore
    import json
    
    # Add to database
    memory = add_memory(item)
    
    # Generate and store embedding
    try:
        embedding_service = EmbeddingService()
        vector_store = VectorStore()
        
        # Generate embedding
        embedding = embedding_service.generate_embedding(memory.content)
        
        # Store in vector database
        vector_store.add_memory(
            memory_id=memory.id,
            content=memory.content,
            embedding=embedding,
            metadata={
                "type": memory.type,
                "source": memory.source,
                "timestamp": memory.timestamp.isoformat(),
                "confidence": memory.confidence
            }
        )
        
        # Store embedding in SQL database as JSON
        memory.embedding = json.dumps(embedding)
        from ..services.memory_store import update_memory
        update_memory(memory)
        
    except Exception as e:
        print(f"Warning: Failed to generate embedding: {e}")
    
    return memory


@router.get("/memory", response_model=list[MemoryItem])
def get_memories(memory_type: str | None = None) -> list[MemoryItem]:
    """List memories, optionally filtered by type."""
    return list_memories(memory_type)