from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import ModuleCreate
from app.services import module_service
from app.api.deps import require_instructor

router = APIRouter(prefix="/module", tags=["Module"])


@router.post("/", dependencies=[Depends(require_instructor)])
async def create_module(module: ModuleCreate, db: AsyncSession = Depends(get_db)):
    return await module_service.create_module(db, module)

@router.get("/course")
async def get_modules_for_course(course_path_id: UUID, db: AsyncSession = Depends(get_db)):
    return await module_service.list_modules_for_course(db, course_path_id)

@router.get("/")
async def get_module(module_id: UUID, db: AsyncSession = Depends(get_db)):
    module = await module_service.get_module(db, module_id)
    return [module] if module else []