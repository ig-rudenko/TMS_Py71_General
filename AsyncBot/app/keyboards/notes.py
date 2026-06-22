from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.callbacks.general import submit_callback, clear_state_callback


def get_note_create_submit_keyboard_markup() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✅ Создать", callback_data=submit_callback))
    keyboard.add(InlineKeyboardButton(text="❌ Отмена", callback_data=clear_state_callback))
    return keyboard.as_markup()
