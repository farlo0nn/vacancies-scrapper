import json 

from kafka import KafkaProducer


from pracujpl.interfaces import MessageService
from pracujpl.interfaces.data_models import VacancyData
from logger import logger 
from config import KAFKA_BOOTSTRAP_SERVERS

class KafkaMessageService(MessageService):

    def __init__(self, bootstrap_servers: str|list[str]) -> None:
        logger.info(f"{KAFKA_BOOTSTRAP_SERVERS} {bootstrap_servers}")
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers, 
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def send_vacancy(self, vacancy: VacancyData):
        self.producer.send("vacancy", vacancy.asDict())
    
    def close(self) -> None:
        self.producer.flush()
        self.producer.close()