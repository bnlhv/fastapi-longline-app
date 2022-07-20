""" Module of all business logic layer """
from typing import List

from models import User, UserOut_Pydantic, UserIn_Pydantic


async def get_all_users() -> List[UserOut_Pydantic]:
    users = await User.all()
    return UserOut_Pydantic.from_queryset(users)


async def get_filtered_users(**kwargs: int) -> List[UserOut_Pydantic]:
    users = await User.filter(**kwargs)
    return UserOut_Pydantic.from_queryset(users)


async def get_user(id: int = None) -> UserOut_Pydantic:
    user = await User.get(id=id)
    return UserOut_Pydantic.from_queryset_single(user)


async def create_user(user_data: UserIn_Pydantic) -> UserOut_Pydantic:
    user = await User.create(**user_data.dict(exclude_unset=True))
    return UserOut_Pydantic.from_tortoise_orm(user)


async def update_user(user_id: int, data: UserIn_Pydantic) -> UserOut_Pydantic:
    await User.filter(id=user_id).update(**data.dict())
    return UserOut_Pydantic.from_queryset_single(User.get(id=user_id))
