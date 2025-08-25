import os 
from dotenv import load_dotenv

load_dotenv()


# Scraping 
BASE_DOMAIN = os.environ.get("BASE_DOMAIN", "https://pracuj.pl") 
BASE_URL = BASE_DOMAIN + os.environ.get("BASE_ROUTE","/praca?sc=0&pn=1")

# Scrapy 
VACANCIES_SPIDER_ALLOWED_DOMAINS = os.environ.get("VACANCIES_SPIDER_ALLOWED_DOMAINS", ["pracuj.pl"])


# Messaging 
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_VACANCIES_SEND_TOPIC = os.environ.get("KAFKA_VACANCIES_SEND_TOPIC", "vacancy")

# Cache
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

# Logging
LOG_FILE = os.environ.get("LOG_FILE", "logs/log.log")
