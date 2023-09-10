from aiogram import Router

from .starts import router as starts_router
from .menu import router as menu_router
from .change_userdata import router as change_userdata_router
from .echo import router as echo_router

router = Router()
router.include_routers(
    starts_router,
    menu_router,
    change_userdata_router,
    echo_router
)
