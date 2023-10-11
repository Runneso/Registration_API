from db import Base, engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer
from datetime import datetime
from asyncio import run


class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_login: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    user_password: Mapped[str] = mapped_column(Text, nullable=False)
    user_datetime_registration: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


async def create_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()
