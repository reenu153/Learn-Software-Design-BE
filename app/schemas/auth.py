from pydantic import BaseModel
from uuid import UUID
from app.enums.user_role import UserRole
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    role: UserRole
    access_token: str

    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: UUID
    username: str
    role: UserRole
    created_at: datetime | None = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str