from os import getenv

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.states import IssueState
from database import orm

router = Router()


@router.message(Command("issue"))
async def cmd_issue(message: Message, state: FSMContext):
    """
    Функция для обработки команды /issue.

    Функция устанавливает состояние IssueState в issue и отправляет сообщение с предложением оставить предложение по
    улучшению функциональности бота.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    await state.set_state(state=IssueState.issue)
    await message.answer(text="Замечательно, мы всегда приветствуем предложения по улучшению функциональности. "
                              "Что Вы бы хотели предложить?")


@router.message(IssueState.issue)
async def process_issue(message: Message, bot: Bot, state: FSMContext, sessionmaker: async_sessionmaker):
    """
    Функция для обработки состояния issue из IssueState.

    Функция получает данные пользователя из базы данных для формирования текста сообщения, формирует сам текст и
    отправляет его главному администратору, оповещая об этом пользователя.

    :param message: Объект сообщения.
    :type message: Message
    :param bot: Объект бота.
    :type bot: Bot
    :param state: Состояние с данными.
    :type state: FSMContext
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    user = await orm.get_user(user_id=message.from_user.id,
                              sessionmaker=sessionmaker)
    text = f"Предложение от {user.name} из {user.department}\n\n{message.text}"
    await state.clear()
    await bot.send_message(chat_id=int(getenv("MAIN_ADMIN")),
                           text=text)
    await message.answer(text="Ваше предложение по улучшению было отправлено")
