import streamlit as st
import requests

# 🔗 Your deployed API
API_URL = "https://resume-analyzer-ai-4xml.onrender.com/analyze"

st.set_page_config(page_title="Resume Analyzer AI", layout="centered")

st.title("📄 Resume Analyzer AI")
st.write("Upload your resume and check your job match score 🚀")

# 📄 Upload resume
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# 🎯 Input fields
required_skills = st.text_input("Enter required skills (comma-separated)")
role = st.selectbox(
    "OR select a role",
    ["", "software engineer", "ml engineer", "frontend developer"]
)

# 🚀 Button
if st.button("Analyze Resume"):

    if file is None:
        st.error("Please upload a resume")
    else:
        with st.spinner("Analyzing resume..."):

            # Prepare request
            files = {"file": file.getvalue()}
            data = {
                "required_skills": required_skills,
                "role": role
            }

            # Call API
            response = requests.post(API_URL, files=files, data=data)

            if response.status_code == 200:
                result = response.json()

                st.success("Analysis Complete ✅")

                st.subheader("📊 Summary")
                st.write(result["summary"])

                st.subheader("✅ Matched Skills")
                st.write(result["matched_skills"])

                st.subheader("❌ Missing Skills")
                st.write(result["missing_skills"])

                st.subheader("💡 Recommendations")
                for rec in result["recommendations"]:
                    st.write("- ", rec)

            else:
                st.error("Something went wrong. Try again.")