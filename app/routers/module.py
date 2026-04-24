from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from .. import models, schemas
from uuid import UUID

router = APIRouter(prefix="/module", tags=["Module"])


@router.post("/")
async def create_modules(module: schemas.ModuleCreate, db: AsyncSession = Depends(get_db)):
    db_module = models.Module(**module.dict())
    db.add(db_module)
    await db.commit()
    await db.refresh(db_module)
    return db_module


@router.get("/course")
async def get_modules(course_path_id:UUID, db: AsyncSession = Depends(get_db)):
    statement = select(models.Module).where(models.Module.course_path_id == course_path_id)
    result = await db.execute(statement)
    return result.scalars().all()

@router.get("/")
async def get_modules(module_id:UUID, db: AsyncSession = Depends(get_db)):
    statement = select(models.Module).where(models.Module.id == module_id)
    result = await db.execute(statement)
    return result.scalars().all()
