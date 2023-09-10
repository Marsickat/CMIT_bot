from aiogram.fsm.state import StatesGroup, State


class CreateRequestState(StatesGroup):
    description = State()
    confirm = State()
