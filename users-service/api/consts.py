""" Module of all consts in this service """
from enum import Enum


class ModelSettings(Enum):
    MAX_STR_LENGTH: int = 50
    MAX_COD_LENGTH: int = 10


class AppSettings(Enum):
    DB_FILENAME: str = "database.db"
    DB_PATH: str = f"sqlite:///database.db"
