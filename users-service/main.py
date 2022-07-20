from typing import Dict

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from api.database import setup_db
from api.routers import user_router

app = FastAPI(title="Users Service API", root_path="/api/v1")
setup_db()

app.include_router(router=user_router)


@app.get(path="/", status_code=200)
def root() -> Dict:
    """ Root users-service path """
    return {"message": "Welcome to root path!"}


register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == '__main__':
    # debug purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug", reload=True)
