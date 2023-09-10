from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="menu", description="Отправляет список доступных команд"),
        BotCommand(command="change_userdata", description="Изменить Ваши данные"),
        BotCommand(command="echo", description="Отправляет вам ваше же сообщение"),
        BotCommand(command="dice", description="Кидает кубик"),
        BotCommand(command="basketball", description="Бросает мяч"),
        BotCommand(command="bowling", description="Бросает шар"),
        BotCommand(command="football", description="Пинает мяч")
    ])
