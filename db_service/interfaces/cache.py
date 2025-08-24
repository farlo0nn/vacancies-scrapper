from abc import ABC, abstractmethod
from typing import List


class CacheService(ABC):

    @abstractmethod
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        "Initialise redis instance"
        pass

    @abstractmethod
    def get_criterion_values(self, criterion: str) -> List[str]:
        "Get criterion values from cache"
        pass

    @abstractmethod
    def cache_criterion_values(self, criterion: str, values: List[str]) -> None:
        "Add criterion values to cache"
        pass

    @abstractmethod
    def _get_criterion_cache_key(criterion: str) -> str:
        "Generate key for specific criterion"
        pass
