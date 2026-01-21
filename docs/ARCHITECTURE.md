# Teacher Assistance Platform (TAP) - Architecture Documentation

## Overview

The Teacher Assistance Platform (TAP) is an AI-powered system that processes lecture audio and study materials to automatically generate educational content including notes, assignments, and flashcards.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React)                                │
│                         (Already Implemented)                                │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ HTTP/REST
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FASTAPI BACKEND                                    │
│  ┌─────────────┐ ┌──────────────┐ ┌───────────────┐ ┌──────────────────┐   │
│  │ Auth Router │ │Course Router │ │Lecture Router │ │ Content Router   │   │
│  │ /api/v1/auth│ │/api/v1/courses│ │/api/v1/lectures│ │ /api/v1/content │   │
│  └─────────────┘ └──────────────┘ └───────────────┘ └──────────────────┘   │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│   SERVICES    │         │  AI PIPELINE  │         │   DATABASE    │
│               │         │  (LangGraph)  │         │               │
│ ┌───────────┐ │         │ ┌───────────┐ │         │ ┌───────────┐ │
│ │ Document  │ │         │ │  Context  │ │         │ │  MongoDB  │ │
│ │ Processor │ │────────▶│ │ Retrieval │ │         │ │  Atlas    │ │
│ └───────────┘ │         │ └─────┬─────┘ │         │ └───────────┘ │
│ ┌───────────┐ │         │       ▼       │         │ ┌───────────┐ │
│ │  Audio    │ │         │ ┌───────────┐ │         │ │ ChromaDB  │ │
│ │ Processor │ │────────▶│ │   Notes   │ │         │ │ (Vectors) │ │
│ │ (Whisper) │ │         │ │ Generator │ │         │ └───────────┘ │
│ └───────────┘ │         │ └─────┬─────┘ │         │ ┌───────────┐ │
│ ┌───────────┐ │         │       ▼       │         │ │   Redis   │ │
│ │ Embedding │ │────────▶│ ┌───────────┐ │         │ │(Optional) │ │
│ │  Service  │ │         │ │Assignment │ │         │ └───────────┘ │
│ └───────────┘ │         │ │ Generator │ │         └───────────────┘
│ ┌───────────┐ │         │ └─────┬─────┘ │
│ │  Vector   │ │         │       ▼       │
│ │   Store   │◀──────────│ ┌───────────┐ │
│ └───────────┘ │         │ │ Flashcard │ │
└───────────────┘         │ │ Generator │ │
                          │ └───────────┘ │
                          └───────┬───────┘
                                  │
                                  ▼
                          ┌───────────────┐
                          │ External APIs │
                          │ ┌───────────┐ │
                          │ │  Groq API │ │
                          │ │  (LLM)    │ │
                          │ └───────────┘ │
                          │ ┌───────────┐ │
                          │ │HuggingFace│ │
                          │ │(Embeddings)│ │
                          │ └───────────┘ │
                          └───────────────┘
```

## Data Flow

### 1. Teacher Uploads Study Material

```
Teacher → Upload PDF/DOCX/PPTX → Document Processor → 
→ Text Extraction → Chunking → Embedding Generation → 
→ ChromaDB (Vector Store) + MongoDB (Metadata)
```

### 2. Teacher Uploads Lecture Audio

```
Teacher → Upload Audio (MP3/WAV) → Whisper Transcription →
→ Transcript Text → Chunking → Embedding → ChromaDB + MongoDB
```

### 3. Content Generation (LangGraph Workflow)

```
Trigger Generation →
  1. Retrieve Context (Vector Search) →
  2. Generate Notes (Groq LLM) →
  3. Generate Assignment (Groq LLM) →
  4. Generate Flashcards (Groq LLM) →
  5. Save to MongoDB →
Done
```

### 4. Student Views Content

```
Student → Request Notes/Assignment/Flashcards →
→ Auth Check → Course Enrollment Check →
→ Fetch from MongoDB → Return JSON
```

## API Endpoints

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register new user |
| POST | `/login` | Login and get JWT |
| POST | `/logout` | Logout user |

### Courses (`/api/v1/courses`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/` | Create course (Teacher) |
| GET | `/` | List courses |
| GET | `/{id}` | Get course details |
| PUT | `/{id}` | Update course (Teacher) |
| DELETE | `/{id}` | Delete course (Teacher) |
| POST | `/{id}/enroll` | Enroll student (Teacher) |

