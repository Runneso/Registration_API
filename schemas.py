from pydantic import BaseModel, Field


class Status(BaseModel):
    status: str = Field(..., description="Status value")


class Token(BaseModel):
    token: str = Field(..., description="JWT token")


class User(BaseModel):
    username: str = Field(..., min_length=6, max_length=30, pattern="[a-zA-Z0-9-]+", description="User username")
    email: str = Field(..., min_length=4, max_length=50, description="User email")
    password: str = Field(..., min_length=6, max_length=100, description="User password")


class UserProfile(BaseModel):
    username: str = Field(..., min_length=6, max_length=30, pattern="[a-zA-Z0-9-]+", description="User username")
    email: str = Field(..., min_length=4, max_length=50, description="User email")


class UserSignIn(BaseModel):
    username: str = Field(..., min_length=6, max_length=30, pattern="[a-zA-Z0-9-]+", description="User username")
    password: str = Field(..., min_length=6, max_length=100, description="User password")


class PasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=6, max_length=100, description="User password")
    new_password: str = Field(..., min_length=6, max_length=100, description="User password")


class ErrorResponse(BaseModel):
    reason: str
