from config import get_settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

settings = get_settings()
database_url = f"postgresql+psycopg2://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"
engine = create_engine(database_url, pool_size=10 ** 3)


class Base(DeclarativeBase):
    pass
