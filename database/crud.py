from fastapi.security import OAuth2PasswordRequestForm

from schemas import (CreateUser,
                     UpdateUser,
                     UpdatePassword)
from settings import Config, load_config
from .models import (Users,
                     UsersTokens,
                     UsersFriends)

from datetime import datetime, timedelta

import jwt
from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bcrypt import hashpw
from loguru import logger


class CRUD:
    config: Config = load_config()

    @classmethod
    def get_token(cls, user_id: int):
        token = jwt.encode(
            payload={
                "id": user_id,
                "createdAt": datetime.now().timestamp(),
                "destroyedAt": (datetime.now() + timedelta(days=cls.config.jwt.JWT_TIME_LIVE)).timestamp()
            },
            key=cls.config.jwt.JWT_SECRET_KEY,
            algorithm=cls.config.jwt.JWT_ALGORITHM
        )

        return token

    @classmethod
    def get_hash(cls, password: str):
        return hashpw(
            password=password.encode("utf-8"),
            salt=cls.config.bcrypt.HASH_SALT.encode("utf-8")
        ).decode("utf-8")

    @classmethod
    async def auth(cls, token: str, session: AsyncSession):
        try:
            payload = jwt.decode(
                jwt=token,
                key=cls.config.jwt.JWT_SECRET_KEY,
                algorithms=[cls.config.jwt.JWT_ALGORITHM]
            )
        except Exception as error:
            logger.error(error)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token!")

        if datetime.now().timestamp() > payload["destroyedAt"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token!")

        user = await cls.get_user_by_id(payload["id"], session)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token!")

        timestamp = user.token.timestamp

        if timestamp > payload["createdAt"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token!")
        return user

    @classmethod
    async def get_user_by_id(cls, user_id: int, session: AsyncSession):
        sql_query = select(Users).filter(Users.id == user_id)

        result = await session.execute(sql_query)
        return result.scalars().first()

    @classmethod
    async def get_users_orm(cls, session: AsyncSession):
        sql_query = select(Users).order_by(Users.id)

        result = await session.execute(sql_query)
        return result.unique().scalars().all()

    @classmethod
    async def create_user_orm(cls, user_data: CreateUser, session: AsyncSession):
        try:
            user_data.password = cls.get_hash(user_data.password)
            new_user = Users(**user_data.model_dump())  # type: ignore[call-arg]
            token = UsersTokens(timestamp=datetime.now().timestamp())  # type: ignore[call-arg]
            new_user.token = token
            session.add(new_user)
            await session.commit()
        except Exception as error:
            logger.error(error)
            await session.close()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict user data!")

        await session.close()

        return cls.get_token(new_user.id)

    @classmethod
    async def sign_in_orm(cls, user_data: OAuth2PasswordRequestForm, session: AsyncSession):
        sql_query = select(Users).filter(Users.username.like(user_data.username))

        result = await session.execute(sql_query)
        user = result.scalars().first()
        await session.close()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist!")

        if user.password != cls.get_hash(user_data.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")

        return cls.get_token(user.id)

    @classmethod
    async def my_profile_orm(cls, token: str, session: AsyncSession):
        return await cls.auth(token, session)

    @classmethod
    async def update_profile_orm(cls, token: str, user_data: UpdateUser, session: AsyncSession):
        user = await cls.auth(token, session)

        if user_data.new_email is not None:
            user.email = user_data.new_email

        if user_data.new_username is not None:
            user.username = user_data.new_username

        try:
            await session.commit()
        except Exception as error:
            logger.error(error)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict user data!")

        await session.close()
        return user

    @classmethod
    async def update_password_orm(cls, token: str, password_data: UpdatePassword, session: AsyncSession):
        user = await cls.auth(token, session)

        if user.password != cls.get_hash(password_data.old_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")

        user.password = cls.get_hash(password_data.new_password)
        user.token.timestamp = datetime.now().timestamp()

        await session.commit()
        await session.close()

    @classmethod
    async def my_friends_orm(cls, token: str, session: AsyncSession):
        user = await cls.auth(token, session)

        return [friend.friend for friend in user.friends]

    @classmethod
    async def add_friend_orm(cls, token: str, friend_id: int, session: AsyncSession):
        friend = await cls.get_user_by_id(friend_id, session)

        if friend is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend not found!")

        user = await cls.auth(token, session)

        if user.id == friend_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User cannot add himself in friends!")

        friend = UsersFriends(friend=friend_id)  # type: ignore[call-arg]
        friends = {friend.friend for friend in user.friends}

        if friend.friend in friends:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Friend already in user`s friends!")

        user.friends.add(friend)

        await session.commit()
        await session.close()

        return [friend.friend for friend in user.friends]

    @classmethod
    async def remove_friend_orm(cls, token: str, friend_id: int, session: AsyncSession):
        friend = await cls.get_user_by_id(friend_id, session)

        if friend is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend not found!")

        user = await cls.auth(token, session)
        friend = UsersFriends(friend=friend_id)  # type: ignore[call-arg]
        friends = {friend.friend for friend in user.friends}

        if friend.friend not in friends:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No same user in user`s friends!")

        for friend in user.friends:
            if friend.friend == friend_id:
                await session.delete(friend)
                break

        await session.commit()
        await session.close()
