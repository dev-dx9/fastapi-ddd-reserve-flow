from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
    )

    mode: Literal['TEST', 'LOCAL', 'DEV', 'PROD']

    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername='postgresql+asyncpg',
            username=self.db_username,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    @property
    def is_debug(self) -> bool:
        return self.mode in {'LOCAL', 'DEV'}


settings = Settings()  # pyright: ignore[reportCallIssue]
