# File: app/core/dependencies.py
"""
FastAPI dependencies for authentication and authorization.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from jose import jwt, JWTError

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("TAP.Dependencies")

# Security scheme for Swagger UI
security = HTTPBearer(auto_error=False)


async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    """
    Extract and validate user from JWT token.
    
    The token is expected in the Authorization header as:
    Authorization: Bearer <token>
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    
    
    try:
        # Decode Supabase JWT
        # Note: Supabase uses a separate JWT_SECRET (not the anon key) for signing
        # For development, we decode without signature verification
        # In production, add SUPABASE_JWT_SECRET to .env and verify properly
        payload = jwt.decode(
            token,
            "",  # Empty key required by python-jose even when not verifying
            algorithms=["HS256"],
            options={
                "verify_signature": False,  # Supabase JWT secret is different from anon key
                "verify_aud": False,
                "verify_exp": True  # Still verify expiration
            }
        )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user ID",
            )
        
        # Extract user metadata from token
        user_metadata = payload.get("user_metadata", {})
        
        return {
            "id": user_id,
            "email": payload.get("email", ""),
            "role": user_metadata.get("role", "student"),
            "first_name": user_metadata.get("first_name", ""),
            "last_name": user_metadata.get("last_name", ""),
            "year": user_metadata.get("year", ""),
        }
        
    except JWTError as e:
        logger.warning(f"JWT validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


async def require_teacher(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency that requires the user to be a teacher.
    """
    if current_user.get("role") != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Teacher role required.",
        )
    return current_user


async def require_student(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency that requires the user to be a student.
    """
    if current_user.get("role") != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Student role required.",
        )
    return current_user


async def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict[str, Any]]:
    """
    Get user if authenticated, None otherwise.
    Useful for endpoints that work with or without auth.
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

