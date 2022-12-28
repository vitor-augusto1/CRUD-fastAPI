from typing import List
from uuid import UUID
from fastapi.encoders import jsonable_encoder

from fastapi.responses import JSONResponse
from user_models import UserBase, UserCreate, UserOptional

from fastapi import APIRouter, HTTPException

router = APIRouter()

user_list: List[UserBase] = [
    UserCreate(
        id=UUID("440b410e-9192-4e15-bd59-234e933b411b"),
        password="asdjcajkdbvjkdvjadcv",
        first_name="Vitor Augusto",
        email="vitor@vitor.com",
        last_name="Guimaraes",
        age=19,
        year=2003
    )
]


@router.post("/api/v1/user")
async def create_new_user(new_user: UserCreate):
    if any(new_user.email == user.email for user in user_list):
        raise HTTPException(status_code=409, detail={
            "error": "User already exists or an Invalid email was provided"
        })
    user_list.append(new_user)
    return JSONResponse(status_code=200, content={
        "success": "User created successfully"
    })


@router.get("/api/v1/user/{user_id}")
async def get_user(user_id: UUID):
    for user in user_list:
        if user.id == user_id:
            return JSONResponse(status_code=200, content={
                "user": jsonable_encoder(user)
            })
    raise HTTPException(status_code=404, detail={
        "error": "User does not exists"
    })


@router.put("/api/v1/user/{user_id}")
async def update_user(user_id: UUID, new_user_information: UserBase):
    for user in user_list:
        if user.id == user_id:
            i = user_list.index(user)
            user_list[i] = new_user_information
            return JSONResponse(status_code=200, content={
                "success": "User updated successfully"
            })
    raise HTTPException(status_code=404, detail={
        "error": "User not found"
    })


@router.patch("/api/v1/user/{user_id}")
async def update_user_information(user_id: UUID, new_user_information: UserOptional):
    for stored_user in user_list:
        if stored_user.id == user_id:
            stored_user_model = UserOptional(**dict(stored_user))
            new_user_data = new_user_information.dict(exclude_unset=True)
            updated_User = stored_user_model.copy(update=new_user_data)
            i = user_list.index(stored_user)
            user_list[i] = updated_User
            return updated_User
    raise HTTPException(status_code=400, detail={
        "error": "User not found"
    })


@router.delete("/api/v1/user/{id}")
async def delete_user(id: UUID):
    for user in user_list:
        if user.id == id:
            i = user_list.index(user)
            del user_list[i]
            return True
    raise HTTPException(status_code=404, detail={
        "error": "User not found"
    })
