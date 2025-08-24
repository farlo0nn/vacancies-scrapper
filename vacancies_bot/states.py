from aiogram.fsm.state import StatesGroup, State

class FilterState(StatesGroup):
    choosing_criterion = State()
    choosing_value = State()

class SettingsState(StatesGroup):
    consuming_vacancies = State()
    configuration = State()