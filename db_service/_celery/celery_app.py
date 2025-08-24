from celery import Celery 

app = Celery('vacancies_processor', broker='redis://localhost:6379')

app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]

app.autodiscover_tasks(["_celery"]) 