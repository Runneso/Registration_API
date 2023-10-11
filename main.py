from typing import List
from datetime import datetime
from hashlib import sha256
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker
from crud import CRUD
from db import engine
from models import Users
from schemas import User, NewUser

api = FastAPI()
session = async_sessionmaker(bind=engine, expire_on_commit=False)
db = CRUD()


@api.get("/users", status_code=200, response_model=List[User])
async def get_all_users():
    users = await db.get_all_users(session)
    return users


@api.get("/create", status_code=201)
async def create_user(user_data: NewUser):
    user = Users(user_login=user_data.user_login,
                 user_password=sha256(bytes(user_data.user_password, encoding="utf-8")).hexdigest(),
                 user_datetime_registration=datetime.utcnow())
    user = await db.create_user(session, user)
    return user
