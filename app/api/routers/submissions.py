from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas import EvaluationRequest, HintRequest
from app.services import progress_service, submission_service

router = APIRouter()

@router.get("/progress")
async def get_my_progress(
    course_path_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await progress_service.get_module_progress(db, current_user.id, course_path_id)


@router.post("/evaluate-diagram")
async def evaluate_diagram(
    request: EvaluationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await submission_service.evaluate_submission(db, current_user, request)


@router.post("/submissions/took-hint")
async def mark_took_hint(
    body: HintRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await submission_service.mark_took_hint(db, current_user, body.submission_id)


@router.get("/questions/{question_id}/submissions")
async def get_submissions(
    question_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await submission_service.list_submissions(db, current_user, question_id)