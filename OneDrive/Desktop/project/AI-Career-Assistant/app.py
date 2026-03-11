import streamlit as st
import pdfplumber
from google import genai
import re

# -------------------------------
# GEMINI API KEY
# -------------------------------
client = genai.Client(api_key="AIzaSyANG5zR_gq8dSQnL6DPJnlrCsaoAlfO12w")

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Career Assistant")
st.write("Analyze resumes, build new resumes, and prepare for interviews using AI.")

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3 = st.tabs([
    "📄 Resume Analyzer",
    "📝 Resume Builder",
    "🎤 Interview Preparation"
])

# ==================================================
# TAB 1 : RESUME ANALYZER (YOUR CURRENT FEATURE)
# ==================================================
with tab1:

    st.header("📄 Resume Analyzer")

    def extract_text_from_pdf(file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def analyze_resume(resume_text):

        resume_text = resume_text[:4000]

        prompt = f"""
You are an expert resume reviewer.

Analyze the resume and provide:

Resume Score: <number>/100

Skills Found:
- skill
- skill

Missing Skills:
- skill
- skill

Suggested Improvements:
- improvement
- improvement

Recommended Career Roles:
- role
- role

Resume:
{resume_text}
"""

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return response.text

    def extract_score(text):
        match = re.search(r'(\d{1,3})/100', text)
        if match:
            return int(match.group(1))
        return None

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:

        st.success("Resume uploaded successfully!")

        resume_text = extract_text_from_pdf(uploaded_file)

        if st.button("🔍 Analyze Resume"):

            with st.spinner("Analyzing resume with AI..."):

                try:
                    result = analyze_resume(resume_text)

                    score = extract_score(result)

                    st.subheader("📊 Resume Analysis")

                    if score:
                        st.metric("Resume Score", f"{score}/100")
                        st.progress(score)

                    st.write(result)

                except:
                    st.error("AI busy. Showing demo output.")

                    st.write("""
Resume Score: 82/100

Skills Found:
- Python
- HTML
- CSS
- JavaScript

Missing Skills:
- Docker
- AWS
- Kubernetes

Suggested Improvements:
- Add project metrics
- Include GitHub links

Recommended Roles:
- Full Stack Developer
- Software Engineer
""")
def create_skill_chart(result_text):

    skills_found = []
    missing_skills = []

    lines = result_text.split("\n")

    found_section = False
    missing_section = False

    for line in lines:

        if "Skills Found" in line:
            found_section = True
            missing_section = False
            continue

        if "Missing Skills" in line:
            missing_section = True
            found_section = False
            continue

        if line.startswith("-"):
            skill = line.replace("-", "").strip()

            if found_section:
                skills_found.append(skill)

            if missing_section:
                missing_skills.append(skill)

    data = {
        "Skill": skills_found + missing_skills,
        "Status": ["Found"] * len(skills_found) + ["Missing"] * len(missing_skills)
    }

    df = pd.DataFrame(data)

    return df

# ==================================================
# TAB 2 : RESUME BUILDER
# ==================================================
with tab2:

    st.header("📝 AI Resume Builder")

    name = st.text_input("Full Name")
    skills = st.text_area("Skills")
    education = st.text_area("Education")
    experience = st.text_area("Experience / Projects")

    if st.button("Generate Resume"):

        prompt = f"""
Create a professional resume using the information below.

Name: {name}
Skills: {skills}
Education: {education}
Experience: {experience}

Generate a clean resume format with sections.
"""

        with st.spinner("Generating resume..."):

            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )

                st.subheader("Generated Resume")
                st.write(response.text)

            except:
                st.error("AI busy. Showing demo resume.")

                st.write("""
John Doe

Skills
- Python
- C
- HTML
- CSS

Education
B.Tech Computer Science

Project
Smart Helmet Crash Detection System using IoT and ML
""")


# ==================================================
# TAB 3 : INTERVIEW PREPARATION
# ==================================================
with tab3:

    st.header("🎤 Interview Preparation")

    resume_text = st.text_area("Paste your resume text")

    if st.button("Generate Interview Questions"):

        prompt = f"""
Based on this resume generate:

1. 5 Technical interview questions
2. 5 Behavioral interview questions
3. 3 HR questions

Resume:
{resume_text}
"""

        with st.spinner("Generating interview questions..."):

            try:
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt
                )

                st.subheader("Interview Questions")
                st.write(response.text)

            except:
                st.error("AI busy. Showing demo questions.")

                st.write("""
Technical Questions
• Explain REST API
• What is OOP?
• Difference between SQL and NoSQL

Behavioral Questions
• Describe a challenging project
• How do you manage deadlines?

HR Questions
• Why should we hire you?
• Where do you see yourself in 5 years?
""")