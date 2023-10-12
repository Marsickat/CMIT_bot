from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import callbacks as cb
from bot import keyboards as kb
from bot.utils import answer_text
from database import orm

router = Router()


@router.message(Command("check_requests"))
async def cmd_check_request(message: Message, sessionmaker: async_sessionmaker):
    """
    Функция для обработки команды /check_requests.

    Функция получает активные заявки всех пользователей из базы данных. При наличии заявок формируется текст сообщения
    по каждой заявке, при отсутствии заявок выводится сообщение об их отсутствии. Также при наличии заявок формируется
    inline-клавиатура с кнопками, показывающими информацию о каждой заявке.

    :param message: Объект сообщения.
    :type message: Message
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    requests = await orm.get_active_requests(user_id=message.from_user.id,
                                             sessionmaker=sessionmaker)
    text = ""
    for request in requests:
        text += f"Заявка №{request.request_id}, статус - {request.status}\n"
    if text:
        await message.answer(text=text,
                             reply_markup=kb.inline.active_requests(requests=requests,
                                                                    media=False,
                                                                    media_id=0,
                                                                    admin=False))
    else:
        await message.answer(text="У вас нет активных заявок")


@router.callback_query(cb.RequestCallback.filter(F.media))
async def send_request(callback: CallbackQuery, callback_data: cb.RequestCallback, sessionmaker: async_sessionmaker):
    """
    Функция для обработки callback-запроса inline-кнопки "Отправить прикрепленный к заявке медиафайл".

    Функция принимает в callback_data id заявки и с помощью нее получает выбранную пользователем заявку из базы данных.
    В зависимости от наличия media в заявке отправляет сообщение пользователю с информацией о заявке.

    :param callback: Объект callback-запроса.
    :type callback: CallbackQuery
    :param callback_data: Объект RequestCallback.
    :type callback_data: cb.RequestCallback
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    request = await orm.get_request(request_id=callback_data.id,
                                    sessionmaker=sessionmaker)
    if request.photo_id:
        await callback.message.answer_photo(photo=str(request.photo_id),
                                            caption=f"Фотография из заявки №{request.request_id}")
    elif request.video_id:
        await callback.message.answer_video(video=str(request.video_id),
                                            caption=f"Видео из заявки №{request.request_id}")
    else:
        await callback.message.answer(text=f"У заявки №{request.request_id} нет медиафайла")
    await callback.answer()


@router.callback_query(cb.RequestCallback.filter())
async def check_request_cb(callback: CallbackQuery, callback_data: cb.RequestCallback,
                           sessionmaker: async_sessionmaker):
    """
    Функция для обработки callback-запроса при выборе inline-кнопки с заявкой.

    Функция получает активные заявки пользователя из базы данных, чтобы затем отправить их для формирования новой
    клавиатуры. Затем получает выбранную пользователем в inline-клавиатуре заявку из базы данных. Получает данные
    пользователя из базы данных. Формирует текст ответа и редактирует сообщение с новыми данными.

    :param callback: Объект callback-запроса.
    :type callback: CallbackQuery
    :param callback_data: Объект RequestCallback.
    :type callback_data: cb.RequestCallback
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    if callback_data.admin:
        requests = await orm.get_all_active_requests(sessionmaker=sessionmaker)
    else:
        requests = await orm.get_active_requests(user_id=callback.from_user.id,
                                                 sessionmaker=sessionmaker)
    request = await orm.get_request(request_id=callback_data.id,
                                    sessionmaker=sessionmaker)
    user = await orm.get_user(user_id=request.user_fk,
                              sessionmaker=sessionmaker)
    text = answer_text(request_id=request.request_id,
                       name=user.name,
                       department=user.department,
                       status=request.status,
                       description=request.req_description,
                       is_request_id=True,
                       is_status=True)
    try:
        await callback.message.edit_text(text=text,
                                         reply_markup=kb.inline.active_requests(
                                             requests=requests,
                                             media=request.photo_id or request.video_id,
                                             media_id=callback_data.id,
                                             admin=callback_data.admin)
                                         )
    except TelegramBadRequest:
        pass
    finally:
        await callback.answer(text=f"Информация о заявке №{request.request_id}")


@router.message(Command("check_request"))
async def cmd_check_request(message: Message, command: CommandObject, sessionmaker: async_sessionmaker):
    """
    Функция для команды /check_request.

    Функция получает данные пользователя и список его запросов из базы данных. Если пользователь передал номер заявки,
    то функция проверяет наличие заявки с таким номером из списка заявок пользователя. Если заявка с таким номером есть,
    то функция формирует текст ответа с информацией о заявке и отправляет его, если заявки с таким номером нет, то
    пользователю отправляется сообщение с информацией, что такой заявки у пользователя нет. В случае, если пользователь
    вместе с командой не передал номер заявки, то ему отправляется сообщение, что нужно отправить номер заявки.

    :param message: Объект сообщения.
    :type message: Message
    :param command: Объект команды.
    :type command: CommandObject
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    user = await orm.get_user(user_id=message.from_user.id,
                              sessionmaker=sessionmaker)
    requests = await orm.get_requests(user_id=message.from_user.id,
                                      sessionmaker=sessionmaker)
    if command.args:
        for request in requests:
            if request.request_id == int(command.args):
                text = answer_text(request_id=request.request_id,
                                   name=user.name,
                                   department=user.department,
                                   status=request.status,
                                   description=request.req_description,
                                   is_request_id=True,
                                   is_status=True)
                if request.photo_id:
                    await message.answer_photo(photo=request.photo_id,
                                               caption=text)
                elif request.video_id:
                    await message.answer_video(video=request.video_id,
                                               caption=text)
                else:
                    await message.answer(text=text,
                                         reply_markup=ReplyKeyboardRemove())
                break
        else:
            await message.answer(text="К сожалению, заявки с таким номером от Вас нет")
        return
    else:
        await message.answer(text="Вы не ввели номер заявки. Пример - <code>/check_request 17</code>")
