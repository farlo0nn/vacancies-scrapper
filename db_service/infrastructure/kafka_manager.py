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
        """
        Sends a message to a Kafka topic synchronously:
        - Runs an async producer inside a separate event loop to avoid blocking the main loop.
        - Submits the async task to a thread pool executor.
        - Waits for the result with a timeout of 20 seconds.
        - Returns once the message is successfully sent or raises TimeoutError if exceeded.
        """

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
        """
        Asynchronous helper for send_message:
        - Creates a temporary Kafka producer instance.
        - Starts the producer and serializes the message to JSON.
        - Sends the message to the given Kafka topic and waits for acknowledgment.
        - Ensures the producer is stopped after the operation, even if an error occurs.
        """

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
        """
        Asynchronous method for creating consumer
        - creates consumer for provided topics 
        - starts consumer so it receives messages 
        """
        
        
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
