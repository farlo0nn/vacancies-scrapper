import traceback


from infrastructure.kafka_manager import kafka_manager
from repositories.user_repository import UserRepository
from logger import logger


class UserService:

    def __init__(self) -> None:
        self.user_repository = UserRepository()

    def get_user_data(self, data: dict) -> None:
        try:
            request_id = data["request_id"]
            user_id = data["user_id"]
            user_data = self.user_repository.get_user_data(data)

            response = {
                "request_id": request_id,
                "user_id": user_id,
                "preferences": user_data,
            }

            kafka_manager.send_message("get_user_data_response", response)
        except Exception as e:
            logger.error(
                f"Error occurred while getting user data: {traceback.format_exc()}"
            )
            raise e

    def upsert_user_data(self, data: dict):
        try:
            self.user_repository.upsert_user_from_dict(data)
            logger.info("User's data was upserted")
        except Exception as e:
            logger.exception(f"Could update user's data")
            raise e

    def is_user_consuming(self, data: dict):
        logger.info("User's activity handler")
        try:
            request_id = data["request_id"]
            user_id = data["user_id"]
            is_consuming = False
            change_value = data["change"]

            is_consuming = self.user_repository.is_user_consuming(user_id, change_value)

            response = {
                "request_id": request_id,
                "user_id": user_id,
                "is_consuming": is_consuming,
            }
            kafka_manager.send_message("is_user_consuming_response", response)
        except KeyError:
            logger.exception("Invalid structure of user_active request")
            raise
