import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- FORCE PATH TO /tmp ---
# Humne check kiya ke root mein file nahi ban rahi, isliye hum 
# system ke temporary folder ko use kar rahe hain jo hamesha writable hota hai.
SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/admissions.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()