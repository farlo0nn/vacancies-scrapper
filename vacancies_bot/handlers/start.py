from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.menus import criteria_keyboard
from states import FilterState
from services.kafka.client import kafka_client
from logger import logger 

router = Router()

CRITERIA = {"Category": "category", "Location":"location", "Work Schedule": "work_schedule", "Work Model": "work_model", "Experience": "experience", "Contract Type": "contract_type"}

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_data = {
        "id": message.from_user.id,
        "username": message.from_user.username,
        "preferences": {}
    }
    await kafka_client.send_user_data(user_data)
    await message.answer("Welcome! Choose a filter criterion:", reply_markup=criteria_keyboard(CRITERIA))
    await state.set_state(FilterState.choosing_criterion)
