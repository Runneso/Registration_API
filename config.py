from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PREFIX: str
    HASH_SALT: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")


class Constants(BaseSettings):
    OK: str = "OK"
    TIME_PATTERN: str = "%Y-%m-%dT%H:%M:%SZ"
    version: str = "v1"
    PREFIX: str = "/api/"
    JWT_TIME_LIVE: float = 60 * 60 * 24


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_constants():
    return Constants()
