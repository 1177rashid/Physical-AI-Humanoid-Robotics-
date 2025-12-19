from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class UserLabSubmission(Base, TimestampMixin):
    __tablename__ = "user_lab_submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    lab_exercise_id = Column(UUID(as_uuid=True), ForeignKey("lab_exercises.id"), nullable=False)
    submission_content = Column(Text, nullable=False)
    submission_files = Column(ARRAY(String), default=[])  # Store as JSON strings
    status = Column(String(20), nullable=False)  # Enum values will be validated at application level
    grade = Column(Integer)  # 0-100
    feedback = Column(Text)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    graded_at = Column(DateTime(timezone=True))

    # Relationships
    user = relationship("User", back_populates="user_lab_submissions")
    lab_exercise = relationship("LabExercise", back_populates="user_lab_submissions")