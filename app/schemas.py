from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum
from uuid import UUID

class PromptCreate(BaseModel):
    prompt_text: str

class UserResponse(BaseModel):
    id: str
    username: str
    role: str


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

    class Config:
        from_attributes = True

class ModuleCreate(BaseModel):
    title: str
    description: Optional[str]
    order_index: int
    course_path_id: str
    points: Optional[int] = 0


class CourseCreate(BaseModel):
    title: str
    description: Optional[str]
    difficulty_level: Optional[str]

class EvaluationRequest(BaseModel):
    # question_id:str
    question_id: UUID
    solution: str


class EvaluationResponse(BaseModel):
    feedback: str
    passed: bool
    grade: str | None = None


class UserRole(str, Enum):
    student = "student"
    instructor = "instructor"


class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.student


class UserResponse(BaseModel):
    id: UUID
    username: str
    role: UserRole

    class Config:
        from_attributes = True

class SubmissionRequest(BaseModel):
    question_id: str
    solution_text: str

class LoginRequest(BaseModel):
    username: str
    password: str