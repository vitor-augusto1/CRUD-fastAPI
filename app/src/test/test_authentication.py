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

