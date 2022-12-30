from uuid import UUID
from sqlalchemy.orm import Session

from .User_Model import User

def get_user_by_id(database_session: Session, user_id: UUID):
    return database_session.query(User).filter(User.id == user_id).first()
def get_user_by_email(database_session: Session, user_email: str):
    return database_session.query(User).filter(User.email == user_email).first()
