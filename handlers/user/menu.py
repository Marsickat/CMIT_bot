from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Список доступных команд:\n\n"
                         "/change_userdata - Изменить Ваши данные\n")
