import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError, jwt

from token_schema import TokenData

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def create_jwt_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    data_to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        data_to_encode, str(SECRET_KEY), algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_jwt_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data
