from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import QuestionCreate, QuestionResponse
from app.services import question_service
from app.api.deps import require_instructor

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/module", response_model=List[QuestionResponse])
async def get_module_questions(module_id: UUID, db: AsyncSession = Depends(get_db)):
    return await question_service.list_for_module(db, module_id)


@router.get("/")
async def get_question(question_id: UUID, db: AsyncSession = Depends(get_db)):
    return await question_service.get_question(db, question_id)


@router.post("/module", response_model=QuestionResponse, dependencies=[Depends(require_instructor)])
async def create_question(
    module_id: UUID,
    question_data: QuestionCreate,
    db: AsyncSession = Depends(get_db),
):
    return await question_service.create_question(db, module_id, question_data)