from datetime import timedelta, datetime
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.user import User
from app.utils.consts import settings
from app.utils.security import verify_password

oauth2_scheme = OAuth2PasswordBearer(f"{settings.API_V1_STR}/auth/login")


def _create_access_token(token_type: str, lifetime: timedelta, sub: int):
    """
    Create a Json Web Token so that user can authenticate and login.

    :param token_type: Type of token.
    :param lifetime: The amount of time the token is valid.
    :param sub: User specific identification.
    :return: JWT Object.
    """
    payload = {
        "type": token_type,
        "exp": datetime.utcnow() + lifetime,
        # iat = Issued at
        "iat": datetime.utcnow(),
        "sub": str(sub),
    }
    return jwt.encode(
        claims=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_access_token(*, sub: int) -> str:
    """ :returns: created JWT."""
    return _create_access_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
        sub=sub,
    )


async def authenticate(
        *,
        email: str,
        password: str,
        db_session: AsyncSession
) -> Optional[User]:
    """ Authenticate user by checking hashed password """
    user = await db_session.execute(select(User).where(User.email == email))
    user = user.first()[0]
    if not user or not verify_password(plain_password=password,
                                       hashed_password=user.hashed_password):
        return None
    return user
