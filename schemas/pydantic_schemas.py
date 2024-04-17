from datetime import datetime
from typing import Optional

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


class UpdateUser(BaseModel):
    new_username: Optional[str] = None
    new_email: Optional[str] = None


class UpdatePassword(BaseModel):
    old_password: str
    new_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
