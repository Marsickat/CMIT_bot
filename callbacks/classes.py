from aiogram.filters.callback_data import CallbackData


class RequestCallback(CallbackData, prefix="reqfab"):
    action: str
    media: bool
    id: int
