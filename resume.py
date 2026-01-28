import streamlit as st
from pypdf import PdfReader
import ollama

st.set_page_config(page_title="AI Resume Interview", layout="centered")

st.title("📄 AI Resume Analyzer")

# -----------------------------
# Extract Resume Text
# -----------------------------
def extract_resume_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text[:4000]   # limit for speed

# -----------------------------
# Generate Resume Summary
# -----------------------------
def generate_summary(resume_text):
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

# -----------------------------
# Generate Interview Questions
# -----------------------------
def generate_questions(resume_text):
    prompt = f"""
    Based on the resume below, generate interview questions.

    Rules:
    - ONLY questions
    - No answers
    - Technical + project-based
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

# -----------------------------
# Upload Resume
# -----------------------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    resume_text = extract_resume_text(uploaded_file)
    st.success("Resume uploaded successfully!")

    # Session State
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "questions" not in st.session_state:
        st.session_state.questions = ""

    # -----------------------------
    # Buttons
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📝 Generate Resume Summary"):
            with st.spinner("Generating summary..."):
                st.session_state.summary = generate_summary(resume_text)

    with col2:
        if st.button("🎯 Generate Interview Questions"):
            with st.spinner("Generating questions..."):
                st.session_state.questions = generate_questions(resume_text)

    # -----------------------------
    # Output
    # -----------------------------
    if st.session_state.summary:
        st.subheader("📌 Resume Summary")
        st.write(st.session_state.summary)

    if st.session_state.questions:
        st.subheader("🎤 Interview Questions")
        st.write(st.session_state.questions)