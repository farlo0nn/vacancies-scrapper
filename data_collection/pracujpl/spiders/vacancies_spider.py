import scrapy

from logger import logger 
from scrapy.http import TextResponse
from scrapy import signals
from scrapy.linkextractors import LinkExtractor
from config import BASE_URL, VACANCIES_SPIDER_ALLOWED_DOMAINS, KAFKA_BOOTSTRAP_SERVERS

from pracujpl.interfaces import (
    CacheService, URLBuilder, VacancyExtractor, 
    MessageService, VacancySectionSelector
)

from pracujpl.services.cache.redis_cache import RedisCache
from pracujpl.services.url_building.pracujpl_url_builder import PracujplURLBuilder
from pracujpl.services.extraction.pracujpl_vacancy_extractor import PracujplVacancyExtractor
from pracujpl.services.messaging.kafka_messaging_service import KafkaMessagingService
from pracujpl.services.selecting.pracujpl_vacancy_section_selector import PracujplVacancySectionSelector

class VacanciesSpider(scrapy.Spider):
    name = "vacancies"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains = VACANCIES_SPIDER_ALLOWED_DOMAINS
        self.start_urls = [BASE_URL]
        self.link_extractor: LinkExtractor = LinkExtractor(allow=r'https?://(?:www\.)?pracuj\.pl/praca/[^,]+,oferta,\d+(?:\?[^\s]*)?')
        self.cache_service: CacheService = kwargs["cache_service"]
        self.url_builder: URLBuilder = kwargs["url_builder"]
        self.vacancy_extractor: VacancyExtractor = kwargs["vacancy_extractor"]
        self.messaging_service: MessageService = kwargs["messaging_service"]
        self.vacancy_section_selector: VacancySectionSelector = kwargs["vacancy_section_selector"]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        "Factory method with dependency injection"
        spider = super().from_crawler(crawler, *args, **kwargs)
        
        crawler.signals.connect(
            lambda spider_inst, reason:  (
                spider_inst.message_service.close()
                if hasattr() and spider_inst.message_service
                else None 
            ), 
            signal=signals.spider_closed 
        )

        return spider

    def parse(self, response: TextResponse):
        self.logger.info(f"Fetched: {response.url}")
        if not self.vacancy_section_selector.vacancy_page_exists(response):
            retry_count = response.meta.get("retry_count", 0)
            if retry_count < 2:  
                logger.warning(f"Empty page, retrying: {response.url}")
                yield scrapy.Request(
                    response.url,
                    callback=self.parse,
                    meta={"retry_count": retry_count + 1},
                    dont_filter=True
                )
            else:
                logger.error(f"Such url doesn't contain any vacancies: {response.url}")
                return 

        links = self.link_extractor.extract_links(response)
        

        for link in links:
            vacancy_id = link.url.split(",oferta,")[-1].split("?")[0]
            
            if self.cache_service.is_processed(vacancy_id):
                logger.info(f"Skipping already processed vacancy: {vacancy_id}")
                self.crawler.engine.close_spider(self, reason="going through already processed vacancy")
            else:
                yield scrapy.Request(
                    url=link.url,
                    callback=self.parse_vacancy,
                    meta={"vacancy_id": vacancy_id, "vacancy_url": link.url}
                )

        next_page_url = self.url_builder.build_next_page_url(response.url)

        yield scrapy.Request(
            url=next_page_url,
            callback=self.parse
        )

    def parse_vacancy(self, response: TextResponse):
        vacancy = self.vacancy_extractor.extract_vacancy_data(response)

        self.cache_service.mark_processed(vacancy.id)
        self.messaging_service.send_vacancy(vacancy)