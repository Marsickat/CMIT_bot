from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import async_sessionmaker

import keyboards.inline
from callbacks import RequestCallback
from database import orm
from utils import RequestStatus

router = Router()


@router.message(Command("check_requests"))
async def cmd_check_request(message: Message, sessionmaker: async_sessionmaker):
    requests = await orm.get_requests(message.from_user.id, sessionmaker)
    text = ""
    for request in requests:
        if request.status != RequestStatus.completed:
            text += f"Заявка №{request.request_id}, статус - {request.status}\n"
    await message.answer(text,
                         reply_markup=keyboards.inline.active_requests(requests))


@router.callback_query(RequestCallback.filter(), flags={"counter": True})
async def check_request_cb(callback: CallbackQuery, callback_data: RequestCallback, sessionmaker: async_sessionmaker):
    request = await orm.get_request(callback_data.id, sessionmaker)
    user = await orm.get_user(request.user_fk, sessionmaker)
    await callback.message.answer(f"<b>Заявка №{request.request_id}</b>\n\n"
                                  f"<b>Отправитель:</b> {user.name}\n"
                                  f"<b>Кабинет/отделение:</b> {user.department}\n"
                                  f"<b>Статус заявки:</b> {request.status}\n"
                                  "<b>Текст заявки:</b>\n"
                                  f"{request.description}\n\n",
                                  reply_markup=ReplyKeyboardRemove())
    await callback.answer(f"Информация о заявке №{request.request_id}")
