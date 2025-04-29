# 🧠 ATS Resume Analyzer – Match Your Resume to Any Job Description

This project simulates an Applicant Tracking System (ATS) to evaluate how well a resume matches a job description. It helps job seekers quickly identify missing skills, tools, or experiences that might be keeping them from landing interviews.

✅ Upload your resume as a PDF  
✅ Paste any job description  
✅ Get a match score (0–100)  
✅ See what's missing  
✅ Improve your resume before applying

---

## 📌 Features

- 📄 Upload resume in PDF format
- 📋 Paste job description as plain text
- 🔍 Extract and compare keywords using spaCy NLP
- 📊 Calculate ATS-style match score (0–100)
- 🚨 Identify missing skills, tools, and experience
- 💡 Suggest what to add to your resume

---

## 💡 How It Works

1. Extract text from uploaded **resume PDF** using `pdfplumber`
2. Extract **keywords** from resume and job description using `spaCy`
3. Compare both sets to:
   - Calculate match score
   - Identify missing keywords
   - Suggest improvements

---

## 🛠 Tech Stack

- **Python 3**
- [Google Colab](https://colab.research.google.com/)
- [`pdfplumber`](https://github.com/jsvine/pdfplumber) – for PDF text extraction
- [`spaCy`](https://spacy.io/) – for NLP and keyword extraction
- `google.colab.files` – for file upload

---

## 🔧 Setup Instructions (Google Colab)

1. Clone or open this repo in Google Colab
2. Install required libraries:

```python
!pip install pdfplumber
!pip install spacy
!python -m spacy download en_core_web_sm
