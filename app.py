import streamlit as st
import requests
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
import re

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


# 📄 PDF GENERATION
def generate_pdf(result):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph(result["summary"], styles["Title"]))
    content.append(Paragraph(f"Matched Skills: {', '.join(result['matched_skills'])}", styles["Normal"]))
    content.append(Paragraph(f"Missing Skills: {', '.join(result['missing_skills'])}", styles["Normal"]))

    doc.build(content)
    buffer.seek(0)
    return buffer


# 🔍 HIGHLIGHT FUNCTION
def highlight_skills(text, skills):
    for skill in skills:
        pattern = re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)
        text = pattern.sub(
            f"<span style='background-color:#22c55e; color:black; padding:2px 4px; border-radius:4px;'>{skill}</span>",
            text
        )
    return text


API_URL = "https://resume-analyzer-ai-4xml.onrender.com/analyze"

st.set_page_config(page_title="AI Resume Matcher", layout="centered")

# 🔐 LOGIN
if "user" not in st.session_state:
    st.title("🔐 Login")
    username = st.text_input("Enter your name to continue")
    if st.button("Login"):
        st.session_state["user"] = username
        st.success(f"Welcome {username}")
    st.stop()

# 🕒 HISTORY
if "history" not in st.session_state:
    st.session_state["history"] = []


# 🎨 UI
st.markdown("<h1 style='text-align:center;'>🚀 AI Resume Matcher</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Welcome, {st.session_state['user']}</p>", unsafe_allow_html=True)

st.markdown("---")

file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

col1, col2 = st.columns(2)

with col1:
    required_skills = st.text_input("Required Skills")

with col2:
    role = st.selectbox("Select Role", ["", "software engineer", "ml engineer", "frontend developer"])

st.markdown("---")

# 🚀 ANALYZE
if st.button("🔍 Analyze Resume"):

    if file is None:
        st.error("Please upload a resume")
        st.stop()

    if not required_skills and not role:
        st.warning("Enter skills or select a role")
        st.stop()

    with st.spinner("Analyzing your resume..."):

        # ✅ Extract text from PDF properly
        reader = PdfReader(file)
        resume_text = ""
        for page in reader.pages:
            if page.extract_text():
                resume_text += page.extract_text()

        files = {"file": file.getvalue()}
        data = {
            "required_skills": required_skills,
            "role": role
        }

        response = requests.post(API_URL, files=files, data=data)

        if response.status_code == 200:

            result = response.json()

            # save history
            st.session_state["history"].append(result)

            st.markdown("---")

            # 🎯 SCORE (fixed)
            score = float(re.findall(r"\d+\.?\d*", result["summary"])[0])

            st.markdown("## 🎯 Match Score")
            st.progress(score / 100)
            st.markdown(f"<h2 style='text-align:center; color:#22c55e;'>{score}%</h2>", unsafe_allow_html=True)

            # 📊 PIE CHART
            matched = len(result["matched_skills"])
            missing = len(result["missing_skills"])

            fig, ax = plt.subplots()
            ax.pie([matched, missing], labels=["Matched", "Missing"], autopct="%1.1f%%")
            st.pyplot(fig)

            st.markdown("---")

            # 📊 RESULTS
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### ✅ Matched Skills")
                for skill in result["matched_skills"]:
                    st.markdown(f"✔️ {skill}")

            with col2:
                st.markdown("### ❌ Missing Skills")
                for skill in result["missing_skills"]:
                    st.markdown(f"❌ {skill}")

            st.markdown("---")

            # 💡 RECOMMENDATIONS
            st.markdown("### 💡 Recommendations")
            for rec in result["recommendations"]:
                st.info(rec)

            st.markdown("---")

            # 🔍 HIGHLIGHT (FIXED)
            st.markdown("### 🔍 Resume Highlights")

            resume_text = resume_text.replace("\n", "  \n")
            highlighted = highlight_skills(resume_text, result["matched_skills"])

            st.markdown(highlighted[:3000], unsafe_allow_html=True)

            st.markdown("---")

            # 📄 DOWNLOAD
            pdf = generate_pdf(result)

            st.download_button(
                label="📄 Download Report",
                data=pdf,
                file_name="resume_analysis.pdf",
                mime="application/pdf"
            )

        else:
            st.error("Something went wrong.")


# 🕒 HISTORY
st.markdown("---")
st.subheader("🕒 Past Analyses")

for i, item in enumerate(st.session_state["history"]):
    st.write(f"{i+1}. {item['summary']}")