from typing import Dict

from fastapi import FastAPI, status, APIRouter

from app.utils.consts import settings
from app.utils.database import create_db_and_tables
from app.routes.auth import auth_router
from app.routes.user import user_router

app = FastAPI(title="Users Service API")

root_router = APIRouter()


@app.on_event("startup")
async def on_startup():
    """ When this service startup do these operations. """
    await create_db_and_tables()
    print("Database Created.")


@root_router.get(path="/", status_code=status.HTTP_200_OK)
async def root() -> Dict:
    """ Root users-service path """
    return {"message": "Welcome to root path!"}


app.include_router(router=user_router, prefix=settings.API_V1_STR)
app.include_router(router=auth_router, prefix=settings.API_V1_STR)
app.include_router(router=root_router)

if __name__ == '__main__':
    # debug purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug", reload=True)
