from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, PastDate


class RootResponse(BaseModel):
    message: str

class TweetRequest(BaseModel):
    content: str
    username: str

class UpdateTweetRequest(BaseModel):
    content: Optional[str]
    username: Optional[str]

class GetTweetResponse(BaseModel):
    id: int
    username: str
    content: str
    created_at: datetime

    class Config:
        orm_mode: bool = True

class CreateUserRequest(BaseModel):
    username: str
    name: str
    email: EmailStr
    birth_date: str # Create a pydantic date schema


class UpdateUserRequest(BaseModel):
    phone: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    website: Optional[str]


class LoginResponse(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: str
