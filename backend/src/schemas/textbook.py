from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class TextbookModuleBase(BaseModel):
    title: str
    slug: str
    content: str
    category: str
    prerequisites: List[str] = []
    learning_objectives: List[str] = []
    estimated_duration: Optional[int] = None  # in minutes
    is_published: bool = False


class TextbookModuleCreate(TextbookModuleBase):
    pass


class TextbookModuleUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    prerequisites: Optional[List[str]] = None
    learning_objectives: Optional[List[str]] = None
    estimated_duration: Optional[int] = None
    is_published: Optional[bool] = None


class TextbookModuleResponse(TextbookModuleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedTextbookModules(BaseModel):
    data: List[TextbookModuleResponse]
    total: int
    skip: int
    limit: int