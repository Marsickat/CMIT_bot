from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models import UserModel, RequestModel
from utils import RequestStatus


async def add_request(user_id: int, req_description: str, photo_id: Optional[str], video_id: Optional[str],
                      sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        request = RequestModel(req_description=req_description,
                               photo_id=photo_id,
                               video_id=video_id,
                               status=RequestStatus.in_queue)
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
                              requests=[RequestModel(req_description="Тестовый запрос",
                                                     status=RequestStatus.completed,
                                                     completion_time=datetime.now())]))
        await session.commit()


async def change_userdata(user_id: int, name: str, department: str, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        user.name = name
        user.department = department
        await session.commit()


async def get_active_requests(user_id: int, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
    requests = []
    for request in user.requests:
        if request.status != RequestStatus.completed:
            requests.append(request)
    return requests


async def get_request(request_id: int, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        return await session.get(RequestModel, request_id)


async def get_requests(user_id: int, sessionmaker: async_sessionmaker):
    async with sessionmaker() as session:
        user = await session.get(UserModel, user_id)
        return user.requests


async def get_user(user_id: int, sessionmaker: async_sessionmaker):
    # user = (await session.execute(select(UserModel).filter_by(user_id=user_id))).scalar_one_or_none()
    async with sessionmaker() as session:
        return await session.get(UserModel, user_id)
