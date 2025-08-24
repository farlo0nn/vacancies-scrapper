from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.menus import configuration_keyboard, criteria_keyboard
from states import FilterState, SettingsState
from services.kafka.client import kafka_client
from logger import logger 
from config import CRITERIA

router = Router()


@router.message(F.text == "Settings")
async def settings_handler(message: types.Message, state: FSMContext):
    """
    Processes the "Settings" message:
    - Sets the FSM state to SettingsState.configuration.
    - Fetches the user's current notification activity via Kafka.
    - Updates the reply keyboard to the configuration menu.
    """
    
    logger.info("Settings called")
    await state.set_state(SettingsState.configuration)
    is_active = await kafka_client.send_is_consuming_request(message.from_user.id)
    logger.info(is_active)
    await message.answer("Settings:", reply_markup=configuration_keyboard(is_active))

@router.message(F.text == "Preferences")
async def preferences_config_handler(message: types.Message, state: FSMContext):
    """
    Processes the "Preferences" message:
    - Retrieves the user's preferences from Kafka.
    - Updates local user_data with preferences.
    - Sends a message prompting the user to choose a filter criterion.
    - Sets the FSM state to FilterState.choosing_criterion.
    """

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
    """
    Processes messages ending with "notifications":
    - Toggles the user's notification activity via Kafka.
    - Retrieves the updated is_consuming status.
    - Updates the reply keyboard to reflect the new activity status.
    """

    logger.info("Changing is user consuming")
    is_consuming_response = await kafka_client.send_is_consuming_request(message.from_user.id, change=True)
    is_consuming = is_consuming_response["is_consuming"]
    logger.info(is_consuming)
    await message.answer("Changed activity", reply_markup=configuration_keyboard(is_consuming))