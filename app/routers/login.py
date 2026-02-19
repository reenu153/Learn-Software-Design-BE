from passlib.context import CryptContext
from fastapi import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta

# move to env
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=2)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
async def login(user_data: LoginSchema, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": str(user.id), "role": user.role}
    )

    return {"access_token": token, "token_type": "bearer"}

def require_instructor(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.instructor:
        raise HTTPException(status_code=403, detail="Only instructors allowed")
    return current_user

