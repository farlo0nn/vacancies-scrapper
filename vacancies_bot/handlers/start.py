from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.menus import criteria_keyboard
from states import FilterState
from services.kafka.client import kafka_client
from logger import logger 
from config import CRITERIA

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Handles "start" command:
    - Creates new user with its id and username.
    - Sends user data to Kafka.
    - Replies with welcoming message
    - Sets FSM state to FilterState.choosing_criterion.
    """
    
    user_data = {
        "id": message.from_user.id,
        "username": message.from_user.username,
        "preferences": {}
    }
    await kafka_client.send_user_data(user_data)
    await message.answer("Welcome! Choose a filter criterion:", reply_markup=criteria_keyboard(CRITERIA))
    await state.set_state(FilterState.choosing_criterion)
