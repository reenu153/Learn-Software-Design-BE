from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    order_index = Column(Integer)

    course_path_id = Column(Integer, ForeignKey("course_paths.id"))

    course_path = relationship("CoursePath", back_populates="modules")
    questions = relationship("Question", back_populates="module", cascade="all, delete")

class CoursePath(Base):
    __tablename__ = "course_paths"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    difficulty_level = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    modules = relationship("Module", back_populates="course_path", cascade="all, delete")