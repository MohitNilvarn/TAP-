# File: app/api/v1/auth.py
import logging
from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from fastapi.responses import JSONResponse
from app.schemas.auth import UserSignup, UserLogin
from app.db.supabase import supabase
from app.core.logger import get_logger

logger = get_logger("TAP.Auth")

router = APIRouter()

# --- 1. SIGNUP ---
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    logger.info(f"SIGNUP REQUEST: Received for email: {user.email}")
    
    try:
        # Pass role, first_name, and last_name to Supabase Metadata
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role  # Crucial: Save role to metadata
                }
            }
        })

        if not response.user and not response.session:
            raise HTTPException(status_code=400, detail="Signup failed. User might already exist.")
            
        return {"message": "User created successfully", "user_id": response.user.id}

    except Exception as e:
        logger.error(f"CRITICAL SIGNUP ERROR: {str(e)}", exc_info=True)
        if "User already registered" in str(e):
             raise HTTPException(status_code=400, detail="This email is already registered.")
        raise HTTPException(status_code=400, detail=f"Signup failed: {str(e)}")

# --- 2. LOGIN (THIS WAS MISSING) ---
@router.post("/login")
async def login(user: UserLogin, response: Response):
    try:
        # 1. Authenticate with Supabase (Check Password)
        session = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if not session.user or not session.session:
             raise HTTPException(status_code=401, detail="Invalid credentials")

        # 2. GET THE REAL ROLE (From Database Metadata)
        # Default to 'student' if missing to be safe
        actual_role = session.user.user_metadata.get("role", "student")

        # 3. SECURITY CHECK: Does the role match the portal?
        # If I am a 'student' trying to login as 'teacher', BLOCK ME.
        if actual_role != user.role:
            logger.warning(f"Security Alert: User {user.email} (role: {actual_role}) tried to access {user.role} portal.")
            
            # Sign them out immediately so the session is killed
            supabase.auth.sign_out()
            
            raise HTTPException(
                status_code=403, 
                detail=f"Access Denied. You are a {actual_role}, not a {user.role}."
            )

        # 4. If roles match, proceed!
        return {
            "access_token": session.session.access_token,
            "token_type": "bearer",
            "user": {
                "id": session.user.id,
                "email": session.user.email,
                "role": actual_role,
                "first_name": session.user.user_metadata.get("first_name", ""),
                "last_name": session.user.user_metadata.get("last_name", "")
            }
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid email or password")

# --- 3. LOGOUT ---
@router.post("/logout")
async def logout(response: Response, request: Request):
    try:
        # 1. Tell Supabase to revoke the session
        # We need the user's access token to sign them out securely
        access_token = request.cookies.get("access_token")
        
        # If you aren't using cookies and sending Authorization header instead:
        # access_token = request.headers.get("Authorization").split("Bearer ")[1]

        if access_token:
            # This invalidates the refresh token on Supabase's side
            supabase.auth.sign_out()
        
        # 2. Clear the cookies (Crucial if you use HTTP-only cookies)
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        
        return {"message": "Logged out successfully"}

    except Exception as e:
        # Even if Supabase errors, we should still clear local cookies
        response.delete_cookie(key="access_token")
        return JSONResponse(status_code=500, content={"detail": str(e)})