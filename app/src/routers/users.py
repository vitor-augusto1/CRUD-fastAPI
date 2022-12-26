from typing import List
from uuid import UUID, uuid4

from fastapi.responses import JSONResponse
from user_models import User

from fastapi import APIRouter, HTTPException

router = APIRouter()

user_list: List[User] = [
    User(
        id=UUID("440b410e-9192-4e15-bd59-234e933b411b"),
        first_name="Vitor Augusto",
        email="vitor@vitor.com",
        last_name="Guimaraes",
        age=19,
        year=2003
    )
]
print(user_list[0].id)


@router.post("/api/v1/user")
async def create_new_user(new_user: User):
    if any(new_user.email == user.email for user in user_list):
        raise HTTPException(status_code=409, detail={
            "error": "User already exists or Invalid email"
        })
    user_list.append(new_user)
    return JSONResponse(status_code=200, content={
        "success": "User created successfully"
    })

@router.get("/api/v1/user/{id}")
async def get_user(id: UUID):
    ...

@router.put("/api/v1/user/{id}")
async def update_user(*, id: UUID, new_user_information: User):
    ...

@router.delete("/api/v1/user/{id}")
async def delete_user(id: UUID):
    ...
