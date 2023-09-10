from aiogram import Router

from .starts import router as starts_router
from .menu import router as menu_router
from .create_request import router as create_request_router
from .check_request import router as check_request_router
from .change_userdata import router as change_userdata_router
from .echo import router as echo_router

router = Router()
router.include_routers(
    starts_router,
    menu_router,
    create_request_router,
    check_request_router,
    change_userdata_router,
    echo_router
)
