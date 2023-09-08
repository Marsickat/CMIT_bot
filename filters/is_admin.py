from aiogram import types
from aiogram.filters import BaseFilter


class IsAdminFilter(BaseFilter):
    def __init__(self, admins: list):
        self.admins = admins

    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in self.admins
