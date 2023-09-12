from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker


def create_engine(url: URL | str) -> AsyncEngine:
    """
    Функция для создания асинхронной машины соединений.

    :param url: Ссылка на базу данных.
    :type url: URL | str

    :return: Асинхронная машина соединений.
    :rtype: AsyncEngine
    """
    return create_async_engine(url, echo=True, pool_pre_ping=True)


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    """
    Функция для создания фабрики для сессий.

    :param engine: Асинхронная машина соединений.
    :type engine: AsyncEngine

    :return: Асинхронная фабрика для сессий.
    :rtype: async_sessionmaker
    """
    return async_sessionmaker(engine)


async def proceed_schemas(engine: AsyncEngine, metadata: MetaData) -> None:
    """
    Функция для инициализации базы данных.

    :param engine: Асинхронная машина соединений.
    :type engine: AsyncEngine
    :param metadata: Метадата таблиц базы данных.
    :type metadata: MetaData

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
