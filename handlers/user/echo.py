from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("echo"))
async def cmd_echo(message: Message):
    print(message.text)
    await message.answer(message.text)
