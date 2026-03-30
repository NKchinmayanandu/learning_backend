from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from apps.database import Base
url = "postgresql://chinmay:2007@localhost:5432/restaurant_db"
engine = create_engine(url,echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()