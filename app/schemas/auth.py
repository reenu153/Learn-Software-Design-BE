from pydantic import BaseModel
from uuid import UUID
from app.enums.user_role import UserRole

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.student

class UserResponse(BaseModel):
    id: UUID
    username: str
    role: UserRole
    access_token: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str