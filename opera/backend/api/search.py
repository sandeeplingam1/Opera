"""Search endpoints for semantic memory retrieval."""
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from opera.backend.services.embeddings import EmbeddingService
from opera.backend.services.vector_store import VectorStore

router = APIRouter(prefix="/search", tags=["search"])

# Initialize services
try:
    embedding_service = EmbeddingService()
    vector_store = VectorStore()
except ValueError as e:
    embedding_service = None
    vector_store = None
    print(f"Warning: Search services not initialized: {e}")


class SearchRequest(BaseModel):
    query: str
    memory_type: Optional[str] = None
    limit: int = 10


class SearchResult(BaseModel):
    id: int
    content: str
    memory_type: str
    source: str
    timestamp: str
    confidence: float
    similarity_score: float


@router.post("/semantic", response_model=List[SearchResult])
def semantic_search(request: SearchRequest):
    """
    Search for memories using semantic similarity.
    
    Args:
        request: Search request with query and filters
        
    Returns:
        List of similar memories ranked by relevance
    """
    if not embedding_service or not vector_store:
        raise HTTPException(
            status_code=503,
            detail="Search service not available. Please configure OPENAI_API_KEY."
        )
    
    # Generate embedding for the query
    query_embedding = embedding_service.generate_embedding(request.query)
    
    # Build filter if memory type specified
    filter_dict = None
    if request.memory_type:
        filter_dict = {"type": request.memory_type}
    
    # Search vector store
    results = vector_store.search_similar(
        query_embedding=query_embedding,
        n_results=request.limit,
        filter_dict=filter_dict
    )
    
    # Format results
    formatted_results = []
    for result in results:
        metadata = result['metadata']
        formatted_results.append(SearchResult(
            id=result['id'],
            content=result['content'],
            memory_type=metadata.get('type', 'unknown'),
            source=metadata.get('source', 'unknown'),
            timestamp=metadata.get('timestamp', ''),
            confidence=metadata.get('confidence', 1.0),
            similarity_score=1.0 - result['distance'] if result['distance'] else 0.0
        ))
    
    return formatted_results
