from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="menu", description="Отправить список доступных команд"),
        BotCommand(command="create_request", description="Создать заявку"),
        BotCommand(command="check_requests", description="Посмотреть активные заявки"),
        BotCommand(command="change_userdata", description="Изменить Ваши данные"),
        # BotCommand(command="echo", description="Ответить Вашим же сообщение"),
        # BotCommand(command="dice", description="Кинуть кубик"),
        # BotCommand(command="basketball", description="Бросить мяч"),
        # BotCommand(command="bowling", description="Бросить шар"),
        # BotCommand(command="football", description="Пнуть мяч")
    ])
