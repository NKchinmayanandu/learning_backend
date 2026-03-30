from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from apps.database import get_db
from apps.models import User
from apps.utils.jwt import create_token
from apps.utils.security import verify_password,hash_password
from apps.schemas import UserCreate,UserLogin

router = APIRouter(prefix="/auth",tags=["auths"])

@router.post("/signup")
def signup(data:UserCreate,db:Session=Depends(get_db)):
    existing = db.query(User).filter(User.email==data.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="user already exist")
    user = User(
        email = data.email,
        password = hash_password(data.password)
    )
@router.post("/login")
def login(data:UserLogin,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email==data.email).first()
    if not user or not verify_password(data.password,User.password):
        raise HTTPException(status_code=400,detail="invalid credentials")
    
    token = create_token({"user_id":User.id})
    return {"acess_token":token}