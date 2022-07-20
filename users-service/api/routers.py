""" Module for all services route endpoints """

from fastapi import APIRouter, status

from services import *

user_router = APIRouter(prefix="/users")


@user_router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=UserOut_Pydantic,
)
def get_users() -> List[UserOut_Pydantic]:
    return await get_all_users()
