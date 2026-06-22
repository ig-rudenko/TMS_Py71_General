from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

from ..callbacks.general import (
    show_notes_callback,
    create_note_callback,
    clear_state_callback,
    go_to_home_callback,
)


def get_general_keyboard_markup() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Список заметок", callback_data=show_notes_callback))
    keyboard.add(InlineKeyboardButton(text="Создать заметку", callback_data=create_note_callback))
    return keyboard.as_markup()


def get_cancel_keyboard_markup() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="❌ Отмена", callback_data=clear_state_callback))
    return keyboard.as_markup()


def get_go_home_keyboard_markup() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔝 Вернуться", callback_data=go_to_home_callback))
    return keyboard.as_markup()
