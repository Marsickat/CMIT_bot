from aiogram.filters.callback_data import CallbackData


class RequestCallback(CallbackData, prefix="reqfab"):
    """
    Callback класс для работы с заявкой пользователя.

    :ivar action: Действие с заявкой.
    :ivar media: Флаг на наличие медиа в заявке.
    :ivar id: ID заявки.
    """
    action: str
    media: bool
    id: int
