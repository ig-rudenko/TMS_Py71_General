from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from ..callbacks.general import show_notes, create_note, clear_state


def get_general_keyboard_markup() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Список заметок", callback_data=show_notes))
    keyboard.add(InlineKeyboardButton(text="Создать заметку", callback_data=create_note))
    return keyboard.as_markup()


def get_cancel_keyboard_markup() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="❌ Отмена", callback_data=clear_state))
    return keyboard.as_markup()
