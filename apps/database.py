from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,create_session

url = "postgresql://chinmay:2007@localhost:5432/fastapi_db"
engine = create_engine(url,echo=True)

SessionLocal = create_session(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()