from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm.collections import InstrumentedList

from callbacks.classes import RequestCallback
from utils import RequestStatus


def active_requests(requests: InstrumentedList) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for request in requests:
        if request.status != RequestStatus.completed:
            builder.button(text=f"Заявка №{request.request_id}, статус - {request.status}",
                           callback_data=RequestCallback(action="view", id=request.request_id))
    builder.adjust(1)
    return builder.as_markup()
