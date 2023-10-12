from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import ColumnElement, Result, ScalarResult
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import callbacks as cb
from database.models import RequestModel


def active_requests(requests: ScalarResult[RequestModel] | list[ColumnElement], is_media: bool, is_request: bool,
                    media_id: int = 0, request_id: int = 0) -> InlineKeyboardMarkup:
    """
    Функция для формирования inline-клавиатуры с активными заявками.

    :param requests: Запросы.
    :type requests: Result[tuple[RequestModel]] | list[ColumnElement]
    :param is_media: Флаг для добавления inline-кнопки отправки прикрепленного к заявке медиафайла.
    :type is_media: bool
    :param is_request: Флаг для добавления inline-кнопки выполнения заявки.
    :type is_request: bool
    :param media_id: Номер заявки.
    :type media_id: int
    :param request_id: ID запроса.
    :type request_id: int
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: Inline-клавиатура с заявками и, возможно, кнопкой отправки прикрепленного к заявке медиафайла.
    :rtype: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()
    for request in requests:
        builder.button(text=f"Заявка №{request.request_id}, статус - {request.status}",
                       callback_data=cb.RequestCallback(action="view",
                                                        media=False,
                                                        id=request.request_id))
    if is_media:
        builder.button(text="Отправить прикрепленный к заявке медиафайл",
                       callback_data=cb.RequestCallback(action="view",
                                                        media=True,
                                                        id=media_id))
    if is_request and request_id:
        builder.button(text="Выполнить заявку",
                       callback_data=f"complete_{request_id}")
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
