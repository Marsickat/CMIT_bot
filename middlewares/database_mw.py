from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UserModel


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        async with AsyncSession(data["async_engine"]) as session:
            data["session"] = session
            tg_id = data["event_from_user"].id
            user = (await session.execute(select(UserModel).where(UserModel.user_id == tg_id))).scalar_one_or_none()
            data["user"] = user
            return await handler(event, data)
