""" Module of Base model of this service """
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class BaseSQLModel(SQLModel):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
