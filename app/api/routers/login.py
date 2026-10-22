from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas import LoginRequest, UserCreate, UserResponse
from app.services import auth_service

router = APIRouter()


@router.post("/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    token = await auth_service.authenticate(db, req.username, req.password)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await auth_service.register(db, user)


@router.post("/user")
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user