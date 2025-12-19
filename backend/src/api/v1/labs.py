from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime

from pydantic import BaseModel
from ...services.content_service import LabService, TextbookService
from ...config.database import SessionLocal
from ...models.lab_exercise import LabExercise as LabExerciseModel
from ...models.user_lab_submission import UserLabSubmission as UserLabSubmissionModel


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


# Pydantic models for API responses
class LabExercise(BaseModel):
    id: UUID
    module_id: UUID
    title: str
    description: str
    difficulty: str
    instructions: str
    code_samples: List[str]
    expected_outcomes: List[str]
    prerequisites: List[str]
    simulation_required: bool
    estimated_duration: int
    is_published: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLabSubmission(BaseModel):
    id: UUID
    user_id: UUID
    lab_exercise_id: UUID
    submission_content: str
    submission_files: List[str]
    status: str
    grade: Optional[int]
    feedback: Optional[str]
    submitted_at: datetime
    graded_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/textbook/modules/{module_id}/labs", response_model=List[LabExercise])
async def get_labs_for_module(module_id: UUID, db=Depends(get_db)):
    """
    Get all lab exercises associated with a specific module
    """
    # Validate that the module exists
    module = TextbookService.get_module_by_id(db, module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    labs = LabService.get_lab_exercises_by_module(db, module_id)
    return labs


@router.get("/labs/{lab_id}", response_model=LabExercise)
async def get_lab_exercise_by_id(lab_id: UUID, db=Depends(get_db)):
    """
    Get a specific lab exercise by its ID
    """
    lab = LabService.get_lab_exercise_by_id(db, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab exercise not found")
    return lab


@router.post("/labs/submit", response_model=UserLabSubmission)
async def submit_lab_solution(
    lab_exercise_id: UUID,
    submission_content: str,
    submission_files: List[str] = [],
    user_id: Optional[UUID] = None,  # In a real app, this would come from auth
    db=Depends(get_db)
):
    """
    Submit a solution for a lab exercise
    """
    try:
        # Validate that the lab exercise exists
        lab = LabService.get_lab_exercise_by_id(db, lab_exercise_id)
        if not lab:
            raise HTTPException(status_code=404, detail="Lab exercise not found")

        # Validate submission content length
        if not submission_content or len(submission_content.strip()) < 10:
            raise HTTPException(
                status_code=422,
                detail="Submission content must be at least 10 characters long"
            )

        # Validate submission files count
        if len(submission_files) > 10:
            raise HTTPException(
                status_code=422,
                detail="Maximum of 10 files allowed per submission"
            )

        # In a real application, you would validate user_id and permissions
        # For now, we'll use a placeholder user_id if none is provided
        if not user_id:
            user_id = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")  # Placeholder

        # Create the submission
        submission = UserLabSubmissionModel(
            user_id=user_id,
            lab_exercise_id=lab_exercise_id,
            submission_content=submission_content,
            submission_files=submission_files,
            status="submitted",
            grade=None,
            feedback=None
        )

        db.add(submission)
        db.commit()
        db.refresh(submission)

        return submission
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail="Internal server error during submission")


@router.put("/labs/submissions/{submission_id}", response_model=UserLabSubmission)
async def update_lab_submission(
    submission_id: UUID,
    submission_content: Optional[str] = None,
    submission_files: Optional[List[str]] = None,
    status: Optional[str] = None,
    db=Depends(get_db)
):
    """
    Update a lab submission (for revisions or resubmissions)
    """
    try:
        # Get the existing submission
        from sqlalchemy import select
        stmt = select(UserLabSubmissionModel).where(UserLabSubmissionModel.id == submission_id)
        result = db.execute(stmt)
        submission = result.scalar_one_or_none()

        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found")

        # Update fields if provided
        if submission_content is not None:
            if len(submission_content.strip()) < 10:
                raise HTTPException(
                    status_code=422,
                    detail="Submission content must be at least 10 characters long"
                )
            submission.submission_content = submission_content

        if submission_files is not None:
            if len(submission_files) > 10:
                raise HTTPException(
                    status_code=422,
                    detail="Maximum of 10 files allowed per submission"
                )
            submission.submission_files = submission_files

        if status is not None:
            # Validate status value
            valid_statuses = ["submitted", "grading", "graded", "revised"]
            if status not in valid_statuses:
                raise HTTPException(
                    status_code=422,
                    detail=f"Status must be one of: {valid_statuses}"
                )
            submission.status = status

        db.commit()
        db.refresh(submission)

        return submission
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail="Internal server error during submission update")


@router.get("/users/{user_id}/submissions", response_model=List[UserLabSubmission])
async def get_user_submissions(user_id: UUID, db=Depends(get_db)):
    """
    Get all lab submissions for a specific user
    """
    # In a real app, you'd validate that the requesting user has permission to view these submissions
    query = "SELECT * FROM user_lab_submissions WHERE user_id = :user_id ORDER BY submitted_at DESC"
    # This is simplified - in reality, we'd use SQLAlchemy properly
    from sqlalchemy import select
    stmt = select(UserLabSubmissionModel).where(UserLabSubmissionModel.user_id == user_id)
    submissions = db.execute(stmt).scalars().all()
    return submissions


@router.get("/labs/{lab_id}/submissions", response_model=List[UserLabSubmission])
async def get_lab_submissions(lab_id: UUID, db=Depends(get_db)):
    """
    Get all submissions for a specific lab exercise
    """
    # Validate that the lab exercise exists
    lab = LabService.get_lab_exercise_by_id(db, lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab exercise not found")

    # In a real app, you'd validate permissions (only instructors can see all submissions)
    from sqlalchemy import select
    stmt = select(UserLabSubmissionModel).where(UserLabSubmissionModel.lab_exercise_id == lab_id)
    submissions = db.execute(stmt).scalars().all()
    return submissions