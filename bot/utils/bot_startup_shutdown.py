from os import getenv

from aiogram import Bot


async def send_message_startup(bot: Bot) -> None:
    """
    Функция, выполняемая при запуске бота.
    Функция присылает текст пользователям при запуске бота.

    :param bot: Объект бота.
    :type bot: Bot

    :return: None
    """
    text = "Бот запущен!\n\n"
    for user in eval(getenv("ADMINS")):
        await bot.send_message(user, text)


async def send_message_shutdown(bot: Bot) -> None:
    """
    Функция, выполняемая при выключении бота.
    Функция присылает текст пользователям при выключении бота.

    :param bot: Объект бота.
    :type bot: Bot

    :return: None
    """
    text = "Бот остановлен\n\n"
    for user in eval(getenv("ADMINS")):
        await bot.send_message(user, text)
