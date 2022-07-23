""" User routes """
from typing import List

from fastapi import APIRouter, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from api.database import get_session
from api.models.user import UserUpdate, UserRead, UserCreate
from api.services import user as service

user_router = APIRouter(prefix="/users")


@user_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserRead]
)
async def get_users(
        session: AsyncSession = Depends(get_session),
) -> List[UserRead]:
    return await service.get_all_users(session)


@user_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(get_session),
) -> UserRead:
    return await service.create_user(user=user, session=session)


@user_router.get(
    path="/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_session),
) -> UserRead:
    return await service.get_user(user_id=user_id, session=session)


@user_router.put(
    path="/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def update_user(
        user_id: int,
        user: UserUpdate,
        session: AsyncSession = Depends(get_session),
) -> UserRead:
    return await service.update_user(
        user_id=user_id,
        user_data=user,
        session=session,
    )


@user_router.delete(
    path="/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_session),
) -> None:
    return await service.delete_user(user_id=user_id, session=session)
