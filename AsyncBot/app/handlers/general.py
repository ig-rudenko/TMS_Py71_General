from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ..callbacks.general import clear_state
from ..services.users import get_user_by_id, create_user
from ..states.notes import CreateNoteStateGroup
from ..text.welcome import WELCOME_TEXT
from ..keyboards.general import get_general_keyboard_markup

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    from_user = message.from_user

    user_model = await get_user_by_id(from_user.id)
    if user_model is None:
        await create_user(tg_id=from_user.id, username=from_user.username or str(from_user.id))

    await message.answer(WELCOME_TEXT, reply_markup=get_general_keyboard_markup())


@router.callback_query(F.data == clear_state)
async def clear_state_handler(callback_data: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_data.message.answer("Отмена действия")
    await callback_data.answer()
