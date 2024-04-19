from schemas import (GetUser,
                     CreateUser,
                     UpdateUser,
                     UpdatePassword,
                     Token)
from database import get_async_session, CRUD
from routes.responses import load_responses, Responses
from routes.limiter import limiter

from typing import (List,
                    Annotated)

from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer("/api/v1/users/signIn")
responses: Responses = load_responses()
users: APIRouter = APIRouter(prefix="/users")
db: CRUD = CRUD()


@users.get(
    "/getUsers",
    response_model=List[GetUser],
    status_code=status.HTTP_200_OK,
    responses=responses.users.get_users
)
async def get_users(
        session: AsyncSession = Depends(get_async_session)
):
    return await db.get_users_orm(session)


@users.post(
    "/createUser",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    responses=responses.users.create_user
)
@limiter.limit("5/minute")
async def create_user(
        request: Request,
        user_data: CreateUser,
        session: AsyncSession = Depends(get_async_session)
):
    token = await db.create_user_orm(user_data, session)
    return {"access_token": token, "token_type": "bearer"}


@users.post(
    "/signIn",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses=responses.users.sign_in
)
@limiter.limit("5/minute")
async def sign_in(
        request: Request,
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)
):
    token = await db.sign_in_orm(user_data, session)
    return {"access_token": token, "token_type": "bearer"}


@users.get(
    "/myProfile",
    response_model=GetUser,
    status_code=status.HTTP_200_OK,
    responses=responses.users.my_profile
)
async def my_profile(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_async_session)
):
    return await db.my_profile_orm(token, session)


@users.patch(
    "/updateProfile",
    response_model=GetUser,
    status_code=status.HTTP_201_CREATED,
    responses=responses.users.update_profile
)
async def update_profile(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_data: UpdateUser,
        session: AsyncSession = Depends(get_async_session)
):
    return await db.update_profile_orm(token, user_data, session)


@users.patch(
    "/updatePassword",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    responses=responses.users.update_password
)
async def update_password(
        token: Annotated[str, Depends(oauth2_scheme)],
        password_data: UpdatePassword,
        session: AsyncSession = Depends(get_async_session)
):
    await db.update_password_orm(token, password_data, session)


@users.get(
    "/myFriends",
    response_model=List[int],
    status_code=status.HTTP_200_OK,
    responses=responses.users.my_friends
)
async def my_friends(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_async_session)
):
    return await db.my_friends_orm(token, session)


@users.post(
    "/addFriend",
    response_model=List[int],
    status_code=status.HTTP_201_CREATED,
    responses=responses.users.add_friend
)
async def add_friend(
        token: Annotated[str, Depends(oauth2_scheme)],
        friend_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await db.add_friend_orm(token, friend_id, session)


@users.delete(
    "/removeFriend",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.users.remove_friend
)
async def remove_friend(
        token: Annotated[str, Depends(oauth2_scheme)],
        friend_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    await db.remove_friend_orm(token, friend_id, session)
