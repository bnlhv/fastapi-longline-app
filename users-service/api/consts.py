""" Module of all consts in this service """
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URI: Optional[str] = f"sqlite+aiosqlite:///database.db"
    MAX_STR_LENGTH: int = 50
    MAX_COD_LENGTH: int = 10

    class Config:
        case_sensitive = True


settings = Settings()
