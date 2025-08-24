import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from infrastructure.celery.celery_app import app

from services.vacancy_service import VacancyService
from services.user_service import UserService
from services.criterion_service import CriterionService

vacancy_service = VacancyService()
user_service = UserService()
criterion_service = CriterionService()


@app.task(name="infrastructure.celery.tasks.handle_vacancy")
def handle_vacancies(vacancy_json: dict) -> None:
    vacancy_service.save_vacancy(vacancy_json)


@app.task(name="infrastructure.celery.tasks.handle_criterion_values")
def handle_criterion_values(criterion_request: dict) -> None:
    criterion_service.criterion_data(criterion_request)


@app.task(name="infrastructure.celery.tasks.handle_is_user_consuming_request")
def handle_is_user_consuming_request(request_data: dict):
    user_service.is_user_consuming(request_data)


@app.task(name="infrastructure.celery.tasks.handle_upsert_user_data")
def handle_upsert_user_data(data: dict):
    user_service.upsert_user_data(data)


@app.task(name="infrastructure.celery.tasks.handle_get_user_data")
def handle_get_user_data(data: dict):
    user_service.get_user_data(data)
