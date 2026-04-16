from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class StudentAdmission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)