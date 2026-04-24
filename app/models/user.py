from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from ..database import Base
import enum, uuid
from ..enums.progress_status import ProgressStatus

class UserRole(str, enum.Enum):
    student = "student"
    instructor = "instructor"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,default=uuid.uuid4)
  
    username = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        SQLAlchemyEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.student
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    progress_records = relationship(
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

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)

    solution_text = Column(Text, nullable=False)

    ai_feedback = Column(Text, nullable=True)
    grade = Column(String(50), nullable=True)
    passed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    question = relationship("Question", back_populates="submissions")


class StudentQuestionProgress(Base):
    __tablename__ = "student_question_progress"

    id = Column(Integer, primary_key=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)

    status = Column(
        SQLAlchemyEnum(ProgressStatus, name="progress_status"),
        default=ProgressStatus.not_started,
        nullable=False
    )

    attempts = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0,nullable=True)

    last_attempt_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress_records")
    question = relationship("Question", back_populates="progress_records")

