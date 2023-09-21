from os import getenv

from sqlalchemy import URL

from .engine import create_engine, get_session_maker, proceed_schemas
from .redis import redis
from . import models, orm

# Создание ссылки для базы данных
postgres_url = URL.create(
    drivername=getenv("POSTGRES_DRIVERNAME"),
    username=getenv("POSTGRES_USER"),
    password=getenv("POSTGRES_PASSWORD"),
    host=getenv("POSTGRES_HOST"),
    port=getenv("POSTGRES_PORT"),
    database=getenv("POSTGRES_DB")
)

async_engine = create_engine(postgres_url)  # Создание асинхронной машины соединений
async_sessionmaker = get_session_maker(async_engine)  # Создание асинхронной фабрики для сессий
