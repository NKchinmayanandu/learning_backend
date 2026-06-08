from sqlalchemy.orm import Session
from apps.models import User


def get_user_by_id(user_id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id == user_id).first()
