from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, get_db
from schemas import AdmissionCreate

# Database Tables create karna
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS: Frontend aur Backend ko connect karne ke liye zaroori hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit-admission")
def create_admission(admission: AdmissionCreate, db: Session = Depends(get_db)):
    try:
        new_student = models.StudentAdmission(
            full_name=admission.fullName,
            dob=admission.dob,
            gender=admission.gender,
            nationality=admission.nationality
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return {"status": "success", "message": "Admission successful!", "id": new_student.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students")
def list_students(db: Session = Depends(get_db)):
    return db.query(models.StudentAdmission).all()
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.StudentAdmission).filter(models.StudentAdmission.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Deleted successfully"}

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_data: AdmissionCreate, db: Session = Depends(get_db)):
    student_query = db.query(models.StudentAdmission).filter(models.StudentAdmission.id == student_id)
    student = student_query.first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_query.update({
        "full_name": updated_data.fullName,
        "dob": updated_data.dob,
        "gender": updated_data.gender,
        "nationality": updated_data.nationality
    })
    db.commit()
    return {"message": "Updated successfully"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)