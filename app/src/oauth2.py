from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.token import verify_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    return verify_jwt_token(token, credentials_exception)
