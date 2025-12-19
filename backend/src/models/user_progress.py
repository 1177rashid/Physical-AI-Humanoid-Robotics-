from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class UserProgress(Base, TimestampMixin):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    module_id = Column(UUID(as_uuid=True), ForeignKey("textbook_modules.id"), nullable=False)
    status = Column(String(20), nullable=False)  # Enum values will be validated at application level
    completion_percentage = Column(Integer, default=0)  # 0-100
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now())
    time_spent = Column(Integer, default=0)  # in seconds

    # Relationships
    user = relationship("User", back_populates="user_progress")
    module = relationship("TextbookModule", back_populates="user_progress")