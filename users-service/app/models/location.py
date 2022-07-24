""" Module Location model """
from typing import Optional

from sqlmodel import Field, SQLModel

from app.utils.consts import settings


class Location(SQLModel, table=True):
    """ Location model that describes where user lives """
    id: Optional[int] = Field(default=None, primary_key=True)
    home_number: str = Field(nullable=True)
    street: str = Field(max_length=settings.MAX_STR_LENGTH)
    city: str = Field(max_length=settings.MAX_STR_LENGTH)
    country_code: str = Field(max_length=settings.MAX_COD_LENGTH)
    postcode: str = Field(index=True, max_length=settings.MAX_COD_LENGTH)
    # resident_id: Optional[int] = Field(
    #     default=None,
    #     foreign_key="user.id"
    # )

    def __str__(self) -> str:
        """ :returns: Override str of model and return assemble of values. """
        return (f"{self.street} {self.home_number}, {self.city}, "
                f"{self.country_code}")
