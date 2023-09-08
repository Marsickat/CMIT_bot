from sqlalchemy import URL

from config import config
from . import models, orm
from .engine import create_engine, get_session_maker, proceed_schemas

postgres_url = URL.create(
    drivername=config.db_drivername,
    username=config.db_username,
    password=config.db_password,
    host=config.db_host,
    port=config.db_port,
    database=config.db_database
)
async_engine = create_engine(postgres_url)
async_sessionmaker = get_session_maker(async_engine)
