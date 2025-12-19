from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ARRAY
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class LearningResource(Base, TimestampMixin):
    __tablename__ = "learning_resources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    resource_type = Column(String(50), nullable=False)  # Enum values will be validated at application level
    content = Column(Text)
    file_path = Column(String(500))
    module_id = Column(UUID(as_uuid=True), ForeignKey("textbook_modules.id"), nullable=True)
    lab_exercise_id = Column(UUID(as_uuid=True), ForeignKey("lab_exercises.id"), nullable=True)
    capstone_project_id = Column(UUID(as_uuid=True), ForeignKey("capstone_projects.id"), nullable=True)
    tags = Column(ARRAY(String), default=[])
    is_published = Column(Boolean, default=False)

    # Relationships
    module = relationship("TextbookModule", back_populates="learning_resources")
    lab_exercise = relationship("LabExercise", back_populates="learning_resources")
    capstone_project = relationship("CapstoneProject", back_populates="learning_resources")


# Add the back_populates relationships to TextbookModule, LabExercise, and CapstoneProject
