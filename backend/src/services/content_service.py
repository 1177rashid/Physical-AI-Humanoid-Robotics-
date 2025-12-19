from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func
from uuid import UUID
import uuid

from ..models.textbook_module import TextbookModule
from ..models.learning_resource import LearningResource
from ..models.lab_exercise import LabExercise
from ..utils.error_handler import CustomException, ErrorCode


class TextbookService:
    @staticmethod
    def get_all_modules(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        published: bool = True
    ) -> tuple[List[TextbookModule], int]:
        """Get all textbook modules with optional filtering"""
        query = select(TextbookModule)

        # Apply filters
        if published is not None:
            query = query.where(TextbookModule.is_published == published)
        if category:
            query = query.where(TextbookModule.category == category)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = db.execute(count_query).scalar()

        # Apply pagination
        query = query.offset(skip).limit(limit)

        modules = db.execute(query).scalars().all()
        return modules, total

    @staticmethod
    def get_module_by_id(db: Session, module_id: UUID) -> Optional[TextbookModule]:
        """Get a textbook module by its ID"""
        query = select(TextbookModule).where(TextbookModule.id == module_id)
        return db.execute(query).scalar_one_or_none()

    @staticmethod
    def create_module(db: Session, title: str, slug: str, content: str, category: str,
                     prerequisites: List[str] = None, learning_objectives: List[str] = None,
                     estimated_duration: Optional[int] = None, is_published: bool = False) -> TextbookModule:
        """Create a new textbook module"""
        if prerequisites is None:
            prerequisites = []
        if learning_objectives is None:
            learning_objectives = []

        # Check if slug already exists
        existing_module = db.execute(
            select(TextbookModule).where(TextbookModule.slug == slug)
        ).scalar_one_or_none()

        if existing_module:
            raise CustomException(
                ErrorCode.RESOURCE_ALREADY_EXISTS,
                detail=f"Module with slug '{slug}' already exists"
            )

        db_module = TextbookModule(
            title=title,
            slug=slug,
            content=content,
            category=category,
            prerequisites=prerequisites,
            learning_objectives=learning_objectives,
            estimated_duration=estimated_duration,
            is_published=is_published
        )

        db.add(db_module)
        db.commit()
        db.refresh(db_module)

        return db_module

    @staticmethod
    def update_module(db: Session, module_id: UUID, title: Optional[str] = None,
                     slug: Optional[str] = None, content: Optional[str] = None,
                     category: Optional[str] = None, prerequisites: Optional[List[str]] = None,
                     learning_objectives: Optional[List[str]] = None,
                     estimated_duration: Optional[int] = None,
                     is_published: Optional[bool] = None) -> Optional[TextbookModule]:
        """Update a textbook module"""
        db_module = TextbookService.get_module_by_id(db, module_id)
        if not db_module:
            return None

        # Update fields if provided
        if title is not None:
            db_module.title = title
        if slug is not None:
            db_module.slug = slug
        if content is not None:
            db_module.content = content
        if category is not None:
            db_module.category = category
        if prerequisites is not None:
            db_module.prerequisites = prerequisites
        if learning_objectives is not None:
            db_module.learning_objectives = learning_objectives
        if estimated_duration is not None:
            db_module.estimated_duration = estimated_duration
        if is_published is not None:
            db_module.is_published = is_published

        db.commit()
        db.refresh(db_module)
        return db_module

    @staticmethod
    def delete_module(db: Session, module_id: UUID) -> bool:
        """Delete a textbook module"""
        db_module = TextbookService.get_module_by_id(db, module_id)
        if not db_module:
            return False

        db.delete(db_module)
        db.commit()
        return True

    @staticmethod
    def get_module_resources(db: Session, module_id: UUID) -> List[LearningResource]:
        """Get all learning resources associated with a module"""
        query = select(LearningResource).where(
            LearningResource.module_id == module_id
        )
        return db.execute(query).scalars().all()

    @staticmethod
    def get_resources_by_module_category(db: Session, category: str) -> List[LearningResource]:
        """Get all learning resources for modules in a specific category"""
        query = select(LearningResource).join(TextbookModule).where(
            and_(
                TextbookModule.category == category,
                TextbookModule.id == LearningResource.module_id
            )
        )
        return db.execute(query).scalars().all()


class LabService:
    @staticmethod
    def get_lab_exercises_by_module(db: Session, module_id: UUID) -> List[LabExercise]:
        """Get all lab exercises associated with a module"""
        query = select(LabExercise).where(LabExercise.module_id == module_id)
        return db.execute(query).scalars().all()

    @staticmethod
    def get_lab_exercise_by_id(db: Session, lab_id: UUID) -> Optional[LabExercise]:
        """Get a lab exercise by its ID"""
        query = select(LabExercise).where(LabExercise.id == lab_id)
        return db.execute(query).scalar_one_or_none()


class LearningResourceService:
    @staticmethod
    def get_resource_by_id(db: Session, resource_id: UUID) -> Optional[LearningResource]:
        """Get a learning resource by its ID"""
        query = select(LearningResource).where(LearningResource.id == resource_id)
        return db.execute(query).scalar_one_or_none()

    @staticmethod
    def create_resource(db: Session, title: str, resource_type: str, content: Optional[str] = None,
                       file_path: Optional[str] = None, module_id: Optional[UUID] = None,
                       lab_exercise_id: Optional[UUID] = None, capstone_project_id: Optional[UUID] = None,
                       tags: Optional[List[str]] = None, is_published: bool = False) -> LearningResource:
        """Create a new learning resource"""
        if tags is None:
            tags = []

        db_resource = LearningResource(
            title=title,
            resource_type=resource_type,
            content=content,
            file_path=file_path,
            module_id=module_id,
            lab_exercise_id=lab_exercise_id,
            capstone_project_id=capstone_project_id,
            tags=tags,
            is_published=is_published
        )

        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)

        return db_resource