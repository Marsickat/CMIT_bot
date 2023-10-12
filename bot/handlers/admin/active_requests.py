from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import keyboards as kb
from database import orm

router = Router()


@router.message(Command("active_requests"))
async def cmd_active_requests(message: Message, sessionmaker: async_sessionmaker):
    """
    Функция для обработки команды /active_requests.

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
                                                                    media=False,
                                                                    media_id=0,
                                                                    admin=True))
    else:
        await message.answer(text="В данный момент нет активных заявок")
