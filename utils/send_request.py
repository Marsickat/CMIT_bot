from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import config
from database import orm


async def send_request(bot: Bot, user_id: int, sessionmaker: async_sessionmaker):
    user = await orm.get_user(user_id, sessionmaker)
    request = user.requests[-1]
    text = f"Заявка номер {request.request_id}\n\n"
    text += f"<b>Отправитель:</b> {user.name}\n"
    text += f"<b>Кабинет/отделение:</b> {user.department}\n"
    text += "<b>Текст заявки:</b>\n"
    text += f"{request.req_description}"
    for admin in config.admins:
        if request.photo_id:
            await bot.send_photo(admin, request.photo_id, caption=text)
        else:
            await bot.send_message(admin, text)
