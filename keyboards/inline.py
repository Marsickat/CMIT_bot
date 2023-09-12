from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import ColumnElement, Result

from callbacks.classes import RequestCallback
from database.models import RequestModel


def active_requests(requests: Result[tuple[RequestModel]] | list[ColumnElement], media: bool,
                    media_id: int) -> InlineKeyboardMarkup:
    """
    Функция для формирования inline-клавиатуры с активными заявками.

    :param requests: Запросы.
    :type requests: Result[tuple[RequestModel]] | list[ColumnElement]
    :param media: Флаг для добавления inline-кнопки отправки прикрепленного к заявке медиафайла.
    :type media: bool
    :param media_id: Номер заявки
    :type media_id: int

    :return: Inline-клавиатура с заявками и, возможно, кнопкой отправки прикрепленного к заявке медиафайла.
    :rtype: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for request in requests:
        builder.button(text=f"Заявка №{request.request_id}, статус - {request.status}",
                       callback_data=RequestCallback(action="view",
                                                     media=False,
                                                     id=request.request_id))
    if media:
        builder.button(text="Отправить прикрепленный к заявке медиафайл",
                       callback_data=RequestCallback(action="view",
                                                     media=True,
                                                     id=media_id))
    builder.adjust(1)
    return builder.as_markup()
