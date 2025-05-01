import streamlit as st
import pdfplumber
import spacy
import os
import warnings
import logging

# === Suppress warnings and logs ===
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# === Load spaCy model from local directory ===
model_path = os.path.join(os.path.dirname(__file__), "en_core_web_sm")
nlp = spacy.load(model_path)

# === Extract text from uploaded PDF ===
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# === Relevance filter for keywords ===
def is_relevant_keyword(keyword):
    irrelevant = {
        "the needs", "their needs", "a focus", "customer", "user", "project", "projects", "stakeholders",
        "your responsibilities", "multiple customers", "role", "good understanding", "responsibility",
        "background", "team", "client", "clients", "tasks", "services", "approach", "environment"
    }
    return (
        keyword not in irrelevant
        and len(keyword.split()) <= 4
        and not keyword.startswith(("the ", "your ", "our "))
    )

# === Extract keywords from technical sentences ===
def extract_keywords(text):
    doc = nlp(text)
    valid_keywords = set()
    for sent in doc.sents:
        sentence = sent.text.lower()
        if any(word in sentence for word in [
            "experience", "proficient", "familiar", "design", "develop", "build",
            "manage", "implement", "hands-on", "expertise", "knowledge", "skills in", "tools like"
        ]):
            for chunk in sent.noun_chunks:
                keyword = chunk.text.strip().lower()
                if (
                    len(keyword) > 2
                    and not keyword.isnumeric()
                    and is_relevant_keyword(keyword)
                ):
                    valid_keywords.add(keyword)
    return valid_keywords

# === Calculate score and missing terms ===
def calculate_score(resume_keywords, jd_keywords):
    matched_keywords = jd_keywords & resume_keywords
    missing_keywords = jd_keywords - resume_keywords
    total = len(jd_keywords)
    matched = len(matched_keywords)
    match_score = round((matched / total) * 100, 2) if total > 0 else 0
    return match_score, matched_keywords, missing_keywords

# === Generate smart suggestions ===
def generate_suggestion(keyword):
    keyword = keyword.lower()
    suggestion_templates = {
        "airflow": "✔ Built and scheduled automated ETL workflows using Apache Airflow.",
        "snowflake": "✔ Implemented cloud-based data warehousing using Snowflake.",
        "aws": "✔ Deployed scalable data infrastructure using AWS services like S3, Lambda, and EC2.",
        "gcp": "✔ Built and managed big data solutions on Google Cloud Platform (GCP).",
        "etl": "✔ Designed and optimized end-to-end ETL pipelines for real-time and batch processing.",
        "sql": "✔ Developed complex SQL queries and stored procedures for analytics reporting.",
        "python": "✔ Built data transformation scripts and machine learning pipelines using Python.",
        "dbt": "✔ Created and documented transformation models using dbt for the analytics layer.",
        "docker": "✔ Containerized applications and workflows using Docker for consistent deployment.",
        "kubernetes": "✔ Managed container orchestration and deployment with Kubernetes.",
        "ci/cd": "✔ Implemented CI/CD pipelines for automated testing and deployment.",
    }
    return suggestion_templates.get(
        keyword,
        f"✔ Consider adding a strong bullet point that demonstrates hands-on experience with <b>{keyword}</b>."
    )

# === Streamlit UI ===
st.set_page_config(page_title="ATS Resume Analyzer", layout="wide")
st.markdown("<h1 style='color:#2F80ED;'>📄 ATS Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#444;'>Upload your resume and paste the job description to get a match score and tailored suggestions to improve it.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📎 Upload Your Resume PDF", type=["pdf"])
job_description = st.text_area("📋 Paste Job Description Text Here")

# === Run the analysis ===
if uploaded_file and job_description:
    if st.button("🔍 Analyze Resume"):
        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            resume_keywords = extract_keywords(resume_text)
            jd_keywords = extract_keywords(job_description)
            score, matched, missing = calculate_score(resume_keywords, jd_keywords)

        color = "#27ae60" if score >= 75 else "#f39c12" if score >= 50 else "#c0392b"
        st.markdown(f"<h3 style='color:{color}'>✅ Match Score: {score}/100</h3>", unsafe_allow_html=True)
        st.progress(score / 100)

        if missing:
            st.warning("### ❌ Missing Keywords")
            badges = " ".join([
                f"<span style='background:#ddd;color:#111;border-radius:8px;padding:6px 10px;margin:2px;display:inline-block;'>{kw}</span>"
                for kw in list(missing)[:10]
            ])
            st.markdown(badges, unsafe_allow_html=True)

            st.info("### ✍️ Suggestions to Improve Your Resume")
            shown = 0
            for keyword in list(missing):
                suggestion = generate_suggestion(keyword)
                st.markdown(
                    f"<div style='background:#f7f9fc;color:#222;padding:10px 15px;border-left:5px solid #2F80ED;border-radius:4px;margin:8px 0;'>{suggestion}</div>",
                    unsafe_allow_html=True
                )
                shown += 1
                if shown >= 7:
                    break
        else:
            st.success("🎉 Great! Your resume covers all major requirements.")
else:
    st.info("⬆️ Upload your resume and paste a job description to begin.")
