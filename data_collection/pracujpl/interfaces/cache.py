from abc import ABC, abstractmethod


class CacheService(ABC):
    
    @abstractmethod
    def is_processed(self, item_id: str) -> bool:
        "Check if item has been processed"
        pass 

    @abstractmethod
    def mark_processed(self, item_id: str) -> None: 
        "Mark item as processed"
        pass 