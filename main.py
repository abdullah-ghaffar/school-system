from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal, get_db
from pydantic import BaseModel
from typing import List

# Database tables create karne ke liye
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Admission System API")

# --- CORS SETTINGS ---
# Isse aapka React (Localhost) Leapcell se connect ho payega
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Model (Data Validation) ---
# Ye aapke React ke formData (fullName, dob, gender, nationality) se match karta hai
class AdmissionCreate(BaseModel):
    fullName: str
    dob: str
    gender: str
    nationality: str

# --- Health Check Routes (Leapcell ke liye) ---
@app.get("/kaithhealthcheck")
@app.get("/kaithheathcheck")
def health_check():
    return {"status": "ok", "message": "Backend is running!"}

# --- API Endpoints ---

# 1. Welcome Route
@app.get("/")
def read_root():
    return {"message": "School API is Live", "docs": "/docs"}

# 2. CREATE: Naya admission jama karne ke liye
@app.post("/admissions/")
def create_admission(admission: AdmissionCreate, db: Session = Depends(get_db)):
    db_admission = models.Admission(
        fullName=admission.fullName,
        dob=admission.dob,
        gender=admission.gender,
        nationality=admission.nationality
    )
    db.add(db_admission)
    db.commit()
    db.refresh(db_admission)
    return {"message": "Admission saved successfully", "data": db_admission}

# 3. READ: Saare students ki list dekhne ke liye (Admin Panel ke liye)
@app.get("/admissions/")
def get_all_admissions(db: Session = Depends(get_db)):
    return db.query(models.Admission).all()

# 4. UPDATE: Student ka data edit karne ke liye
@app.put("/admissions/{student_id}")
def update_student(student_id: int, admission: AdmissionCreate, db: Session = Depends(get_db)):
    db_student = db.query(models.Admission).filter(models.Admission.id == student_id).first()
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Naya data update ho raha hai
    db_student.fullName = admission.fullName
    db_student.dob = admission.dob
    db_student.gender = admission.gender
    db_student.nationality = admission.nationality
    
    db.commit()
    db.refresh(db_student)
    return {"message": "Student updated successfully", "data": db_student}

# 5. DELETE: Student ko delete karne ke liye
@app.delete("/admissions/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(models.Admission).filter(models.Admission.id == student_id).first()
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}