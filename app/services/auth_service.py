from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AppError, AuthError
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.schemas import UserCreate


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def authenticate(db: AsyncSession, username: str, password: str) -> str:
    user = await get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise AuthError("Invalid credentials")
    return create_access_token({"sub": str(user.id)})


async def register(db: AsyncSession, data: UserCreate) -> dict:
    if await get_user_by_username(db, data.username):
        raise AppError("username already registered")

    user = User(
        username=data.username,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "access_token": create_access_token({"sub": str(user.id)}),
    }