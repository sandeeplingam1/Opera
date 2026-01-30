"""Memory tools for Opera."""
from typing import List, Dict, Any
from opera.backend.tools.registry import tool, ToolPermission
from opera.backend.services.memory_store import add_memory, list_memories
from opera.backend.models.memory import MemoryItem


@tool(
    name="store_memory",
    description="Store a new memory item",
    permissions=[ToolPermission.WRITE],
    examples=["store_memory(type='episodic', content='Had lunch with Sarah', source='manual')"]
)
def store_memory(
    memory_type: str,
    content: str,
    source: str = "tool",
    confidence: float = 1.0
) -> str:
    """Store a new memory in the database."""
    item = MemoryItem(
        type=memory_type,
        content=content,
        source=source,
        confidence=confidence
    )
    
    memory = add_memory(item)
    return f"Stored memory with ID {memory.id}"


@tool(
    name="fetch_memories",
    description="Fetch memories, optionally filtered by type",
    permissions=[ToolPermission.READ],
    examples=["fetch_memories(memory_type='episodic')"]
)
def fetch_memories(memory_type: str = None) -> List[Dict[str, Any]]:
    """Fetch memories from the database."""
    memories = list_memories(memory_type)
    
    return [
        {
            "id": m.id,
            "type": m.type,
            "content": m.content,
            "source": m.source,
            "timestamp": m.timestamp.isoformat(),
            "confidence": m.confidence
        }
        for m in memories
    ]


@tool(
    name="search_memories",
    description="Search memories using semantic similarity",
    permissions=[ToolPermission.READ],
    examples=["search_memories(query='project meetings')"]
)
def search_memories(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search for memories using semantic similarity."""
    from opera.backend.services.embeddings import EmbeddingService
    from opera.backend.services.vector_store import VectorStore
    
    try:
        embedding_service = EmbeddingService()
        vector_store = VectorStore()
        
        query_embedding = embedding_service.generate_embedding(query)
        results = vector_store.search_similar(query_embedding, n_results=limit)
        
        return [
            {
                "id": r["id"],
                "content": r["content"],
                "metadata": r["metadata"],
                "similarity": 1.0 - r["distance"] if r["distance"] else 0.0
            }
            for r in results
        ]
    except Exception as e:
        return [{"error": f"Search failed: {e}"}]
