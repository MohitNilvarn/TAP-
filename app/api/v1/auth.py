# File: app/api/v1/auth.py
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserSignup, UserLogin
from app.db.supabase import supabase
from app.core.logger import get_logger

# Initialize logger for this module
logger = get_logger("TAP.Auth")

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    logger.info(f"SIGNUP REQUEST: Received for email: {user.email}")
    
    try:
        logger.debug(f"Sending signup request to Supabase for {user.email}")
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })

        if not response.user and not response.session:
            logger.error(f"SIGNUP FAILED: Empty response from Supabase. Payload: {response}")
            raise HTTPException(status_code=400, detail="Signup failed. User might already exist.")
            
        logger.info(f"SIGNUP SUCCESS: User created with ID: {response.user.id}")
        return {"message": "User created successfully", "user_id": response.user.id}

    except Exception as e:
        logger.error(f"CRITICAL SIGNUP ERROR: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/login")
async def login(user: UserLogin):
    logger.info(f"LOGIN REQUEST: Received for email: {user.email}")
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        if not response.session:
            logger.warning(f"LOGIN FAILED: No session returned for {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        logger.info(f"LOGIN SUCCESS: User {response.user.id} logged in.")
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }

    except Exception as e:
        logger.error(f"LOGIN ERROR: {str(e)}", exc_info=True)
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")