from aiogram import Bot

from config import config


async def send_message_startup(bot: Bot):
    text = "Бот запущен!\n\n"
    for user in config.admins:
        await bot.send_message(user, text)


async def send_message_shutdown(bot: Bot):
    text = "Бот остановлен\n\n"
    for user in config.admins:
        await bot.send_message(user, text)
