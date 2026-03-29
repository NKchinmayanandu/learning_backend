from jose import jwt
from datetime import datetime,timedelta

SECERT_KEY = "secret"
ALGORITHM = "HS256"

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update(expire)
    return jwt.encode(to_encode,secret_key = SECERT_KEY,algorithm=ALGORITHM)