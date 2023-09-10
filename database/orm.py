from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models import UserModel, RequestModel


async def add_request(user_id: int, description: str, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        request = RequestModel(description=description)
        user.requests.append(request)
        await session.commit()


async def add_user(user_id: int, username: Optional[str], first_name: Optional[str], last_name: Optional[str],
                   name: str, department: str, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        session.add(UserModel(user_id=user_id,
                              username=username,
                              first_name=first_name,
                              last_name=last_name,
                              name=name,
                              department=department,
                              requests=[RequestModel(description="Тестовый запрос", completion_time=datetime.now())]))
        await session.commit()


async def change_userdata(user_id: int, name: str, department: str, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        user.name = name
        user.department = department
        await session.commit()


async def get_requests(user_id: int, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        return user.requests[-1]


async def get_user(user_id: int, sessionmaker: async_sessionmaker):
    # user = (await session.execute(select(UserModel).filter_by(user_id=user_id))).scalar_one_or_none()
    async with sessionmaker() as session:
        return await session.get(UserModel, user_id)
