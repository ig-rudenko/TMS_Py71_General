from src.application.services.cache import AbstractCache
from src.infrastructure.cache.local import InMemoryCache
from src.infrastructure.cache.redis import RedisCache
from src.infrastructure.settings import settings

__cache__: AbstractCache | None = None


def get_cache() -> AbstractCache:
    global __cache__

    if __cache__ is not None:
        return __cache__

    if settings.redis_host:
        cache: AbstractCache = RedisCache(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password,
            max_connections=settings.redis_max_connections,
        )
    else:
        cache = InMemoryCache()

    __cache__ = cache

    return cache
