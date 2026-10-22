from pydantic import BaseModel
from typing import Optional,Dict, Any
from uuid import UUID

class QuestionCreate(BaseModel):
    type: str
    question_text: str
    points: int
    starter_diagram: Optional[str] =  None
    difficulty: Optional[str] = None
    task_description: Optional[str] = None
    prompt: str


class QuestionResponse(QuestionCreate):
    id: UUID
    type:str
    difficulty:str
    points:int
    task_description: Optional[str]
    starter_diagram: Optional[str]
    question_text: str
    module_id: UUID
    diagram_to_fill: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True