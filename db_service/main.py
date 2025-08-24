import asyncio

from infrastructure.kafka_manager import kafka_manager
from infrastructure.celery.tasks import (
    handle_vacancies,
    handle_criterion_values,
    handle_upsert_user_data,
    handle_is_user_consuming_request,
    handle_get_user_data,
)
from logger import logger


async def main():
    consumer = await kafka_manager.create_consumer(
        [
            "vacancy",
            "get_criterion",
            "user_data",
            "is_user_consuming_request",
            "get_user_data",
        ]
    )
    try:
        async for message in consumer:
            logger.info(f"message topic: {message.topic}")
            match message.topic:
                case "vacancy":
                    vacancy_json = message.value
                    logger.info("Received vacancy")
                    handle_vacancies.delay(vacancy_json)
                case "get_criterion":
                    criterion_request = message.value
                    handle_criterion_values.delay(criterion_request)
                case "user_data":
                    user_data = message.value
                    logger.info("Started processing user's data")
                    handle_upsert_user_data.delay(user_data)
                case "is_user_consuming_request":
                    request_data = message.value
                    logger.info("Processing user activity request")
                    handle_is_user_consuming_request.delay(request_data)
                case "get_user_data":
                    data = message.value
                    handle_get_user_data.delay(data)
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
