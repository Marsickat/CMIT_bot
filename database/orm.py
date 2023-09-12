from datetime import datetime
from typing import Optional

from sqlalchemy import select, ColumnElement, Result
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm.collections import InstrumentedList

from database.models import UserModel, RequestModel
from utils import RequestStatus


async def add_request(user_id: int, req_description: str, photo_id: Optional[str], video_id: Optional[str],
                      sessionmaker: async_sessionmaker) -> None:
    """
    Функция для добавления заявки в базу данных.

    :param user_id: Уникальный ID пользователя в Telegram.
    :type user_id: int
    :param req_description: Описание заявки пользователя.
    :type req_description: str
    :param photo_id: ID фотографии, прикрепленной к заявке (при ее наличии).
    :type photo_id: Optional[str]
    :param video_id: ID видео, прикрепленного к заявке (при его наличии).
    :type video_id: Optional[str]
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: None
    """
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        request = RequestModel(req_description=req_description,
                               photo_id=photo_id,
                               video_id=video_id,
                               status=RequestStatus.in_queue)
        user.requests.append(request)
        await session.commit()


async def add_request_executor(user_id: int, request_id: int, sessionmaker: async_sessionmaker) -> None:
    """
    Функция для добавления исполнителя для заявки в базу данных.

    :param user_id: Уникальный ID пользователя в Telegram.
    :type user_id: int
    :param request_id: ID заявки пользователя.
    :type request_id: int
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: None
    """
    async with sessionmaker() as session:
        request = await session.get(RequestModel, request_id)
        request.executor = user_id
        await session.commit()


async def add_user(user_id: int, username: Optional[str], first_name: Optional[str], last_name: Optional[str],
                   name: str, department: str, sessionmaker: async_sessionmaker) -> None:
    """
    Функция для добавления пользователя в базу данных.

    :param user_id: Уникальный ID пользователя в Telegram.
    :type user_id: int
    :param username: Username пользователя в Telegram.
    :type username: Optional[str]
    :param first_name: Имя пользователя в Telegram.
    :type first_name: Optional[str]
    :param last_name: Фамилия пользователя в Telegram.
    :type last_name: Optional[str]
    :param name: Имя, указанное пользователем при регистрации в базе данных.
    :type name: str
    :param department: Отделение, указанное пользователем при регистрации в базе данных.
    :type department: str
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: None
    """
    async with sessionmaker() as session:
        session.add(UserModel(user_id=user_id,
                              username=username,
                              first_name=first_name,
                              last_name=last_name,
                              name=name,
                              department=department,
                              requests=[RequestModel(req_description="Тестовый запрос",
                                                     status=RequestStatus.completed,
                                                     completion_time=datetime.now())]))
        await session.commit()


async def change_userdata(user_id: int, name: str, department: str, sessionmaker: async_sessionmaker) -> None:
    """
    Функция для добавления пользователя в базу данных.

    :param user_id: Уникальный ID пользователя в Telegram.
    :type user_id: int
    :param name: Имя, указанное пользователем при регистрации в базе данных.
    :type name: str
    :param department: Отделение, указанное пользователем при регистрации в базе данных.
    :type department: str
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: None
    """
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        user.name = name
        user.department = department
        await session.commit()


async def get_active_requests(user_id: int, sessionmaker: async_sessionmaker) -> list[ColumnElement]:
    """
    Функция для получения активных заявок пользователя из базы данных.

    :param user_id: Уникальный ID пользователя в Telegram.
    :type user_id: int
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: Список активных заявок пользователя.
    :rtype: list[ColumnElement]
    """
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
    requests = []
    for request in user.requests:
        if request.status != RequestStatus.completed:
            requests.append(request)
    return requests


async def get_all_active_requests(sessionmaker: async_sessionmaker) -> Result[tuple[RequestModel]]:
    """
    Функция для получения всех активных заявок пользователей из базы данных.

    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: Список активных заявок пользователя.
    :rtype: Result[tuple[RequestModel]]
    """
    async with sessionmaker() as session:
        return await session.execute(select(RequestModel).where(RequestModel.status != RequestStatus.completed))


async def get_request(request_id: int, sessionmaker: async_sessionmaker) -> Optional[RequestModel]:
    """
    Функция для получения конкретной заявки пользователей из базы данных.

    :param request_id: Уникальный ID заявки пользователя.
    :type request_id: int
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: Список активных заявок пользователя.
    :rtype: Optional[RequestModel]
    """
    async with sessionmaker() as session:
        return await session.get(RequestModel, request_id)


async def get_requests(user_id: int, sessionmaker: async_sessionmaker) -> InstrumentedList:
    """
    Функция для получения всех активных заявок пользователя из базы данных.

    :param user_id: Уникальный ID пользователя Telegram.
    :type user_id: int
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: Список активных заявок пользователя.
    :rtype: Optional[RequestModel]
    """
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        return user.requests


async def get_user(user_id: int, sessionmaker: async_sessionmaker) -> Optional[UserModel]:
    """
    Функция для получения пользователя из базы данных.

    :param user_id: Уникальный ID пользователя Telegram.
    :type user_id: int
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker

    :return: Список активных заявок пользователя.
    :rtype: Optional[RequestModel]
    """
    # user = (await session.execute(select(UserModel).filter_by(user_id=user_id))).scalar_one_or_none()
    async with sessionmaker() as session:
        return await session.get(UserModel, user_id)
