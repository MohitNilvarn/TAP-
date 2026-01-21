# File: app/core/dependencies.py
"""
FastAPI dependencies for authentication and authorization.
"""
from fastapi import Depends, HTTPException, status, Header
from typing import Optional, Dict, Any
from jose import jwt, JWTError

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("TAP.Dependencies")


async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Extract and validate user from JWT token.
    
    The token is expected in the Authorization header as:
    Authorization: Bearer <token>
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    
    try:
        # Decode Supabase JWT (using HS256)
        # Note: In production, verify with Supabase JWT secret
        payload = jwt.decode(
            token,
            settings.SUPABASE_KEY,  # Supabase anon key can be used for basic validation
            algorithms=["HS256"],
            options={"verify_aud": False}  # Supabase tokens don't always have aud
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


async def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """
    Get user if authenticated, None otherwise.
    Useful for endpoints that work with or without auth.
    """
    if not authorization:
        return None
    
    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None
