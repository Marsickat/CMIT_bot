from sqlalchemy import URL, MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker


def create_engine(url: URL | str) -> AsyncEngine:
    return create_async_engine(url, echo=True, pool_pre_ping=True)


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine)


async def proceed_schemas(engine: AsyncEngine, metadata: MetaData):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
