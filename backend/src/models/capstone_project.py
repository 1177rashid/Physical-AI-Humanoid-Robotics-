from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ARRAY
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class CapstoneProject(Base, TimestampMixin):
    __tablename__ = "capstone_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    overview = Column(Text, nullable=False)
    requirements = Column(ARRAY(String), default=[])
    voice_integration_required = Column(Boolean, default=False)
    simulation_components = Column(ARRAY(String), default=[])
    evaluation_criteria = Column(ARRAY(String), default=[])
    estimated_duration = Column(Integer)  # in hours
    is_published = Column(Boolean, default=False)

    # Relationships
    learning_resources = relationship("LearningResource", back_populates="capstone_project")