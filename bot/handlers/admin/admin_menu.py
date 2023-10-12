from aiogram import Router
from aiogram.filters import Command, or_f
from aiogram.types import Message

router = Router()


@router.message(or_f(Command("admin_menu"), Command("am")))
async def cmd_admin_menu(message: Message):
    """
    Функция для обработки команды /admin_menu и /am.

    Функция отправляет сообщение со списком доступных команд.

    :param message: Объект сообщения.
    :type message: Message
    """
    await message.answer(text="Список доступных команд:\n\n"
                              "/all_active_requests - Посмотреть все активные заявки\n"
                              "/my_active_requests - Посмотреть мои активные заявки")
