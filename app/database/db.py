
from database.models import *
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from settings import get_settings

# Create the engine for SQLAlchemy (SQLModel uses SQLAlchemy under the hood)
engine = create_engine(get_settings().DATABASE_URL.unicode_string(), echo=False)
get_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

def init_db():
    SQLModel.metadata.create_all(engine)