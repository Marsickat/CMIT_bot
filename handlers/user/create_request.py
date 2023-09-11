from aiogram import Router, F, Bot
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import async_sessionmaker

import keyboards as kb
from database import orm
from states import CreateRequestState
from utils import answer_text
from utils import send_request

router = Router()


@router.message(Command("create_request"))
async def cmd_create_request(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    user = await orm.get_user(message.from_user.id, sessionmaker)
    await state.set_state(CreateRequestState.description)
    await message.answer(f"Здравствуйте, {user.name}! Опишите Вашу проблему. "
                         "Вы также можете прислать фотографию или видео с подписью проблемы.",
                         reply_markup=kb.reply.cancel_create_request())


@router.message(or_f(*CreateRequestState.__states__), F.text.casefold() == "отменить создание заявки")
async def cancel_create_request(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание заявки отменено",
                         reply_markup=ReplyKeyboardRemove())


@router.message(CreateRequestState.description)
async def process_description(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    user = await orm.get_user(message.from_user.id, sessionmaker)
    text = "Хорошо. Давайте сверим данные:\n\n"
    # text += f"<b>Отправитель:</b> {user.name}\n"
    # text += f"<b>Кабинет/отделение:</b> {user.department}\n"
    # text += "<b>Текст заявки:</b>\n"
    if message.photo:
        description = message.caption
        photo_id = message.photo[-1].file_id
        text += answer_text(user.name, user.department, message.caption)
        # text += f"{message.caption}\n\n"
        text += "\n\nВсё верно?"
        await state.update_data(description=description, photo_id=photo_id, video_id=None)
        await message.answer_photo(message.photo[-1].file_id,
                                   caption=text,
                                   reply_markup=kb.reply.yes_no())
    elif message.video:
        description = message.caption
        video_id = message.video.file_id
        text += answer_text(user.name, user.department, message.caption)
        # text += f"{message.caption}\n\n"
        text += "\n\nВсё верно?"
        await state.update_data(description=description, photo_id=None, video_id=video_id)
        await message.answer_video(message.video.file_id,
                                   caption=text,
                                   reply_markup=kb.reply.yes_no())
    else:
        await state.update_data(description=message.text, photo_id=None, video_id=None)
        text += answer_text(user.name, user.department, message.text)
        # text += f"{message.text}\n\n"
        text += "\n\nВсё верно?"
        await message.answer(text,
                             reply_markup=kb.reply.yes_no())
    await state.set_state(CreateRequestState.confirm)


@router.message(CreateRequestState.confirm, F.text.casefold() == "да")
async def process_confirm_yes(message: Message, bot: Bot, state: FSMContext, sessionmaker: async_sessionmaker):
    data = await state.get_data()
    await state.clear()
    await orm.add_request(message.from_user.id, data["description"], data["photo_id"], data["video_id"], sessionmaker)
    requests = await orm.get_active_requests(message.from_user.id, sessionmaker)
    await message.answer(f"Ваша заявка создана под номером <b>{requests[-1].request_id}</b>",
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
