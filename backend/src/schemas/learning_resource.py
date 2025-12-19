from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class LearningResourceBase(BaseModel):
    title: str
    resource_type: str  # e.g., 'code_sample', 'diagram', 'simulation_config', 'documentation', 'video', 'dataset'
    content: Optional[str] = None
    file_path: Optional[str] = None
    module_id: Optional[UUID] = None
    lab_exercise_id: Optional[UUID] = None
    capstone_project_id: Optional[UUID] = None
    tags: List[str] = []
    is_published: bool = False


class LearningResourceCreate(LearningResourceBase):
    pass


class LearningResourceUpdate(BaseModel):
    title: Optional[str] = None
    resource_type: Optional[str] = None
    content: Optional[str] = None
    file_path: Optional[str] = None
    module_id: Optional[UUID] = None
    lab_exercise_id: Optional[UUID] = None
    capstone_project_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None


class LearningResourceResponse(LearningResourceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True