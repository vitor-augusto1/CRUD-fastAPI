import pydantic
from utils.convert_to_optional import convert_to_optional

from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

class UserBase(BaseModel):
    id: UUID
    first_name: str
    email: str
    password: str
    middle_name: Optional[str]
    last_name: str
    age: int
    year: int


class UserCreate(UserBase):
    password: str


class UserOptional(UserBase):
    __annotations__ = convert_to_optional(UserBase)
