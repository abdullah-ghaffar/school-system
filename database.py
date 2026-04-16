import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Configuration ---

# Leapcell ya serverless environments mein root directory 'read-only' ho sakti hai.
# Isliye hum check karte hain ke agar environment variable 'LEAPCELL_SERVICE_ID' maujood hai,
# toh database ko /tmp folder mein banayein kyunke wo 'writable' hota hai.

if os.environ.get("LEAPCELL_SERVICE_ID"):
    # Server path
    SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/admissions.db"
    print("Running on Cloud: Using /tmp/admissions.db")
else:
    # Local machine path
    SQLALCHEMY_DATABASE_URL = "sqlite:///./admissions.db"
    print("Running Locally: Using ./admissions.db")

# --- Engine Setup ---

# connect_args={"check_same_thread": False} sirf SQLite ke liye zaroori hota hai
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- Dependency ---

# Is function ko FastAPI ke routes mein 'Depends(get_db)' ke taur par use karte hain
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()