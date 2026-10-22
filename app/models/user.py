from sqlalchemy import Column, String, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.db.session import Base
import uuid
from ..enums.user_role import UserRole


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
