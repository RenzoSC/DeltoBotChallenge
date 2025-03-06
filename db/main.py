# models.py
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from db.tables import Base
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Creates all tables in the database if they are not created yet"""
    Base.metadata.create_all(bind=engine)
