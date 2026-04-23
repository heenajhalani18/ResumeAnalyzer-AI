import streamlit as st
import requests

API_URL = "https://resume-analyzer-ai-4xml.onrender.com/analyze"

st.set_page_config(page_title="AI Resume Matcher", layout="centered")

# 🎨 CUSTOM STYLING
st.markdown("""
    <style>
        .main {
            background-color: #0f172a;
            color: white;
        }
        .stButton>button {
            background-color: #6366f1;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .stFileUploader {
            background-color: #1e293b;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 🚀 HEADER
st.markdown("<h1 style='text-align: center;'>🚀 AI Resume Matcher</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analyze your resume and discover skill gaps instantly</p>", unsafe_allow_html=True)

st.markdown("---")

# 📄 INPUT CARD
st.markdown("### 📄 Upload Resume")

file = st.file_uploader("Upload PDF", type=["pdf"])

col1, col2 = st.columns(2)

with col1:
    required_skills = st.text_input("Required Skills")

with col2:
    role = st.selectbox("Select Role", ["", "software engineer", "ml engineer", "frontend developer"])

st.markdown("---")

# 🚀 ANALYZE BUTTON
if st.button("🔍 Analyze Resume"):

    if file is None:
        st.error("Please upload a resume")
        st.stop()

    if not required_skills and not role:
        st.warning("Enter skills or select a role")
        st.stop()

    with st.spinner("Analyzing your resume..."):

        files = {"file": file.getvalue()}
        data = {
            "required_skills": required_skills,
            "role": role
        }

        response = requests.post(API_URL, files=files, data=data)

        if response.status_code == 200:
            result = response.json()

            st.markdown("---")

            # 🎯 SCORE SECTION
            score = float(result["summary"].split()[3])

            st.markdown("## 🎯 Match Score")
            st.progress(score / 100)
            st.markdown(f"<h2 style='text-align:center; color:#22c55e;'>{score}%</h2>", unsafe_allow_html=True)

            st.markdown("---")

            # 📊 RESULTS GRID
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

        else:
            st.error("Something went wrong. Please try again.")