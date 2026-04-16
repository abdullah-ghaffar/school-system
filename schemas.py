from pydantic import BaseModel

class AdmissionCreate(BaseModel):
    fullName: str
    dob: str
    gender: str
    nationality: str

    class Config:
        from_attributes = True