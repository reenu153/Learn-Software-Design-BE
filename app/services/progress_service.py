from datetime import datetime
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.enums.progress_status import ProgressStatus
from app.models import Module, Question, StudentQuestionProgress


async def get_module_progress(db: AsyncSession, user_id: UUID, course_path_id: UUID) -> list[dict]:
    total_xp = (
        select(func.coalesce(func.sum(Question.points), 0))
        .where(Question.module_id == Module.id)
        .correlate(Module)
        .scalar_subquery()
    )
    earned_xp = (
        select(func.coalesce(func.sum(StudentQuestionProgress.xp_earned), 0))
        .join(Question, Question.id == StudentQuestionProgress.question_id)
        .where(Question.module_id == Module.id, StudentQuestionProgress.user_id == user_id)
        .correlate(Module)
        .scalar_subquery()
    )
    query = (
        select(
            Module.id,
            Module.title,
            Module.description,
            Module.order_index,
            earned_xp.label("earned_xp"),
            total_xp.label("total_xp"),
        )
        .where(Module.course_path_id == course_path_id)
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
    result = await db.execute(
        select(StudentQuestionProgress).where(
            StudentQuestionProgress.user_id == user_id,
            StudentQuestionProgress.question_id == question.id,
        )
    )
    progress = result.scalar_one_or_none()

    if progress is None:
        progress = StudentQuestionProgress(
            user_id=user_id, question_id=question.id, attempts=0, xp_earned=0
        )
        db.add(progress)

    now = datetime.utcnow()
    progress.attempts += 1
    progress.last_attempt_at = now

    if progress.status != ProgressStatus.completed:
        if passed:
            progress.status = ProgressStatus.completed
            progress.xp_earned = question.points
            progress.completed_at = now
        else:
            progress.status = ProgressStatus.in_progress

    await db.commit()
    return progress