"""
Authentication middleware for dual-mode authentication.

Production: Client certificate validation and JWT generation
Development: Mock user identity via X-Mock-User header
"""

from fastapi import Header, HTTPException, status
from typing import Optional
import jwt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"

def create_jwt(user_identity: str) -> str:
    """Create JWT token from user identity"""
    payload = {
        "sub": user_identity,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=8),
        "mode": "development" if os.getenv("ENVIRONMENT") == "development" else "production"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

async def get_current_user(
    x_mock_user: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
) -> dict:
    """
    Get current user from either mock header (dev) or JWT (production)
    """
    # Development mode: Accept mock user header
    if x_mock_user:
        return {
            "identity": x_mock_user,
            "mode": "development",
            "jwt": create_jwt(x_mock_user)
        }
    
    # Production mode: Require JWT
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication provided"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
        
        payload = verify_jwt(token)
        return {
            "identity": payload["sub"],
            "mode": payload.get("mode", "production"),
            "jwt": token
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )
