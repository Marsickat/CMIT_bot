from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    """
    Группа состояний для регистрации пользователя.

    :ivar name: Имя пользователя.
    :ivar department: Подразделение пользователя.
    :ivar confirm: Подтверждение изменений.
    """
    name = State()
    department = State()
    confirm = State()
