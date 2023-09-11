from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from config import config
from database import orm
from states import IssueState

router = Router()


@router.message(Command("issue"))
async def cmd_issue(message: Message, state: FSMContext):
    await state.set_state(IssueState.issue)
    await message.answer("Замечательно, мы всегда приветствуем предложения по улучшению функциональности. "
                         "Что Вы бы хотели предложить?")


@router.message(IssueState.issue)
async def process_issue(message: Message, bot: Bot, state: FSMContext, sessionmaker: async_sessionmaker):
    user = await orm.get_user(message.from_user.id, sessionmaker)
    text = f"Предложение от {user.name} из {user.department}\n\n{message.text}"
    await state.clear()
    await bot.send_message(config.main_admin, text)
    await message.answer("Ваше предложение по улучшению было отправлено")
