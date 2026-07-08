import pickle
from typing import Any

from redis.asyncio import ConnectionPool, Redis

from src.application.services.cache import AbstractCache


class RedisCache(AbstractCache):
    def __init__(self, host: str, port: int, db: int, password: str | None = None, max_connections: int = 5):
        self._pool = ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            socket_timeout=2,
            socket_connect_timeout=2,
            max_connections=max_connections,
        )
        self._redis = Redis(connection_pool=self._pool)

    async def get(self, key: str) -> Any | None:
        value = await self._redis.get(key)
        if value is not None:
            return pickle.loads(value)  # type: ignore
        return None

    async def set(self, key: str, value: Any, timeout: int) -> None:
        await self._redis.set(key, pickle.dumps(value), ex=timeout)

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)
