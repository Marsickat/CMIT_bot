from os import getenv

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_commands(bot: Bot) -> None:
    """
    Функция для установки команд для бота.

    :param bot: Объект бота.
    :type bot: Bot

    :return: None
    """
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="menu", description="Отправить список доступных команд"),
        BotCommand(command="create_request", description="Создать заявку"),
        BotCommand(command="check_requests", description="Посмотреть активные заявки"),
        BotCommand(command="change_userdata", description="Изменить свои данные"),
        BotCommand(command="issue", description="Отправить пожелание по улучшению"),
        # BotCommand(command="echo", description="Ответить Вашим же сообщение"),
        # BotCommand(command="dice", description="Кинуть кубик"),
        # BotCommand(command="basketball", description="Бросить мяч"),
        # BotCommand(command="bowling", description="Бросить шар"),
        # BotCommand(command="football", description="Пнуть мяч")
    ])
    for admin in eval(getenv("ADMINS")):
        await bot.set_my_commands([
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="menu", description="Отправить список доступных команд"),
            BotCommand(command="admin_menu", description="(/am) Команды администратора"),
            BotCommand(command="all_active_requests", description="Отправить список всех текущих заявок"),
            BotCommand(command="my_active_requests", description="Отправить список своих текущих заявок"),
            BotCommand(command="create_request", description="Создать заявку"),
            BotCommand(command="check_requests", description="Посмотреть активные заявки"),
            BotCommand(command="change_userdata", description="Изменить свои данные"),
            BotCommand(command="issue", description="Отправить пожелание по улучшению"),
            # BotCommand(command="echo", description="Ответить Вашим же сообщение"),
            # BotCommand(command="dice", description="Кинуть кубик"),
            # BotCommand(command="basketball", description="Бросить мяч"),
            # BotCommand(command="bowling", description="Бросить шар"),
            # BotCommand(command="football", description="Пнуть мяч")
        ], scope=BotCommandScopeChat(chat_id=admin))
