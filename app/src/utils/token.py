from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from jose import JWTError, jwt
from token_schema import Token, TokenData

SECRET_KEY = '2c1f5d3baf228e5cd69d15df429ad032fea06f5d44ba2c773c4a710507e9ce0c'
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
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_jwt_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data
