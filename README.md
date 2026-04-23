# 🤖 ResumeAnalyzer-AI

ResumeAnalyzer-AI is an AI-powered backend system that analyzes resumes (PDF format), extracts relevant skills, matches them against job requirements, and provides actionable recommendations.

---

## 🌐 Live Demo

*🔗 Web App: https://resume-analyzer-heenajhalani.streamlit.app/
*🔗 API Docs: https://resume-analyzer-ai-4xml.onrender.com/docs
*Live Demo: https://resume-analyzer-heenajhalani.streamlit.app/
---
## 🚀 Features

* 📄 Upload PDF resumes
* 🧠 Skill extraction using NLP
* 🔄 Synonym normalization (Node.js, JS, etc.)
* ⚖️ Match score calculation
* 💡 Smart recommendations for missing skills
* 🎯 Role-based analysis (Software Engineer, ML Engineer, etc.)
* 🌐 REST API built using FastAPI

---

## 🛠️ Tech Stack

* Python
* FastAPI
* PyPDF2
* NLP (rule-based + normalization)
* Uvicorn

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000/docs

---

## 📥 API Usage

### Endpoint:

POST `/analyze`

### Inputs:

* Resume (PDF file)
* Required skills (comma-separated) OR role

---

## 📤 Example Output

```json
{
  "summary": "Your resume matches 66.67% of the required skills",
  "matched_skills": ["python", "react"],
  "missing_skills": ["node.js"],
  "recommendations": ["Learn Node.js for backend development"]
}
```

---

## 🎯 Key Highlights

* Combines NLP + backend engineering
* Real-world use case (resume screening)
* Modular architecture
* Ready for deployment

---

## 👩‍💻 Author

Heena Jhalani
