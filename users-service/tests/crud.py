import string
from typing import Dict

import pytest
from faker.generator import random
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
async def test_good_create_user(async_client: AsyncClient, payload: Dict):
    response = await async_client.post(V1_PATH + "/users/", json=payload)
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
async def test_bad_create_user(async_client: AsyncClient, payload: Dict):
    response = await async_client.post(V1_PATH + "/users/", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_all_users(async_client: AsyncClient):
    response = await async_client.get(V1_PATH + "/users/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("create_data", [{
    "full_name": "Ben",
    "email": random.choice(string.ascii_letters) + "@gmail.com",
    "password": "aa",
}])
@pytest.mark.asyncio
async def test_get_user(async_client: AsyncClient, create_data: Dict):
    # Create the User first
    response = await async_client.post(V1_PATH + "/users/", json=create_data)
    assert response.status_code == status.HTTP_201_CREATED

    user = response.json()
    response = await async_client.get(V1_PATH + f"/users/{user['id']}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_bad_get_user(async_client: AsyncClient):
    response = await async_client.get(V1_PATH + "/users/1/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "create_data, update_data", [(
            {
                "full_name": "Ben",
                "email": random.choice(string.ascii_letters) + "@gmail.com",
                "password": "aa",
            },
            {
                "full_name": "BenBen",
            }
    )]
)
@pytest.mark.asyncio
async def test_update_user(async_client: AsyncClient, create_data: Dict,
                           update_data: Dict):
    # Create the User first
    response = await async_client.post(V1_PATH + "/users/", json=create_data)
    assert response.status_code == status.HTTP_201_CREATED
    user = response.json()
    response = await async_client.put(V1_PATH + f"/users/{user['id']}/",
                                      json=update_data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("create_data", [{
    "full_name": "Ben",
    "email": random.choice(string.ascii_letters) + "@gmail.com",
    "password": "aa",
}])
@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient, create_data: Dict):
    # Create the User first
    response = await async_client.post(V1_PATH + "/users/", json=create_data)
    assert response.status_code == status.HTTP_201_CREATED

    user = response.json()
    response = await async_client.delete(V1_PATH + f"/users/{user['id']}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.parametrize("create_data", [{
    "full_name": "Ben",
    "email": random.choice(string.ascii_letters) + "@gmail.com",
    "password": "aa",
}])
@pytest.mark.asyncio
async def test_bad_delete_user(async_client: AsyncClient, create_data: Dict):
    # Create the User first
    response = await async_client.post(V1_PATH + "/users/", json=create_data)
    assert response.status_code == status.HTTP_201_CREATED

    user = response.json()
    response = await async_client.delete(V1_PATH + f"/users/{user['id'] + 1}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
