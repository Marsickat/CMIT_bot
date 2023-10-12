from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import ColumnElement, Result, ScalarResult

from bot.callbacks.classes import RequestCallback
from database.models import RequestModel


def active_requests(requests: ScalarResult[RequestModel] | list[ColumnElement], media: bool,
                    media_id: int, admin: bool) -> InlineKeyboardMarkup:
    """
    Функция для формирования inline-клавиатуры с активными заявками.

    :param requests: Запросы.
    :type requests: Result[tuple[RequestModel]] | list[ColumnElement]
    :param media: Флаг для добавления inline-кнопки отправки прикрепленного к заявке медиафайла.
    :type media: bool
    :param media_id: Номер заявки.
    :type media_id: int
    :param admin: Флаг для проверки отправителя запроса.
    :type admin: bool

    :return: Inline-клавиатура с заявками и, возможно, кнопкой отправки прикрепленного к заявке медиафайла.
    :rtype: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for request in requests:
        builder.button(text=f"Заявка №{request.request_id}, статус - {request.status}",
                       callback_data=RequestCallback(action="view",
                                                     media=False,
                                                     id=request.request_id,
                                                     admin=admin))
    if media:
        builder.button(text="Отправить прикрепленный к заявке медиафайл",
                       callback_data=RequestCallback(action="view",
                                                     media=True,
                                                     id=media_id,
                                                     admin=admin))
    builder.adjust(1)
    return builder.as_markup()


def take_request(request_id: int) -> InlineKeyboardMarkup:
    """
    Функция для формирования inline-клавиатуры с кнопкой для принятия заявки.

    :param request_id: ID заявки.
    :type request_id: int

    :return: Inline-клавиатура с кнопкой для принятия заявки.
    :rtype: InlineKeyboardMarkup
    """
    keyboard = [
        [InlineKeyboardButton(text="Принять заявку",
                              callback_data=f"request_{request_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
