from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class LoginUserSchema(BaseModel):
    username: str = Field(max_length=64)
    password: str = Field(max_length=64)


class RegisterUserSchema(LoginUserSchema):
    pass


class UserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime


class ApiTokenSchema(BaseModel):
    key: str
