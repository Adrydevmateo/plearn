from pydantic import BaseModel

class ResumeData(BaseModel):
    title: str
    name: str
    profession: str
