from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from apps.models import User
from apps.schemas import UserLogin
from apps.utils.security import verify_password
from apps.redis import redis_client


def authenticate_user(data: UserLogin, db: Session):
    rate_limit_key = f"login:{data.email}"

    attempts = redis_client.get(rate_limit_key)
    if attempts and int(attempts) >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again later.",
        )

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        current_attempts = redis_client.incr(rate_limit_key)
        if current_attempts == 1:
            redis_client.expire(rate_limit_key, 60)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    redis_client.delete(rate_limit_key)
    return user
