from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError
from app.models import Question
from app.schemas import QuestionCreate
from app.services import module_service


async def list_for_module(db: AsyncSession, module_id: UUID) -> list[Question]:
    result = await db.execute(select(Question).where(Question.module_id == module_id))
    return result.scalars().all()


async def get_question(db: AsyncSession, question_id: UUID) -> Question | None:
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalar_one_or_none()


async def create_question(db: AsyncSession, module_id: UUID, data: QuestionCreate) -> Question:
    if not await module_service.get_module(db, module_id):
        raise NotFoundError("Module not found")

    question = Question(module_id=module_id, **data.model_dump())
    db.add(question)
    await db.commit()
    return question