### Materials (`/api/v1`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/{course_id}/materials` | Upload material (Teacher) |
| GET | `/{course_id}/materials` | List materials |
| GET | `/materials/{id}` | Get material details |
| DELETE | `/materials/{id}` | Delete material (Teacher) |

### Lectures (`/api/v1`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/{course_id}/lectures` | Create lecture with audio (Teacher) |
| GET | `/{course_id}/lectures` | List lectures |
| GET | `/lectures/{id}` | Get lecture details |
| POST | `/lectures/{id}/transcribe` | Transcribe audio (Teacher) |
| POST | `/lectures/{id}/generate` | Generate content (Teacher) |
| GET | `/lectures/{id}/transcript` | Get transcript |
| DELETE | `/lectures/{id}` | Delete lecture (Teacher) |

### Content (`/api/v1`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/lectures/{id}/notes` | Get notes |
| GET | `/lectures/{id}/assignment` | Get assignment |
| GET | `/lectures/{id}/flashcards` | Get flashcards |
| GET | `/lectures/{id}/content` | Get all content |
| PATCH | `/content/{id}` | Edit content (Teacher) |
| DELETE | `/content/{id}` | Delete content (Teacher) |

## JSON Output Formats

### Notes

```json
{
  "title": "Lecture Notes: Binary Trees",
  "summary": "Introduction to binary tree data structures...",
  "sections": [
    {
      "heading": "What is a Binary Tree?",
      "content": "A binary tree is a hierarchical...",
      "key_points": [
        "Each node has at most 2 children",
        "Root is the topmost node",
        "Leaves have no children"
      ]
    }
  ],
  "key_takeaways": [...],
  "vocabulary": [
    {"term": "Node", "definition": "..."}
  ],
  "further_reading": [...]
}
```

### Assignment

```json
{
  "title": "Practice Questions: Binary Trees",
  "description": "Test your understanding...",
  "total_points": 100,
  "questions": [
    {
      "type": "mcq",
      "question": "What is the maximum...",
      "options": ["A) 10", "B) 15", "C) 31", "D) 32"],
      "correct_answer": "C",
      "explanation": "...",
      "points": 10,
      "difficulty": "easy"
    },
    {
      "type": "short_answer",
      "question": "Explain inorder traversal...",
      "expected_answer": "...",
      "keywords": ["left", "root", "right"],
      "points": 15,
      "difficulty": "medium"
    }
  ]
}
```

### Flashcards

```json
{
  "title": "Flashcards: Binary Trees",
  "description": "Study cards for revision",
  "cards": [
    {
      "front": "What is a binary tree?",
      "back": "A tree data structure where each node has at most two children",
      "difficulty": "easy"
    },
    {
      "front": "What is the height of a complete binary tree with n nodes?",
      "back": "floor(log2(n))",
      "difficulty": "medium"
    }
  ]
}
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend Framework | FastAPI | REST API, async support |
| Authentication | Supabase | User management, JWT |
| Primary Database | MongoDB Atlas | Document storage |
| Vector Database | ChromaDB | Semantic search |
| Cache (Optional) | Redis | Session cache |
| LLM | Groq (llama3-70b) | Content generation |
| Embeddings | HuggingFace (MiniLM) | Semantic embeddings |
| Transcription | faster-whisper | Audio to text |
| Document Processing | pypdf, python-docx | Text extraction |
| AI Orchestration | LangGraph | Workflow management |

## Environment Variables

```env
# Supabase (Auth)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-supabase-key

# MongoDB Atlas
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net
MONGODB_DB_NAME=tap_database

# Redis (Optional)
REDIS_URL=redis://localhost:6379

# Groq API
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama3-70b-8192

# HuggingFace (Optional - uses local models by default)
HUGGINGFACE_API_KEY=your-hf-key
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Storage
CHROMA_PERSIST_DIR=./chroma_db
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=50
```

## Setup and Deployment

### Local Development

1. **Clone and Install**
   ```bash
   cd "backend TAP"
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # Copy .env.example to .env and fill in values
   cp .env.example .env
   ```

3. **Install FFmpeg** (Required for audio processing)
   - Windows: `winget install ffmpeg`
   - Mac: `brew install ffmpeg`

4. **Run Server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Access API Docs**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Production Deployment

1. Use gunicorn with uvicorn workers
2. Set up MongoDB Atlas cluster
3. Configure CORS for frontend domain
4. Use environment secrets management
5. Set up monitoring (Datadog, Sentry)

## Security Considerations

- JWT tokens validated on every protected endpoint
- Role-based access control (Teacher vs Student)
- Course enrollment verification for content access
- File upload size limits and type validation
- Input sanitization for all user data
