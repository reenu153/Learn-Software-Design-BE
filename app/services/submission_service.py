import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import AppError, NotFoundError
from app.llm.client import evaluate_solution
from app.models import Question, StudentSubmission, User
from app.schemas import EvaluationRequest
from app.services import progress_service, question_service
from app.helpers.generate_textual_repr import generate_text
from uuid import UUID


def normalize_solution(request: EvaluationRequest) -> str:
    if request.solution_type == "text":
        return request.solution_text
    if request.solution_type == "mermaid":
        return request.mermaid_code
    if request.solution_type == "reactflow":
        return generate_text(request.graph)
    raise AppError("Invalid solution type")


def build_question_context(question: Question) -> str:
    parts = []
    if question.question_text:
        parts.append(f"QUESTION:\n{question.question_text}")
    if question.task_description:
        parts.append(f"TASK DESCRIPTION:\n{question.task_description}")
    if question.starter_diagram:
        parts.append(f"STARTER DIAGRAM:\n{question.starter_diagram}")
    return "\n\n".join(parts)


async def evaluate_submission(db: AsyncSession, user: User, request: EvaluationRequest) -> dict:
    normalized = normalize_solution(request)

    submission = StudentSubmission(
        user_id=user.id,
        question_id=request.question_id,
        solution_type=request.solution_type,
        solution_text=request.solution_text if request.solution_type == "text" else None,
        solution_json=request.graph if request.solution_type == "reactflow" else None,
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    question = await question_service.get_question(db, request.question_id)
    if not question:
        raise NotFoundError("Question not found")

    result = evaluate_solution(build_question_context(question), normalized, question.prompt)
    submission.ai_feedback = json.dumps(result["feedback"])
    submission.passed = result["passed"]
    await db.commit()

    await progress_service.record_attempt(db, user.id, question, submission.passed)

    return {
        "submission_id": submission.id,
        "feedback": submission.ai_feedback,
        "passed": submission.passed,
    }

async def mark_took_hint(db: AsyncSession, user: User, submission_id: int) -> dict:
    result = await db.execute(
        select(StudentSubmission).where(
            StudentSubmission.id == submission_id,
            StudentSubmission.user_id == user.id,
        )
    )
    submission = result.scalar_one_or_none()
    if not submission:
        raise NotFoundError("Submission not found")

    if submission.took_hint:
        return {"updated": False, "message": "Already marked"}

    submission.took_hint = True
    await db.commit()
    return {"updated": True}


async def list_submissions(db: AsyncSession, user: User, question_id: UUID) -> list[StudentSubmission]:
    result = await db.execute(
        select(StudentSubmission).where(
            StudentSubmission.user_id == user.id,
            StudentSubmission.question_id == question_id,
        )
    )
    return result.scalars().all()