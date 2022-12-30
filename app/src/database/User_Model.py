from sqlalchemy import Column, Integer, String
from .connection import Base, engine

class User(Base):
    __tablename__ = "users"

    id = Column(String(100), unique=True, primary_key=True)
    first_name = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(90))
    middle_name = Column(String(100), default=None)
    last_name = Column(String(100))
    age = Column(Integer)
    year = Column(Integer)

    def __repr__(self) -> str:
        return f'{self.first_name} {self.last_name} - {self.id}'

User.metadata.create_all(bind=engine)
