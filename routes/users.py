from schemas import (GetUser,
                     CreateUser,
                     UpdateUser,
                     UpdatePassword,
                     Token)
from database import get_async_session, CRUD

from typing import (List,
                    Annotated)

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer("/api/v1/users/signIn")
users: APIRouter = APIRouter(prefix="/users")
db: CRUD = CRUD()


@users.get(
    "/getUsers",
    response_model=List[GetUser],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 0,
                            "username": "Alex",
                            "email": "alex@gmail.com",
                            "createdAt": "2024-04-17T13:07:25.709Z"
                        }
                    ]
                }
            },
            "model": List[GetUser],
        },
    }
)
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return await db.get_users_orm(session)


@users.post(
    "/createUser",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                        "token_type": "bearer"
                    }
                }
            },
            "model": Token,
        },
        status.HTTP_409_CONFLICT: {
            "content": {
                "application/json": {
                    "example": {"detail": "Conflict user data!"}
                }
            },
            "description": "Conflict Error",
        },
    }
)
async def create_user(
        user_data: CreateUser,
        session: AsyncSession = Depends(get_async_session)
):
    token = await db.create_user_orm(user_data, session)
    return {"access_token": token, "token_type": "bearer"}


@users.post(
    "/signIn",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                        "token_type": "bearer"
                    }
                }
            },
            "model": Token,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid password!"}
                }
            },
            "description": "Unauthorized Error",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"detail": "User doesnt exist!"}
                }
            },
            "description": "Not found Error",
        }
    }
)
async def sign_in(
        user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_async_session)
):
    token = await db.sign_in_orm(user_data, session)
    return {"access_token": token, "token_type": "bearer"}


@users.get(
    "/myProfile",
    response_model=GetUser,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "id": 0,
                        "username": "Alex",
                        "email": "alex@gmail.com",
                        "createdAt": "2024-04-17T13:07:25.709Z"
                    }
                }
            },
            "model": GetUser,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid JWT token!"}
                }
            },
            "description": "Unauthorized Error",
        }
    }
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
    responses={
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {
                        "id": 0,
                        "username": "Alex",
                        "email": "alex@gmail.com",
                        "createdAt": "2024-04-17T13:07:25.709Z"
                    }
                }
            },
            "model": GetUser,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid JWT token!"}
                }
            },
            "description": "Unauthorized Error",
        }
    },
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
    responses={
        status.HTTP_201_CREATED: {
            "content": None,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid JWT token!"}
                }
            },
            "description": "Unauthorized Error",
        },
    }
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
    responses={
        status.HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        1,
                    }
                }
            },
            "model": List[int],
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid JWT token!"}
                }
            },
            "description": "Unauthorized Error",
        }
    }
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
    responses={
        status.HTTP_201_CREATED: {
            "content": {
                "application/json": {
                    "example": {
                        1, 2
                    }
                }
            },
            "model": List[int],
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid JWT token!"}
                }
            },
            "description": "Unauthorized Error",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"detail": "Friend not found!"}
                }
            },
            "description": "Not found Error",
        },
        status.HTTP_409_CONFLICT: {
            "content": {
                "application/json": {
                    "example": {"detail": "Friend already in user`s friends!"}
                }
            },
            "description": "Conflict Error",
        }
    }
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
    responses={
        status.HTTP_204_NO_CONTENT: {
            "content": None,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid JWT token!"}
                }
            },
            "description": "Unauthorized Error",
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"detail": "Friend not found!"}
                }
            },
            "description": "Not found Error",
        },
        status.HTTP_409_CONFLICT: {
            "content": {
                "application/json": {
                    "example": {"detail": "No same user in user`s friends!"}
                }
            },
            "description": "Conflict Error",
        }
    }
)
async def remove_friend(
        token: Annotated[str, Depends(oauth2_scheme)],
        friend_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    await db.remove_friend_orm(token, friend_id, session)
