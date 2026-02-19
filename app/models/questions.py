from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))
    question_text = Column(Text, nullable=False)
    difficulty = Column(String(50))

    module_id = Column(Integer, ForeignKey("modules.id"))

    module = relationship("Module", back_populates="questions")
    prompts = relationship("Prompt", back_populates="question", cascade="all, delete")

    submissions = relationship(
        "StudentSubmission",
        back_populates="question",
        cascade="all, delete"   
    )
