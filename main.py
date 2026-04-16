from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal, get_db
from pydantic import BaseModel

# Database tables create karein
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware (React ke liye lazmi)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Checks for Leapcell
@app.get("/kaithhealthcheck")
@app.get("/kaithheathcheck")
def health_check():
    return {"status": "ok"}

# --- Pydantic Model (React Form se match hona chahiye) ---
class AdmissionCreate(BaseModel):
    fullName: str
    dob: str
    gender: str
    nationality: str

# --- API Endpoints ---

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
    return {"message": "Admission saved successfully!", "data": db_admission}

@app.get("/admissions/")
def get_admissions(db: Session = Depends(get_db)):
    return db.query(models.Admission).all()