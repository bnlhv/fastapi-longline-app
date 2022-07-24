""" Module User model """
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import String, Column
from sqlmodel import Field, SQLModel

from app.utils.consts import settings


class BaseUser(SQLModel):
    full_name: str = Field(max_length=settings.MAX_STR_LENGTH)
    email: EmailStr = Field(sa_column=Column("email", String, unique=True))
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_superuser: bool = Field(default=False)

    def __str__(self) -> str:
        """ :returns: Override str of model and return user name. """
        return self.full_name


class User(BaseUser, table=True):
    """ General User in the application """
    id: Optional[int] = Field(default=None, index=True, primary_key=True)
    hashed_password: Optional[str] = (
        Field(sa_column=Column("hashed_password", String, unique=True))
    )


class UserRead(BaseUser):
    """ Class for User read from DB, for validation purposes """
    id: int


class UserCreate(BaseUser):
    """ Class for User creation for validation purposes """
    password: str


class UserUpdate(SQLModel):
    """ User update pydantic model for validation """
    full_name: Optional[str] = Field(max_length=settings.MAX_STR_LENGTH)
    email: Optional[EmailStr]
