from datetime import datetime

from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    email: str
    password: str


class GetUser(BaseModel):
    id: int
    username: str
    email: str
    createdAt: datetime
