# File: app/schemas/course.py
"""
Pydantic schemas for Course API operations.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    """Schema for creating a new course."""
    name: str = Field(..., description="Course name", max_length=200)
    code: str = Field(..., description="Course code (e.g., CS201)", max_length=20)
    description: Optional[str] = Field(None, description="Course description")
    semester: Optional[str] = Field(None, description="Semester (e.g., 'Fall 2024')")
    year: Optional[str] = Field(None, description="Academic year (e.g., 'SE', 'TE')")
    syllabus_content: Optional[str] = Field(None, description="Syllabus text content")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Data Structures and Algorithms",
                "code": "CS201",
                "description": "Fundamentals of data structures",
                "semester": "Fall 2024",
                "year": "SE"
            }
        }


class CourseUpdate(BaseModel):
    """Schema for updating a course."""
    name: Optional[str] = Field(None, max_length=200)
    code: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    semester: Optional[str] = None
    year: Optional[str] = None
    syllabus_content: Optional[str] = None


class CourseResponse(BaseModel):
    """Schema for course response."""
    id: str = Field(..., description="Course ID")
    teacher_id: str
    name: str
    code: str
    description: Optional[str] = None
    semester: Optional[str] = None
    year: Optional[str] = None
    syllabus_content: Optional[str] = None
    enrolled_students: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CourseListResponse(BaseModel):
    """Schema for listing courses."""
    courses: List[CourseResponse]
    total: int


class EnrollRequest(BaseModel):
    """Schema for enrolling a student."""
    student_id: str = Field(..., description="Student's Supabase user ID")
