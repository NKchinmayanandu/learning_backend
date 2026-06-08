from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models import User
from apps.schemas import UserLogin, TokenResponse # Assuming these exist
from apps.utils.security import verify_password
from apps.utils.jwt import create_token
from apps.redis import redis_client

router = APIRouter()

def authenticate_user(data: UserLogin, db: Session):
    rate_limiting_key = f"login:{data.email}"

    # 1. Rate Limiting Check
    attempts = redis_client.get(rate_limiting_key)
    if attempts and int(attempts) >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many attempts, try again later"
        )
    
    # 2. Database Query
    user = db.query(User).filter(User.email == data.email).first()
    
    # 3. Authentication Check
    if not user or not verify_password(data.password, user.password):
        current_attempts = redis_client.incr(rate_limiting_key)
        if current_attempts == 1:
            redis_client.expire(rate_limiting_key, 60)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    
    # 4. Success: Reset rate limit and RETURN the user
    redis_client.delete(rate_limiting_key)
    return user
