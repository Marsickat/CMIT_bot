from aiogram import Router
from aiogram.enums import DiceEmoji
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("dice"))
async def cmd_dice(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)


@router.message(Command("basketball"))
async def cmd_basketball(message: Message):
    await message.answer_dice(emoji=DiceEmoji.BASKETBALL)


@router.message(Command("bowling"))
async def cmd_basketball(message: Message):
    await message.answer_dice(emoji=DiceEmoji.BOWLING)


@router.message(Command("football"))
async def cmd_basketball(message: Message):
    await message.answer_dice(emoji=DiceEmoji.FOOTBALL)
