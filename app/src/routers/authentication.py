from login_schema import Login
from database.User_Model import User

from utils.verify_password import verify_user_password

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database import database_actions


router = APIRouter(
    tags=["authentication"]
)


@router.post("/login")
def login(login_request: Login, database: Session = Depends(database_actions.get_database)):
    user = database.query(User).filter(User.email == login_request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail={
            "error": "Invalid Credentials"
        })
    if not verify_user_password(user.password, login_request.password):
        raise HTTPException(status_code=404, detail={
            "error": "Invalid Credentials"
        })
    return user
