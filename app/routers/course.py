from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/")
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.CoursePath(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    return db.query(models.CoursePath).all()
