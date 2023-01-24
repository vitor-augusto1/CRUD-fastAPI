from uuid import uuid4
import json

from datetime import datetime

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

    def test_should_return_422_unprocessable_entity_on_missing_required_fields(self):
        random_uuid = uuid4()
        data = {
            "email": f"test+{random_uuid}@email.com",
            "middle_name": "Test",
            "age": 19,
            "password": "new_password"
        }
        headers = {'Content-Type': 'application/json'}
        response = httpx.post(
            "http://localhost:8000/api/v1/user/",
            content=json.dumps(data),
            headers=headers
        )
        assert response.status_code == 422

    def test_should_return_200_on_successful_user_creation(self):
        now = datetime.now()
        data = {
            "first_name": "Test user",
            "email": f"test+{now.second}+test@email.com",
            "middle_name": "Test",
            "last_name": "Test",
            "age": 19,
            "year": 2003,
            "password": f"{now.day}+{now.hour}"
        }
        headers = {'Content-Type': 'application/json'}
        response = httpx.post(
            "http://localhost:8000/api/v1/user/",
            content=json.dumps(data),
            headers=headers
        )
        assert response.status_code == 200


class TestGetUserInformation:
    def test_should_return_401_unauthorized_on_invalid_JWT_token(self):
        headers = {
            "Authorization": "Bearer XXYxWv4Z4-L5K3nJvejYpNP8rjiMIfAjs"
        }
        response = httpx.get(
            "http://localhost:8000/api/v1/user/me",
            headers=headers
        )
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}

    def test_should_return_401_unauthorized_when_user_does_not_send_the_token(self):
        response = httpx.get(
            "http://localhost:8000/api/v1/user/me"
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_should_return_200_ok_on_valid_token(self):
        response = httpx.post(
            "http://localhost:8000/login",
            data={"username": "new@new.com", "password": "123"},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response_json = response.json()
        jwt_token = response_json.get('access_token')
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }
        response = httpx.get(
            "http://localhost:8000/api/v1/user/me",
            headers=headers
        )
        assert response.status_code == 200


class TestUpdateUserInformation:
    def test_should_return_200_ok_on_successful_update(self):
        login_response = httpx.post(
            "http://localhost:8000/login",
            data={"username": "new@new.com", "password": "123"},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response_json = login_response.json()
        jwt_token = response_json.get('access_token')
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        new_user_data = {
            "first_name": "New Data",
            "email": "new@new.com",
            "middle_name": "New",
            "last_name": "New Data",
            "age": 19,
            "year": 2003
        }
        response = httpx.put(
            "http://localhost:8000/api/v1/user/me",
            content=json.dumps(new_user_data),
            headers=headers
        )
        assert response.status_code == 200
        assert response.json() == {'success': 'User updated successfully'}
