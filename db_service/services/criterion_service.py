import json

from repositories.criterion_repository import CriterionRepository
from logger import logger
from infrastructure.kafka_manager import kafka_manager
from infrastructure.redis_cache import redis_cache


class CriterionService:

    def __init__(self) -> None:
        self.criterion_repository = CriterionRepository()

    def criterion_data(self, data: dict):
        try:
            request_id = data["request_id"]
            criterion = data["criterion"]

            cache_key = f"criterion:{criterion}"
            cached = redis_cache.get(cache_key)
            if cached:
                values = json.loads(cached)

            values = redis_cache.get_criterion_values(criterion)

            if values is None:
                values = self.criterion_repository.get_criterion_values(criterion)
                redis_cache.cache_criterion_values(criterion, values)

            response = {
                "request_id": request_id,
                "criterion": criterion,
                "values": values,
            }
            kafka_manager.send_message("criterion_response", response)
        except KeyError:
            logger.error("Invalid structure of criterion request")
            raise KeyError
