from aiogram.fsm.state import StatesGroup, State


class CreateRequestState(StatesGroup):
    """
    Группа состояний для создания заявки.

    :ivar description: Описание заявки.
    :ivar confirm: Подтверждение изменений.
    """
    description = State()
    confirm = State()
