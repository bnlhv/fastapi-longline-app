import asyncio
from typing import Callable, Generator

import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from app.utils.database import engine, async_session


# pytestmark = pytest.mark.anyio

@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.run_sync(SQLModel.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest_asyncio.fixture()
def override_get_session(db_session: AsyncSession) -> Callable:
    async def _override_get_session():
        yield db_session

    return _override_get_session


@pytest_asyncio.fixture()
def app(override_get_session: Callable) -> FastAPI:
    from app.utils.dependencies import get_db_session
    from main import app

    app.dependency_overrides[get_db_session] = override_get_session
    return app


@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncClient:
    """ :returns: Async Client instance for testing. """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
