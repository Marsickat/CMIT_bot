from aiogram.fsm.state import StatesGroup, State


class IssueState(StatesGroup):
    """
    Группа состояний для отправки предложения по улучшению функциональности бота.

    :ivar issue: Предложение по улучшению.
    """
    issue = State()
