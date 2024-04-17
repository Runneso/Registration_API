from contextlib import asynccontextmanager

from database import make_migrations
from routes import users

import uvicorn
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    await make_migrations()
    yield
    print("Shutdown")


api: FastAPI = FastAPI(lifespan=lifespan)

api.include_router(
    users,
    prefix="/api/v1/users",
    tags=["users"],
)

if __name__ == "__main__":
    uvicorn.run(api)
