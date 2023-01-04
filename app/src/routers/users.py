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
router = APIRouter(
    prefix="/api/v1/user"
)


@router.post("/api/v1/user")
@router.post("/")
async def create_new_user(new_user: UserCreate,
                          database: Session = Depends(database_actions.get_database)):
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
@router.get("/{user_id}")
async def get_user(user_id: UUID, database: Session = Depends(database_actions.get_database)):
    user = database_actions.get_user_by_id(database, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail={
            "error": "User not found"
        })
    return JSONResponse(status_code=200, content={
        "success": jsonable_encoder(user)
    })


@router.put("/api/v1/user/{user_id}")
@router.put("/{user_id}")
async def update_user(user_id: UUID, new_user_information: UserBase,
                      database_session: Session = Depends(database_actions.get_database)):
    stored_user = database_actions.get_user_by_id(database_session, user_id)
    if stored_user is None:
        raise HTTPException(status_code=404, detail={
            "error": "User not found"
        })
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(database_actions.update_user(
            database_session, stored_user, new_user_information
        ))
    )


@router.patch("/api/v1/user/{user_id}")
@router.patch("/{user_id}")
async def update_user_information(
    user_id: UUID, new_user_information: UserOptional,
    database_session: Session = Depends(database_actions.get_database)):

    stored_user = database_actions.get_user_by_id(database_session, user_id)
    if stored_user is None:
        raise HTTPException(status_code=404, detail={
            "error": "User not found"
        })
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder(database_actions.update_user(
            database_session, stored_user, new_user_information
        ))
    )


@router.delete("/api/v1/user/{user_id}")
@router.delete("/{user_id}")
async def delete_user(user_id: UUID,
                      database_session: Session = Depends(database_actions.get_database)):
    stored_user = database_actions.get_user_by_id(database_session, user_id)
    if stored_user is None:
        raise HTTPException(status_code=404, detail={
            "error": "User not found"
        })
    return JSONResponse(status_code=200, content=database_actions.delete_user(
        database_session, stored_user
    ))
