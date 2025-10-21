# src/core/cache.py
import redis.asyncio as redis
import json
import logging
from typing import Optional, Dict, Any, Callable, Coroutine

logger = logging.getLogger(__name__)


class CachingService:
    _conn: Optional[redis.Redis] = None

    @classmethod
    async def open_conn(cls, host: str = "localhost", port: int = 6379, db: int = 0, max_connections: int = 50):
        """Open a Redis connection pool."""
        if cls._conn is None:
            cls._conn = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                max_connections=max_connections
            )
            try:
                await cls._conn.ping()
                logger.info("Redis connection established")
            except Exception as e:
                cls._conn = None
                logger.error(f"Redis connection failed: {e}")
                raise RuntimeError("Failed to connect to Redis")
        return cls._conn

    @classmethod
    async def close_conn(cls):
        """Close the Redis connection."""
        if cls._conn:
            await cls._conn.close()
            cls._conn = None
            logger.info("Redis connection closed")

    @classmethod
    async def set(cls, key: str, value: Any, ttl: int = 3600):
        """Set a value in Redis with optional TTL."""
        if cls._conn is None:
            raise RuntimeError("Redis connection not initialized")
        try:
            await cls._conn.set(key, json.dumps(value), ex=ttl)
            logger.debug(f"Set key '{key}' in Redis (TTL={ttl}s)")
        except Exception as e:
            logger.error(f"Failed to set key '{key}' in Redis: {e}")
            raise

    @classmethod
    async def get(cls, key: str) -> Optional[Any]:
        """Retrieve a value from Redis."""
        if cls._conn is None:
            raise RuntimeError("Redis connection not initialized")
        try:
            result = await cls._conn.get(key)
            logger.debug(f"Retrieved key '{key}' from Redis")
            return json.loads(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get key '{key}' from Redis: {e}")
            raise

    @classmethod
    async def cache_or_fetch(
        cls,
        key: str,
        fetch_func: Callable[[], Coroutine[Any, Any, Any]],
        ttl: int = 3600
    ) -> Any:
        """
        Try cache first; otherwise fetch via `fetch_func`, cache it, and return.
        
        `fetch_func` must be an async function returning data serializable to JSON.
        """
        cached = await cls.get(key)
        if cached is not None:
            logger.info(f"Cache hit for key '{key}'")
            return cached

        logger.info(f"Cache miss for key '{key}', fetching data...")
        data = await fetch_func()
        await cls.set(key, data, ttl)
        return data
