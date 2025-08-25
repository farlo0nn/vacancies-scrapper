from celery import Celery
from config import REDIS_HOST, REDIS_PORT

app = Celery("vacancies_processor", broker=f"redis://{REDIS_HOST}:{REDIS_PORT}")

app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]

app.autodiscover_tasks(["infrastructure.celery"])
