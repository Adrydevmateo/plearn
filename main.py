# Builtins
import uuid
from io import BytesIO
from pydantic import BaseModel

# External
from fastapi import FastAPI, APIRouter
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from weasyprint import HTML

from templates.classic import classic_template

class ResumeData(BaseModel):
    template: str
    title: str
    name: str
    profession: str

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "Welcome to my API!"}

@app.post("/generate-resume")
async def generate_resume(data: ResumeData):
    if data.template == "classic":
        html_content = classic_template.format(
            title=data.title,
            name=data.name,
            profession=data.profession
        )
    pdf_bytes = BytesIO()
    HTML(string=html_content).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)
    pdf_filename = f"resume_{uuid.uuid4().hex}.pdf"
    return StreamingResponse(pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={pdf_filename}"})