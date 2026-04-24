from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Question, Module
from app.schemas import QuestionCreate, QuestionResponse
from typing import List
from uuid import UUID

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/module", response_model=List[QuestionResponse])
async def get_module_questions(module_id:UUID,db: AsyncSession = Depends(get_db)):
    statement = (
        select(Question)
        .where(Question.module_id == module_id)
    )

    result = await db.execute(statement)

    questions = result.scalars().all()

    return [QuestionResponse.model_validate(q) for q in questions]

@router.get("/",)
async def get_question(question_id:UUID,db: AsyncSession = Depends(get_db)):
    statement = select(Question).where(Question.id == question_id)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

@router.post("/module", response_model=QuestionResponse)
async def create_question(
    module_id: UUID,
    question_data: QuestionCreate,
    db: AsyncSession = Depends(get_db),
):
    # 1️⃣ Check module exists
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # 2️⃣ Create Question
    new_question = Question(
        type=question_data.type,
        question_text=question_data.question_text,
        difficulty=question_data.difficulty,
        points=question_data.points,
        module_id=module_id,
        task_description=question_data.task_description,
        starter_diagram=question_data.starter_diagram,
        prompt=question_data.prompt
    )

    db.add(new_question)
    await db.commit()
    return QuestionResponse.model_validate(new_question)


