from typing import Dict

from fastapi import FastAPI, APIRouter

app = FastAPI(title="app API")

router = APIRouter()


@router.get(path="/", status_code=200)
def root() -> Dict:
    """ Root app path """
    return {"message": "Welcome to root path!"}


app.include_router(router=router)

if __name__ == '__main__':
    # debug purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug", reload=True)
