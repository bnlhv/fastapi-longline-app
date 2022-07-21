""" Module for all services route endpoints """
from typing import List

from fastapi import APIRouter, status

import services
from models import UserIn_Pydantic, UserOut_Pydantic

user_router = APIRouter(prefix="/users")


@user_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=UserOut_Pydantic,
)
async def get_users() -> List[UserOut_Pydantic]:
    return await services.get_all_users()


@user_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut_Pydantic
)
async def create_user(user: UserIn_Pydantic) -> List[UserOut_Pydantic]:
    return await services.create_user(user)


@user_router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOut_Pydantic,
)
async def get_user(user_id: int) -> UserOut_Pydantic:
    return await services.get_user(user_id)


@user_router.put(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserOut_Pydantic,
)
async def update_user(user_id: int, user: UserIn_Pydantic) -> UserOut_Pydantic:
    return await services.update_user(user_id=user_id, data=user)
