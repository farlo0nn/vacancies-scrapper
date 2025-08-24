from repositories.vacancy_repository import VacancyRepository
from infrastructure.kafka_manager import kafka_manager
from logger import logger


class VacancyService:

    def __init__(self) -> None:
        self.vacancy_repository = VacancyRepository()

    def save_vacancy(self, vacancy_json: dict) -> None:
        vacancy_id = None
        try:
            vacancy_id = vacancy_json["id"]
        except KeyError:
            logger.error("Failed to handle vacancy. Invalid json structure.")
            raise KeyError

        if self.vacancy_repository.exists(vacancy_id):
            logger.info(f"Vacancy {vacancy_id} has already been processed.")
            return
        else:
            self.vacancy_repository.create(vacancy_json)

        try:
            subscribers = self.vacancy_repository.determine_target_users(vacancy_id)
            if len(subscribers) == 0:
                return

            vacancy_json["subscribers"] = subscribers
            kafka_manager.send_message("telegram_vacancy", vacancy_json)
            logger.info(f"Vacancy {vacancy_id} sent to Kafka successfully")
        except KeyError:
            logger.error("Failed to handle vacancy. Invalid json structure.")
        except Exception as kafka_error:
            logger.error(
                f"Database save successful but Kafka send failed for vacancy {vacancy_id}: {str(kafka_error)}"
            )
