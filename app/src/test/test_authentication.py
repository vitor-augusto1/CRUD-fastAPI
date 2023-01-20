from fastapi import HTTPException, status
import httpx
from utils.token import verify_jwt_token

def test_should_return_404_not_found_on_invalid_credentials():
    response = httpx.post(
        "http://localhost:8000/login",
        data={"username": "test@test.com", "password": "password"},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    assert response.status_code == 404
    assert response.json() == {'detail': {'error': 'Invalid Credentials'}}

def test_should_return_401_unauthorized_on_invalid_password():
    response = httpx.post(
        "http://localhost:8000/login",
        data={"username": "invalid@user.com", "password": "password"},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': {'error': 'Invalid Credentials'}}

def test_should_return_a_valid_JWT_token_on_successful_login():
    response = httpx.post(
        "http://localhost:8000/login",
        data={"username": "invalid@user.com", "password": "123"},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    response_json = response.json()
    jwt_token = response_json.get('access_token')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    response = verify_jwt_token(jwt_token, credentials_exception)
    assert response.email == "invalid@user.com"
