from db import Base, engine
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer, Float
from config import get_constants
from datetime import datetime

constants = get_constants()


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    createdAt: Mapped[str] = mapped_column(Text, default=datetime.now().strftime(constants.TIME_PATTERN))


class PasswordUpdates(Base):
    __tablename__ = "passwordUpdates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    timestamp: Mapped[float] = mapped_column(Float, default=datetime.now().timestamp())


def create_db() -> None:
    Base.metadata.create_all(engine)
