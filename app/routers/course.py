from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/")
async def create_course(course: schemas.CourseCreate, db: AsyncSession = Depends(get_db)):
    db_course = models.CoursePath(**course.dict())
    db.add(db_course)
    await db.commit()
    await db.refresh(db_course)
    return db_course


@router.get("/")
async def get_courses(db: AsyncSession = Depends(get_db)):
    statement = select(models.CoursePath)
    result = await db.execute(statement)
    return result.scalars().all()
