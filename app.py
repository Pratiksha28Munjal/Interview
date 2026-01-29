import streamlit as st
import requests
from pypdf import PdfReader
import ollama
import hashlib
import sqlite3
import auth
from auth import *





st.set_page_config(
    page_title="AI Interview Mate",
    layout="centered",
    initial_sidebar_state="collapsed"
)




# ---------------- SESSION INIT ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None

#st.write("PAGE:", st.session_state.page)
#st.write("USER:", st.session_state.user)



# ---------------- AUTH ROUTER ----------------
if st.session_state.page in ["login", "register"]:
    auth.show_auth()
    st.stop()




# ---------------- PAGE CONFIG ----------------


st.set_page_config(
    page_title="AI Interview Mate",
    layout="centered",
    initial_sidebar_state="collapsed"
)



# ---------------- CSS ----------------
st.markdown("""
<style>
            


st.markdown(
    "<h1 style='text-align: center;'>Interview Mate</h1>",
    unsafe_allow_html=True
)
            


/* FULL WHITE PAGE FORCE */
.stApp {
    background-color: #ffffff !important;
}

/* Remove dark theme */
html, body {
    background-color: #ffffff !important;
}

/* Center auth card */
.auth-card {
    max-width: 420px;
    margin: auto;
    margin-top: 90px;
    padding: 40px;
    border-radius: 18px;
    background: white;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.15);
}

/* Titles */
.auth-title {
    font-size: 28px;
    font-weight: 700;
    text-align: center;
    color: black;
}

.auth-sub {
    text-align: center;
    color: #666;
    margin-bottom: 25px;
}

/* Inputs */
input {
    background: #f3f3f3 !important;
    color: black !important;
}

/* Buttons */
button {
    background: black !important;
    color: white !important;
    border-radius: 10px !important;
    height: 42px !important;
}

/* Labels */
label {
    color: black !important;
}



            




/* App background */
.stApp {
background:#F8FAFC;
}

/* Main title */
.main-title {
font-size:38px;
font-weight:700;
text-align:center;
color:#111b33;
margin-bottom:25px;
}

/* Sidebar name */
.sidebar-name {
font-size:18px;
font-weight:600;
text-align:left;
color:#f0f8ff;
margin-bottom:15px;
}

/* Dashboard cards */
.dashboard-card {
background:#FFFFFF;
padding:20px;
border-radius:18px;
box-shadow:0 10px 25px rgba(0,0,0,.08);
height:100px;
transition:0.3s;
border:1px solid #E5E7EB;
border-left:6px solid #2563EB;
color:#334155;
}
 
.dashboard-card{
width:200px;
} 
                        
.dashboard-card:hover {
transform:translateY(-6px);
}

.dashboard-card h3 {
margin-bottom:8px;
color:#0F172A;
}

/* Content cards */
.card {
background:#FFFFFF;
padding:20px;
border-radius:18px;
box-shadow:0 8px 20px rgba(0,0,0,.08);
margin-bottom:18px;
border:1px solid #E5E7EB;
color:#334155;
}

/* Section title */
.section-title {
font-size:20px;
font-weight:600;
margin-top:20px;
margin-bottom:12px;
color:#0F172A;
}

/* Header box */
.header-box {
background:#2563EB;
padding:35px;
border-radius:20px;
color:white;
margin-bottom:30px;
}

/* Fix input + selectbox text color */
input, textarea {
    color: black !important;
}

div[data-baseweb="select"] span {
    color: black !important;
}

/* Dropdown options */
div[role="listbox"] * {
    color: black !important;
}

/* Placeholder labels */
label {
    color: #0F172A !important;
}


</style>
""", unsafe_allow_html=True)

# DATABASE SETUP
# --------------------------------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# UTILS
# --------------------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "mock_question" not in st.session_state:
    st.session_state.mock_question = ""

if "mock_domain" not in st.session_state:
    st.session_state.mock_domain = ""

if "mock_step" not in st.session_state:
    st.session_state.mock_step = 0

if "mock_result" not in st.session_state:
    st.session_state.mock_result = ""

if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""


if "saved" not in st.session_state:
    st.session_state.saved = []

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "questions" not in st.session_state:
    st.session_state.questions = ""

if "company_questions" not in st.session_state:
    st.session_state.company_questions = ""





# ---------------- OLLAMA CONFIG ----------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

def generate_roadmap(goal, duration, level):
    prompt = f"""
You are an expert career mentor and technical interviewer.

Create a COMPLETE learning + interview preparation roadmap.

Use ONLY this format:

Core Topics to Study:
- List main subjects for {goal}

Technical Skills:
- Programming languages
- Frameworks/tools
- Projects to build

Interview Preparation:
DSA:
- What data structures and algorithms to practice

Coding:
- What type of problems to solve
- Platforms (LeetCode, HackerRank etc)

Aptitude:
- Quantitative
- Logical reasoning
- Verbal

Technical Interview:
- Core concepts
- System design (if applicable)

HR Interview:
- Resume tips
- Common HR questions
- Communication skills

Step by Step Learning Path:
1. Clear steps from beginner to job-ready

Weekly Plan:
Week 1:
Week 2:
Week 3:
(continue based on duration)

Tools & Resources:
- Courses
- Platforms
- GitHub
- Practice sites

Mini Projects:
- Small real-world projects

Final Outcome:
- Skills gained
- Job readiness

Career Goal: {goal}
Duration: {duration}
Level: {level}

Do not add extra explanation.
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=300)
        return r.json().get("response", "No AI response")
    except:
        return "❌ Ollama is not running. Please start Ollama."
    
def generate_mock_question(domain, level):

    prompt = f"""
