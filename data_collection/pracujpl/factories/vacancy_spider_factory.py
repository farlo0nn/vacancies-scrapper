from pracujpl.spiders.vacancies_spider import VacanciesSpider
from pracujpl.interfaces import (
    CacheService, URLBuilder, VacancyExtractor, 
    MessageService, VacancySectionSelector
)

from pracujpl.services.url_building.pracujpl_url_builder import PracujplURLBuilder
from pracujpl.services.extraction.pracujpl_vacancy_extractor import PracujplVacancyExtractor
from pracujpl.services.selecting.pracujpl_vacancy_section_selector import PracujplVacancySectionSelector

class VacancySpiderFactory:
    
    def __init__(self) -> None:
        pass 

    @staticmethod
    def create_spider_cls(
            cache_service: CacheService,
            messaging_service: MessageService,
            url_builder: URLBuilder = PracujplURLBuilder(),
            vacancy_extractor: VacancyExtractor = PracujplVacancyExtractor(),
            vacancy_section_selector: VacancySectionSelector = PracujplVacancySectionSelector()
        ):
        """
        Fabric method for creating custom vacancy 
        spider classes with certain services provided
        - creates and returns custom vacancy spider class 
        """
        
        class _VacanciesSpider(VacanciesSpider):
            def __init__(self, *args, **kwargs):
                super().__init__(
                    cache_service=cache_service,
                    url_builder=url_builder,
                    vacancy_extractor=vacancy_extractor,
                    messaging_service=messaging_service,
                    vacancy_section_selector=vacancy_section_selector,
                    *args,
                    **kwargs
                )
        return _VacanciesSpider