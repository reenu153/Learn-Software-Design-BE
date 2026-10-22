from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Module
from app.schemas import ModuleCreate

async def create_module(db: AsyncSession, data: ModuleCreate) -> Module:
    module = Module(**data.model_dump())
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return module


async def list_modules_for_course(db: AsyncSession, course_path_id: UUID) -> list[Module]:
    result = await db.execute(select(Module).where(Module.course_path_id == course_path_id))
    return result.scalars().all()


async def get_module(db: AsyncSession, module_id: UUID) -> Module | None:
    result = await db.execute(select(Module).where(Module.id == module_id))
    return result.scalar_one_or_none()