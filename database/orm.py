from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserModel


async def add_user(user_id: int, username: Optional[str], first_name: Optional[str], last_name: Optional[str],
                   name: str, department: str, session: AsyncSession):
    async with session.begin():
        session.add(UserModel(user_id=user_id,
                              username=username,
                              first_name=first_name,
                              last_name=last_name,
                              name=name,
                              department=department))


async def get_user(user_id: int, session: AsyncSession):
    return (await session.execute(select(UserModel).where(UserModel.user_id == user_id))).scalar_one_or_none()
