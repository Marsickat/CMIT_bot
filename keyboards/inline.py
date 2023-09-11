from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm.collections import InstrumentedList

from callbacks.classes import RequestCallback


def active_requests(requests: InstrumentedList, media: bool, media_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for request in requests:
        builder.button(text=f"Заявка №{request.request_id}, статус - {request.status}",
                       callback_data=RequestCallback(action="view", media=False, id=request.request_id))
    if media:
        builder.button(text="Отправить прикрепленный к заявке медиафайл",
                       callback_data=RequestCallback(action="view", media=True, id=media_id))
    builder.adjust(1)
    return builder.as_markup()
