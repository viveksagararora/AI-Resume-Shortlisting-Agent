# AI Resume Shortlisting Agent

## Project Overview

The AI Resume Shortlisting Agent is an AI-powered recruiter workflow automation system developed to simplify the resume screening and candidate shortlisting process.

The system:

* Parses resumes and job descriptions
* Performs semantic similarity matching
* Evaluates candidates using rubric-based AI scoring
* Ranks candidates automatically
* Supports HR override decisions
* Generates shortlist reports

The application uses transformer-based semantic embeddings and NLP techniques for intelligent candidate evaluation.

This project was developed as part of the TCI AI Enablement Internship Assignment.

---

# Setup Instructions

## Clone Repository

git clone <your-github-repo-link>

## Navigate to Project Folder

cd AI_Resume_Agent

## Create Virtual Environment

python -m venv venv

## Activate Virtual Environment (Windows)

.\venv\Scripts\activate

## Install Dependencies

pip install -r requirements.txt

## Run Application

streamlit run app.py

---

# Agent Architecture Diagram

```text
Job Description Upload
        ↓
Resume Upload
        ↓
Resume Parsing
        ↓
Embedding Generation
        ↓
Semantic Similarity Matching
        ↓
Rubric-Based AI Scoring
        ↓
Candidate Ranking
        ↓
HR Override
        ↓
CSV Report Export
```

# LLM & Framework Choice with Rationale

Frontend Framework: Streamlit
Reason: Rapid development of interactive AI workflow applications.

Programming Language: Python
Reason: Strong ecosystem for AI, NLP, and Machine Learning development.

Embedding Model: all-MiniLM-L6-v2
Reason: Lightweight, fast, free, and effective for semantic similarity tasks.

NLP Framework: Sentence Transformers
Reason: Efficient semantic embedding generation for resumes and job descriptions.

Similarity Metric: Cosine Similarity
Reason: Accurate semantic comparison between embeddings.

Resume Parsing Libraries: PyMuPDF and python-docx
Reason: Reliable text extraction from PDF and DOCX resumes.

Data Handling: Pandas
Reason: Structured candidate report generation and export.

Future Enhancement:
Future versions can integrate LLM-powered evaluation pipelines with LangChain-based caching and vector database support for scalable recruiter workflows.

---

# Security Mitigations

API Key Exposure
Mitigation: API keys stored securely in `.env` files.

Prompt Injection
Mitigation: Structured rubric-based evaluation pipeline used.

PII Exposure
Mitigation: Resume processing performed locally.

Unauthorized Access
Mitigation: Localhost-based deployment.

Hallucination Risk
Mitigation: Rule-based scoring with semantic thresholds.

Data Leakage
Mitigation: No permanent storage of resume data.

---

# Author

Vivek Sagar Arora
B.Tech CSE (AI/ML)