Act as technical interviewer.

Domain: {domain}
Level: {level}

Ask ONE interview question only.
No explanation.
"""

    try:
        r = ollama.chat(
            model=MODEL,
            messages=[{"role":"user","content":prompt}]
        )
        return r["message"]["content"]
    except:
        return "Ollama error"
    
def evaluate_answer(question, user_answer):

    prompt = f"""
You are a technical interviewer.

Question:
{question}

User Answer:
{user_answer}

Now provide:

1. Correct Answer (short)
2. Feedback on user's answer
3. Score out of 10

Keep simple.
"""

    try:
        r = ollama.chat(
            model=MODEL,
            messages=[{"role":"user","content":prompt}]
        )
        return r["message"]["content"]
    except:
        return "Evaluation error"


    


def generate_company_questions(company, role):

    prompt = f"""
Generate interview questions for {company} company.

Role: {role}

Rules:
- Technical + HR + Coding
- 10 to 12 questions
- Real interview style
- Only questions

"""

    try:
        r = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return r["message"]["content"]
    except:
        return "Ollama connection failed."

    
    # ---------------- RESUME FUNCTIONS ----------------

def extract_resume_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text[:4000]

def generate_resume_summary(resume_text):
    prompt = f"""
Generate a SHORT professional resume summary.

Rules:
- 3 to 5 bullet points
- Mention role, skills, projects
- No contact details
- Concise & interview-ready

Resume:
{resume_text}
"""

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.3}
    )

    return response["message"]["content"]

def generate_interview_questions(resume_text):
    prompt = f"""
Based on the resume below, generate interview questions.

Rules:
- ONLY questions
- No answers
- Technical + project-based
- Include DSA + coding + projects
- 8 to 10 questions

