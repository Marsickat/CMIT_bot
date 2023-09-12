from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject


class CheckRequestMiddleware(BaseMiddleware):
    """
    Middleware класс, предназначения пока нет.

    :ivar counter: Счетчик.
    """

    def __init__(self) -> None:
        """
        Инициализирует новый экземпляр класса.
        Устанавливает счетчик запросов в начальное значение 0.
        """
        self.counter = 0

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        """
        Вызывается при обработке запроса. Увеличивает счетчик запросов при наличии флага "counter" в данных запроса.

        :param handler: Обработчик запроса.
        :type handler: Callable[[TelegramObject, Dict[str, Any]]
        :param event: Объект запроса.
        :type event: TelegramObject
        :param data: Данные запроса.
        :type data: Dict[str, Any]

        :return: Результат обработки запроса.
        :rtype: Any
        """
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
