from aiogram import Router, F, Bot
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import async_sessionmaker

import keyboards as kb
from database import orm
from states import CreateRequestState
from utils.send_request import send_request

router = Router()


@router.message(Command("create_request"))
async def cmd_create_request(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    user = await orm.get_user(message.from_user.id, sessionmaker)
    await state.set_state(CreateRequestState.description)
    await message.answer(f"Здравствуйте, {user.name}! Опишите Вашу проблему",
                         reply_markup=kb.reply.cancel_create_request())


@router.message(or_f(*CreateRequestState.__states__), F.text.casefold() == "отменить создание заявки")
async def cancel_create_request(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание заявки отменено",
                         reply_markup=ReplyKeyboardRemove())


@router.message(CreateRequestState.description)
async def process_description(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    user = await orm.get_user(message.from_user.id, sessionmaker)
    await state.update_data(description=message.text)
    await state.set_state(CreateRequestState.confirm)
    await message.answer("Хорошо. Давайте сверим данные:\n\n"
                         f"<b>Отправитель:</b> {user.name}\n"
                         f"<b>Кабинет/отделение:</b> {user.department}\n"
                         "<b>Текст заявки:</b>\n"
                         f"{message.text}\n\n"
                         "Всё верно?",
                         reply_markup=kb.reply.yes_no())


@router.message(CreateRequestState.confirm, F.text.casefold() == "да")
async def process_confirm_yes(message: Message, bot: Bot, state: FSMContext, sessionmaker: async_sessionmaker):
    data = await state.get_data()
    await state.clear()
    await orm.add_request(message.from_user.id, data["description"], sessionmaker)
    request = await orm.get_requests(message.from_user.id, sessionmaker)
    await message.answer(f"Ваша заявка создана под номером <b>{request.request_id}</b>",
                         reply_markup=ReplyKeyboardRemove())
    await send_request(bot, message.from_user.id, sessionmaker)


@router.message(CreateRequestState.confirm, F.text.casefold() == "нет")
async def process_confirm_no(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание заявки отменено",
                         reply_markup=ReplyKeyboardRemove())


@router.message(CreateRequestState.confirm)
async def process_confirm(message: Message):
    await message.answer('Извините, я не понял. Для подтверждения или отмены изменений отправьте "да" или "нет"',
                         reply_markup=kb.reply.yes_no())
