from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

import keyboards as kb
from database import orm
from states.register_state import RegisterState

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    user = await orm.get_user(message.from_user.id, session)
    if user is None:
        await state.set_state(RegisterState.name)
        await message.answer("Здравствуйте, Вас приветствует бот для принятия заявок в ЦМИТ.\n\n"
                             "Похоже, вы открыли бота впервые."
                             "Для принятия заявок мне нужна некоторая информация о Вас.\n"
                             "Как к Вам обращаться?",
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Добро пожаловать, {user.name}!",
                             reply_markup=ReplyKeyboardRemove())


@router.message(RegisterState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegisterState.department)
    await message.answer("Хорошо. Из какого Вы кабинета/отделения?",
                         reply_markup=ReplyKeyboardRemove())


@router.message(RegisterState.department)
async def process_department(message: Message, state: FSMContext):
    await state.update_data(department=message.text)
    data = await state.get_data()
    await state.set_state(RegisterState.confirm)
    await message.answer("Отлично! Давайте проверим информацию.\n\n"
                         f"Ваше имя: {data['name']}\n"
                         f"Ваше подразделение: {message.text}\n\n"
                         "Всё верно?",
                         reply_markup=kb.reply.yes_no())


@router.message(RegisterState.confirm, F.text.casefold() == "да")
async def process_confirm_yes(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await state.clear()
    await orm.add_user(message.from_user.id,
                       message.from_user.username,
                       message.from_user.first_name,
                       message.from_user.last_name,
                       data["name"],
                       data["department"],
                       session)
    await message.answer("Спасибо! Я запомнил.",
                         reply_markup=ReplyKeyboardRemove())


@router.message(RegisterState.confirm, F.text.casefold() == "нет")
async def process_confirm_no(message: Message, state: FSMContext):
    await state.set_state(RegisterState.name)
    await message.answer("Ничего страшного, начнем заново\n\n"
                         "Как к Вам обращаться?",
                         reply_markup=ReplyKeyboardRemove())
