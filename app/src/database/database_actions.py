from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from user_schema import UserBase, UserCreate, UserOptional
from utils import HashPassword

from .connection import SessionLocal
from .User_Model import User


def get_database():
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()


def get_user_by_id(database_session: Session, user_id: UUID):
    return database_session.query(User).filter(User.id == user_id).first()


def get_user_by_email(database_session: Session, user_email: str):
    return (
        database_session.query(User).filter(User.email == user_email).first()
    )


def create_new_user(database_session: Session, new_user: UserCreate):
    try:
        hashed_password = (HashPassword.bcrypt(new_user.password),)
        new_user = User(
            id=new_user.id,
            first_name=new_user.first_name,
            email=new_user.email,
            password=hashed_password,
            middle_name=new_user.middle_name,
            last_name=new_user.last_name,
            age=new_user.age,
            year=new_user.year,
        )
        database_session.add(new_user)
        database_session.commit()
        database_session.refresh(new_user)
        return {'user': [new_user.first_name, new_user.email]}
    except IntegrityError:
        database_session.rollback()


def update_user(
    database_session: Session,
    stored_user: User,
    new_user_information: UserOptional | UserBase,
):
    new_data = new_user_information.dict(exclude_unset=True)
    for key, value in new_data.items():
        setattr(stored_user, key, value)
    database_session.add(stored_user)
    database_session.commit()
    database_session.refresh(stored_user)
    return {'success': 'User updated successfully'}


def delete_user(database_session: Session, user: User):
    print(user)
    database_session.delete(user)
    database_session.commit()
    return {'success': 'User deleted successfully'}
