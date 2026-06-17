from aiogram.fsm.state import StatesGroup, State


class CreateNoteStateGroup(StatesGroup):
    title = State()
    content = State()
    submit = State()
