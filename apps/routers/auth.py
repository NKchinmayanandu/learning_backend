from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models import User
from apps.utils.jwt import create_token
from apps.utils.security import verify_password,hash_password
from apps.schemas import UserCreate,UserLogin
from apps.redis import redis_client
from apps.schemas import TokenResponse
from apps.services.auth_services import authenticate_user
router = APIRouter(prefix="/auth",tags=["auth"])   

@router.post("/signup")
def signup(data:UserCreate,db:Session=Depends(get_db)):
    existing = db.query(User).filter(User.email==data.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="user already exists")
    user = User(
        email = data.email,
        password = hash_password(data.password),
        role = data.role)
    db.add(user)
    try:
        db.commit()
    except:
        db.rollback()
    
    db.refresh(user)
    return {"message":"user created"}

@router.post("/login",response_model=TokenResponse)
def login(data:UserLogin,db:Session=Depends(get_db)):
    user = authenticate_user(data=data,db=db)
    token = create_token({"user_id": user.id})
    return {"access_token": token,
            "token_type":"bearer"}

