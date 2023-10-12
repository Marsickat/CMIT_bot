from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker

from database import orm

router = Router()


@router.callback_query(F.data.startswith("complete_"))
async def complete_request(callback: CallbackQuery, sessionmaker: async_sessionmaker):
    """
    Функция для выполнения заявки администратором.

    Функция получает заявку по ее ID. Сравнивает исполнителя заявки и того, кто ее выполнил. В случае совпадения
    устанавливает статус о выполнении заявки, иначе сообщает, что администратор не может выполнить чужую заявку.

    :param callback: Объект callback-запроса.
    :type callback: CallbackQuery
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    request_id = int(callback.data.split("_")[-1])
    request = await orm.get_request(request_id=request_id, sessionmaker=sessionmaker)
    if request.executor == callback.from_user.id:
        await orm.complete_request(request_id=request_id, sessionmaker=sessionmaker)
        await callback.message.answer(f"Заявка №{request_id} выполнена")
    else:
        await callback.message.answer("Нельзя выполнить данную заявку, т.к. это не Ваша заявка")
    await callback.answer()
