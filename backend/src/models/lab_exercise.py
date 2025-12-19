from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ARRAY
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class LabExercise(Base, TimestampMixin):
    __tablename__ = "lab_exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    module_id = Column(UUID(as_uuid=True), ForeignKey("textbook_modules.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    difficulty = Column(String(20), nullable=False)  # Enum values will be validated at application level
    instructions = Column(Text, nullable=False)
    code_samples = Column(ARRAY(String), default=[])  # Store as JSON strings
    expected_outcomes = Column(ARRAY(String), default=[])
    prerequisites = Column(ARRAY(String), default=[])
    simulation_required = Column(Boolean, default=False)
    estimated_duration = Column(Integer)  # in minutes
    is_published = Column(Boolean, default=False)

    # Relationships
    module = relationship("TextbookModule", back_populates="lab_exercises")
    learning_resources = relationship("LearningResource", back_populates="lab_exercise")


# Add the back_populates relationship to TextbookModule
from .textbook_module import TextbookModule

TextbookModule.lab_exercises = relationship("LabExercise", back_populates="module")