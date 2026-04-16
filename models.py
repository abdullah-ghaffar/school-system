from sqlalchemy import Column, Integer, String
from database import Base

class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String)
    dob = Column(String)
    gender = Column(String)
    nationality = Column(String)