from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import async_sessionmaker

import keyboards as kb
from callbacks import RequestCallback
from database import orm

router = Router()


@router.message(Command("check_requests"))
async def cmd_check_request(message: Message, sessionmaker: async_sessionmaker):
    requests = await orm.get_active_requests(message.from_user.id, sessionmaker)
    text = ""
    for request in requests:
        text += f"Заявка №{request.request_id}, статус - {request.status}\n"
    if text:
        await message.answer(text,
                             reply_markup=kb.inline.active_requests(requests, False, 0))
    else:
        await message.answer("У вас нет активных заявок")


@router.callback_query(RequestCallback.filter(F.media))
async def send_photo_request(callback: CallbackQuery, callback_data: RequestCallback, sessionmaker: async_sessionmaker):
    request = await orm.get_request(callback_data.id, sessionmaker)
    if request.photo_id:
        await callback.message.answer_photo(request.photo_id,
                                            caption=f"Фотография из заявки №{request.request_id}")
        await callback.answer()
    elif request.video_id:
        await callback.message.answer_video(request.video_id,
                                            caption=f"Видео из заявки №{request.request_id}")
        await callback.answer()
    else:
        await callback.message.answer(f"У заявки №{request.request_id} нет медиафайла")
        await callback.answer()


@router.callback_query(RequestCallback.filter())
async def check_request_cb(callback: CallbackQuery, callback_data: RequestCallback, sessionmaker: async_sessionmaker):
    requests = await orm.get_active_requests(callback.from_user.id, sessionmaker)
    request = await orm.get_request(callback_data.id, sessionmaker)
    user = await orm.get_user(request.user_fk, sessionmaker)
    await callback.message.edit_text(f"<b>Заявка №{request.request_id}</b>\n\n"
                                     f"<b>Отправитель:</b> {user.name}\n"
                                     f"<b>Кабинет/отделение:</b> {user.department}\n"
                                     f"<b>Статус заявки:</b> {request.status}\n"
                                     "<b>Текст заявки:</b>\n"
                                     f"{request.req_description}\n\n",
                                     reply_markup=kb.inline.active_requests(requests, True, callback_data.id))
    await callback.answer(f"Информация о заявке №{request.request_id}")


@router.message(Command("check_request"))
async def cmd_check_request(message: Message, command: CommandObject, sessionmaker: async_sessionmaker):
    user = await orm.get_user(message.from_user.id, sessionmaker)
    requests = await orm.get_requests(message.from_user.id, sessionmaker)
    if command.args:
        for request in requests:
            if request.request_id == int(command.args):
                text = f"<b>Заявка №{request.request_id}</b>\n\n"
                text += f"<b>Отправитель:</b> {user.name}\n"
                text += f"<b>Кабинет/отделение:</b> {user.department}\n"
                text += f"<b>Статус заявки:</b> {request.status}\n"
                text += "<b>Текст заявки:</b>\n"
                text += f"{request.req_description}\n\n"
                if request.photo_id:
                    await message.answer_photo(request.photo_id, caption=text)
                elif request.video_id:
                    await message.answer_video(request.video_id, caption=text)
                else:
                    await message.answer(text,
                                         reply_markup=ReplyKeyboardRemove())
                break
        else:
            await message.answer("К сожалению, заявки с таким номером от Вас нет")
        return
    else:
        await message.answer("Вы не ввели номер заявки. Пример - <code>/check_request 17</code>")
