from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    email: str
    middle_name: Optional[str] = None
    last_name: str
    age: int
    year: int
