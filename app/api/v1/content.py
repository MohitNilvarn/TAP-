# File: app/api/v1/content.py
"""
Generated content retrieval and editing endpoints.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any, Optional
from datetime import datetime

from app.core.logger import get_logger
from app.core.dependencies import get_current_user, require_teacher
from app.schemas.content import (
    ContentResponse,
    ContentListResponse,
    ContentUpdateRequest,
    ContentType
)
from app.models.course import Course
from app.models.lecture import Lecture
from app.models.content import GeneratedContent, ContentType as ModelContentType

logger = get_logger("TAP.Content")
router = APIRouter()


@router.get("/lectures/{lecture_id}/notes", response_model=Optional[ContentResponse])
async def get_notes(
    lecture_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get generated notes for a lecture.
    """
    return await _get_content(lecture_id, ModelContentType.NOTES, current_user)


@router.get("/lectures/{lecture_id}/assignment", response_model=Optional[ContentResponse])
async def get_assignment(
    lecture_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get generated assignment for a lecture.
    """
    return await _get_content(lecture_id, ModelContentType.ASSIGNMENT, current_user)


@router.get("/lectures/{lecture_id}/flashcards", response_model=Optional[ContentResponse])
async def get_flashcards(
    lecture_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get generated flashcards for a lecture.
    """
    return await _get_content(lecture_id, ModelContentType.FLASHCARDS, current_user)


@router.get("/lectures/{lecture_id}/content", response_model=ContentListResponse)
async def get_all_content(
    lecture_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all generated content (notes, assignment, flashcards) for a lecture.
    """
    # Verify access
    lecture = await Lecture.get(lecture_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    await _verify_course_access(lecture.course_id, current_user)
    
    # Fetch all content
    notes = await GeneratedContent.find_one(
        GeneratedContent.lecture_id == lecture_id,
        GeneratedContent.content_type == ModelContentType.NOTES
    )
    
    assignment = await GeneratedContent.find_one(
        GeneratedContent.lecture_id == lecture_id,
        GeneratedContent.content_type == ModelContentType.ASSIGNMENT
    )
    
    flashcards = await GeneratedContent.find_one(
        GeneratedContent.lecture_id == lecture_id,
        GeneratedContent.content_type == ModelContentType.FLASHCARDS
    )
    
    return ContentListResponse(
        lecture_id=lecture_id,
        notes=_to_response(notes) if notes else None,
        assignment=_to_response(assignment) if assignment else None,
        flashcards=_to_response(flashcards) if flashcards else None
    )


@router.patch("/content/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: str,
    update_data: ContentUpdateRequest,
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Update/edit generated content. Teachers only.
    """
    content = await GeneratedContent.get(content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Verify ownership
    lecture = await Lecture.get(content.lecture_id)
    if not lecture or lecture.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Update content
    content.content = update_data.content
    content.is_edited = True
    content.version += 1
    content.updated_at = datetime.utcnow()
    
    await content.save()
    
    logger.info(f"Content updated: {content_id} (version {content.version})")
    
    return _to_response(content)


@router.delete("/content/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: str,
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Delete generated content. Teachers only.
    """
    content = await GeneratedContent.get(content_id)
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Verify ownership
    lecture = await Lecture.get(content.lecture_id)
    if not lecture or lecture.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    await content.delete()
    logger.info(f"Content deleted: {content_id}")


# Helper functions

async def _get_content(
    lecture_id: str,
    content_type: ModelContentType,
    current_user: Dict[str, Any]
) -> Optional[ContentResponse]:
    """Helper to get specific content type."""
    lecture = await Lecture.get(lecture_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    await _verify_course_access(lecture.course_id, current_user)
    
    content = await GeneratedContent.find_one(
        GeneratedContent.lecture_id == lecture_id,
        GeneratedContent.content_type == content_type
    )
    
    if not content:
        return None
    
    return _to_response(content)


async def _verify_course_access(course_id: str, current_user: Dict[str, Any]):
    """Verify user has access to course."""
    course = await Course.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user["role"] == "teacher" and course.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if current_user["role"] == "student" and current_user["id"] not in course.enrolled_students:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")


def _to_response(content: GeneratedContent) -> ContentResponse:
    """Convert model to response schema."""
    return ContentResponse(
        id=str(content.id),
        lecture_id=content.lecture_id,
        course_id=content.course_id,
        content_type=ContentType(content.content_type.value),
        content=content.content,
        metadata=content.metadata,
        version=content.version,
        is_edited=content.is_edited,
        created_at=content.created_at,
        updated_at=content.updated_at
    )
