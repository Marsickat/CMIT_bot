from aiogram import Router

from .admin import router as admin_router
from .user import router as user_router

main_router = Router()
main_router.include_routers(
    admin_router,
    user_router
)
