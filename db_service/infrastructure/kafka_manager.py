import json
import asyncio

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from concurrent.futures import ThreadPoolExecutor
from config import KAFKA_BOOTSTRAP_SERVERS
from typing import List


class AsyncKafkaManager:
    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=2)

    def send_message(self, topic: str, message: dict):
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(self._send_async(topic, message))
            finally:
                loop.close()

        future = self._executor.submit(run_async)
        return future.result(timeout=20)

    async def _send_async(self, topic: str, message: dict):
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )
        await producer.start()
        try:
            await producer.send_and_wait(topic, message)
        finally:
            await producer.stop()

    async def create_consumer(self, topics: str | List[str]):
        if isinstance(topics, str):
            topics = [topics]

        consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            enable_auto_commit=True
        )
        await consumer.start()
        return consumer


kafka_manager = AsyncKafkaManager()
