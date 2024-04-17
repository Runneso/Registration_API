from database.db import Base, engine

from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, BigInteger, Float, ForeignKey


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)
    createdAt: Mapped[float] = mapped_column(Float, default=datetime.now().timestamp())
    token: Mapped["UsersTokens"] = relationship(back_populates="user", uselist=False, lazy=False)
    friends: Mapped[List["UsersFriends"]] = relationship(back_populates="user", lazy=False, collection_class=set)


class UsersTokens(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    timestamp: Mapped[float] = mapped_column(Float)
    user: Mapped["Users"] = relationship(back_populates="token", uselist=False, lazy=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))


class UsersFriends(Base):
    __tablename__ = "friends"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    friend: Mapped[int] = mapped_column(BigInteger)
    user: Mapped["Users"] = relationship(back_populates="friends", uselist=False, lazy=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey("users.id"))


async def make_migrations() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()
