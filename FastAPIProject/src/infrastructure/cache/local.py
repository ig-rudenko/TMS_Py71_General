from datetime import datetime, timedelta
from typing import Any, TypedDict

from src.application.services.cache import AbstractCache


class _ValueType(TypedDict):
    data: Any
    expires: datetime


class InMemoryCache(AbstractCache):
    """Кэш данных в памяти."""

    def __init__(self) -> None:
        self._cache: dict[str, _ValueType] = {}

    async def get(self, key: str) -> Any | None:
        if value := self._cache.get(key, None):
            if value["expires"] > datetime.now():
                return value["data"]
            else:
                await self.delete(key)
        return None

    async def set(self, key: str, value: Any, timeout: int) -> None:
        self._cache[key] = {
            "data": value,
            "expires": datetime.now() + timedelta(seconds=timeout),
        }

    async def delete(self, key: str) -> None:
        self._cache.pop(key, None)
