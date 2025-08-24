import traceback


from pracujpl.interfaces.cache import CacheService
from logger import logger
from redis import Redis

class RedisCache(CacheService):

    def __init__(self, host:str='localhost', port:int=6379, db:int=0) -> None:
        self.r = Redis(host=host, port=port, db=db)

    def is_processed(self, item_id: str) -> bool:
        try:
            if self.r.sismember("processed_vacancies", item_id):
                logger.info(f"Vacancy is already processed: {item_id}")
                return True 
            return False 
        except Exception as e:
            logger.error(f"Failed to check Redis for vacancy: {item_id}. {traceback.format_exc()}")
            raise e 
    
    def mark_processed(self, item_id: str) -> None:
        try:
            self.r.sadd("processed_vacancies", item_id)
        except Exception as e:  
            logger.info(f"Failed to mark vacancy {item_id} as processed. {traceback.format_exc()}")
            raise e 