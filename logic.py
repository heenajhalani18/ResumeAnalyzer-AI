#import spacy
from PyPDF2 import PdfReader

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

SYNONYMS = {
    "nodejs": "node.js",
    "node js": "node.js",
    "js": "javascript",
    "data structures & algorithms": "data structures",
    "dsa": "data structures",
}
ROLE_SKILLS = {
    "software engineer": ["python", "javascript", "sql", "data structures"],
    "ml engineer": ["python", "machine learning", "deep learning", "nlp"],
    "frontend developer": ["react", "javascript", "html", "css"]
}

# predefined skills
SKILLS_DB = [
    "python", "java", "c++", "machine learning",
    "data analysis", "sql", "deep learning",
    "nlp", "fastapi", "django", "flask",
    "react", "html", "css", "javascript"
]


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text

def normalize(text):
    text = text.lower()
    for k, v in SYNONYMS.items():
        text = text.replace(k, v)
    return text


def extract_skills(text):
    text = normalize(text)
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


def match_score(candidate_skills, required_skills):
    if len(required_skills) == 0:
        return 0, []

    matched = set(candidate_skills) & set(required_skills)
    score = len(matched) / len(required_skills)

    return round(score * 100, 2), list(matched)

def missing_skills(candidate_skills, required_skills):
    return list(set(required_skills) - set(candidate_skills))

def generate_recommendations(missing_skills):
    
    recommendations_map = {
        "python": "Improve Python proficiency by building projects and practicing coding problems",
        "sql": "Learn SQL for database querying and management",
        "react": "Practice building frontend applications using React",
        "javascript": "Strengthen JavaScript fundamentals and async programming",
        "node.js": "Learn Node.js for backend development",
        "machine learning": "Study ML algorithms and build ML projects",
        "deep learning": "Explore neural networks and deep learning frameworks",
        "nlp": "Learn Natural Language Processing techniques",
        "data structures": "Practice data structures and algorithms for problem-solving",
        "html": "Improve HTML skills for structuring web pages",
        "css": "Enhance CSS for responsive and modern UI design"
    }

    recommendations = []

    for skill in missing_skills:
        if skill in recommendations_map:
            recommendations.append(recommendations_map[skill])
        else:
            recommendations.append(f"Consider learning {skill}")

    return recommendations
