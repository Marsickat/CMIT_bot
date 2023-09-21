import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from bot import handlers
from bot import utils
import database as db


async def main():
    # Инициализация
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    bot_obj = Bot(token=getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)

    # Выбор хранилища
    # dp = Dispatcher(storage=MemoryStorage())
    dp = Dispatcher(storage=RedisStorage(db.redis))

    # Инициализация базы данных (вместо alembic)
    # await db.proceed_schemas(db.async_engine, db.models.BaseModel.metadata)

    # Подключение хэндлеров
    dp.include_router(handlers.main_router)

    # Подключение мидлварей
    # dp.update.middleware(mw.DatabaseMiddleware())

    # Установка команд в меню
    await utils.set_commands(bot_obj)

    # Подключение функций запуска и остановки
    dp.startup.register(utils.send_message_startup)
    dp.shutdown.register(utils.send_message_shutdown)

    # Запуск
    await bot_obj.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot_obj, sessionmaker=db.async_sessionmaker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
