# EduPath Admin - Smart College Admissions Platform

**Project Link:** https://github.com/josephlualbak/edupath.git
---

## 📘 Project Summary

EduPath Admin is a **smart admissions platform** designed to **automate student placement** into university programs based on secondary school results. Built for college administrators, it evaluates eligibility, assigns students to courses across multiple universities, supports manual overrides, and generates **professional per-student and full allocations PDFs** for reporting.

---

## 🎯 Core Objectives

- Streamline university admissions and reduce administrative workload  
- Ensure **fair and transparent** student placement  
- Provide **audit trails**, override functionality, and professional reports  

---

## 🧩 Features

- **Excel Upload:** Supports batch student records with subjects and grades  
- **Course Matching Engine:** Allocates students to best-fit courses across all universities  
- **Manual Override:** Admins can reassign students in real-time via UI  
- **Per-Student Reports:** HTML and PDF reports showing scores, allocation, and reasoning  
- **Full Allocations PDF:** Professional, multi-page PDF for all students  
- **Immediate Updates:** Overrides are reflected instantly in the browser  
- **Offline Ready:** Local caching of student and university data  

---

## 📁 University JSON Format

Universities and courses are loaded from a JSON file:

```json
[
  {
    "name": "University of Nairobi",
    "country": "Kenya",
    "courses": [
      {"name": "Computer Science", "min_score": 12},
      {"name": "Arts", "min_score": 8}
    ]
  },
  {
    "name": "Makerere University",
    "country": "Uganda",
    "courses": [
      {"name": "Medicine", "min_score": 13},
      {"name": "Education", "min_score": 9}
    ]
  }
]
⚙️ Installation & Running Instructions
1. Clone or Download the Project
git clone https://github.com/josephlualbak/edupath.git
cd edupath

2. Create a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Install Required Dependencies
pip install fastapi uvicorn pandas openpyxl weasyprint jinja2


Explanation of Key Libraries:

fastapi → Web backend for serving API and UI

uvicorn → ASGI server to run FastAPI

pandas → Excel parsing and data manipulation

openpyxl → Reading/writing .xlsx files

weasyprint → PDF generation from HTML

jinja2 → HTML templating for per-student reports

4. Prepare University Data

Ensure universities.json exists in the project root with all university and course information.

5. Prepare Sample Student Excel

Create students.xlsx with the following columns:

Student ID | Name | Math | Biology | Chemistry | English | History


Grades can be A, B, C, etc., and will be automatically converted to numeric scores.

6. Start the Server
uvicorn api:app --reload


Server runs at: http://127.0.0.1:8000

--reload enables live reload during development

7. Access the Admin UI

Open your browser and go to:

http://127.0.0.1:8000


Features available from the UI:

Upload Excel for allocation

View per-student allocations

Apply manual overrides

Download per-student PDF or full allocations PDF

8. Manual Overrides

Enter Student ID, University, and Course in the “Manual Override” form

Overrides are applied immediately in the table and in reports

9. PDF Reports

Per-student PDF: Click the Student ID in the table to generate a report

Full Allocations PDF: Click Download PDF button to get a multi-page, professional PDF with all students

10. Stopping the Server

Press CTRL+C in the terminal where uvicorn is running.
