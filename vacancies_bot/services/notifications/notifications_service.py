import asyncio 
import traceback 


from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from logger import logger 
from bot import bot 
from .utils import load_html_template

class NotificationsService:

    def __init__(self, bot: Bot):
        self.bot = bot 
        self.template = load_html_template()

    async def send_vacancy_message(self, vacancy_data: dict) -> None:
        vacancy_message = self._format_vacancy_message(vacancy_data)
        subscribers = vacancy_data["subscribers"]
        logger.info(f"{len(vacancy_message)}: {vacancy_message}")
        for user_id in subscribers:
            try:
                await self.bot.send_message(
                    chat_id = user_id, 
                    text=vacancy_message, 
                    parse_mode=ParseMode.HTML
                )
                await asyncio.sleep(0.05)
            except Exception as e:
                logger.error(f"Error occurred while sending vacancy message to user \nTraceback: {traceback.format_exc()}")
                raise e

    def _format_vacancy_message(self, data: dict) -> str:
        try:
            return self.template.render(**data)
        except KeyError as e:
            logger.error(f"Missing key in vacancy data: {e}\n{traceback.format_exc()}")
            raise
        except Exception as e:
            logger.error(f"Failed to render vacancy message:\n{traceback.format_exc()}")
            raise

    
notifications_service = NotificationsService(bot)