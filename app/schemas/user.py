from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: int
    username: str

class UserResponse(UserBase):
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(UserBase):  # Used when creating a new user
    pass


