# File: app/models/content.py
"""
Generated Content model for MongoDB.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from beanie import Document
from pydantic import Field
from enum import Enum


class ContentType(str, Enum):
    NOTES = "notes"
    ASSIGNMENT = "assignment"
    FLASHCARDS = "flashcards"


class GeneratedContent(Document):
    """
    Represents AI-generated content (notes, assignments, flashcards).
    """
    lecture_id: str = Field(..., description="Reference to the lecture")
    course_id: str = Field(..., description="Reference to the course")
    content_type: ContentType = Field(..., description="Type of content")
    
    # Content in JSON format
    content: Dict[str, Any] = Field(
        ...,
        description="Generated content in structured JSON format"
    )
    
    # Example content structures:
    # Notes: {
    #   "title": "Lecture Notes: Binary Trees",
    #   "summary": "...",
    #   "sections": [{"heading": "...", "content": "...", "key_points": [...]}],
    #   "key_takeaways": [...]
    # }
    #
    # Assignment: {
    #   "title": "Practice Questions",
    #   "questions": [
    #     {"type": "mcq", "question": "...", "options": [...], "answer": "...", "explanation": "..."},
    #     {"type": "short_answer", "question": "...", "answer": "..."},
    #     {"type": "long_answer", "question": "...", "rubric": "..."}
    #   ]
    # }
    #
    # Flashcards: {
    #   "title": "Flashcards: Binary Trees",
    #   "cards": [
    #     {"front": "What is a binary tree?", "back": "..."},
    #     {"front": "...", "back": "..."}
    #   ]
    # }
    
    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Generation metadata (model used, tokens, etc.)"
    )
    
    # Versioning (for edits)
    version: int = Field(default=1, description="Content version number")
    is_edited: bool = Field(default=False, description="Whether content was manually edited")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "generated_content"
        
    class Config:
        json_schema_extra = {
            "example": {
                "lecture_id": "lecture-uuid-123",
                "course_id": "course-uuid-456",
                "content_type": "notes",
                "content": {
                    "title": "Lecture Notes: Binary Trees",
                    "summary": "Introduction to binary tree data structures",
                    "sections": []
                }
            }
        }
