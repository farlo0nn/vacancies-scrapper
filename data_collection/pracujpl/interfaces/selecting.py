from abc import ABC, abstractmethod
from typing import Any
from scrapy.http import TextResponse


class CriterionSelector(ABC):
    
    @abstractmethod
    def get_criterion_data(self, response: TextResponse, feature: str) -> Any:
        "Selects vacancy's criterion data "
        pass 

class VacancySectionSelector(ABC):

    @abstractmethod
    def get_vacancy_section(self, response: TextResponse) -> TextResponse:
        "Selects vacancy section"
        pass 

    def vacancy_page_exists(self, response: TextResponse) -> TextResponse:
        "Checks if there are vacancies on the web page"
        pass 