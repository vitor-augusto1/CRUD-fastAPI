from uuid import UUID
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from oauth2 import get_current_user

from user_schema import UserBase, UserCreate, UserOptional, ShowUser
from database.connection import SessionLocal, engine
from database import database_actions, User_Model

#User_Model.User.metadata.create_all(bind=engine)

router = APIRouter(
    tags=["users"],
    prefix="/api/v1/user"
)


@router.post("/")
async def create_new_user(new_user: UserCreate,
                          database: Session = Depends(database_actions.get_database)):
    user = database_actions.get_user_by_email(database, new_user.email)
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


@router.get("/me")
async def get_user(database: Session = Depends(database_actions.get_database),
                   current_user: User_Model.User = Depends(get_current_user)):
    user = database_actions.get_user_by_email(database, str(current_user.email))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error": "User not found"
        })
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "success": jsonable_encoder(user)
    })


@router.put("/me")
async def update_user(new_user_information: UserBase,
                      database_session: Session = Depends(database_actions.get_database),
                      current_user: User_Model.User = Depends(get_current_user)):
    stored_user = database_actions.get_user_by_email(
        database_session, str(current_user.email)
    )
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error": "User not found"
        })
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(database_actions.update_user(
            database_session, stored_user, new_user_information
        ))
    )


@router.patch("/me")
async def update_user_information(new_user_information: UserOptional,
    database_session: Session = Depends(database_actions.get_database),
    current_user: User_Model.User = Depends(get_current_user)):
    stored_user = database_actions.get_user_by_email(
        database_session, str(current_user.email)
    )
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error": "User not found"
        })
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(database_actions.update_user(
            database_session, stored_user, new_user_information
        ))
    )


@router.delete("/me")
async def delete_user(
    database_session: Session = Depends(database_actions.get_database),
    current_user: User_Model.User = Depends(get_current_user)):
    stored_user = database_actions.get_user_by_email(
        database_session, str(current_user.email)
    )
    if stored_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
            "error": "User not found"
        })
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=database_actions.delete_user(
        database_session, stored_user
    ))
