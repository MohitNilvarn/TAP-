# File: app/main.py
"""
Teacher Assistance Platform API - Main Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import setup_logging, get_logger
from app.db.mongodb import connect_to_mongodb, close_mongodb_connection
from app.db.redis import connect_to_redis, close_redis_connection

# Import routers
from app.api.v1 import auth
from app.api.v1 import courses
from app.api.v1 import materials
from app.api.v1 import lectures
from app.api.v1 import content

# Setup Logging
setup_logging()
logger = get_logger("TAP.Main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    # Startup
    logger.info("Application is STARTING UP...")
    
    # Connect to MongoDB
    await connect_to_mongodb()
    
    # Connect to Redis (optional)
    await connect_to_redis()
    
    logger.info("Application startup complete!")
    
    yield
    
    # Shutdown
    logger.info("Application is SHUTTING DOWN...")
    await close_mongodb_connection()
    await close_redis_connection()
    logger.info("Application shutdown complete!")


# Create FastAPI app
app = FastAPI(
    title="Teacher Assistance Platform API",
    description="""
    A comprehensive API for the Teacher Assistance Platform (TAP).
    
    ## Features
    - **Course Management**: Create and manage courses
    - **Material Upload**: Upload study materials (PDF, DOCX, PPTX)
    - **Lecture Management**: Upload lecture audio and transcripts
    - **AI Content Generation**: Generate notes, assignments, and flashcards
    - **Semantic Search**: Context-aware content retrieval
    
    ## Tech Stack
    - FastAPI, MongoDB Atlas, ChromaDB
    - Groq LLM (llama3-70b), HuggingFace Embeddings
    - LangGraph for AI workflows
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    courses.router,
    prefix="/api/v1/courses",
    tags=["Courses"]
)

app.include_router(
    materials.router,
    prefix="/api/v1",
    tags=["Materials"]
)

app.include_router(
    lectures.router,
    prefix="/api/v1",
    tags=["Lectures"]
)

app.include_router(
    content.router,
    prefix="/api/v1",
    tags=["Content"]
)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "TAP API is running",
        "version": "1.0.0"
    }


@app.get("/api/v1/health", tags=["Health"])
def detailed_health():
    """Detailed health check with system info."""
    return {
        "status": "healthy",
        "service": "Teacher Assistance Platform",
        "version": "1.0.0",
        "components": {
            "api": "operational",
            "database": "operational",
            "ai_pipeline": "operational"
        }
    }