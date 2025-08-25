from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from logger import logger 
from typing import Dict

def criteria_keyboard(criteria: Dict[str, str]):
    """
    Inline keyboard of criteria to select users' preferences
    - Creates keyboard with button for each criterion
    """

    keyboard = []
    keyboard = [
        [InlineKeyboardButton(text=c, callback_data=f"crit:{criteria[c]}")] for c in criteria.keys()
    ]

    keyboard.append(
        [InlineKeyboardButton(text="Submit Preferences", callback_data=f"submit_preferences")]
    )


    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )

def values_keyboard(all_values: list[str], selected: list[str], page: int, total_pages: int, criterion: str):
    """
    Inline keyboard of values for certain criterion to select users' preferences
    - Creates keyboard with button for each value 
    - Marks each value with tick if it is selected by user and cross if not 
    - Adds pagination to show predefined number of values at once 
    """
    
    buttons = []
    for v in all_values:
        checked = "✅" if v in selected else "❌"
        buttons.append([InlineKeyboardButton(
            text=f"{checked} {v}",
            callback_data=f"val:{criterion}:{v}"
        )])
    logger.info(page)
    
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"page:{criterion}:{page-1}"))
    if page < total_pages:
        nav.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"page:{criterion}:{page+1}"))
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton(text="Submit", callback_data=f"submit_val:{criterion}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def main_keyboard():

    
    keyboard = [
        [KeyboardButton(text="Settings")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard = True 
    )

def configuration_keyboard(is_listening: bool = True):
    """
    Builds a reply keyboard for the settings menu in the Telegram bot.
    The keyboard provides two options:
    - "Preferences" — allows the user to configure their filtering preferences.
    - Notifications toggle — text depends on whether the user is currently listening/consuming.
        - If `is_consuming` is True: shows "❌ Disable notifications".
        - If `is_consuming` is False: shows "✅ Enable notifications".
    """

    notifications_message = "❌ Disable notifications" if is_listening else "✅ Enable notifications"
    keyboard = [
        [KeyboardButton(text="Preferences")],
        [KeyboardButton(text=notifications_message)]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard = True,
        one_time_keyboard=True
    )