# File: app/schemas/lecture.py
"""
Pydantic schemas for Lecture API operations.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class TranscriptionStatus(str, Enum):
    PENDING = "pending"
    TRANSCRIBING = "transcribing"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerationStatus(str, Enum):
    NOT_STARTED = "not_started"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class LectureCreate(BaseModel):
    """Schema for creating a lecture."""
    title: str = Field(..., description="Lecture title", max_length=300)
    description: Optional[str] = Field(None, description="Lecture description")
    lecture_date: Optional[datetime] = Field(None, description="When the lecture was held")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Introduction to Binary Trees",
                "description": "Covers basic tree concepts and binary tree operations",
                "lecture_date": "2024-01-15T10:00:00Z"
            }
        }


class LectureResponse(BaseModel):
    """Full lecture response."""
    id: str
    course_id: str
    teacher_id: str
    title: str
    description: Optional[str] = None
    lecture_date: Optional[datetime] = None
    audio_filename: Optional[str] = None
    audio_duration_seconds: Optional[float] = None
    transcription_status: TranscriptionStatus
    generation_status: GenerationStatus
    created_at: datetime
    transcribed_at: Optional[datetime] = None
    generated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LectureListResponse(BaseModel):
    """List of lectures response."""
    lectures: List[LectureResponse]
    total: int


class TranscriptResponse(BaseModel):
    """Transcript response."""
    lecture_id: str
    transcript: Optional[str] = None
    segments: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Transcript segments with timestamps"
    )
    status: TranscriptionStatus


class TranscribeRequest(BaseModel):
    """Request to trigger transcription."""
    force: bool = Field(
        default=False,
        description="Force re-transcription even if already done"
    )


class GenerateRequest(BaseModel):
    """Request to trigger content generation."""
    content_types: List[str] = Field(
        default=["notes", "assignment", "flashcards"],
        description="Types of content to generate"
    )
    force: bool = Field(
        default=False,
        description="Force regeneration even if already done"
    )
