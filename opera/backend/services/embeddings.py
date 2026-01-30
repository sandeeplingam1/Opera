"""Embedding service for generating vector representations of text."""
from typing import List
from openai import OpenAI
from opera.backend.config import config


class EmbeddingService:
    """Service for generating embeddings from text."""
    
    def __init__(self):
        """Initialize the embedding service with OpenAI client."""
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_EMBEDDING_MODEL
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding vector for the given text.
        
        Args:
            text: The text to embed
            
        Returns:
            A list of floats representing the embedding vector
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]


class LocalEmbeddingService:
    """Service for generating embeddings using local sentence-transformers."""
    
    def __init__(self):
        """Initialize the local embedding service."""
        from sentence_transformers import SentenceTransformer
        
        self.model_name = config.LOCAL_EMBEDDING_MODEL
        print(f"Loading local embedding model: {self.model_name}...")
        self.model = SentenceTransformer(
            self.model_name,
            cache_folder=config.MODEL_CACHE_DIR
        )
        print("Local embedding model loaded successfully")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding vector for the given text using local model.
        
        Args:
            text: The text to embed
            
        Returns:
            A list of floats representing the embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch using local model.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return [emb.tolist() for emb in embeddings]


# Global embedding service instance
_embedding_service = None

def get_embedding_service():
    """Get or create the global embedding service based on configuration."""
    global _embedding_service
    if _embedding_service is None:
        if config.USE_LOCAL_MODEL:
            print("Initializing local embedding service...")
            _embedding_service = LocalEmbeddingService()
        else:
            print("Initializing OpenAI embedding service...")
            _embedding_service = EmbeddingService()
    return _embedding_service
