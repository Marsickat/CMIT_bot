from os import getenv

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import keyboards as kb
from bot.utils import answer_text
from database import orm


async def send_request(bot: Bot, user_id: int, sessionmaker: async_sessionmaker) -> None:
    """
    Функция для отправки заявки администраторам при ее создании.
    Функция получает данные пользователя из базы данных, формирует текст заявки и отправляет его администраторам,
    прикрепляя inline-кнопку для принятия заявки.

    :param bot: Объект бота.
    :type bot: Bot
    :param user_id: ID пользователя, создавшего заявку.
    :type user_id: int
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: None
    """
    user = await orm.get_user(user_id=user_id,
                              sessionmaker=sessionmaker)
    request = user.requests[-1]
    text = answer_text(request_id=request.request_id,
                       name=user.name,
                       department=user.department,
                       status=None,
                       description=request.req_description,
                       is_request_id=True,
                       is_status=False)
    for admin in eval(getenv("ADMINS")):
        if request.photo_id:
            await bot.send_photo(chat_id=admin,
                                 photo=request.photo_id,
                                 caption=text,
                                 reply_markup=kb.inline.take_request(request_id=request.request_id))
        elif request.video_id:
            await bot.send_video(chat_id=admin,
                                 video=request.video_id,
                                 caption=text,
                                 reply_markup=kb.inline.take_request(request_id=request.request_id))
        else:
            await bot.send_message(chat_id=admin,
                                   text=text,
                                   reply_markup=kb.inline.take_request(request_id=request.request_id))
