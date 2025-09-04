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
