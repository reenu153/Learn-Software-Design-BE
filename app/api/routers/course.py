from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import CourseCreate
from app.services import course_service
from app.api.deps import require_instructor

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", dependencies=[Depends(require_instructor)])
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    return await course_service.create_course(db, course)

@router.get("/")
async def get_courses(db: AsyncSession = Depends(get_db)):
    return await course_service.list_courses(db)