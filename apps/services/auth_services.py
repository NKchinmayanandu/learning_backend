from apps.redis import redis_client
from apps.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from apps.models import User
from apps.utils.security import verify_password
from apps.utils.jwt import create_token
def authenticate_user(data:dict,db:Session):

    rate_limiting_key = f"login:{data.email}"

    attempts =  redis_client.get(rate_limiting_key)

    if attempts and int(attempts)>=5:
        raise HTTPException(status_code=429,detail="too many attempts,try again later")
    
    user = db.query(User).filter(User.email==data.email).first()

    if not user or not verify_password(data.password,user.password):
        current_attempts = redis_client.incr(rate_limiting_key)

        if current_attempts == 1:
            redis_client.expire(rate_limiting_key,60)

        raise HTTPException(status_code=400,detail="invalid credentials")
    
    redis_client.delete(rate_limiting_key)
    
    
    

        

