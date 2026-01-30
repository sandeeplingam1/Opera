"""Vector store service using ChromaDB for semantic memory search."""
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from opera.backend.config import config
from opera.backend.models.memory import MemoryItem


class VectorStore:
    """Service for storing and searching memory embeddings."""
    
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        self.client = chromadb.Client(Settings(
            persist_directory=config.CHROMA_PERSIST_DIR,
            anonymized_telemetry=False
        ))
        
        # Get or create collection for memories
        self.collection = self.client.get_or_create_collection(
            name="memories",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_memory(
        self, 
        memory_id: int, 
        content: str, 
        embedding: List[float],
        metadata: Dict
    ) -> None:
        """
        Add a memory to the vector store.
        
        Args:
            memory_id: Unique identifier for the memory
            content: The text content
            embedding: The embedding vector
            metadata: Additional metadata (type, timestamp, etc.)
        """
        self.collection.add(
            ids=[str(memory_id)],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )
    
    def search_similar(
        self, 
        query_embedding: List[float], 
        n_results: int = 10,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar memories.
        
        Args:
            query_embedding: The query embedding vector
            n_results: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of similar memories with scores
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter_dict
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and results['ids'][0]:
            for i, memory_id in enumerate(results['ids'][0]):
                formatted_results.append({
                    'id': int(memory_id),
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def update_memory(
        self,
        memory_id: int,
        content: str,
        embedding: List[float],
        metadata: Dict
    ) -> None:
        """Update an existing memory in the vector store."""
        self.collection.update(
            ids=[str(memory_id)],
            embeddings=[embedding],
            documents=[content],
            metadatas=[metadata]
        )
    
    def delete_memory(self, memory_id: int) -> None:
        """Delete a memory from the vector store."""
        self.collection.delete(ids=[str(memory_id)])
