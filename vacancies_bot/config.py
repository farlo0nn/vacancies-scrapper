import os 
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Message templates 
TEMPLATE_DIR = os.environ.get("TEMPLATE_DIR", "templates/")
VACANCY_MESSAGE_TEMPLATE_FILE = os.environ.get("VACANCY_MESSAGE_TEMPLATE_FILE", "vacancy_message.html")

# Logging
LOG_FILE = "log/log.log"