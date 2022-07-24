from typing import Any

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.auth import authenticate, create_access_token
from app.utils.dependencies import get_db_session, get_current_user
from app.models.user import UserRead, UserCreate, User
from app.services import user as service

auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
)
async def signup(
        *,
        user: UserCreate,
        session: AsyncSession = Depends(get_db_session),
) -> UserRead:
    """ Signup user with create user service """
    return await service.create_user(user_in=user, session=session)


@auth_router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
)
async def login(
        session: AsyncSession = Depends(get_db_session),
        login_form: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """ Login user with Fastapi auth form data and return JWT """
    user = await authenticate(
        email=login_form.username,
        password=login_form.password,
        db_session=session,
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad credentials")
    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@auth_router.post(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    """ Fetch the current logged-in user """
    return UserRead(**current_user.dict())
