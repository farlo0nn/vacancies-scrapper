from abc import ABC, abstractmethod
from .data_models import VacancyData
from scrapy.http import TextResponse


class VacancyExtractor(ABC):
    
    @abstractmethod 
    def extract_vacancy_data(self, response: TextResponse) -> VacancyData:
        "Extracts vacancy data from the webpage"
        pass 
