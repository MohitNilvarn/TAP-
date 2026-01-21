# File: app/api/v1/lectures.py
"""
Lecture management endpoints with audio upload and transcription.
"""
import os
import uuid
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from typing import Dict, Any, List, Optional
from datetime import datetime

from app.core.config import settings
from app.core.logger import get_logger
from app.core.dependencies import require_teacher, get_current_user
from app.schemas.lecture import (
    LectureCreate,
    LectureResponse,
    LectureListResponse,
    TranscriptResponse,
    TranscribeRequest,
    GenerateRequest,
    TranscriptionStatus,
    GenerationStatus
)
from app.models.course import Course
from app.models.lecture import (
    Lecture,
    TranscriptionStatus as ModelTranscriptionStatus,
    GenerationStatus as ModelGenerationStatus
)
from app.services.audio_processor import transcribe_audio, get_audio_duration
from app.services.vector_store import add_documents
from app.ai.graph import run_content_generation

logger = get_logger("TAP.Lectures")
router = APIRouter()

# Allowed audio extensions
ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "m4a", "ogg", "flac", "webm"}


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


@router.post("/{course_id}/lectures", response_model=LectureResponse, status_code=status.HTTP_201_CREATED)
async def create_lecture(
    course_id: str,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Create a new lecture with optional audio file.
    """
    # Validate course
    course = await Course.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Create lecture
    lecture = Lecture(
        course_id=course_id,
        teacher_id=current_user["id"],
        title=title,
        description=description
    )
    
    # Handle audio file if provided
    if audio_file:
        ext = get_file_extension(audio_file.filename)
        if ext not in ALLOWED_AUDIO_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Audio format not allowed. Allowed: {', '.join(ALLOWED_AUDIO_EXTENSIONS)}"
            )
        
        # Save audio file
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_id = str(uuid.uuid4())
        audio_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.{ext}")
        
        try:
            content = await audio_file.read()
            with open(audio_path, "wb") as f:
                f.write(content)
            
            lecture.audio_filename = audio_file.filename
            lecture.audio_path = audio_path
            lecture.audio_duration_seconds = get_audio_duration(audio_path)
            
            logger.info(f"Saved audio file: {audio_path}")
            
        except Exception as e:
            logger.error(f"Audio save error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save audio file")
    
    await lecture.insert()
    logger.info(f"Lecture created: {lecture.id}")
    
    return LectureResponse(
        id=str(lecture.id),
        course_id=lecture.course_id,
        teacher_id=lecture.teacher_id,
        title=lecture.title,
        description=lecture.description,
        lecture_date=lecture.lecture_date,
        audio_filename=lecture.audio_filename,
        audio_duration_seconds=lecture.audio_duration_seconds,
        transcription_status=TranscriptionStatus(lecture.transcription_status.value),
        generation_status=GenerationStatus(lecture.generation_status.value),
        created_at=lecture.created_at,
        transcribed_at=lecture.transcribed_at,
        generated_at=lecture.generated_at
    )


@router.get("/{course_id}/lectures", response_model=LectureListResponse)
async def list_lectures(
    course_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    List all lectures for a course.
    """
    course = await Course.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check access
    if current_user["role"] == "teacher" and course.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if current_user["role"] == "student" and current_user["id"] not in course.enrolled_students:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    lectures = await Lecture.find(Lecture.course_id == course_id).to_list()
    
    return LectureListResponse(
        lectures=[
            LectureResponse(
                id=str(l.id),
                course_id=l.course_id,
                teacher_id=l.teacher_id,
                title=l.title,
                description=l.description,
                lecture_date=l.lecture_date,
                audio_filename=l.audio_filename,
                audio_duration_seconds=l.audio_duration_seconds,
                transcription_status=TranscriptionStatus(l.transcription_status.value),
                generation_status=GenerationStatus(l.generation_status.value),
                created_at=l.created_at,
                transcribed_at=l.transcribed_at,
                generated_at=l.generated_at
            )
            for l in lectures
        ],
        total=len(lectures)
    )


@router.get("/lectures/{lecture_id}", response_model=LectureResponse)
async def get_lecture(
    lecture_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a specific lecture by ID.
    """
    lecture = await Lecture.get(lecture_id)
    
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    # Check course access
    course = await Course.get(lecture.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user["role"] == "teacher" and course.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if current_user["role"] == "student" and current_user["id"] not in course.enrolled_students:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    return LectureResponse(
        id=str(lecture.id),
        course_id=lecture.course_id,
        teacher_id=lecture.teacher_id,
        title=lecture.title,
        description=lecture.description,
        lecture_date=lecture.lecture_date,
        audio_filename=lecture.audio_filename,
        audio_duration_seconds=lecture.audio_duration_seconds,
        transcription_status=TranscriptionStatus(lecture.transcription_status.value),
        generation_status=GenerationStatus(lecture.generation_status.value),
        created_at=lecture.created_at,
        transcribed_at=lecture.transcribed_at,
        generated_at=lecture.generated_at
    )


@router.post("/lectures/{lecture_id}/transcribe", response_model=TranscriptResponse)
async def transcribe_lecture(
    lecture_id: str,
    request: TranscribeRequest = TranscribeRequest(),
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Transcribe lecture audio using Whisper.
    """
    lecture = await Lecture.get(lecture_id)
    
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    if lecture.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not lecture.audio_path:
        raise HTTPException(status_code=400, detail="No audio file uploaded for this lecture")
    
    # Check if already transcribed
    if lecture.transcription_status == ModelTranscriptionStatus.COMPLETED and not request.force:
        return TranscriptResponse(
            lecture_id=str(lecture.id),
            transcript=lecture.transcript,
            segments=lecture.transcript_segments,
            status=TranscriptionStatus.COMPLETED
        )
    
    # Update status
    lecture.transcription_status = ModelTranscriptionStatus.TRANSCRIBING
    await lecture.save()
    
    try:
        logger.info(f"Starting transcription for lecture: {lecture_id}")
        
        result = transcribe_audio(lecture.audio_path)
        
        lecture.transcript = result["transcript"]
        lecture.transcript_segments = result["segments"]
        lecture.transcription_status = ModelTranscriptionStatus.COMPLETED
        lecture.transcribed_at = datetime.utcnow()
        
        # Index transcript in vector store
        if result["transcript"]:
            from app.services.document_processor import chunk_text
            chunks = chunk_text(result["transcript"])
            
            if chunks:
                chunk_ids = [f"{lecture.id}_transcript_{i}" for i in range(len(chunks))]
                metadatas = [
                    {
                        "source": "lecture_transcript",
                        "lecture_id": str(lecture.id),
                        "title": lecture.title,
                        "chunk_index": i
                    }
                    for i in range(len(chunks))
                ]
                
                add_documents(
                    course_id=lecture.course_id,
                    documents=chunks,
                    metadatas=metadatas,
                    ids=chunk_ids
                )
                
                lecture.embedding_ids = chunk_ids
        
        await lecture.save()
        
        logger.info(f"Transcription complete for lecture: {lecture_id}")
        
        return TranscriptResponse(
            lecture_id=str(lecture.id),
            transcript=lecture.transcript,
            segments=lecture.transcript_segments,
            status=TranscriptionStatus.COMPLETED
        )
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        lecture.transcription_status = ModelTranscriptionStatus.FAILED
        lecture.transcription_error = str(e)
        await lecture.save()
        
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.get("/lectures/{lecture_id}/transcript", response_model=TranscriptResponse)
async def get_transcript(
    lecture_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get the transcript for a lecture.
    """
    lecture = await Lecture.get(lecture_id)
    
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    # Check course access
    course = await Course.get(lecture.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user["role"] == "teacher" and course.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if current_user["role"] == "student" and current_user["id"] not in course.enrolled_students:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    return TranscriptResponse(
        lecture_id=str(lecture.id),
        transcript=lecture.transcript,
        segments=lecture.transcript_segments,
        status=TranscriptionStatus(lecture.transcription_status.value)
    )


@router.post("/lectures/{lecture_id}/generate")
async def generate_content(
    lecture_id: str,
    request: GenerateRequest = GenerateRequest(),
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Generate notes, assignments, and flashcards for a lecture.
    Requires transcript to be available.
    """
    lecture = await Lecture.get(lecture_id)
    
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    if lecture.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if lecture.transcription_status != ModelTranscriptionStatus.COMPLETED or not lecture.transcript:
        raise HTTPException(
            status_code=400,
            detail="Transcript not available. Please transcribe the lecture first."
        )
    
    # Check if already generated
    if lecture.generation_status == ModelGenerationStatus.COMPLETED and not request.force:
        return {
            "message": "Content already generated",
            "lecture_id": str(lecture.id),
            "status": "completed"
        }
    
    # Update status
    lecture.generation_status = ModelGenerationStatus.GENERATING
    await lecture.save()
    
    try:
        logger.info(f"Starting content generation for lecture: {lecture_id}")
        
        # Run the LangGraph workflow
        result = await run_content_generation(
            lecture_id=str(lecture.id),
            course_id=lecture.course_id,
            transcript=lecture.transcript,
            lecture_title=lecture.title,
            content_types=request.content_types
        )
        
        if result.get("error"):
            raise Exception(result["error"])
        
        return {
            "message": "Content generated successfully",
            "lecture_id": str(lecture.id),
            "status": "completed",
            "generated_types": result.get("completed_types", [])
        }
        
    except Exception as e:
        logger.error(f"Content generation error: {str(e)}")
        lecture.generation_status = ModelGenerationStatus.FAILED
        lecture.generation_error = str(e)
        await lecture.save()
        
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")


@router.delete("/lectures/{lecture_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lecture(
    lecture_id: str,
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Delete a lecture. Teachers only.
    """
    lecture = await Lecture.get(lecture_id)
    
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    
    if lecture.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You can only delete your own lectures")
    
    # Delete audio file
    if lecture.audio_path and os.path.exists(lecture.audio_path):
        os.remove(lecture.audio_path)
    
    # Delete from vector store
    from app.services.vector_store import delete_documents
    if lecture.embedding_ids:
        delete_documents(lecture.course_id, lecture.embedding_ids)
    
    # Delete associated content
    from app.models.content import GeneratedContent
    await GeneratedContent.find(GeneratedContent.lecture_id == lecture_id).delete()
    
    await lecture.delete()
    logger.info(f"Lecture deleted: {lecture_id}")
