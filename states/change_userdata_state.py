from aiogram.fsm.state import StatesGroup, State


class ChangeUserdataState(StatesGroup):
    name = State()
    department = State()
    confirm = State()
