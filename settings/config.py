import os
from pydantic_settings import BaseSettings
from functools import lru_cache

from dotenv import load_dotenv


class PostgresConfig(BaseSettings):
    POSTGRES_DRIVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str


class BcryptConfig(BaseSettings):
    HASH_SALT: str


class JWTConfig(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_TIME_LIVE: int
    JWT_ALGORITHM: str


class Config(BaseSettings):
    postgres: PostgresConfig
    bcrypt: BcryptConfig
    jwt: JWTConfig


@lru_cache
def load_config() -> Config:
    load_dotenv()
    return Config(
        postgres=PostgresConfig(
            POSTGRES_DRIVER=os.getenv("POSTGRES_DRIVER"),
            POSTGRES_USER=os.getenv("POSTGRES_USER"),
            POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
            POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
            POSTGRES_PORT=int(os.getenv("POSTGRES_PORT")),
            POSTGRES_DB=os.getenv("POSTGRES_DB")
        ),
        bcrypt=BcryptConfig(
            HASH_SALT=os.getenv("HASH_SALT")
        ),
        jwt=JWTConfig(
            JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
            JWT_TIME_LIVE=int(os.getenv("JWT_TIME_LIVE")),
            JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
        )
    )
