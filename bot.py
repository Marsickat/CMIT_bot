import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

import database as db
import middlewares as mw
import handlers
import utils
from config import config


async def main():
    # Инициализация
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)

    # Выбор хранилища
    dp = Dispatcher(storage=MemoryStorage())
    # dp = Dispatcher(storage=RedisStorage.from_url(config.redis_url.get_secret_value()))

    # Подключение хэндлеров
    dp.include_router(handlers.router)

    # Подключение мидлварей
    dp.update.middleware(mw.DatabaseMiddleware())

    # Установка команд в меню
    await utils.set_commands(bot)

    # Подключение функций запуска и остановки
    # dp.startup.register(utils.send_message_startup)
    # dp.shutdown.register(utils.send_message_shutdown)

    # Инициализация базы данных
    await db.proceed_schemas(db.async_engine, db.models.BaseModel.metadata)

    # Запуск
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, async_engine=db.async_engine)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")