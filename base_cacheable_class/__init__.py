from .base import BaseCacheableClass
from .cache.in_memory import InMemoryCache, InMemoryCacheDecorator
from .interfaces import CacheDecoratorInterface, CacheInterface, SyncCacheInterface
from .models import CacheItem

from .cache.in_memory.sync import SyncInMemoryCache, SyncInMemoryCacheDecorator

__all__ = [
    "BaseCacheableClass",
    "CacheInterface",
    "CacheDecoratorInterface",
    "CacheItem",
    "InMemoryCache",
    "InMemoryCacheDecorator",
    "SyncCacheInterface",
    "SyncInMemoryCache",
    "SyncInMemoryCacheDecorator",
]

# Conditional export for Redis classes
try:
    from .cache.redis import RedisCache, RedisCacheDecorator

    __all__.extend(["RedisCache", "RedisCacheDecorator"])
except ImportError:
    # Redis is optional
    pass