Resume:
{resume_text}
"""

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.4}
    )

    return response["message"]["content"]



# ---------------- SIDEBAR ----------------
if st.session_state.page != "login":
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=80)
        st.markdown(f"<div class='sidebar-name'>{st.session_state.user[1]}</div>", unsafe_allow_html=True)

        if st.button(" Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button(" Generate Roadmap"):
            st.session_state.page = "roadmap"
            st.rerun()

        if st.button("Resume"):
            st.session_state.page = "resume"
            st.rerun()

        if st.button(" Question Bank"):
           st.session_state.page = "question_bank"


        if st.button("Mock Interview"):
           st.session_state.page = "mock"
           st.rerun()

        if st.button(" Saved"):
           st.session_state.page = "saved"
           st.rerun()

        if st.button(" Logout"):
           st.session_state.user = None
           st.session_state.page = "login"
           st.rerun()




# ---------------- DASHBOARD ----------------
if st.session_state.page == "dashboard":

    st.markdown("""
    <div class='header-box'>
    <h1>AI Interview Platform</h1>
    <p>Your personal interview & roadmap assistant</p>
    </div>
    """,unsafe_allow_html=True)

    c1,c2,c3,c4,c5=st.columns(5)

    with c1:
        st.markdown("<div class='dashboard-card'><h3>Roadmap</h3></div>",unsafe_allow_html=True)

        #if st.button("Open Roadmap"):
            #st.session_state.page="roadmap"
           # st.rerun()

    with c2:
        st.markdown("<div class='dashboard-card'><h3>Resume</h3></div>",unsafe_allow_html=True)

        #if st.button("Open Resume"):
           # st.session_state.page="resume"
           # st.rerun()

    with c3:
        st.markdown("<div class='dashboard-card'><h3>Question Bank</h3></div>",unsafe_allow_html=True)

        #if st.button("Open Question Bank"):
           # st.session_state.page="question_bank"
           # st.rerun()

    with c4:
        st.markdown("<div class='dashboard-card'><h3>Mock Interview</h3></div>",unsafe_allow_html=True)

        #if st.button(" Mock Interview", key="goto_mock"):
          # st.session_state.page = "mock"
          # st.rerun()


    with c5:
        st.markdown("<div class='dashboard-card'><h3>Saved</h3></div>",unsafe_allow_html=True)


        #if st.button("Open Saved"):
           # st.session_state.page="saved"
           # st.rerun()
    
    
    
# ---------------- ROADMAP PAGE ----------------
elif st.session_state.page == "roadmap":

    st.markdown("<div class='main-title'>Create Your Roadmap</div>", unsafe_allow_html=True)

    goal = st.text_input("Career Goal")
    duration = st.selectbox("Duration", ["3 Months", "6 Months", "1 Year"])
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Roadmap"):
        if goal.strip() == "":
            st.warning("Enter career goal")
        else:
            with st.spinner("AI is generating roadmap..."):
                st.session_state.roadmap_output = generate_roadmap(goal, duration, level)
                st.session_state.page = "result"
                st.rerun()

# ---------------- RESULT PAGE ----------------
elif st.session_state.page == "result":

    st.markdown("<div class='main-title'>Your AI Roadmap</div>", unsafe_allow_html=True)

    if st.session_state.roadmap_output not in st.session_state.saved:
       st.session_state.saved.append(st.session_state.roadmap_output)


    blocks = st.session_state.roadmap_output.split("\n\n")

    for block in blocks:
        block = block.strip()
        if block.endswith(":"):
            st.markdown(f"<div class='section-title'>{block}</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                f"<div class='card'>{block.replace(chr(10), '<br>')}</div>",
                unsafe_allow_html=True
            )

   #progress = st.slider("Your Learning Progress %", 0, 100)
    #st.progress(progress)

    st.markdown("<br>", unsafe_allow_html=True)

# -------- Top Row Buttons --------
    col1, col2, col3 = st.columns(3)

    with col1:
      if st.button("Download Roadmap", use_container_width=True):
        pass

    with col2:
       if st.button("Save Roadmap", use_container_width=True):
        pass

    with col3:
       if st.button("Generate New", use_container_width=True):
        pass

# Space
    st.markdown("<br><br>", unsafe_allow_html=True)

# -------- Center Dashboard Button --------
    left, center, right = st.columns([2,1,2])

    with center:
      if st.button("Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()

    # ---------------- Mock Page ----------------
elif st.session_state.page == "mock":

    st.markdown("<div class='main-title'>Mock Interview</div>", unsafe_allow_html=True)

    domain = st.selectbox(
        "Choose Domain",
        ["Python","Java","Web Development","Data Science","AI/ML"]
    )

    level = st.selectbox(
        "Difficulty Level",
        ["Beginner","Intermediate","Advanced"]
    )

    # --- Buttons in one row ---
    col1, col2, col3 = st.columns(3)

    with col1:
      start = st.button("Start Interview", use_container_width=True)

    with col2:
      submit = st.button("Submit Answer", use_container_width=True)

    with col3:
      next_q = st.button("Next Question", use_container_width=True)

    st.write("")  # space

# --- End interview centered ---
    colA, colB, colC = st.columns([1,2,1])

    with colB:
      end = st.button("End Interview", use_container_width=True)



# ---------------- SAVED ROADMAPS PAGE ----------------
elif st.session_state.page == "saved":

    st.markdown("<div class='main-title'>Saved Roadmaps</div>", unsafe_allow_html=True)

    if len(st.session_state.saved) == 0:
        st.info("No saved roadmaps yet.")
    else:
        for i, roadmap in enumerate(st.session_state.saved, 1):
            st.markdown(
                f"<div class='card'><b>Roadmap {i}</b><br>{roadmap.replace(chr(10), '<br>')}</div>",
                unsafe_allow_html=True
            )

    if st.button(" Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


# ---------------- RESUME PAGE ----------------
elif st.session_state.page == "resume":

    st.markdown("<div class='main-title'>AI Resume Interview</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_file:
        resume_text = extract_resume_text(uploaded_file)
        st.success("Resume uploaded successfully!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(" Generate Summary"):
                with st.spinner("Generating summary..."):
                    st.session_state.summary = generate_resume_summary(resume_text)

        with col2:
            if st.button(" Interview Questions"):
                with st.spinner("Generating questions..."):
                    st.session_state.questions = generate_interview_questions(resume_text)

        if st.session_state.summary:
            st.markdown("<div class='section-title'>Resume Summary</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'>{st.session_state.summary.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

        if st.session_state.questions:
            st.markdown("<div class='section-title'>Interview Questions</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'>{st.session_state.questions.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

    if st.button(" Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

#----------------Question Bank-----------------------------#

elif st.session_state.page == "question_bank":

    st.markdown("<div class='main-title'>Question Bank</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs([" Company Based", " General Interview"])

    # -------- COMPANY BASED QUESTIONS --------
    with tab1:
        st.markdown("<div class='section-title'>Company Based Interview Questions</div>", unsafe_allow_html=True)

        company = st.text_input("Company Name (e.g. Google, Amazon)")
        role = st.text_input("Role (e.g. Software Engineer, Frontend Developer)")

        if st.button("Generate Company Questions"):
            if company.strip() == "" or role.strip() == "":
                st.warning("Please enter both company and role.")
            else:
                with st.spinner("Generating real interview questions..."):
                    st.session_state.company_questions = generate_company_questions(company, role)

        if st.session_state.company_questions:
            st.markdown(
                f"<div class='card'>{st.session_state.company_questions.replace(chr(10), '<br>')}</div>",
                unsafe_allow_html=True
            )

    # -------- GENERAL QUESTIONS (OPTIONAL) --------
    with tab2:
        st.info("General interview questions coming soon 🚀")

    if st.button(" Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()


