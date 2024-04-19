from contextlib import asynccontextmanager

from database import make_migrations
from routes.limiter import limiter
from routes import users

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
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

api.state.limiter = limiter  # type: ignore[call-arg]
api.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler  # type: ignore[call-arg]
)

origins = [

]

api.add_middleware(
    CORSMiddleware,  # type: ignore[call-arg]
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.add_middleware(
    SlowAPIMiddleware  # type: ignore[call-arg]
)

api.include_router(
    users,
    prefix="/api/v1",
    tags=["users"],
)

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0")
