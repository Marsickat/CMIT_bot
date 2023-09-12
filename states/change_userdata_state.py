from aiogram.fsm.state import StatesGroup, State


class ChangeUserdataState(StatesGroup):
    """
    Группа состояний для изменения данных пользователя.

    :ivar name: Имя пользователя.
    :ivar department: Подразделение пользователя.
    :ivar confirm: Подтверждение изменений.
    """
    name = State()
    department = State()
    confirm = State()
