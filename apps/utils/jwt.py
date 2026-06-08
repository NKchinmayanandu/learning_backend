from datetime import datetime, timezone, timedelta
from jose import jwt
from apps.config import settings

SECERT_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECERT_KEY, algorithm=ALGORITHM)
