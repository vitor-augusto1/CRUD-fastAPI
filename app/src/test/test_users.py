from uuid import uuid4
import json

import httpx

class TestCreateNewUser:
    def test_should_return_400_bad_request_on_invalid_email(self):
        data = {
            "first_name": "New User",
            "email": "alredytakenemailcom",
            "middle_name": "User new",
            "last_name": "Last Name",
            "age": 19,
            "year": 2003,
            "password": "new_password"
        }
        headers = {'Content-Type': 'application/json'}
        response = httpx.post("http://localhost:8000/api/v1/user/", content=json.dumps(data), headers=headers)
        assert response.status_code == 400
        assert response.json() == {'detail': {'error': 'Invalid Email'}}

    def test_should_return_400_bad_request_on_email_already_exists(self):
        data = {
            "first_name": "New User",
            "email": "alredytaken@email.com",
            "middle_name": "User new",
            "last_name": "Last Name",
            "age": 19,
            "year": 2003,
            "password": "new_password"
        }
        headers = {'Content-Type': 'application/json'}
        response = httpx.post("http://localhost:8000/api/v1/user/", content=json.dumps(data), headers=headers)
        assert response.status_code == 400
        assert response.json() == {'detail': {'error': 'Email already registered'}}

    def test_should_return_200_on_successful_user_creation(self):
        random_uuid = uuid4()
        data = {
            "first_name": "Test user",
            "email": f"test+{random_uuid}@email.com",
            "middle_name": "Test",
            "last_name": "Test",
            "age": 19,
            "year": 2003,
            "password": "new_password"
        }
        headers = {'Content-Type': 'application/json'}
        response = httpx.post(
            "http://localhost:8000/api/v1/user/",
            content=json.dumps(data),
            headers=headers
        )
        assert response.status_code == 200

