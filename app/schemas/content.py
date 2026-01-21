# File: app/schemas/content.py
"""
Pydantic schemas for Generated Content API operations.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ContentType(str, Enum):
    NOTES = "notes"
    ASSIGNMENT = "assignment"
    FLASHCARDS = "flashcards"


# =====================
# Notes Schema
# =====================
class NoteSection(BaseModel):
    """A section within lecture notes."""
    heading: str
    content: str
    key_points: List[str] = []


class NotesContent(BaseModel):
    """Structured notes content."""
    title: str
    summary: str
    sections: List[NoteSection]
    key_takeaways: List[str] = []


# =====================
# Assignment Schema
# =====================
class MCQQuestion(BaseModel):
    """Multiple choice question."""
    type: str = "mcq"
    question: str
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None


class ShortAnswerQuestion(BaseModel):
    """Short answer question."""
    type: str = "short_answer"
    question: str
    expected_answer: str
    keywords: List[str] = []


class LongAnswerQuestion(BaseModel):
    """Long answer/essay question."""
    type: str = "long_answer"
    question: str
    rubric: Optional[str] = None
    points: Optional[int] = None


class AssignmentContent(BaseModel):
    """Structured assignment content."""
    title: str
    description: Optional[str] = None
    total_points: Optional[int] = None
    questions: List[Dict[str, Any]]  # Can be MCQ, short, or long answer


# =====================
# Flashcard Schema
# =====================
class Flashcard(BaseModel):
    """A single flashcard."""
    front: str = Field(..., description="Question or term")
    back: str = Field(..., description="Answer or definition")
    difficulty: Optional[str] = Field(None, description="easy/medium/hard")


class FlashcardsContent(BaseModel):
    """Structured flashcards content."""
    title: str
    description: Optional[str] = None
    cards: List[Flashcard]


# =====================
# API Response Schemas
# =====================
class ContentResponse(BaseModel):
    """Response for generated content."""
    id: str
    lecture_id: str
    course_id: str
    content_type: ContentType
    content: Dict[str, Any]
    metadata: Dict[str, Any] = {}
    version: int
    is_edited: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentListResponse(BaseModel):
    """List of content for a lecture."""
    lecture_id: str
    notes: Optional[ContentResponse] = None
    assignment: Optional[ContentResponse] = None
    flashcards: Optional[ContentResponse] = None


class ContentUpdateRequest(BaseModel):
    """Request to update/edit content."""
    content: Dict[str, Any] = Field(..., description="Updated content")


class GenerationStatusResponse(BaseModel):
    """Status of content generation."""
    lecture_id: str
    status: str
    notes_generated: bool = False
    assignment_generated: bool = False
    flashcards_generated: bool = False
    error: Optional[str] = None
