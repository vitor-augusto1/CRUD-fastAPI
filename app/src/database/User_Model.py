from sqlalchemy import Column, Integer, String
from connection import Base

class User(Base):
    __tablename__ = "users"
    first_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    year = Column(Integer)
    id = Column(String, unique=True, primary_key=True)
