from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from config import config
import os

POSRGRES_DATABASE_URL = os.environ.get('DATABASE_URL', "postgresql://postgres:102296@localhost:5432/farmsupp")

engine = create_engine( POSRGRES_DATABASE_URL )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()