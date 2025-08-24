import json 
import asyncio 
import uuid
import traceback

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord
from logger import logger 
from typing import List, Dict, Callable

class KafkaClient:

    def __init__(self) -> None:
        self.producer: AIOKafkaProducer|None = None 
        self.consumer: AIOKafkaConsumer|None = None 
        self.producer_running: bool = False 
        self.consumer_running: bool = False 
        self.message_handlers: Dict[str, Callable] = {}
        self.global_handler: Callable|None = None 
        self.pending_requests: Dict[str, str] = {}

    async def start_producer(self) -> None: 
        self.producer = AIOKafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda x: json.dumps(x).encode("utf-8")
        )
        self.producer_running = True 
        await self.producer.start()

    async def stop_producer(self):
        if self.producer:
            self.producer_running = False 
            await self.producer.stop()

    async def start_consumer(self, topics: List[str], group_id: str = "telegram-group") -> None: 
        if self.consumer_running:
            logger.info("Consumer is already running")
            return 
        
        try:
            self.consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers="localhost:9092",
                group_id=group_id,
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )

            await self.consumer.start()
            self.consumer_running = True
            self.consumer_task = asyncio.create_task(self._consumer_loop())

            logger.info(f"Consumer started for topics: {topics}")

        except Exception as e:
            logger.error("Couldn't start consumer")
            raise e

    async def stop_consumer(self):
        if self.consumer_running:
            if self.consumer_task and not self.consumer_task.done():
                self.consumer_task.cancel()
                try:
                    await self.consumer_task
                except asyncio.CancelledError:
                    pass
            
            if self.consumer:
                await self.consumer.stop() 
                self.consumer = None

    async def _consumer_loop(self):
        try: 
            async for message in self.consumer:
                if not self.consumer_running:
                    break

                try:
                    await self._handle_message(message)
                    await self.consumer.commit()
                except Exception as e:
                    logger.error(f"Couldn't process message: {message.topic}\nError: {traceback.format_exc()}"
                )
        except asyncio.CancelledError:
            logger.info("Consumer loop was cancelled")            
        except Exception as e:
            logger.error(f"Error occurred while running consumer loop: {traceback.format_exc()}")
            raise e
        
    async def _handle_message(self, message: ConsumerRecord):
        try:
            topic = message.topic 
            data = message.value 

            logger.info(f"Started processing message: {topic}")
            handler = self.message_handlers.get(topic)
            if handler is not None:
                await handler(data, topic)
            elif self.global_handler is not None:
                await self.global_handler(data, topic)
            else:
                logger.warning(f"No handler for message: {topic}")

        except Exception as e:
            logger.error(f"Error occurred while processing message: {message.topic}")

    def register_handler(self, topics: str|list[str], handler: Callable):
        if isinstance(topics, str):
            self.message_handlers[topics] = handler
            logger.info(f"Added new handler to topic {topics}")
        elif isinstance(topics, list):
            for topic in topics: 
                self.message_handlers[topic] = handler
                logger.info(f"Added new handler to topic {topic}")
        else:
            raise TypeError("Invalid type of topic")

    def set_global_handler(self, handler: Callable):
        self.global_handler = handler
        logger.info(f"Added global handler")

    def on_message_handler(self, topics: str|list[str]):
        def wrapper(handler: Callable):
            self.register_handler(topics, handler)                    
            return handler 
        return wrapper 

    async def send_user_data(self, user_data: dict, is_future: bool = False):
        if not self.producer:
            raise RuntimeError("Kafka producer is not started")
        logger.info(user_data)
        if not is_future: 
            await self.producer.send("user_data", user_data)
        else:
            req_id = str(uuid.uuid4())
            user_data.update({"request_id": req_id})
            fut = asyncio.get_event_loop().create_future()
            self.pending_requests[req_id] = fut
            await self.producer.send_and_wait("user_data", user_data)
            return await fut 

    async def get_user_data(self, user_id: int):
        req_id = str(uuid.uuid4())
        request = {
            "request_id": req_id,
            "user_id": user_id 
        }
        fut = asyncio.get_event_loop().create_future()
        self.pending_requests[req_id] = fut
        await self.producer.send_and_wait("get_user_data", request)
        return await fut 

    async def send_criterion_request(self, payload: dict):
        req_id = str(uuid.uuid4())
        payload.update({"request_id": req_id})
        fut = asyncio.get_event_loop().create_future()
        self.pending_requests[req_id] = fut
        await self.producer.send_and_wait("get_criterion", payload)
        return await fut 

    async def send_is_consuming_request(self, user_id: int, change: bool = False):
        req_id = str(uuid.uuid4())
        request = {
            "request_id": req_id,
            "user_id": user_id,
            "change": change,
        }
        fut = asyncio.get_event_loop().create_future()
        self.pending_requests[req_id] = fut
        await self.producer.send_and_wait("is_user_consuming_request", request)
        return await fut 


    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop_all()

kafka_client = KafkaClient()
