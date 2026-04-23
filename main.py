from fastapi import FastAPI, UploadFile, File, Form
from logic import extract_skills, match_score, missing_skills, extract_text_from_pdf, generate_recommendations, ROLE_SKILLS

app = FastAPI()

# ✅ HOME ROUTE (must exist)
@app.get("/")
def home():
    return {"message": "Resume Analyzer AI is running 🚀"}


# ✅ MAIN API ROUTE
@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    required_skills: str = Form(""),
    role: str = Form(None)
):

    # role-based logic
    if role:
        required_skills_list = ROLE_SKILLS.get(role.lower())
        if not required_skills_list:
            return {"error": "Invalid role provided"}
    else:
        required_skills_list = [
            skill.strip().lower()
            for skill in required_skills.split(",")
            if skill.strip()
        ]

    # extract text
    resume_text = extract_text_from_pdf(file.file)

    # process
    skills = extract_skills(resume_text)
    score, matched = match_score(skills, required_skills_list)
    missing = missing_skills(skills, required_skills_list)

    recommendations = generate_recommendations(missing)

    return {
        "summary": f"Your resume matches {score}% of the required skills",
        "extracted_skills": skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "recommendations": recommendations,
        "total_required_skills": len(required_skills_list),
        "matched_count": len(matched)
    }