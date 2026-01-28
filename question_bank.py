import streamlit as st
import ollama

MODEL = "llama3.2:1b"

def question_bank_page():

    st.header("📝 Question Bank")

    company = st.selectbox("Company", ["Google","Amazon","Microsoft","TCS"])
    role = st.text_input("Job Role")

    if st.button("Generate Questions"):
        
        prompt = f"""
Generate 5 simple and clear interview questions for a beginner level {role} position at {company}.

Rules:
- Use very easy English
- Keep each question short
- Avoid technical jargon
- Suitable for students
- Ask practical basic questions
"""

        try:
            r = ollama.chat(
                model=MODEL,
                messages=[{"role":"user","content":prompt}]
            )

            st.success("Questions Generated:")
            st.write(r["message"]["content"])

        except Exception as e:
            st.error(e)

