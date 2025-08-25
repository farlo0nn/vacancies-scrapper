from abc import ABC, abstractmethod
from logger import logger 

class URLBuilder(ABC):
    
    @abstractmethod
    def build_next_page_url(self, current_url) -> str: 
        "Builds url for the next vacancies page, based on the current page url"
        pass 