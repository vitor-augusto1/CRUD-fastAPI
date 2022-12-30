from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url_object = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="root",
    host="localhost",
    database="Users",
    port=3306
)

engine = create_engine(url_object)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
