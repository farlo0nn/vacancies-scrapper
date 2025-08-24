from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.menus import configuration_keyboard, criteria_keyboard
from states import FilterState, AppState
from services.kafka.client import kafka_client
from logger import logger 

router = Router()

CRITERIA = {"Category": "category", "Location":"location", "Work Schedule": "work_schedule", "Work Model": "work_model", "Experience": "experience", "Contract Type": "contract_type"}


@router.message(F.text == "Settings")
async def settings_handler(message: types.Message, state: FSMContext):
    logger.info("Settings called")
    await state.set_state(AppState.configuration)
    is_active = await kafka_client.send_is_consuming_request(message.from_user.id)
    logger.info(is_active)
    await message.answer("Settings:", reply_markup=configuration_keyboard(is_active))

@router.message(F.text == "Preferences")
async def preferences_config_handler(message: types.Message, state: FSMContext):
    user_data = {
        "id": message.from_user.id,
        "username": message.from_user.username,
        "preferences": {}
    }
    response = await kafka_client.get_user_data(message.from_user.id)
    preferences = response["preferences"]
    user_data["preferences"] = preferences

    await message.answer("Welcome! Choose a filter criterion:", reply_markup=criteria_keyboard(CRITERIA))
    await state.set_state(FilterState.choosing_criterion)

@router.message(F.text.endswith("notifications"))
async def user_consuming_config_handler(message: types.Message, state: FSMContext):
    logger.info("Changing is user consuming")
    is_consuming_response = await kafka_client.send_is_consuming_request(message.from_user.id, change=True)
    is_consuming = is_consuming_response["is_consuming"]
    logger.info(is_consuming)
    await message.answer("Changed activity", reply_markup=configuration_keyboard(is_consuming))