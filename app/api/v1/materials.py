# File: app/api/v1/materials.py
"""
Study material upload and management endpoints.
"""
import os
import uuid
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from typing import Dict, Any, List
from datetime import datetime

from app.core.config import settings
from app.core.logger import get_logger
from app.core.dependencies import require_teacher, get_current_user
from app.schemas.material import (
    MaterialUploadResponse,
    MaterialResponse,
    MaterialListResponse,
    MaterialType,
    ProcessingStatus
)
from app.models.course import Course
from app.models.material import Material, MaterialType as ModelMaterialType, ProcessingStatus as ModelProcessingStatus
from app.services.document_processor import process_document, DocumentProcessorFactory
from app.services.vector_store import add_documents

logger = get_logger("TAP.Materials")
router = APIRouter()

# Allowed file extensions
ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx", "txt", "md"}


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


@router.post("/{course_id}/materials", response_model=MaterialUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_material(
    course_id: str,
    file: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Upload study material (PDF, DOCX, PPTX, TXT, MD) to a course.
    The file will be processed and indexed for semantic search.
    """
    # Validate course exists and belongs to teacher
    course = await Course.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Validate file type
    ext = get_file_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.{ext}")
    
    try:
        content = await file.read()
        file_size = len(content)
        
        # Check file size
        max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB}MB"
            )
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"Saved file: {file_path}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File save error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save file")
    
    # Create material record
    material = Material(
        course_id=course_id,
        teacher_id=current_user["id"],
        filename=file.filename,
        file_type=ModelMaterialType(ext),
        file_path=file_path,
        file_size_bytes=file_size,
        processing_status=ModelProcessingStatus.PROCESSING
    )
    
    await material.insert()
    
    # Process document in background (for now, synchronous)
    try:
        logger.info(f"Processing document: {file.filename}")
        
        result = process_document(file_path, ext)
        
        material.content = result["content"]
        material.chunks = result["chunks"]
        material.metadata = result["metadata"]
        material.processing_status = ModelProcessingStatus.COMPLETED
        material.processed_at = datetime.utcnow()
        
        # Index chunks in vector store
        if result["chunks"]:
            chunk_ids = [f"{material.id}_chunk_{i}" for i in range(len(result["chunks"]))]
            metadatas = [
                {
                    "source": "material",
                    "material_id": str(material.id),
                    "filename": file.filename,
                    "chunk_index": i
                }
                for i in range(len(result["chunks"]))
            ]
            
            add_documents(
                course_id=course_id,
                documents=result["chunks"],
                metadatas=metadatas,
                ids=chunk_ids
            )
            
            material.embedding_ids = chunk_ids
            logger.info(f"Indexed {len(chunk_ids)} chunks for material {material.id}")
        
        await material.save()
        
    except Exception as e:
        logger.error(f"Document processing error: {str(e)}")
        material.processing_status = ModelProcessingStatus.FAILED
        material.processing_error = str(e)
        await material.save()
    
    return MaterialUploadResponse(
        id=str(material.id),
        course_id=course_id,
        filename=file.filename,
        file_type=MaterialType(ext),
        processing_status=ProcessingStatus(material.processing_status.value),
        message="Material uploaded and processing complete" if material.processing_status == ModelProcessingStatus.COMPLETED else "Material uploaded, processing failed"
    )


@router.get("/{course_id}/materials", response_model=MaterialListResponse)
async def list_materials(
    course_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    List all materials for a course.
    """
    course = await Course.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check access
    if current_user["role"] == "teacher" and course.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if current_user["role"] == "student" and current_user["id"] not in course.enrolled_students:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    materials = await Material.find(Material.course_id == course_id).to_list()
    
    return MaterialListResponse(
        materials=[
            MaterialResponse(
                id=str(m.id),
                course_id=m.course_id,
                teacher_id=m.teacher_id,
                filename=m.filename,
                file_type=MaterialType(m.file_type.value),
                file_size_bytes=m.file_size_bytes,
                content=m.content[:500] if m.content else None,  # Truncate for list
                metadata=m.metadata,
                processing_status=ProcessingStatus(m.processing_status.value),
                processing_error=m.processing_error,
                created_at=m.created_at,
                processed_at=m.processed_at
            )
            for m in materials
        ],
        total=len(materials)
    )


@router.get("/materials/{material_id}", response_model=MaterialResponse)
async def get_material(
    material_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get a specific material by ID.
    """
    material = await Material.get(material_id)
    
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    # Check course access
    course = await Course.get(material.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user["role"] == "teacher" and course.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if current_user["role"] == "student" and current_user["id"] not in course.enrolled_students:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    
    return MaterialResponse(
        id=str(material.id),
        course_id=material.course_id,
        teacher_id=material.teacher_id,
        filename=material.filename,
        file_type=MaterialType(material.file_type.value),
        file_size_bytes=material.file_size_bytes,
        content=material.content,
        metadata=material.metadata,
        processing_status=ProcessingStatus(material.processing_status.value),
        processing_error=material.processing_error,
        created_at=material.created_at,
        processed_at=material.processed_at
    )


@router.delete("/materials/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(
    material_id: str,
    current_user: Dict[str, Any] = Depends(require_teacher)
):
    """
    Delete a material. Teachers only.
    """
    material = await Material.get(material_id)
    
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    
    if material.teacher_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You can only delete your own materials")
    
    # Delete file
    if material.file_path and os.path.exists(material.file_path):
        os.remove(material.file_path)
    
    # Delete from vector store
    from app.services.vector_store import delete_documents
    if material.embedding_ids:
        delete_documents(material.course_id, material.embedding_ids)
    
    await material.delete()
    logger.info(f"Material deleted: {material_id}")
