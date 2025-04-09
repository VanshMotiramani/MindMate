from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class SentimentBase(BaseModel):
    sentiments: str

class CreateSentiment(SentimentBase):
    created_at: datetime = datetime.now()

class UserSentiment(SentimentBase):
    id: int

class UserResponse(BaseModel):
    id: int
    email: EmailStr


class SentimentResponse(SentimentBase):
    id: int
    recommendation: dict
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)

class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None