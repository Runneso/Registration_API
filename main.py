from contextlib import asynccontextmanager
from typing import List
from datetime import datetime

import uvicorn
import jwt
from jwt.exceptions import InvalidSignatureError
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from redis import asyncio as aioredis
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from bcrypt import hashpw

from db import engine
from models import create_db, Users
from crud import CRUD
from config import get_settings, get_constants
from schemas import Status, User, UserProfile, UserSignIn, Token, PasswordUpdate, ErrorResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    for router in routers:
        app.include_router(router)
    yield


settings = get_settings()
constants = get_constants()
prefix_url = constants.PREFIX + constants.version

redis = aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
auth = APIRouter()
profile = APIRouter()
limit = APIRouter()
long_operation = APIRouter()
routers = [auth, profile, limit, long_operation]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{prefix_url}/sign-in")
session_maker = sessionmaker(bind=engine)
db = CRUD()


class CustomException(Exception):
    def __init__(self, status_code: int, reason: str):
        self.status_code = status_code
        self.reason = reason


def get_session():
    with session_maker() as session:
        yield session


def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)):
    try:
        data = jwt.decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except InvalidSignatureError:
        raise RequestValidationError(errors="JWT error")

    if datetime.now().timestamp() > data["destroyedAt"]:
        raise RequestValidationError(errors="Timestamp JWT error")

    timestamp = db.get_timestamp_by_username(session, data["username"])

    if timestamp > data["createdAt"]:
        raise RequestValidationError(errors="Timestamp JWT error")
    return db.get_user_by_username(session, data["username"])


def get_hash(password: str):
    return hashpw(password=password.encode("utf-8"), salt=settings.HASH_SALT.encode("utf-8")).decode("utf-8")


@app.get(f"{prefix_url}/ping", status_code=200, response_model=Status)
async def ping():
    return Status(status=constants.OK)


@auth.get(f"{prefix_url}/auth/users", status_code=200, response_model=List[UserProfile])
async def users(session=Depends(get_session)):
    return db.get_users(session)


@auth.post(f"{prefix_url}/auth/registrate", status_code=201, response_model=UserProfile)
async def registrate(user_data: User, session=Depends(get_session)):
    user = Users(username=user_data.username, password=get_hash(user_data.password), email=user_data.email)
    try:
        db.create_user(session, user)
    except IntegrityError:
        raise RequestValidationError(errors="Unique error")

    return UserProfile(username=user_data.username, email=user_data.email)


@auth.post(f"{prefix_url}/auth/sign-in", status_code=200)
async def sign_in(user_data: UserSignIn, session=Depends(get_session)):
    user = db.get_user_by_username(session, user_data.username)

    if user is None:
        raise RequestValidationError(errors="Unreal error")

    if user.password == get_hash(user_data.password):
        token = jwt.encode(payload={"username": user.username,
                                    "createdAt": datetime.now().timestamp(),
                                    "destroyedAt": datetime.now().timestamp() + constants.JWT_TIME_LIVE},
                           key=settings.JWT_SECRET_KEY,
                           algorithm=settings.JWT_ALGORITHM)
        return Token(token=token)

    raise RequestValidationError(errors="Invalid login/password")


@profile.post(f"{prefix_url}/profile/update", status_code=200, response_model=Status)
async def update(password_data: PasswordUpdate, user_data: Users = Depends(get_current_user),
                 session=Depends(get_session)):
    if not user_data.password == get_hash(password_data.old_password):
        raise RequestValidationError(errors="Invalid login/password")

    db.update_password(session, user_data, get_hash(password_data.new_password))
    db.update_timestamp(session, user_data.username)
    return Status(status=constants.OK)


@profile.get(f"{prefix_url}/profile/me", status_code=200, response_model=UserProfile)
async def me(user_data: UserProfile = Depends(get_current_user)):
    return user_data


@limit.get(f"{prefix_url}/limit", status_code=200, response_model=Status)
@limiter.limit("5/minute")
async def limit(request: Request):
    return Status(status=constants.OK)


@long_operation.get(f"{prefix_url}/long_operation", status_code=200, response_model=int)
async def long_operation():
    key = settings.REDIS_PREFIX + "long_operation"
    cache = await redis.get(key)
    if cache:
        return cache
    value = sum(range(10 ** 8))
    await redis.set(key, value)
    await redis.expire(key, 60)
    return value


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(status_code=exc.status_code,
                        content=jsonable_encoder(ErrorResponse(reason=exc.reason)))


if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
