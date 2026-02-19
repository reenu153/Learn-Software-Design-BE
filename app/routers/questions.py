from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Question, Module, Prompt
from app.schemas.question import QuestionCreate, QuestionResponse

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/module/{module_id}", response_model=QuestionResponse)
async def create_question(
    module_id: int,
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
        module_id=module_id,
    )

    db.add(new_question)
    await db.flush()  # important to get new_question.id

    # 3️⃣ Add Prompts (if any)
    for prompt in question_data.prompts:
        new_prompt = Prompt(
            prompt_text=prompt.prompt_text,
            question_id=new_question.id,
        )
        db.add(new_prompt)

    await db.commit()
    await db.refresh(new_question)

    return new_question
