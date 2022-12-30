from uuid import UUID
from sqlalchemy.orm import Session

from User_Model import User

def get_user_by_id(database_session: Session, user_id: UUID):
    return database_session.query(User).filter(User.id == user_id).first()
