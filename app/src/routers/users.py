from uuid import UUID
from user_models import User

from fastapi import APIRouter

router = APIRouter()

user = list()


@router.post("/api/v1/user")
async def create_new_user(new_user: User):
    ...

@router.get("/api/v1/user/{id}")
async def get_user(id: UUID):
    ...

@router.put("/api/v1/user/{id}")
async def update_user(*, id: UUID, new_user_information: User):
    ...

@router.delete("/api/v1/user/{id}")
async def delete_user(id: UUID):
    ...
