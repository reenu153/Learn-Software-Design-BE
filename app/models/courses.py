from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from ..database import Base
import uuid

class Module(Base):
    __tablename__ = "modules"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,default=uuid.uuid4)
    title = Column(String(255))
    description = Column(Text)
    order_index = Column(Integer)
    points= Column(Integer, default=0)

    course_path_id = Column(UUID(as_uuid=True), ForeignKey("course_paths.id"))

    course_path = relationship("CoursePath", back_populates="modules")
    questions = relationship("Question", back_populates="module", cascade="all, delete")

class CoursePath(Base):
    __tablename__ = "course_paths"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True,default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    difficulty_level = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    modules = relationship("Module", back_populates="course_path", cascade="all, delete")