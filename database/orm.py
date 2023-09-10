from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserModel


async def add_user(user_id: int, username: Optional[str], first_name: Optional[str], last_name: Optional[str],
                   name: str, department: str, session: AsyncSession):
    session.add(UserModel(user_id=user_id,
                          username=username,
                          first_name=first_name,
                          last_name=last_name,
                          name=name,
                          department=department))
    await session.commit()


async def change_userdata(user_id: int, name: str, department: str, session: AsyncSession):
    user = (await session.execute(select(UserModel).filter_by(user_id=user_id))).scalar_one()
    user.name = name
    user.department = department
    await session.commit()
