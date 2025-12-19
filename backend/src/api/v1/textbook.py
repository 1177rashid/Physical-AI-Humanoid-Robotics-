from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime

from pydantic import BaseModel
from ...services.content_service import TextbookService
from ...config.database import SessionLocal
from ...models.textbook_module import TextbookModule as TextbookModuleModel
from ...schemas.textbook import PaginatedTextbookModules


# Pydantic models for API responses
class TextbookModule(BaseModel):
    id: UUID
    title: str
    slug: str
    content: str
    category: str
    prerequisites: List[str]
    learning_objectives: List[str]
    estimated_duration: Optional[int]
    is_published: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LearningResource(BaseModel):
    id: UUID
    title: str
    resource_type: str
    content: Optional[str]
    file_path: Optional[str]
    module_id: Optional[UUID]
    lab_exercise_id: Optional[UUID]
    capstone_project_id: Optional[UUID]
    tags: List[str]
    is_published: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/", response_model=PaginatedTextbookModules)
async def get_textbook_modules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    published: bool = Query(True),
    db=Depends(get_db)
):
    """
    Get all textbook modules with optional filtering
    """
    modules, total = TextbookService.get_all_modules(
        db, skip=skip, limit=limit, category=category, published=published
    )

    return PaginatedTextbookModules(
        data=modules,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{module_id}", response_model=TextbookModule)
async def get_textbook_module(module_id: UUID, db=Depends(get_db)):
    """
    Get a specific textbook module by ID
    """
    module = TextbookService.get_module_by_id(db, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.get("/{module_id}/resources")
async def get_module_resources(module_id: UUID, db=Depends(get_db)):
    """
    Get all learning resources associated with a specific module
    """
    # Validate that the module exists
    module = TextbookService.get_module_by_id(db, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    resources = TextbookService.get_module_resources(db, module_id)
    return resources


@router.post("/", response_model=TextbookModule)
async def create_textbook_module(
    title: str,
    slug: str,
    content: str,
    category: str,
    prerequisites: List[str] = [],
    learning_objectives: List[str] = [],
    estimated_duration: Optional[int] = None,
    is_published: bool = False,
    db=Depends(get_db)
):
    """
    Create a new textbook module
    """
    try:
        # Validate category
        valid_categories = ['foundations', 'ros2-nervous-system', 'digital-twins', 'nvidia-isaac', 'vision-language-action', 'humanoid-control', 'capstone']
        if category not in valid_categories:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid category. Must be one of: {valid_categories}"
            )

        # Validate title length
        if not title or len(title.strip()) < 3:
            raise HTTPException(
                status_code=422,
                detail="Title must be at least 3 characters long"
            )

        # Validate slug format
        if not slug or len(slug.strip()) < 3:
            raise HTTPException(
                status_code=422,
                detail="Slug must be at least 3 characters long"
            )

        # Validate content length
        if not content or len(content.strip()) < 10:
            raise HTTPException(
                status_code=422,
                detail="Content must be at least 10 characters long"
            )

        module = TextbookService.create_module(
            db, title=title, slug=slug, content=content, category=category,
            prerequisites=prerequisites, learning_objectives=learning_objectives,
            estimated_duration=estimated_duration, is_published=is_published
        )
        return module
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{module_id}", response_model=TextbookModule)
async def update_textbook_module(
    module_id: UUID,
    title: Optional[str] = None,
    slug: Optional[str] = None,
    content: Optional[str] = None,
    category: Optional[str] = None,
    prerequisites: Optional[List[str]] = None,
    learning_objectives: Optional[List[str]] = None,
    estimated_duration: Optional[int] = None,
    is_published: Optional[bool] = None,
    db=Depends(get_db)
):
    """
    Update an existing textbook module
    """
    try:
        # Check if module exists
        existing_module = TextbookService.get_module_by_id(db, module_id)
        if not existing_module:
            raise HTTPException(status_code=404, detail="Module not found")

        # Validate category if provided
        if category:
            valid_categories = ['foundations', 'ros2-nervous-system', 'digital-twins', 'nvidia-isaac', 'vision-language-action', 'humanoid-control', 'capstone']
            if category not in valid_categories:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid category. Must be one of: {valid_categories}"
                )

        # Validate title if provided
        if title and len(title.strip()) < 3:
            raise HTTPException(
                status_code=422,
                detail="Title must be at least 3 characters long"
            )

        # Validate slug if provided
        if slug and len(slug.strip()) < 3:
            raise HTTPException(
                status_code=422,
                detail="Slug must be at least 3 characters long"
            )

        # Validate content if provided
        if content and len(content.strip()) < 10:
            raise HTTPException(
                status_code=422,
                detail="Content must be at least 10 characters long"
            )

        updated_module = TextbookService.update_module(
            db, module_id, title=title, slug=slug, content=content,
            category=category, prerequisites=prerequisites,
            learning_objectives=learning_objectives,
            estimated_duration=estimated_duration, is_published=is_published
        )

        if not updated_module:
            raise HTTPException(status_code=404, detail="Module not found after update attempt")

        return updated_module
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{module_id}")
async def delete_textbook_module(module_id: UUID, db=Depends(get_db)):
    """
    Delete a textbook module
    """
    try:
        success = TextbookService.delete_module(db, module_id)
        if not success:
            raise HTTPException(status_code=404, detail="Module not found")
        return {"message": "Module deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")