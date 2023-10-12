from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import callbacks as cb
from bot import keyboards as kb
from bot.utils import answer_text
from database import orm

router = Router()


@router.message(Command("all_active_requests"))
async def cmd_active_requests(message: Message, sessionmaker: async_sessionmaker):
    """
    Функция для обработки команды /all_active_requests.

    Функция получает активные заявки всех пользователей из базы данных. При наличии заявок формируется текст сообщения
    по каждой заявке, при отсутствии заявок выводится сообщение об их отсутствии. Также при наличии заявок формируется
    inline-клавиатура с кнопками, показывающими информацию о каждой заявке.

    :param message: Объект сообщения.
    :type message: Message
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    requests = await orm.get_all_active_requests(sessionmaker=sessionmaker)
    text = ""
    for request in requests:
        text += f"Заявка №{request.request_id}, статус - {request.status}\n"
    if text:
        await message.answer(text=text,
                             reply_markup=kb.inline.active_requests(requests=requests,
                                                                    is_media=False,
                                                                    is_request=False))
    else:
        await message.answer(text="В данный момент нет активных заявок")


@router.message(Command("my_active_requests"))
async def cmd_my_active_requests(message: Message, sessionmaker: async_sessionmaker):
    """
    Функция для обработки команды /my_active_requests.

    Функция получает активные заявки, которые принял администратор, из базы данных. При наличии заявок формируется текст
    сообщения по каждой заявке, при отсутствии заявок выводится сообщение об их отсутствии. Также при наличии заявок
    формируется inline-клавиатура с кнопками, показывающими информацию о каждой заявке.

    :param message: Объект сообщения.
    :type message: Message
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    requests = await orm.get_admin_active_requests(user_id=message.from_user.id, sessionmaker=sessionmaker)
    text = ""
    for request in requests:
        text += f"Заявка №{request.request_id}, статус - {request.status}\n"
    if text:
        await message.answer(text=text,
                             reply_markup=kb.inline.active_requests(requests=requests,
                                                                    is_media=False,
                                                                    is_request=False))
    else:
        await message.answer(text="В данный момент нет активных заявок")


@router.callback_query(cb.RequestCallback.filter())
async def check_request_cb(callback: CallbackQuery, callback_data: cb.RequestCallback,
                           sessionmaker: async_sessionmaker):
    """
    Функция для обработки callback-запроса при выборе inline-кнопки с заявкой.

    Функция получает активные заявки пользователя из базы данных, чтобы затем отправить их для формирования новой
    клавиатуры. Затем получает выбранную пользователем в inline-клавиатуре заявку из базы данных. Получает данные
    пользователя из базы данных. Формирует текст ответа и редактирует сообщение с новыми данными.

    :param callback: Объект callback-запроса.
    :type callback: CallbackQuery
    :param callback_data: Объект cb.RequestCallback.
    :type callback_data: cb.RequestCallback
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    requests = await orm.get_admin_active_requests(user_id=callback.from_user.id,
                                                   sessionmaker=sessionmaker)
    request = await orm.get_request(request_id=callback_data.id,
                                    sessionmaker=sessionmaker)
    user = await orm.get_user(user_id=request.user_fk,
                              sessionmaker=sessionmaker)
    text = answer_text(request_id=request.request_id,
                       name=user.name,
                       department=user.department,
                       status=request.status,
                       description=request.req_description,
                       is_request_id=True,
                       is_status=True)
    try:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb.inline.active_requests(
                                             requests=requests,
                                             is_media=request.photo_id or request.video_id,
                                             is_request=True,
                                             media_id=callback_data.id,
                                             request_id=request.request_id)
                                         )
    except TelegramBadRequest:
        pass
    finally:
        await callback.answer(text=f"Информация о заявке №{request.request_id}")
