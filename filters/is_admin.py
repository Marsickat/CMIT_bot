from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdminFilter(BaseFilter):
    """
    Filter класс для определения администратора среди пользователей.

    :ivar admins: Список администраторов.
    """
    def __init__(self, admins: list[int]) -> None:
        """
        Инициализирует новый экземпляр класса.
        Устанавливает список администраторов.

        :param admins: Список ID администраторов.
        :type admins: list[int]
        """
        self.admins = admins

    async def __call__(self, message: Message) -> bool:
        """
        Вызывается при обработке запроса. Возвращает True, если ID пользователя находится в списке администраторов.

        :param message: Объект сообщения.
        :type message: Message

        :return: True, если ID пользователя находится в списке администраторов.
        :rtype: bool
        """
        return message.from_user.id in self.admins
