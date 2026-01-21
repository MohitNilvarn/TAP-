# File: app/core/config.py
import os
from dotenv import load_dotenv
from app.core.logger import get_logger

# Note: We don't run setup_logging() here because main.py handles it.
# We just get a logger instance.
logger = get_logger("TAP.Config")

logger.info("Loading environment variables...")
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Project Info
    PROJECT_NAME: str = "Teacher Assistance Platform"
    
    # Supabase (Auth)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # MongoDB Atlas
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "tap_database")
    
    # Redis (Optional - for caching and Celery)
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    REDIS_ENABLED: bool = bool(os.getenv("REDIS_URL"))
    
    # Groq API (LLM)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    
    # HuggingFace (Embeddings)
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "your-huggingface-api-key-here")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # ChromaDB (Vector Store)
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    
    # File Upload Settings
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    def __init__(self):
        self._validate_config()
    
    def _validate_config(self):
        """Validate required configuration values."""
        errors = []
        
        if not self.SUPABASE_URL:
            errors.append("SUPABASE_URL")
        if not self.SUPABASE_KEY:
            errors.append("SUPABASE_KEY")
        
        if errors:
            for var in errors:
                logger.warning(f"MISSING ENV VAR: {var}")
        
        # Log optional config status
        if not self.REDIS_URL:
            logger.info("Redis not configured - caching disabled")
        
        if self.GROQ_API_KEY == "your-groq-api-key-here":
            logger.warning("Using placeholder GROQ_API_KEY - LLM calls will fail")
        
        if self.HUGGINGFACE_API_KEY == "your-huggingface-api-key-here":
            logger.info("Using placeholder HUGGINGFACE_API_KEY - using local embeddings")
        
        logger.info("Config loaded successfully.")


settings = Settings()