from aiogram import Router

from .starts import router as starts_router
from .echo import router as echo_router

router = Router()
router.include_routers(
    starts_router,
    echo_router
)
