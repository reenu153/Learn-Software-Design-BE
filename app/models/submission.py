from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean,JSON
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.session import Base
from ..enums.progress_status import ProgressStatus


class StudentSubmission(Base):
    __tablename__ = "student_submissions"

    id = Column(Integer, primary_key=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)

    solution_text = Column(Text, nullable=True)
    diagram_json = Column(JSON, nullable=True)
    solution_type = Column(String, nullable=True)   # text | mermaid | reactflow #TODO: make it an enum
    solution_text = Column(Text, nullable=True)
    solution_json = Column(JSON, nullable=True)
    took_hint = Column(Boolean, default=False)

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

