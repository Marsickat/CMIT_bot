from aiogram.fsm.state import StatesGroup, State


class IssueState(StatesGroup):
    issue = State()
