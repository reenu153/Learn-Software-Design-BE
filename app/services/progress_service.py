from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.enums.progress_status import ProgressStatus
from app.models import Module, Question, StudentQuestionProgress


async def get_module_progress(db: AsyncSession, user_id: UUID, course_path_id: UUID) -> list[dict]:
    query = (
        select(
            Module.id,
            Module.title,
            Module.description,
            Module.order_index,
            func.coalesce(func.sum(StudentQuestionProgress.xp_earned), 0).label("earned_xp"),
            func.coalesce(func.sum(func.distinct(Question.points)), 0).label("total_xp"),
        )
        .outerjoin(Question, Question.module_id == Module.id)
        .outerjoin(
            StudentQuestionProgress,
            (StudentQuestionProgress.question_id == Question.id)
            & (StudentQuestionProgress.user_id == user_id),
        )
        .where(Module.course_path_id == course_path_id)
        .group_by(Module.id, Module.title, Module.description, Module.order_index)
        .order_by(Module.order_index)
    )
    rows = (await db.execute(query)).all()

    modules = []
    for r in rows:
        earned_xp = r.earned_xp or 0
        total_xp = r.total_xp or 0
        progress_percent = round((earned_xp / total_xp) * 100) if total_xp > 0 else 0

        modules.append({
            "module_id": r.id,
            "title": r.title,
            "description": r.description,
            "order_index": r.order_index,
            "earned_xp": earned_xp,
            "total_xp": total_xp,
            "progress_percent": progress_percent,
        })
    return modules


async def record_attempt(
    db: AsyncSession, user_id: UUID, question: Question, passed: bool
) -> StudentQuestionProgress:
    progress = StudentQuestionProgress(
        user_id=user_id,
        question_id=question.id,
        status=ProgressStatus.completed if passed else ProgressStatus.in_progress,
        xp_earned=question.points if passed else 0,
        attempts=1,
    )
    db.add(progress)
    await db.commit()
    return progress