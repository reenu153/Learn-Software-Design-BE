from pydantic import BaseModel
from typing import Optional, List, Dict


class PromptCreate(BaseModel):
    prompt_text: str
    prompt_type: str


class QuestionCreate(BaseModel):
    type: str
    question_text: str
    solution_text: Optional[str]
    difficulty: Optional[str]
    metadata: Optional[Dict]
    module_id: int

class PromptResponse(PromptCreate):
    id: int

    class Config:
        from_attributes = True


class QuestionResponse(QuestionCreate):
    id: int
    module_id: int
    prompts: List[PromptResponse]

    class Config:
        from_attributes = True



class ModuleCreate(BaseModel):
    title: str
    description: Optional[str]
    order_index: int
    course_path_id: int


class CourseCreate(BaseModel):
    title: str
    description: Optional[str]
    difficulty_level: Optional[str]
