from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    preferences: Optional[dict] = {}

class UserResponse(CreateUser):
    user_id: int