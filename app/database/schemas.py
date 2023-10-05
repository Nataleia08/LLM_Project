from typing import Optional

from app.database.models import UserRole, User
from datetime import datetime, date
from pydantic import BaseModel, Field, constr, EmailStr

from typing import List, Optional
from fastapi import UploadFile
from pydantic.types import conlist

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    id: int = 1
    username: str = "username"
    email: EmailStr = "useruser@example.com"
    avatar: str
    role: UserRole = UserRole.user
    detail: str = "User successfully created"

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserProfileCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date

    class Config:
        orm_mode = True


class HistoryResponse(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True