import asyncio
import services.kafka.handlers 

from aiogram import Dispatcher
from services.kafka.client import kafka_client
from handlers import preferences, start, settings

from bot import bot 


async def main():
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(preferences.router)
    dp.include_router(settings.router)

    await kafka_client.start_producer()
    await kafka_client.start_consumer(["telegram_vacancy", "criterion_response", "is_user_consuming_response", "get_user_data_response"])
    try:
        await dp.start_polling(bot)
    finally:
        await kafka_client.stop_producer()
        await kafka_client.stop_consumer()

if __name__ == "__main__":
    asyncio.run(main())
