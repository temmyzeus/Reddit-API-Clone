from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from .schemas import RootResponse
from .routers import tweets, users

api = FastAPI(title="Reddit API Clone")

origins: list = ["*"]
api.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)

api.include_router(users.router)
api.include_router(tweets.router)


@api.get("/", status_code=status.HTTP_200_OK, response_model=RootResponse)
def root() -> dict[str]:
    return {"message": "Reddit API Clone with FastAPI"}
