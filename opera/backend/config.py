"""Configuration management for Opera backend."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # LLM Provider Selection
    USE_LOCAL_MODEL = os.getenv("USE_LOCAL_MODEL", "true").lower() == "true"
    
    # OpenAI (fallback/optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Local Models
    LOCAL_MODEL_NAME = os.getenv("LOCAL_MODEL_NAME", "meta-llama/Llama-3.2-1B")
    LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "./models")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./opera.db")
    
    # ChromaDB
    CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

config = Config()
