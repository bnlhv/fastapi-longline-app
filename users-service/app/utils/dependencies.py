from typing import AsyncGenerator, Optional, cast

from fastapi import Depends, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.auth import oauth2_scheme
from app.utils.consts import settings
from app.utils.database import async_session
from app.utils.exceptions import CredentialsException


class TokenData(BaseModel):
    username: Optional[str] = None


async def get_db_session() -> AsyncGenerator:
    """ Create and yield the session to Database once """
    async with async_session() as session:
        yield session


async def get_current_user(
        db_session: AsyncSession = Depends(get_db_session),
        token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_aud": False},
        )
        username = payload.get("sub")
        if not username:
            raise JWTError()

        token_data = TokenData(username=username)
        user = await db_session.get(User, int(token_data.username))
        if not user:
            raise JWTError()

    except JWTError:
        raise CredentialsException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return cast(User, user)

