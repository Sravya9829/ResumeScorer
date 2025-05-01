# 🧠 ATS Resume Analyzer – Match Your Resume to Any Job Description

This project simulates an Applicant Tracking System (ATS) to evaluate how well a resume aligns with a job description. It helps job seekers quickly identify missing skills, tools, or experiences that might be preventing them from landing interviews.

🎯 **Try the Live App:**  
👉 [ATS Resume Analyzer on Streamlit](https://resumescorer-d46tptilat39qtvmzkmy3p.streamlit.app)

---

## ✅ Features

- 📄 Upload your resume as a PDF  
- 📋 Paste any job description as plain text  
- 📊 Get an ATS-style match score (0–100)  
- 🚨 See missing skills, tools, and experiences  
- 💡 Get smart suggestions on what to add to your resume  

---

## 💡 How It Works

1. Extracts text from your uploaded resume PDF using `pdfplumber`  
2. Uses `spaCy` NLP to extract keywords from both resume and job description  
3. Compares both sets to:
   - ✅ Calculate a match score  
   - ❌ Identify what's missing  
   - 💡 Suggest improvements to boost your chances

---

## 🛠 Tech Stack

- **Python 3**
- **Streamlit** – for building the interactive web UI
- **pdfplumber** – for extracting text from PDF resumes
- **spaCy** – for NLP and keyword extraction

---

## 🚀 Setup Instructions (Local)

1. **Clone this repo**
2. Make sure Python 3 is installed
3. Install the required packages:
   ```bash
   pip install streamlit spacy pdfplumber
and run  locally streamlit run app.py
