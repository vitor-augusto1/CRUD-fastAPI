from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import database_actions
from database.User_Model import User
from utils.token import create_jwt_access_token
from utils.verify_password import verify_user_password

router = APIRouter(tags=['authentication'])


@router.post('/login')
def login(
    login_request: OAuth2PasswordRequestForm = Depends(),
    database: Session = Depends(database_actions.get_database),
):
    user = (
        database.query(User)
        .filter(User.email == login_request.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'error': 'Invalid Credentials'},
        )
    if not verify_user_password(user.password, login_request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'error': 'Invalid Credentials'},
        )
    access_token = create_jwt_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
