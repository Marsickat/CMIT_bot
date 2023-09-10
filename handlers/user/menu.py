from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Список доступных команд:\n\n"
                         "/create_request - Создать заявку\n"
                         "/check_requests - Посмотреть активные заявки\n"
                         "/change_userdata - Изменить Ваши данные\n")
