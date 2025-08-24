from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from logger import logger
from typing import Callable

from pracujpl.factories.vacancy_spider_factory import VacancySpiderFactory

def run_spider(spider_class: Callable, **kwargs):
    logger.info("Starting VacanciesSpider crawl...")
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class, **kwargs)
    process.start()

if __name__ == "__main__":
    
    run_spider(
        VacancySpiderFactory.create_spider_cls()
    )

