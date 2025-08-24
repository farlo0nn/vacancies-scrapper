import asyncio 
import traceback 


from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from logger import logger 
from bot import bot 

class NotificationsService:

    def __init__(self, bot: Bot):
        self.bot = bot 

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
        message = ""

        try:
            name = data["name"]
            url = data["url"]
            employer = data["employer"]
            workplace = " ".join(data["workplaces"]) 
            contract_types = ", ".join(data["contract_types"])
            position_levels = ", ".join(data["position_levels"])
            category = data["category"]
            subcategory = data["subcategory"]
            work_models = ", ".join(data["work_models"])
            work_schedule = ", ".join(data["work_schedules"])
      
        except Exception as e:
            logger.error(f"Invalid structure of the vacancy data object. \nTraceback: {traceback.format_exc()}") 
            raise e 

        message = "<b>New vacancy for you:</b>\n"
        message += f"📌 <b>{name}</b>\n"
        message += f"🏢 <b>Company:</b> {employer}\n\n\n"

        message += f"📍 <b>Location: {workplace}</b>\n"
        message += f"📄 Contract: {contract_types}\n"
        message += f"💼 Experience: {position_levels}\n"
        message += f"🔍 Category: {category} -> {subcategory}\n"
        message += f"🗂 Work Model: {work_models}\n"
        message += f"🗓 Schedule: {work_schedule}\n"

        message += f" <a href='{url}'><b>VIEW</b></a>"  

        return message 
    
notifications_service = NotificationsService(bot)