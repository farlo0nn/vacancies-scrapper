from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.menus import values_keyboard, criteria_keyboard, main_keyboard
from states import FilterState, AppState
from services.kafka.client import kafka_client
from logger import logger 

router = Router()

PAGE_SIZE = 3
CRITERIA = {
    "Category": "category", 
    "Location":"location", 
    "Work Schedule": "work_schedule", 
    "Work Model": "work_model", 
    "Experience": "experience", 
    "Contract Type": "contract_type"
}

@router.callback_query(F.data.startswith("crit:"))
async def choose_criterion(callback: types.CallbackQuery, state: FSMContext):
    logger.info("choose_criterion called")
    criterion = callback.data.split(":")[1]
    await state.update_data(current_criterion=criterion)
    await state.set_state(FilterState.choosing_value)

    data = await state.get_data()
    cached_values = data.get("criterion_values", {}).get(criterion)
    logger.info(f"Cached values: {cached_values}")
    if not cached_values:
        logger.info(f"Requesting db service to fetch values for {criterion}")
        response = await kafka_client.send_criterion_request({"criterion": criterion})
        cached_values = response["values"]

        all_vals = data.get("criterion_values", {})
        all_vals[criterion] = cached_values
        await state.update_data(criterion_values=all_vals)

    cached_selected = data.get("preferences", {})
    selected_values = []
    if not cached_selected: 
        logger.info(f"Requesting db service to fetch user preferences, user: {callback.from_user.id}")
        response = await kafka_client.get_user_data(callback.from_user.id)
        logger.info(response)
        selected = response["preferences"]
        await state.update_data(preferences=selected)
        selected_values = selected.get(criterion, [])
    else:
        selected_values = cached_selected.get(criterion, [])    

    page = 1
    total_pages = (len(cached_values) + PAGE_SIZE - 1) // PAGE_SIZE
    kb = values_keyboard(cached_values[:PAGE_SIZE], selected_values, page, total_pages, criterion)

    await callback.message.edit_text(f"Choose a value for {criterion}:", reply_markup=kb)


@router.callback_query(F.data.startswith("val:"))
async def choose_value(callback: types.CallbackQuery, state: FSMContext):
    logger.info("choose_value called")
    _, criterion, value = callback.data.split(":")
    data = await state.get_data()
    prefs = data.get("preferences", {})
    selected = prefs.get(criterion, [])

    if value in selected:
        selected.remove(value)
    else:
        selected.append(value)
    prefs[criterion] = selected
    await state.update_data(preferences=prefs)

    cached_values: list = data.get("criterion_values", {}).get(criterion, [])
    page = cached_values.index(value) // PAGE_SIZE + 1
    logger.info(f"page: {page}")

    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    total_pages = (len(cached_values) + PAGE_SIZE - 1) // PAGE_SIZE

    kb = values_keyboard(cached_values[start:end], selected, page, total_pages, criterion)
    await callback.message.edit_text(f"Select {criterion} values:", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data.startswith("page:"))
async def paginate(callback: types.CallbackQuery, state: FSMContext):
    logger.info("paginate called")
    _, criterion, page = callback.data.split(":")
    page = int(page)

    data = await state.get_data()
    cached_values = data.get("criterion_values", {}).get(criterion)

    if not cached_values:
        response = await kafka_client.send_criterion_request({"criterion": criterion})
        cached_values = response["values"]
        all_vals = data.get("criterion_values", {})
        all_vals[criterion] = cached_values
        await state.update_data(criterion_values=all_vals)

    selected = data.get("preferences", {}).get(criterion, [])

    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    total_pages = (len(cached_values) + PAGE_SIZE - 1) // PAGE_SIZE

    kb = values_keyboard(cached_values[start:end], selected, page, total_pages, criterion)
    await callback.message.edit_text(f"Choose a value for {criterion}:", reply_markup=kb)


@router.callback_query(F.data.startswith("submit_val:"))
async def save_criterion_preferences(callback: types.CallbackQuery, state: FSMContext):
    logger.info("save_criterion_preferences called")

    await callback.message.answer("✅ Criterion data saved!")
    await callback.message.answer("Choose another criterion:", reply_markup=criteria_keyboard(CRITERIA))
    await state.set_state(FilterState.choosing_criterion)

@router.callback_query(F.data.startswith("submit_preferences"))
async def submit_preferences(callback: types.CallbackQuery, state: FSMContext):
    logger.info("submit_preferences called")
    data = await state.get_data()

    user_data = {
        "id": callback.from_user.id,
        "username": callback.from_user.username, 
        "preferences": data.get("preferences", {})
    }

    await state.set_state(AppState.consuming_vacancies)
    await kafka_client.send_user_data(user_data)
    await callback.message.answer("✅ Your preferences have been saved!", reply_markup=main_keyboard())
