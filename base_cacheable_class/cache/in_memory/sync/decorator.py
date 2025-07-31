import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

from ..utils import key_builder, pattern_builder
from ....interfaces import CacheDecoratorInterface, SyncCacheInterface

logger = logging.getLogger(__name__)


class SyncInMemoryCacheDecorator(CacheDecoratorInterface):
    def __init__(self, cache: SyncCacheInterface, default_ttl: int = 60):
        self.cache = cache
        self.default_ttl = default_ttl

    def __call__(self, ttl: int | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                _key = key_builder(func, *args, **kwargs)
                current_ttl = ttl if ttl is not None else self.default_ttl

                try:
                    cached_value = self.cache.get(_key)
                    if cached_value is not None:
                        return cached_value

                    result = func(*args, **kwargs)

                    if result is not None:
                        self.cache.set(_key, result, ttl=current_ttl)

                    return result
                except Exception as e:
                    logger.error(f"Error in cache decorator: {e}")
                    return func(*args, **kwargs)

            return wrapper

        return decorator

    def invalidate(
        self, target_func_name: str, param_mapping: dict[str, str] | None = None
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    pattern = pattern_builder(target_func_name, param_mapping, **kwargs)
                    cached_keys = self.cache.get_keys(pattern)

                    for cache_key in cached_keys:
                        self.cache.delete(cache_key)

                except Exception as e:
                    logger.error(f"Error in cache invalidation: {e}")

                return func(*args, **kwargs)

            return wrapper

        return decorator

    def invalidate_all(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                _key = key_builder(func, *args, **kwargs)
                try:
                    self.cache.clear()
                except Exception as e:
                    logger.error(f"Error in cache clear: {e}")
                return func(*args, **kwargs)

            return wrapper

        return decorator
