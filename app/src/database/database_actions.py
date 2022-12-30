from uuid import UUID
from sqlalchemy.orm import Session

from .User_Model import User
from user_schema import UserCreate

def get_user_by_id(database_session: Session, user_id: UUID):
    return database_session.query(User).filter(User.id == user_id).first()

def get_user_by_email(database_session: Session, user_email: str):
    return database_session.query(User).filter(User.email == user_email).first()

def create_new_user(database_session: Session, new_user: UserCreate):
    new_user = User(
        id=new_user.id,
        first_name=new_user.first_name,
        email=new_user.email,
        password=new_user.password,
        middle_name=new_user.middle_name,
        last_name=new_user.last_name,
        age=new_user.age,
        year=new_user.year
    )
    database_session.add(new_user)
    database_session.commit()
    database_session.refresh(new_user)
    return new_user
