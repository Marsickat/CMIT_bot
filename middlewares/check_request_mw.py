from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject


class CheckRequestMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        counter_requests = get_flag(data, "counter")
        if counter_requests:
            if self.counter <= 0:
                data["counter_requests"] = self.counter
                self.counter += 1
            else:
                data["counter_requests"] = self.counter
        else:
            self.counter = 0
        return await handler(event, data)
