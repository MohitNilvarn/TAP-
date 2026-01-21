# File: app/db/redis.py
"""
Redis connection manager for caching (optional).
Falls back gracefully when Redis is not available.
"""
import redis.asyncio as redis
from typing import Optional, Any
import json
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("TAP.Redis")

# Global client instance
_client: Optional[redis.Redis] = None


async def connect_to_redis() -> bool:
    """
    Initialize Redis connection if configured.
    Returns True if connected, False otherwise.
    """
    global _client
    
    if not settings.REDIS_ENABLED:
        logger.info("Redis not configured - caching disabled")
        return False
    
    try:
        logger.info("Connecting to Redis...")
        _client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        
        # Test connection
        await _client.ping()
        logger.info("Redis connection established successfully.")
        return True
        
    except Exception as e:
        logger.warning(f"Failed to connect to Redis: {str(e)}. Caching disabled.")
        _client = None
        return False


async def close_redis_connection():
    """Close Redis connection."""
    global _client
    
    if _client:
        await _client.close()
        logger.info("Redis connection closed.")


class CacheService:
    """Simple cache service with Redis backend and no-op fallback."""
    
    @staticmethod
    async def get(key: str) -> Optional[Any]:
        """Get value from cache."""
        if _client is None:
            return None
        
        try:
            value = await _client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Cache get error for {key}: {str(e)}")
            return None
    
    @staticmethod
    async def set(key: str, value: Any, expire_seconds: int = 3600) -> bool:
        """Set value in cache with expiration."""
        if _client is None:
            return False
        
        try:
            await _client.set(key, json.dumps(value), ex=expire_seconds)
            return True
        except Exception as e:
            logger.warning(f"Cache set error for {key}: {str(e)}")
            return False
    
    @staticmethod
    async def delete(key: str) -> bool:
        """Delete value from cache."""
        if _client is None:
            return False
        
        try:
            await _client.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete error for {key}: {str(e)}")
            return False
    
    @staticmethod
    async def clear_pattern(pattern: str) -> bool:
        """Delete all keys matching a pattern."""
        if _client is None:
            return False
        
        try:
            keys = await _client.keys(pattern)
            if keys:
                await _client.delete(*keys)
            return True
        except Exception as e:
            logger.warning(f"Cache clear pattern error for {pattern}: {str(e)}")
            return False


# Singleton instance
cache = CacheService()
