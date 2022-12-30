from sqlalchemy import Column, Integer, String
from connection import Base, Session, engine

session = Session()

class User(Base):
    __tablename__ = "users"

    id = Column(String(100), unique=True, primary_key=True)
    first_name = Column(String(15))
    email = Column(String(100), unique=True)
    password = Column(String(90))
    middle_name = Column(String(15), default=None)
    last_name = Column(String(15))
    age = Column(Integer)
    year = Column(Integer)

    def __repr__(self) -> str:
        return f'{self.first_name} {self.last_name} - {self.id}'
