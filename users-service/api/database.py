""" Module of Database engine and initialization """

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# don't delete this, this is for model instantiate (from api import models)
from sqlmodel.ext.asyncio.session import AsyncSession

DB_PROTOCOL = "sqlite+aiosqlite:///"
SQLITE_FILENAME = "users.db"
DB_URL = DB_PROTOCOL + "/" + SQLITE_FILENAME
connect_args = {"check_same_thread": False}
engine = create_async_engine(url=DB_URL, future=True,
                             connect_args=connect_args)


async def create_db_and_tables() -> None:
    """ Creating the database and tables by SQLModels """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """ Create and yield the session to Database once """
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


if __name__ == '__main__':
    """ For first initialization """
    create_db_and_tables()
