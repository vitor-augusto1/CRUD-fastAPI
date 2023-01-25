from uuid import uuid4
import json

from datetime import datetime

import httpx


class TestCreateNewUser:
    url = 'http://localhost:8000/api/v1/user/'
    json_header = {'Content-Type': 'application/json'}

    def test_should_return_400_bad_request_on_invalid_email(self):
        data = {
            'first_name': 'New User',
            'email': 'alredytakenemailcom',
            'middle_name': 'User new',
            'last_name': 'Last Name',
            'age': 19,
            'year': 2003,
            'password': 'new_password',
        }
        response = httpx.post(
            self.url, content=json.dumps(data), headers=self.json_header
        )
        assert response.status_code == 400
        assert response.json() == {'detail': {'error': 'Invalid Email'}}

    def test_should_return_400_bad_request_on_email_already_exists(self):
        data = {
            'first_name': 'New User',
            'email': 'alredytaken@email.com',
            'middle_name': 'User new',
            'last_name': 'Last Name',
            'age': 19,
            'year': 2003,
            'password': 'new_password',
        }
        response = httpx.post(
            self.url, content=json.dumps(data), headers=self.json_header
        )
        assert response.status_code == 400
        assert response.json() == {
            'detail': {'error': 'Email already registered'}
        }

    def test_should_return_422_unprocessable_entity_on_missing_required_fields(
        self,
    ):
        random_uuid = uuid4()
        data = {
            'email': f'test+{random_uuid}@email.com',
            'middle_name': 'Test',
            'age': 19,
            'password': 'new_password',
        }
        response = httpx.post(
            self.url, content=json.dumps(data), headers=self.json_header
        )
        assert response.status_code == 422

    def test_should_return_200_on_successful_user_creation(self):
        now = datetime.now()
        data = {
            'first_name': 'Test user',
            'email': f'test+{now.second}+test@email.com',
            'middle_name': 'Test',
            'last_name': 'Test',
            'age': 20,
            'year': 2002,
            'password': f'{now.day}+{now.hour}',
        }
        response = httpx.post(
            self.url, content=json.dumps(data), headers=self.json_header
        )
        assert response.status_code == 200


class TestGetUserInformation:
    url = 'http://localhost:8000/api/v1/user/me'
    login_url = 'http://localhost:8000/login'
    url_encoder_header = {'Content-Type': 'application/x-www-form-urlencoded'}

    def test_should_return_401_unauthorized_on_invalid_JWT_token(self):
        headers = {'Authorization': 'Bearer XXYxWv4Z4-L5K3nJvejYpNP8rjiMIfAjs'}
        response = httpx.get(self.url, headers=headers)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}

    def test_should_return_401_unauthorized_when_user_does_not_send_the_token(
        self,
    ):
        response = httpx.get(self.url)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Not authenticated'}

    def test_should_return_200_ok_on_valid_token(self):
        response = httpx.post(
            self.login_url,
            data={'username': 'new@new.com', 'password': '123'},
            headers=self.url_encoder_header,
        )
        response_json = response.json()
        jwt_token = response_json.get('access_token')
        headers = {'Authorization': f'Bearer {jwt_token}'}
        response = httpx.get(self.url, headers=headers)
        assert response.status_code == 200


class TestUpdateUserInformation:
    url = 'http://localhost:8000/api/v1/user/me'
    login_url = 'http://localhost:8000/login'
    url_encoder_header = {'Content-Type': 'application/x-www-form-urlencoded'}

    def test_should_return_401_unauthorized_on_invalid_JWT_token(self):
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5c.DU2NTkzMX0',
            'Content-Type': 'application/json',
        }
        new_user_data = {
            'first_name': 'New Data',
            'email': 'new@new.com',
            'middle_name': 'New',
            'last_name': 'New Data',
            'age': 19,
            'year': 2003,
        }
        response = httpx.put(
            self.url, content=json.dumps(new_user_data), headers=headers
        )
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}

    def test_should_return_200_ok_on_successful_update(self):
        login_response = httpx.post(
            self.login_url,
            data={'username': 'new@new.com', 'password': '123'},
            headers=self.url_encoder_header,
        )
        response_json = login_response.json()
        jwt_token = response_json.get('access_token')
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }
        new_user_data = {
            'first_name': 'New Data',
            'email': 'new@new.com',
            'middle_name': 'New',
            'last_name': 'New Data',
            'age': 19,
            'year': 2003,
        }
        response = httpx.put(
            self.url, content=json.dumps(new_user_data), headers=headers
        )
        assert response.status_code == 200
        assert response.json() == {'success': 'User updated successfully'}

    def test_should_return_200_ok_on_successful_partial_update(self):
        login_response = httpx.post(
            self.login_url,
            data={'username': 'new@new.com', 'password': '123'},
            headers=self.url_encoder_header,
        )
        response_json = login_response.json()
        jwt_token = response_json.get('access_token')
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }
        new_user_data = {
            'first_name': 'New First Name',
            'age': 20,
            'year': 2002,
        }
        response = httpx.patch(
            self.url, content=json.dumps(new_user_data), headers=headers
        )
        assert response.status_code == 200
        assert response.json() == {'success': 'User updated successfully'}
