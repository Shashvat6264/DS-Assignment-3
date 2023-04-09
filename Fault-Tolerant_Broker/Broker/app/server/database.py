from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
PORT = os.getenv('PORT')
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app_" + str(PORT) + ".db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from .controllers.SqlDM import *

def get_db():
    db = SessionLocal()
    databaseManager = SqlDM(db)
    try:
        return databaseManager
    finally:
        db.close()