import streamlit as st

st.set_page_config(page_title="Progress Tracker", layout="centered")

st.markdown("""
<style>
.card {
background:#E0F2FE;
padding:20px;
border-radius:16px;
box-shadow:0px 4px 10px rgba(0,0,0,0.12);
text-align:center;
}
.title {
font-size:30px;
font-weight:bold;
color:#1E40AF;
margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# Session
if "progress" not in st.session_state:
    st.session_state.progress = 0

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='title'>📊 Learning Progress</div>", unsafe_allow_html=True)

st.session_state.progress = st.slider(
    "Update your progress",
    0, 100,
    st.session_state.progress
)

st.progress(st.session_state.progress)

st.success(f"Current Progress: {st.session_state.progress}%")

if st.button("Reset"):
    st.session_state.progress = 0
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
