# File: app/schemas/material.py
"""
Pydantic schemas for Material API operations.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class MaterialType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    TXT = "txt"
    MD = "md"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class MaterialUploadResponse(BaseModel):
    """Response after uploading material."""
    id: str = Field(..., description="Material ID")
    course_id: str
    filename: str
    file_type: MaterialType
    processing_status: ProcessingStatus
    message: str = "Material uploaded successfully"

    class Config:
        from_attributes = True


class MaterialResponse(BaseModel):
    """Full material response."""
    id: str
    course_id: str
    teacher_id: str
    filename: str
    file_type: MaterialType
    file_size_bytes: Optional[int] = None
    content: Optional[str] = None
    metadata: Dict[str, Any] = {}
    processing_status: ProcessingStatus
    processing_error: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MaterialListResponse(BaseModel):
    """List of materials response."""
    materials: List[MaterialResponse]
    total: int


class MaterialMetadata(BaseModel):
    """Metadata for a material (used for grounding LLM)."""
    topics: List[str] = Field(default_factory=list, description="Main topics covered")
    keywords: List[str] = Field(default_factory=list, description="Important keywords")
    difficulty_level: Optional[str] = Field(None, description="e.g., 'beginner', 'intermediate', 'advanced'")
    estimated_duration_minutes: Optional[int] = Field(None, description="Estimated reading time")
