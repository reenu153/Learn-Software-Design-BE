# app/routers/submissions.py

from fastapi import APIRouter
from app.schemas import EvaluationRequest, EvaluationResponse
from app.services.llm_service import evaluate_solution
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from sqlalchemy.orm import selectinload
from ..database import get_db
from app.models import User, Question, Module
from ..models.user import StudentQuestionProgress, StudentSubmission
from .login import get_current_user
from uuid import UUID

router = APIRouter()

@router.get("/progress")
async def get_my_progress(
    course_path_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
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
            (StudentQuestionProgress.question_id == Question.id) &
            (StudentQuestionProgress.user_id == current_user.id)
        )
        .where(Module.course_path_id == course_path_id)
        .group_by(
            Module.id,
            Module.title,
            Module.description,
            Module.order_index
        )
        .order_by(Module.order_index)
    )

    result = await db.execute(query)
    rows = result.all()

    modules = []

    for r in rows:
        earned_xp = r.earned_xp or 0
        total_xp = r.total_xp or 0

        progress_percent = 0
        if total_xp > 0:
            progress_percent = round((earned_xp / total_xp) * 100)

        modules.append({
            "module_id": r.id,
            "title": r.title,
            "description": r.description,
            "order_index": r.order_index,
            "earned_xp": earned_xp,
            "total_xp": total_xp,
            "progress_percent": progress_percent
        })

    return modules


@router.post("/evaluate")
async def evaluate(request: EvaluationRequest,current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
 
    submission = StudentSubmission(
        user_id=current_user.id,
        question_id=request.question_id,
        solution_text=request.solution
    )

    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    result = await db.execute(
    select(Question)
    .where(Question.id == request.question_id)
)

    question = result.scalar_one_or_none()

    if not question:    
        raise HTTPException(status_code=404, detail="Question not found")

    result = evaluate_solution(
        question.question_text,
        request.solution,
        question.prompt
    )

    # 3. Update submission record
    submission.ai_feedback = json.dumps(result["feedback"])
    submission.passed = result["passed"]

    await db.commit()

    # 4. Update progress table
    progress = StudentQuestionProgress(
        user_id=current_user.id,
        question_id=request.question_id,
        status="completed" if submission.passed else "in_progress",
        xp_earned=question.points if submission.passed else 0,
        attempts=1
    )

    db.add(progress)
    await db.commit()
    return {
        "submission_id": submission.id,
        "feedback": submission.ai_feedback,
        "passed": submission.passed
    }


@router.get("/progress")
async def get_my_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudentQuestionProgress)
        .where(StudentQuestionProgress.user_id == current_user.id)
    )

    return result.scalars().all()


@router.get("/questions/{question_id}/submissions")
async def get_submissions(
    question_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(StudentSubmission)
        .where(
            StudentSubmission.user_id == current_user.id,
            StudentSubmission.question_id == question_id
        )
    )

    return result.scalars().all()
