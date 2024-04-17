from database.db import Base, engine

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, BigInteger, Date


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, unique=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)
    createdAt: Mapped[datetime] = mapped_column(Date, default=datetime.now())


async def make_migrations() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()
