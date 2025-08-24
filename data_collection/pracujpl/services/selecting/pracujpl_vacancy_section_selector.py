from scrapy.http import TextResponse
from pracujpl.interfaces import VacancySectionSelector
from logger import logger 


class PracujplVacancySectionSelector(VacancySectionSelector):
    
    def __init__(self) -> None:
        super().__init__()

    def vacancy_page_exists(self, response: TextResponse) -> TextResponse:
        logger.info(f"Checking if page exists on address: {response.url}")
        section_offers_exists = response.xpath('//div[@data-test="section-offers"]').get()
        return section_offers_exists is not None  
    
    def get_vacancy_section(self, response: TextResponse) -> TextResponse:
        html = response.xpath('//div[@data-test="section-offers"]').get()
        if html:
            return TextResponse(url=response.url, body=html, encoding='utf-8')
        return None