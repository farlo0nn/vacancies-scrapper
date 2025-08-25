import os
from dotenv import load_dotenv

load_dotenv()

# DB
PG_HOST = os.environ.get("PG_HOST")
PG_USER = os.environ.get("PG_USER")
PG_PASSWORD = os.environ.get("PG_PASSWORD")
PG_PORT = os.environ.get("PG_PORT", 5432)
PG_DBNAME = os.environ.get("PG_DBNAME")

# Messaging
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Cache
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

# Logging
LOG_FILE = os.environ.get("LOG_FILE") or "log/log.log"
