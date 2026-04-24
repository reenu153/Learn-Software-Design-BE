from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
import uuid

class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,default=uuid.uuid4)
    type = Column(String(50))
    question_text = Column(Text, nullable=False)
    difficulty = Column(String(50))
    points=Column(Integer, default=0)
    task_description = Column(Text, nullable=True)
    starter_diagram = Column(Text, nullable=True)
    prompt=Column(Text, nullable=False)

    module_id = Column(UUID(as_uuid=True), ForeignKey("modules.id"))

    module = relationship("Module", back_populates="questions")

    submissions = relationship(
        "StudentSubmission",
        back_populates="question",
        cascade="all, delete"   
    )

    progress_records = relationship(
    "StudentQuestionProgress",
    back_populates="question"
)
