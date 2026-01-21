# File: app/models/lecture.py
"""
Lecture model for MongoDB.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from beanie import Document
from pydantic import Field
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


class Lecture(Document):
    """
    Represents a lecture with audio transcription.
    """
    course_id: str = Field(..., description="Reference to the course")
    teacher_id: str = Field(..., description="Supabase user ID of the teacher")
    
    # Lecture info
    title: str = Field(..., description="Lecture title", max_length=300)
    description: Optional[str] = Field(None, description="Lecture description")
    lecture_date: Optional[datetime] = Field(None, description="When the lecture was held")
    
    # Audio file info
    audio_filename: Optional[str] = Field(None, description="Original audio filename")
    audio_path: Optional[str] = Field(None, description="Path to stored audio file")
    audio_duration_seconds: Optional[float] = Field(None, description="Audio duration")
    
    # Transcript
    transcript: Optional[str] = Field(None, description="Full transcript text")
    transcript_segments: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Transcript with timestamps [{start, end, text}]"
    )
    
    # Status tracking
    transcription_status: TranscriptionStatus = Field(
        default=TranscriptionStatus.PENDING,
        description="Audio transcription status"
    )
    transcription_error: Optional[str] = Field(None, description="Error if transcription failed")
    
    generation_status: GenerationStatus = Field(
        default=GenerationStatus.NOT_STARTED,
        description="Content generation status"
    )
    generation_error: Optional[str] = Field(None, description="Error if generation failed")
    
    # Vector store references (for transcript embeddings)
    embedding_ids: List[str] = Field(
        default_factory=list,
        description="ChromaDB document IDs for transcript embeddings"
    )
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    transcribed_at: Optional[datetime] = Field(None, description="When transcription completed")
    generated_at: Optional[datetime] = Field(None, description="When content generation completed")
    
    class Settings:
        name = "lectures"
        
    class Config:
        json_schema_extra = {
            "example": {
                "course_id": "course-uuid-123",
                "teacher_id": "user-uuid-456",
                "title": "Introduction to Binary Trees",
                "transcription_status": "pending",
                "generation_status": "not_started"
            }
        }
