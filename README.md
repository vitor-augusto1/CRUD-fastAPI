# User CRUD API

This is a simple CRUD (Create, Read, Update, Delete) API for managing users,
built with the [FastAPI](https://fastapi.tiangolo.com/) web framework and
connected to a MySQL database.

## Features

- User registration
- User login
- Retrieve user information
- Update user information
- Delete user

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server

### Installation

1. Clone the repository

`git clone https://github.com/<username>/user-crud-api.git`

2. Create a virtual environment and activate it

`python3 -m venv venv`
`source venv/bin/activate`

3. Install the dependencies

`pip install -r requirements.txt`

4. Create a `.env` file in the root of the project and add the following
variables:

`
DB_HOST="<your_database_url>"
DB_USERNAME="<your_database_username>"
DB_PASSWORD="<your_database_password>"
DB_NAME="<your_database_name>"
DB_PORT=<port_running_the_database>
SECRET_KEY="<your_jwt_secret_key>"
`

5. Run the development server

`uvicorn main:app --reload`

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [MySQL](https://www.mysql.com/) - The database used
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Used for data validation
- [pytest](https://docs.pytest.org/en/latest/) - Used for testing
- [httpx](https://www.python-httpx.org/) - Used for making HTTP requests
- [sqlAlchemy](https://www.sqlalchemy.org/) - Used as ORM for database operations
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Used for handling environment variables
- [bcrypt](https://pypi.org/project/bcrypt/) - Used for password hashing
- [jwt](https://pypi.org/project/PyJWT/) - Used for JSON Web Tokens
