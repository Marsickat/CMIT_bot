from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink
from sqlalchemy.ext.asyncio import async_sessionmaker

from database import orm

router = Router()


@router.callback_query(F.data.startswith("request_"))
async def cmd_active_requests(callback: CallbackQuery, sessionmaker: async_sessionmaker):
    """
    Функция для обработки запроса принятия заявки.

    Функция достает ID запроса из callback-данных, получает заявку пользователя по ID запроса из базы данных. Если
    исполнитель еще не назначен, назначает исполнителем того, кто нажал кнопку, иначе отправляет сообщение с информацией
    о том, кто выполняет заявку, с предложением написать исполнителю (если у исполнителя есть username в Telegram).

    :param callback: Объект callback-запроса.
    :type callback: CallbackQuery
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    request_id = int(callback.data.split("_")[1])
    request = await orm.get_request(request_id=request_id,
                                    sessionmaker=sessionmaker)
    if request.executor is None:
        await orm.add_request_executor(user_id=callback.from_user.id,
                                       request_id=request_id,
                                       sessionmaker=sessionmaker)
        await callback.message.answer(text="Вы приняли данную заявку")
        await callback.answer()
    else:
        user = await orm.get_user(user_id=int(request.executor),
                                  sessionmaker=sessionmaker)
        user_link = hlink(user.name, f'https://t.me/{user.username}') if user.username else user.name
        await callback.message.answer(text=f"Данную задачу в данный момент выполняет {user_link}")
        await callback.answer()
