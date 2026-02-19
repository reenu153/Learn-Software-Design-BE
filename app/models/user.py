from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
import enum

class UserRole(str, enum.Enum):
    student = "student"
    instructor = "instructor"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        SQLAlchemyEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.student
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    solved_questions = relationship(
        "StudentQuestionProgress",
        back_populates="user",
        cascade="all, delete"
    )
    submissions = relationship(
        "StudentSubmission",
        back_populates="user",
        cascade="all, delete"
    )


class StudentSubmission(Base):
    __tablename__ = "student_submissions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    solution_text = Column(Text, nullable=False)

    ai_feedback = Column(Text, nullable=True)
    grade = Column(String(50), nullable=True)
    passed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    question = relationship("Question", back_populates="submissions")

