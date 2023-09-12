from aiogram import Router

from config import config
from filters import IsAdminFilter
from .admin_menu import router as admin_menu_router
from .active_requests import router as active_requests_router
from .take_request import router as take_request_router
from .dice import router as dice_router

router = Router()
router.message.filter(IsAdminFilter(config.admins))  # Подключение фильтра IsAdmin
router.include_routers(
    admin_menu_router,
    active_requests_router,
    take_request_router,
    dice_router
)
