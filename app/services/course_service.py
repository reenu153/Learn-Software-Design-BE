from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CoursePath
from app.schemas import CourseCreate


async def create_course(db: AsyncSession, data: CourseCreate) -> CoursePath:
    course = CoursePath(**data.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


async def list_courses(db: AsyncSession) -> list[CoursePath]:
    result = await db.execute(select(CoursePath))
    return result.scalars().all()