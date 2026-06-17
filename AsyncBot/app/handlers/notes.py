from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..callbacks.general import show_notes, create_note
from ..keyboards.general import get_cancel_keyboard_markup
from ..states.notes import CreateNoteStateGroup
from ..text.notes import NOTE_CREATE_TITLE

router = Router()


@router.callback_query(F.data == show_notes)
async def notes_list_callback_handler(callback_data: CallbackQuery):
    """Отображение списка заметок"""

    await callback_data.answer()


@router.callback_query(F.data == create_note)
async def create_note_callback_handler(callback_data: CallbackQuery, state: FSMContext):
    """Начало создания заметки"""

    await callback_data.message.answer(NOTE_CREATE_TITLE, reply_markup=get_cancel_keyboard_markup())

    await state.set_state(CreateNoteStateGroup.title)

    await callback_data.answer()  # Обязательный ответ!


@router.message(CreateNoteStateGroup.title)
async def create_note_title_handler(message: Message, state: FSMContext):
    print(message.text)

    if len(message.text or "") < 10:
        await message.answer("Введите текст длиной более 10 символов", reply_markup=get_cancel_keyboard_markup())
        return

    await message.answer("Принято, спасибо!")
    await state.clear()

# create_note_content

# create_note_submit