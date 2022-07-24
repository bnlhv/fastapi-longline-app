""" Module of all consts in this service """
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/app/v1"
    DB_URI: Optional[str] = f"sqlite+aiosqlite:///database.db"
    MAX_STR_LENGTH: int = 50
    MAX_COD_LENGTH: int = 10
    JWT_EXPIRE_MINUTES: int = 30
    JWT_SECRET: str = "OVERRIDE_THIS_WITH_ENVIRONMENT_VARIABLE"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True


settings = Settings()
