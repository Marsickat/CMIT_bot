from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: SecretStr
    admins: list
    db_url: SecretStr
    db_drivername: str
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_database: str
    redis_url: SecretStr


config = Settings()
