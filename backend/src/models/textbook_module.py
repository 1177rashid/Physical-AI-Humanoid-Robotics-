from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ARRAY
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class TextbookModule(Base, TimestampMixin):
    __tablename__ = "textbook_modules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # Enum values will be validated at application level
    prerequisites = Column(ARRAY(String), default=[])
    learning_objectives = Column(ARRAY(String), default=[])
    estimated_duration = Column(Integer)  # in minutes
    is_published = Column(Boolean, default=False)

    # Relationships
    lab_exercises = relationship("LabExercise", back_populates="module")
    learning_resources = relationship("LearningResource", back_populates="module")
    user_progress = relationship("UserProgress", back_populates="module")