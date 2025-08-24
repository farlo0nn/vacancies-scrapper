import os 
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Data
CRITERIA = {"Category": "category", "Location":"location", "Work Schedule": "work_schedule", "Work Model": "work_model", "Experience": "experience", "Contract Type": "contract_type"}

# Pagination
PAGE_SIZE = 4

# Message templates 
TEMPLATE_DIR = os.environ.get("TEMPLATE_DIR", "templates/")
VACANCY_MESSAGE_TEMPLATE_FILE = os.environ.get("VACANCY_MESSAGE_TEMPLATE_FILE", "vacancy_message.html")

# Logging
LOG_FILE = "log/log.log"