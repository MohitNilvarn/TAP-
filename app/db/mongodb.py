# File: app/db/mongodb.py
"""
MongoDB Atlas connection manager using Motor (async driver) and Beanie ODM.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("TAP.MongoDB")

# Global client instance
_client: AsyncIOMotorClient = None


async def connect_to_mongodb():
    """Initialize MongoDB connection and Beanie ODM."""
    global _client
    
    try:
        logger.info(f"Connecting to MongoDB...")
        _client = AsyncIOMotorClient(settings.MONGODB_URI)
        
        # Test connection
        await _client.admin.command('ping')
        logger.info("MongoDB connection established successfully.")
        
        # Get database
        db = _client[settings.MONGODB_DB_NAME]
        
        # Import models here to avoid circular imports
        from app.models.course import Course
        from app.models.material import Material
        from app.models.lecture import Lecture
        from app.models.content import GeneratedContent
        
        # Initialize Beanie with document models
        await init_beanie(
            database=db,
            document_models=[Course, Material, Lecture, GeneratedContent]
        )
        
        logger.info(f"Beanie ODM initialized with database: {settings.MONGODB_DB_NAME}")
        
    except Exception as e:
        logger.critical(f"Failed to connect to MongoDB: {str(e)}")
        raise e


async def close_mongodb_connection():
    """Close MongoDB connection."""
    global _client
    
    if _client:
        _client.close()
        logger.info("MongoDB connection closed.")


def get_database():
    """Get the database instance."""
    if _client is None:
        raise RuntimeError("MongoDB not initialized. Call connect_to_mongodb() first.")
    return _client[settings.MONGODB_DB_NAME]
