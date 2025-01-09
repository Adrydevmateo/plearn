# Builtins
import uuid
from io import BytesIO

# External
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from weasyprint import HTML

# Apps
from app.models.resume import ResumeData
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/generate")
async def generate_resume(data: ResumeData, _: dict = Depends(get_current_user)):
    html_template = """<!DOCTYPE html>
        <html>
        <head>
          <style>
            html {{
                font-size: 20px;
                font-weight: bold;
            }}
            body {{
                font-family: Arial, sans-serif;
                background: #242424;
                color: #fff;
            }}
            h1 {{
                color: royalblue;
            }}
          </style>
        </head>
        <body>
          <h1>{title}</h1>
          <p>Name: {name}</p>
          <p>Profession: {profession}</p>
        </body>
        </html>"""
    html_content = html_template.format(
        title=data.title,
        name=data.name,
        profession=data.profession
    )
    pdf_bytes = BytesIO()
    HTML(string=html_content).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)
    pdf_filename = f"resume_{uuid.uuid4().hex}.pdf"
    return StreamingResponse(pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={pdf_filename}"})
