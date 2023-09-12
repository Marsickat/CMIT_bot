from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import config
from database import orm
from utils import answer_text


async def send_request(bot: Bot, user_id: int, sessionmaker: async_sessionmaker) -> None:
    """
    Функция для отправки заявки администраторам при ее создании.
    Функция получает данные пользователя из базы данных, формирует текст заявки и отправляет его администраторам.

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
    for admin in config.admins:
        if request.photo_id:
            await bot.send_photo(chat_id=admin,
                                 photo=request.photo_id,
                                 caption=text)
        elif request.video_id:
            await bot.send_video(chat_id=admin,
                                 video=request.video_id,
                                 caption=text)
        else:
            await bot.send_message(chat_id=admin,
                                   text=text)
