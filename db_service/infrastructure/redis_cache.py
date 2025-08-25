import json

from interfaces.cache import CacheService
from logger import logger
from redis import Redis
from typing import List
from config import REDIS_HOST, REDIS_PORT 

class RedisCache(CacheService):

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        self.r = Redis(host=host, port=port, db=db)

    def get_criterion_values(self, criterion: str) -> List[str]:
        cache_key = self._get_criterion_cache_key(criterion)

        cached_raw_values = self.r.get(cache_key)
        
        values = None 
        if cached_raw_values:
            values = json.loads(cached_raw_values)

        return values

    def cache_criterion_values(self, criterion: str, values: List[str]) -> None:
        cache_key = self._get_criterion_cache_key(criterion)

        try:
            self.r.setex(cache_key, 300, json.dumps(values))
        except Exception as e:
            logger.exception(f"Failed to cache {criterion}'s.")
            raise

    def _get_criterion_cache_key(self, criterion: str):
        return f"criterion:{criterion}"


redis_cache = RedisCache(host=REDIS_HOST, port=REDIS_PORT)
