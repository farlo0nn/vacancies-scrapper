import json

from interfaces.cache import CacheService
from logger import logger
from redis import Redis
from typing import List


class RedisCache(CacheService):

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        self.r = Redis(host=host, port=port, db=db)

    def get_criterion_values(self, criterion: str) -> List[str]:
        cache_key = self._get_criterion_cache_key(criterion)

        cached = redis_cache.get(cache_key)
        if cached:
            values = json.loads(cached)
        return values

    def cache_criterion_values(self, criterion: str, values: List[str]) -> None:
        cache_key = self._get_criterion_cache_key(criterion)

        try:
            redis_cache.setex(cache_key, 300, json.dumps(values))
        except Exception as e:
            logger.exception(f"Failed to cache {criterion}'s.")
            raise

    def _get_criterion_cache_key(criterion: str):
        return f"criterion:{criterion}"


redis_cache = RedisCache()
