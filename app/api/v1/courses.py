# File: app/api/v1/courses.py
"""
Course management endpoints for teachers.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any, List
from datetime import datetime
from beanie import PydanticObjectId

from app.core.logger import get_logger
from app.core.dependencies import get_current_user, require_teacher
from app.schemas.course import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseListResponse,
    EnrollRequest
)
from app.models.course import Course

logger = get_logger("TAP.Courses")
router = APIRouter()


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Create a new course. Teachers only.
    """
    logger.info(f"Creating course: {course_data.name} by teacher {current_user['id']}")
    
    # Check if course code already exists for this teacher
    existing = await Course.find_one(
        Course.teacher_id == current_user["id"],
        Course.code == course_data.code
    )
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course with code {course_data.code} already exists"
        )
    
    # Create course
    course = Course(
        teacher_id=current_user["id"],
        name=course_data.name,
        code=course_data.code,
        description=course_data.description,
        semester=course_data.semester,
        year=course_data.year,
        syllabus_content=course_data.syllabus_content
    )
    
    await course.insert()
    
    logger.info(f"Course created: {course.id}")
    
    return CourseResponse(
        id=str(course.id),
        teacher_id=course.teacher_id,
        name=course.name,
        code=course.code,
        description=course.description,
        semester=course.semester,
        year=course.year,
        syllabus_content=course.syllabus_content,
        enrolled_students=course.enrolled_students,
        created_at=course.created_at,
        updated_at=course.updated_at
    )


@router.get("", response_model=CourseListResponse)
async def list_courses(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    List courses. Teachers see their courses, students see enrolled courses.
    """
    if current_user["role"] == "teacher":
        courses = await Course.find(Course.teacher_id == current_user["id"]).to_list()
    else:
        # Students see courses they're enrolled in
        courses = await Course.find(
            {"enrolled_students": current_user["id"]}
        ).to_list()
    
    return CourseListResponse(
        courses=[
            CourseResponse(
                id=str(c.id),
                teacher_id=c.teacher_id,
                name=c.name,
                code=c.code,
                description=c.description,
                semester=c.semester,
                year=c.year,
                syllabus_content=c.syllabus_content,
                enrolled_students=c.enrolled_students,
                created_at=c.created_at,
                updated_at=c.updated_at
            )
            for c in courses
        ],
        total=len(courses)
    )


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a specific course by ID.
    """
    course = await Course.get(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check access
    if current_user["role"] == "teacher" and course.teacher_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if current_user["role"] == "student" and current_user["id"] not in course.enrolled_students:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not enrolled in this course"
        )
    
    return CourseResponse(
        id=str(course.id),
        teacher_id=course.teacher_id,
        name=course.name,
        code=course.code,
        description=course.description,
        semester=course.semester,
        year=course.year,
        syllabus_content=course.syllabus_content,
        enrolled_students=course.enrolled_students,
        created_at=course.created_at,
        updated_at=course.updated_at
    )


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_data: CourseUpdate,
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Update a course. Teachers only, own courses only.
    """
    course = await Course.get(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.teacher_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own courses"
        )
    
    # Update fields
    update_data = course_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    course.updated_at = datetime.utcnow()
    await course.save()
    
    logger.info(f"Course updated: {course_id}")
    
    return CourseResponse(
        id=str(course.id),
        teacher_id=course.teacher_id,
        name=course.name,
        code=course.code,
        description=course.description,
        semester=course.semester,
        year=course.year,
        syllabus_content=course.syllabus_content,
        enrolled_students=course.enrolled_students,
        created_at=course.created_at,
        updated_at=course.updated_at
    )


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: str,
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Delete a course. Teachers only, own courses only.
    """
    course = await Course.get(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.teacher_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own courses"
        )
    
    await course.delete()
    logger.info(f"Course deleted: {course_id}")


@router.post("/{course_id}/enroll", status_code=status.HTTP_200_OK)
async def enroll_student(
    course_id: str,
    enroll_data: EnrollRequest,
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Enroll a student in a course. Teachers only.
    """
    course = await Course.get(course_id)
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.teacher_id != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage your own courses"
        )
    
    if enroll_data.student_id in course.enrolled_students:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already enrolled"
        )
    
    course.enrolled_students.append(enroll_data.student_id)
    await course.save()
    
    logger.info(f"Student {enroll_data.student_id} enrolled in course {course_id}")
    
    return {"message": "Student enrolled successfully"}
