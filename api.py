# ======================
# api.py - EduPath Admin
# ======================
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil, os
from pathlib import Path
import edupath  # your main allocation logic
import uvicorn

app = FastAPI(title="EduPath Admin")

# Allow cross-origin for frontend testing/demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
REPORT_DIR = BASE_DIR / "reports"
PDF_DIR = BASE_DIR / "pdfs"
UNI_JSON = BASE_DIR / "universities.json"

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

# Store manual overrides in memory
overrides = {}

# ======================
# Serve index.html
# ======================
@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = BASE_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(index_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Index.html not found</h1>")

# ======================
# Upload Excel & Allocate
# ======================
@app.post("/allocate", response_class=HTMLResponse)
async def allocate(file: UploadFile):
    # Save uploaded Excel
    excel_path = UPLOAD_DIR / file.filename
    with open(excel_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Call allocation logic
    df_alloc = edupath.allocate(excel_path, uni_json_path=UNI_JSON, overrides=overrides)

    # Generate per-student reports (HTML & PDF)
    edupath.generate_reports(df_alloc, REPORT_DIR, PDF_DIR)

    # Return updated allocations table HTML
    html_table = edupath.generate_allocations_table(df_alloc)
    return HTMLResponse(html_table)

# ======================
# Manual Override
# ======================
@app.post("/override", response_class=HTMLResponse)
async def apply_override(
    student_id: str = Form(...),
    university: str = Form(...),
    course: str = Form(...)
):
    # Save override
    overrides[student_id] = {"university": university, "course": course}

    # Re-run allocation to apply override
    latest_file = max(UPLOAD_DIR.glob("*.xlsx"), key=os.path.getctime)
    df_alloc = edupath.allocate(latest_file, uni_json_path=UNI_JSON, overrides=overrides)
    edupath.generate_reports(df_alloc, REPORT_DIR, PDF_DIR)
    html_table = edupath.generate_allocations_table(df_alloc)
    return HTMLResponse(html_table)

# ======================
# Per-student PDF download
# ======================
@app.get("/download_pdf/{student_id}")
async def download_student_pdf(student_id: str):
    pdf_path = PDF_DIR / f"{student_id}.pdf"
    if pdf_path.exists():
        return FileResponse(pdf_path, filename=f"{student_id}_report.pdf")
    return HTMLResponse(f"<h3>PDF not found for {student_id}</h3>")

# ======================
# Full allocations PDF download
# ======================
@app.get("/download_full_pdf")
async def download_full_pdf():
    pdf_path = PDF_DIR / "allocations_full.pdf"
    # Generate full allocations PDF if not exists
    if not pdf_path.exists():
        # Find latest Excel
        latest_file = max(UPLOAD_DIR.glob("*.xlsx"), key=os.path.getctime)
        df_alloc = edupath.allocate(latest_file, uni_json_path=UNI_JSON, overrides=overrides)
        edupath.generate_full_pdf(df_alloc, pdf_path)
    return FileResponse(pdf_path, filename="allocations_full.pdf")

# ======================
# Run server
#Please make sure to set host="127.0.0.1" if you run it locally
# ======================
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
