""" Module of all business logic layer """
from typing import List, Optional, cast, Dict

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from api.models.user import User, UserUpdate, UserRead, UserCreate


async def get_user_from_db(user_id: int, session: AsyncSession) -> User:
    """
    Get a specific User by id from the database.

    :param user_id: The to get from DB.
    :param session: Database session object.
    :raises HTTPException: If the user id doesn't exist in the Database.
    :return: User object.
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


async def get_all_users(session: AsyncSession) -> List[UserRead]:
    """ Get all Users """
    users = await session.exec(select(User))
    return cast(List[UserRead], users.all())


async def get_user(user_id: int, session: AsyncSession) -> Optional[UserRead]:
    """ Get a specific User by id """
    user = await get_user_from_db(user_id, session)
    return cast(UserRead, user)


async def create_user(user: UserCreate, session: AsyncSession) -> UserRead:
    """
    Create a user model in the database.

    :param user: The User object to create in the Databse.
    :param session: Database session object.
    :raises IntegrityError: If User's E-mail already exists in the Database.
    :return: User object.
    """
    try:
        user = User.from_orm(user)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return cast(UserRead, user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


async def update_user(
        user_id: int,
        user_data: UserUpdate,
        session: AsyncSession
) -> UserRead:
    """ Update a specific User by id with optional fields """
    user = await get_user_from_db(user_id, session)
    user_data = user_data.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return cast(UserRead, user)


async def delete_user(user_id: int, session: AsyncSession) -> None:
    """ Get a specific User by id """
    user = await get_user_from_db(user_id, session)
    print(user)
    await session.delete(user)
    await session.commit()
