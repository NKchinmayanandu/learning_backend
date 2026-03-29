from fastapi import APIRouter,Depends,HTTPException,status
from apps.database import get_db
from apps.models import User