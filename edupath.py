# ======================
# edupath.py - EduPath Allocation Logic
# ======================
import pandas as pd
import json
from pathlib import Path
from weasyprint import HTML
from datetime import datetime

# ----------------------
# Grade mapping for score calculation
# ----------------------
GRADE_TO_SCORE = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 0
}

# ----------------------
# Allocate students to best-fit courses
# ----------------------
def allocate(excel_path, uni_json_path, overrides=None):
    """
    Allocate students to university courses.
    """
    df = pd.read_excel(excel_path)
    with open(uni_json_path, "r", encoding="utf-8") as f:
        universities = json.load(f)

    df["Allocated University"] = ""
    df["Allocated Course"] = ""
    df["Reasoning"] = ""

    for idx, row in df.iterrows():
        student_id = str(row["Student ID"])

        # Apply override if exists
        if overrides and student_id in overrides:
            df.at[idx, "Allocated University"] = overrides[student_id]["university"]
            df.at[idx, "Allocated Course"] = overrides[student_id]["course"]
            df.at[idx, "Reasoning"] = "Manual override applied"
            continue

        # Compute total score
        total_score = sum(GRADE_TO_SCORE.get(str(row[sub]), 0) for sub in row.index if sub not in ["Student ID", "Name"])

        # Find best-fit course
        uni, course, reason = best_fit_allocation(row, universities, total_score)
        df.at[idx, "Allocated University"] = uni
        df.at[idx, "Allocated Course"] = course
        df.at[idx, "Reasoning"] = reason

    return df

# ----------------------
# Best-fit allocation logic
# ----------------------
def best_fit_allocation(student_row, universities, total_score):
    """
    Find the highest-tier course a student qualifies for across all universities
    """
    best_uni = ""
    best_course = ""
    reasoning = "No suitable course found"

    for uni in universities:
        uni_name = uni["name"]
        for course in uni["courses"]:
            min_score = course.get("min_score", 0)
            if total_score >= min_score:
                # Pick course with highest min_score <= total_score
                if not best_course or min_score > next((c["min_score"] for u in universities for c in u["courses"] if c["name"]==best_course), 0):
                    best_uni = uni_name
                    best_course = course["name"]
                    reasoning = f"Total score {total_score} meets minimum {min_score}"

    return best_uni, best_course, reasoning

# ----------------------
# Generate per-student HTML reports
# ----------------------
def generate_reports(df_alloc, report_dir: Path, pdf_dir: Path):
    """
    Generate HTML and PDF reports per student
    """
    report_dir.mkdir(exist_ok=True)
    pdf_dir.mkdir(exist_ok=True)

    for idx, row in df_alloc.iterrows():
        student_id = str(row["Student ID"])
        html_content = f"""
        <html>
        <head><title>Report {student_id}</title></head>
        <body>
        <h2>Student Report: {row['Name']} ({student_id})</h2>
        <table border="1" cellpadding="5" cellspacing="0">
        <tr><th>Subject</th><th>Grade</th></tr>
        """
        for col in df_alloc.columns:
            if col not in ["Student ID", "Name", "Allocated University", "Allocated Course", "Reasoning"]:
                html_content += f"<tr><td>{col}</td><td>{row[col]}</td></tr>"
        html_content += f"""
        </table>
        <p><b>Allocated University:</b> {row['Allocated University']}</p>
        <p><b>Allocated Course:</b> {row['Allocated Course']}</p>
        <p><b>Reasoning:</b> {row['Reasoning']}</p>
        </body></html>
        """

        html_path = report_dir / f"{student_id}.html"
        html_path.write_text(html_content, encoding="utf-8")

        pdf_path = pdf_dir / f"{student_id}.pdf"
        HTML(string=html_content).write_pdf(pdf_path)

# ----------------------
# Generate full allocations PDF
# ----------------------
def generate_full_pdf(df_alloc, pdf_path: Path):
    """
    Generate a professional, multi-page PDF for all students
    """
    html_content = """
    <html>
    <head>
    <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { text-align: center; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
    th, td { border: 1px solid #333; padding: 5px; text-align: center; font-size: 12px; }
    th { background-color: #3498db; color: white; }
    </style>
    </head>
    <body>
    <h1>Full Student Allocations</h1>
    <table>
    <tr>
        <th>Student ID</th>
        <th>Name</th>
        <th>Allocated University</th>
        <th>Allocated Course</th>
        <th>Reasoning</th>
    </tr>
    """

    for idx, row in df_alloc.iterrows():
        html_content += f"""
        <tr>
            <td>{row['Student ID']}</td>
            <td>{row['Name']}</td>
            <td>{row['Allocated University']}</td>
            <td>{row['Allocated Course']}</td>
            <td>{row['Reasoning']}</td>
        </tr>
        """

    html_content += """
    </table>
    </body></html>
    """

    HTML(string=html_content).write_pdf(pdf_path)

# ----------------------
# NEW: Generate allocations table for HTML injection in browser
# ----------------------
def generate_allocations_table(df_alloc):
    """
    Convert allocations DataFrame to HTML table for immediate browser display
    """
    html = "<table><tr><th>Student ID</th><th>Name</th><th>Allocated University</th><th>Allocated Course</th><th>Reasoning</th></tr>"
    for idx, row in df_alloc.iterrows():
        html += f"<tr><td>{row['Student ID']}</td><td>{row['Name']}</td>"
        html += f"<td>{row['Allocated University']}</td><td>{row['Allocated Course']}</td>"
        html += f"<td>{row['Reasoning']}</td></tr>"
    html += "</table>"
    return html
