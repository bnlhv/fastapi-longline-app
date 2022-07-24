""" Module of Database engine and initialization """

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.utils.consts import settings

connect_args = {"check_same_thread": False}
engine = create_async_engine(
    url=settings.DB_URI,
    future=True,
    connect_args=connect_args,
)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False,
)


async def create_db_and_tables() -> None:
    """ Creating the database and tables by SQLModels """
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


if __name__ == '__main__':
    """ For first initialization """
    create_db_and_tables()
