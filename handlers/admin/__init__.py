from aiogram import Router

from config import config
from filters import IsAdminFilter
from .dice import router as dice_router

router = Router()
router.message.filter(IsAdminFilter(config.admins))
router.include_routers(dice_router)
