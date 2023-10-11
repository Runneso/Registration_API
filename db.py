from dotenv import load_dotenv
from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

engine = create_async_engine(getenv("DATABASE_URL"))


class Base(DeclarativeBase):
    pass
