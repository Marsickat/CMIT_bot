from os import getenv

from aiogram import Router

from bot.filters import IsAdminFilter
from .admin_menu import router as admin_menu_router
from .active_requests import router as active_requests_router
from .take_request import router as take_request_router
from .dice import router as dice_router

router = Router()
router.message.filter(IsAdminFilter(eval(getenv("ADMINS"))))  # Подключение фильтра IsAdmin
router.include_routers(
    admin_menu_router,
    active_requests_router,
    take_request_router,
    dice_router
)
