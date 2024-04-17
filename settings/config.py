import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv


@dataclass
class PostgresConfig:
    POSTGRES_DRIVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str


@dataclass
class Config:
    postgres: PostgresConfig


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
        )
    )
