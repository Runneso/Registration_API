from settings import Config, load_config

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase, declarative_base

config: Config = load_config()


def get_postgres_async_engine() -> AsyncEngine:
    postgres_url: URL = URL.create(
        drivername=config.postgres.POSTGRES_DRIVER,
        username=config.postgres.POSTGRES_USER,
        password=config.postgres.POSTGRES_PASSWORD,
        host=config.postgres.POSTGRES_HOST,
        port=config.postgres.POSTGRES_PORT,
        database=config.postgres.POSTGRES_DB
    )

    async_engine: AsyncEngine = create_async_engine(url=postgres_url)
    return async_engine


engine = get_postgres_async_engine()
Base: DeclarativeBase = declarative_base()


def get_postgres_async_session_maker() -> async_sessionmaker[AsyncSession]:
    async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, expire_on_commit=False)
    return async_session_maker


async def get_async_session() -> AsyncSession:
    async with get_postgres_async_session_maker()() as session:
        yield session
