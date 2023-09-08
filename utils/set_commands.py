from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="echo", description="Отправляет вам ваше же сообщение"),
        BotCommand(command="dice", description="Кидает кубик"),
        BotCommand(command="basketball", description="Бросает мяч"),
        BotCommand(command="bowling", description="Бросает шар"),
        BotCommand(command="football", description="Пинает мяч")
    ])
