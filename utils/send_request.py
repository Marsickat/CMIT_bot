from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import config
from database import orm


async def send_request(bot: Bot, user_id: int, sessionmaker: async_sessionmaker):
    user = await orm.get_user(user_id, sessionmaker)
    for admin in config.admins:
        await bot.send_message(admin,
                               f"Заявка номер {user.requests[-1].request_id}\n\n"
                               f"<b>Отправитель:</b> {user.name}\n"
                               f"<b>Кабинет/отделение:</b> {user.department}\n"
                               "<b>Текст заявки:</b>\n"
                               f"{user.requests[-1].description}")
