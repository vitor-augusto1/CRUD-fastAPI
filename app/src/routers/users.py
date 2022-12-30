from typing import List
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from user_schema import UserBase, UserCreate, UserOptional
from database.connection import SessionLocal, engine
from database import database_actions, User_Model

#User_Model.User.metadata.create_all(bind=engine)

router = APIRouter()


def get_database():
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()


@router.post("/api/v1/user")
async def create_new_user(new_user: UserCreate, database: Session = Depends(get_database)):
    user = database_actions.get_user_by_email(database, new_user.email)
    print(user)
    if user:
        raise HTTPException(status_code=400, detail={
            "error": "Email already registered"
        })
    user_created = database_actions.create_new_user(
        database_session=database, new_user=new_user
    )
    return JSONResponse(status_code=200, content={
        "success": jsonable_encoder(user_created)
    })

@router.get("/api/v1/user/{user_id}")
async def get_user(user_id: UUID, database: Session = Depends(get_database)):
    user = database_actions.get_user_by_id(database, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={
            "error": "User not found"
        })
    return JSONResponse(status_code=200, content={
        "success": jsonable_encoder(user)
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
