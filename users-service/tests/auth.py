from typing import Dict

import pytest
from fastapi import status
from httpx import AsyncClient

from app.utils.consts import settings

V1_PATH = settings.API_V1_STR


@pytest.mark.parametrize(
    "payload", [
        {
            "full_name": "Ben",
            "email": "ben@gmail.com",
            "is_superuser": True,
            "password": "aa",
        },
        {
            "full_name": "Ben",
            "email": "ben@gmail.com",
            "password": "aa",
        },
    ]
)
@pytest.mark.asyncio
async def test_good_signup(async_client: AsyncClient, payload: Dict):
    response = await async_client.post(f"{V1_PATH}/auth/signup", json=payload)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
    "payload", [
        {
            "full_name": "Ben",
            "password": "aa",
        },
        {
            "email": "ben@gmail.com",
            "password": "aa",
        },
        {
            "full_name": "Ben",
            "email": "ben@gmail.com",
        },
    ]
)
@pytest.mark.asyncio
async def test_bad_signup(async_client: AsyncClient, payload: Dict):
    response = await async_client.post(f"{V1_PATH}/auth/signup", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
