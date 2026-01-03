import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import UserSignup, UserLogin
from app.db.supabase import supabase

# 1. Configure Logging
# This ensures errors are printed to your console/terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    logger.info(f"Attempting signup for email: {user.email}")
    
    try:
        # 2. Call Supabase Auth
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })

        # 3. Check for specific Supabase API errors (edge case handling)
        # Sometimes supabase-py wraps errors in the response object
        if not response.user and not response.session:
            # If user is None, it usually means an error or confirmation email is required
            logger.error(f"Signup failed. Response: {response}")
            raise HTTPException(status_code=400, detail="Signup failed. User already exists or invalid data.")
            
        logger.info(f"Signup successful for user_id: {response.user.id}")
        return {"message": "User created successfully", "user_id": response.user.id}

    except Exception as e:
        # 4. Log the FULL error traceback to the terminal
        # This is what you need to look at to fix the issue
        logger.error(f"CRITICAL SIGNUP ERROR: {str(e)}", exc_info=True)
        
        # Return the real error to the client for debugging
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

@router.post("/login")
async def login(user: UserLogin):
    logger.info(f"Attempting login for email: {user.email}")
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        if not response.session:
            logger.warning("Login failed: No session returned")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        logger.info(f"Login successful for user: {response.user.id}")
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "refresh_token": response.session.refresh_token,
            "user": {
                "id": response.user.id,
                "email": response.user.email
            }
        }

    except Exception as e:
        logger.error(f"Login Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")