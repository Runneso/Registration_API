from schemas import GetUser, CreateUser
from database import get_async_session, CRUD

from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

users: APIRouter = APIRouter()
db: CRUD = CRUD()


@users.get(
    "/get_users",
    response_model=List[GetUser],
    status_code=status.HTTP_200_OK,

)
async def get_users(session: AsyncSession = Depends(get_async_session)):
    users_array = await db.get_users_orm(session)

    return users_array


@users.post(
    "/create_user",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_201_CREATED: {"new_": 1}}
)
async def create_user(
        user_data: CreateUser,
        session: AsyncSession = Depends(get_async_session)
):
    await db.create_user_orm(user_data, session)
