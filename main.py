import uuid
from io import BytesIO
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from weasyprint import HTML

app = FastAPI()

# Enable CORS
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"]
)

class ResumeData(BaseModel):
    title: str
    name: str
    profession: str

@app.post("/generate-resume")
async def generate_resume(data: ResumeData):
    # HTML template with placeholders
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

    # Replace placeholders with the provided data
    html_content = html_template.format(
        title=data.title,
        name=data.name,
        profession=data.profession
    )

    # Generate PDF in memory
    pdf_bytes = BytesIO()
    HTML(string=html_content).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)

    pdf_filename = f"resume_{uuid.uuid4().hex}.pdf"

    # Return the PDF as a response
    return StreamingResponse(pdf_bytes, media_type="application/json", headers={"Content-Disposition": f"attachment; filename={pdf_filename}"})
