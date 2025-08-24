from abc import ABC, abstractmethod
from logger import logger 

class URLBuilder(ABC):
    
    @abstractmethod
    def build_next_page_url(self, current_url) -> str: 
        pass 