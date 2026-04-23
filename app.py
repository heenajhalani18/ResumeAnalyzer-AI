import streamlit as st
import requests

API_URL = "https://resume-analyzer-ai-4xml.onrender.com/analyze"

st.set_page_config(page_title="AI Resume Matcher", layout="centered")

# 🎨 HEADER
st.title("🚀 AI Resume Matcher")
st.caption("Get instant resume insights, skill gaps, and recommendations")

st.markdown("---")

# 📄 INPUT SECTION
st.subheader("📄 Upload Your Resume")

file = st.file_uploader("Upload PDF", type=["pdf"])

col1, col2 = st.columns(2)

with col1:
    required_skills = st.text_input("Required Skills (comma-separated)")

with col2:
    role = st.selectbox(
        "Or Select Role",
        ["", "software engineer", "ml engineer", "frontend developer"]
    )

st.markdown("---")

# 🚀 BUTTON
if st.button("🔍 Analyze Resume"):

    if file is None:
        st.error("Please upload a resume")
        st.stop()

    if not required_skills and not role:
        st.error("Enter skills or select a role")
        st.stop()

    with st.spinner("Analyzing... ⏳"):

        files = {"file": file.getvalue()}
        data = {
            "required_skills": required_skills,
            "role": role
        }

        response = requests.post(API_URL, files=files, data=data)

        if response.status_code == 200:
            result = response.json()

            st.markdown("---")

            # 📊 SCORE
            score = result["summary"].split()[3]

            st.metric("🎯 Match Score", f"{score}")

            # 📊 PROGRESS BAR
            st.progress(float(score) / 100)

            st.markdown("---")

            # RESULTS IN COLUMNS
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")
                for skill in result["matched_skills"]:
                    st.success(skill)

            with col2:
                st.subheader("❌ Missing Skills")
                for skill in result["missing_skills"]:
                    st.error(skill)

            st.markdown("---")

            # 💡 RECOMMENDATIONS
            st.subheader("💡 Recommendations")
            for rec in result["recommendations"]:
                st.write("👉", rec)

        else:
            st.error("Something went wrong. Try again.")