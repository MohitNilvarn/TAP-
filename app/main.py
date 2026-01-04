# File: app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth
from app.core.logger import setup_logging, get_logger

# 1. Setup Logging
setup_logging()
logger = get_logger("TAP.Main")

app = FastAPI(title="Teacher Assistance Platform API")

# --- FIX: SIMPLIFY CORS ---
# Using ["*"] allows all origins, which eliminates CORS errors during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NOTE: We REMOVED the 'log_request_body' middleware ---
# It was consuming the request stream and causing the 400/422 errors.

# Include Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.on_event("startup")
async def startup_event():
    logger.info("Application is STARTING UP...")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "TAP API is running"}