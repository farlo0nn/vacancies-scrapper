from abc import ABC, abstractmethod
from .data_models import VacancyData 

class MessageService(ABC):

    @abstractmethod
    def send_vacancy(self, vacancy: VacancyData):
        "Sends vacancy data to message queue"
        pass 

    @abstractmethod
    def close(self) -> None:
        "Clean up resources and closes connection"
        pass 

