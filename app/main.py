# File: app/main.py
from fastapi import FastAPI
from app.api.v1 import auth
from app.core.logger import setup_logging, get_logger

# 1. Initialize Logging Configuration GLOBALLY
setup_logging()

# 2. Get a logger for this specific file
logger = get_logger("TAP.Main")

app = FastAPI(title="Teacher Assistance Platform API")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.on_event("startup")
async def startup_event():
    logger.info("Application is STARTING UP...")
    logger.info("Global logging configured successfully.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application is SHUTTING DOWN...")

@app.get("/")
def health_check():
    logger.info("Health check endpoint called.")
    return {"status": "ok", "message": "TAP API is running"}