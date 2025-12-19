from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # Enum values will be validated at application level
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True))

    # Relationships
    user_progress = relationship("UserProgress", back_populates="user")
    user_lab_submissions = relationship("UserLabSubmission", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")