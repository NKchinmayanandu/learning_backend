from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt 
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models import User
from apps.utils.jwt import SECERT_KEY,ALGORITHM    

outh2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
        token:str=Depends(outh2_scheme),
        db:Session=Depends(get_db)
):
    try:
        payload = jwt.decode(token,SECERT_KEY,ALGORITHM)
        user_id = payload.get("user_id")
    except:
        raise HTTPException(status_code=400,detail="invalid token payload")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user not found")
    
    return user 