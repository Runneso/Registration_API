from contextlib import asynccontextmanager

from database import make_migrations
from routes import users

import uvicorn
from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.add("logging.log", format="{time} {level} {message}", level="DEBUG",
               rotation="10 MB", compression="zip")
    logger.info("Startup")
    await make_migrations()
    yield
    logger.info("Shutdown")


api: FastAPI = FastAPI(lifespan=lifespan)

api.include_router(
    users,
    prefix="/api/v1",
    tags=["users"],
)

if __name__ == "__main__":
    uvicorn.run(api)
