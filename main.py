from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal, get_db
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Database tables create karne ke liye
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Admission System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Iska matlab hai kisi bhi frontend ko allow karo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check Routes (Leapcell Fix) ---
@app.get("/kaithhealthcheck")
@app.get("/kaithheathcheck")
def health_check():
    return {"status": "ok", "message": "Backend is live and healthy!"}

# --- Pydantic Models (Data Validation) ---
class AdmissionCreate(BaseModel):
    student_name: str
    father_name: str
    grade: str
    contact_number: str

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the School Admission API", "docs": "/docs"}

# Admission submit karne ka endpoint
@app.post("/admissions/")
def create_admission(admission: AdmissionCreate, db: Session = Depends(get_db)):
    db_admission = models.Admission(
        student_name=admission.student_name,
        father_name=admission.father_name,
        grade=admission.grade,
        contact_number=admission.contact_number
    )
    db.add(db_admission)
    db.commit()
    db.refresh(db_admission)
    return {"message": "Admission submitted successfully", "data": db_admission}

# Tamam admissions dekhne ka endpoint
@app.get("/admissions/")
def get_all_admissions(db: Session = Depends(get_db)):
    admissions = db.query(models.Admission).all()
    return admissions