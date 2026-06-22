import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputRichMessage

from ..callbacks.general import show_notes_callback, create_note_callback, submit_callback
from ..keyboards.general import get_cancel_keyboard_markup, get_go_home_keyboard_markup
from ..keyboards.notes import get_note_create_submit_keyboard_markup
from ..services.notes import create_note, get_last_notes, get_notes_by_id, find_notes
from ..states.notes import CreateNoteStateGroup
from ..text.notes import NOTE_CREATE_TITLE, NOTE_CREATE_CONTENT, NOTE_CREATE_SUBMIT, NOTE_CREATED

router = Router()


@router.message(Command("note"))
async def find_note_handler(message: Message, command: CommandObject):

    # `/note`
    if command.args is None:
        last_notes = await get_last_notes(limit=1)
        if last_notes:
            note = last_notes[0]
            text = f"ID: `{note.id}`\n\nTitle: *{note.title}*\n\n{note.content}"
        else:
            text = "У вас ещё нет заметок"

        await message.answer_rich(InputRichMessage(markdown=text), parse_mode="HTML")

    # `/note 123`
    elif command.args.isdigit():
        note = await get_notes_by_id(int(command.args))
        if note is not None:
            text = f"ID: `{note.id}`\nTitle: *{note.title}*\n\n{note.content}"
        else:
            text = "Такой заметки нет"

        await message.answer_rich(InputRichMessage(markdown=text), parse_mode="HTML")

    # `/note asllksld`
    else:
        notes = await find_notes(search=command.args, limit=10)
        text = ""
        for note in notes:
            text += f"ID: <code>{note.id}</code>\nTitle: <b>{note.title}</b>\n\n"

        if not text.strip():
            text = "У вас ещё нет заметок"

        await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == show_notes_callback)
async def notes_list_callback_handler(callback_data: CallbackQuery):
    """Отображение списка заметок"""
    last_notes = await get_last_notes()

    text = ""
    for note in last_notes:
        text += f"ID: <code>{note.id}</code>\nTitle: <b>{note.title}</b>\n\n"

    if not text.strip():
        text = "У вас ещё нет заметок"

    await callback_data.message.edit_text(text, parse_mode="HTML", reply_markup=get_go_home_keyboard_markup())
    await callback_data.answer()


@router.callback_query(F.data == create_note_callback)
async def create_note_callback_handler(callback_data: CallbackQuery, state: FSMContext):
    """Начало создания заметки"""

    await state.set_state(CreateNoteStateGroup.title)

    msg = await callback_data.message.answer(NOTE_CREATE_TITLE, reply_markup=get_cancel_keyboard_markup())

    await state.set_data({"start_msg_id": msg.message_id})

    await callback_data.answer()  # Обязательный ответ!


@router.message(CreateNoteStateGroup.title)
async def create_note_title_handler(message: Message, state: FSMContext, bot: Bot):
    """Обработка создания заголовка для заметки"""

    state_data = await state.get_data()
    start_msg_id = state_data["start_msg_id"]

    await message.delete()  # Удаляем сообщение пользователя.

    msg_length = len(message.text or "")

    if 3 > msg_length or msg_length > 64:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=start_msg_id,
            text=NOTE_CREATE_TITLE + "\n\n" + "❗️ Введите текст длиной от 3 до 64 символов❗️",
        )
        return

    state_data["title"] = message.text
    await state.set_state(CreateNoteStateGroup.content)
    await state.set_data(state_data)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=start_msg_id, text=NOTE_CREATE_CONTENT)


@router.message(CreateNoteStateGroup.content)
async def create_note_content_handler(message: Message, state: FSMContext, bot: Bot):
    """Обработка создания содержимого заметки"""

    state_data = await state.get_data()
    start_msg_id = state_data["start_msg_id"]

    await message.delete()  # Удаляем сообщение пользователя.

    msg_length = len(message.text or "")

    if 10 > msg_length:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=start_msg_id,
            text=NOTE_CREATE_CONTENT + "\n\n" + "❗️ Введите текст более 10 символов❗️",
        )
        return

    state_data["content"] = message.text
    await state.set_state(CreateNoteStateGroup.submit)
    await state.set_data(state_data)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=start_msg_id,
        text=NOTE_CREATE_SUBMIT.format(
            title=state_data["title"],
            short_content=state_data["content"][:10] + "...",
        ),
        parse_mode="HTML",
        reply_markup=get_note_create_submit_keyboard_markup(),
    )


@router.callback_query(F.data == submit_callback, CreateNoteStateGroup.submit)
async def create_note_submit_success(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Успешное подтверждение создания заметки"""

    state_data = await state.get_data()
    start_msg_id = state_data["start_msg_id"]

    note = await create_note(
        tg_id=callback.from_user.id, title=state_data["title"], content=state_data["content"]
    )

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=start_msg_id,
        text=NOTE_CREATED.format(
            id=note.id,
            title=state_data["title"],
            short_content=state_data["content"][:10] + "...",
        ),
        parse_mode="HTML",
    )

    await state.clear()
    await callback.answer()

    await asyncio.sleep(5)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=start_msg_id)
