# File: app/models/course.py
"""
Course/Subject model for MongoDB.
"""
from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import Field


class Course(Document):
    """
    Represents a course/subject created by a teacher.
    """
    teacher_id: str = Field(..., description="Supabase user ID of the teacher")
    name: str = Field(..., description="Course name", max_length=200)
    code: str = Field(..., description="Course code (e.g., CS201)", max_length=20)
    description: Optional[str] = Field(None, description="Course description")
    semester: Optional[str] = Field(None, description="Semester (e.g., 'Fall 2024')")
    year: Optional[str] = Field(None, description="Academic year (e.g., 'SE', 'TE')")
    
    # Syllabus can be uploaded as text
    syllabus_content: Optional[str] = Field(None, description="Syllabus text content")
    
    # Enrolled students (list of Supabase user IDs)
    enrolled_students: List[str] = Field(default_factory=list)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "courses"
        
    class Config:
        json_schema_extra = {
            "example": {
                "teacher_id": "uuid-123",
                "name": "Data Structures and Algorithms",
                "code": "CS201",
                "description": "Fundamentals of data structures",
                "semester": "Fall 2024",
                "year": "SE"
            }
        }
