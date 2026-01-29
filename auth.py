import streamlit as st
import sqlite3
import hashlib

#st.title("Interview Mate")
st.markdown(
    "<h1 style='text-align: center;'>Interview Mate</h1>",
    unsafe_allow_html=True
)

        

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS progress (
    user_id INTEGER,
    value INTEGER
)
""")
conn.commit()


c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

# ---------------- PASSWORD HASH ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_progress(user_id, value):
    c.execute("DELETE FROM progress WHERE user_id=?", (user_id,))
    c.execute("INSERT INTO progress VALUES (?,?)", (user_id, value))
    conn.commit()

def load_progress(user_id):
    c.execute("SELECT value FROM progress WHERE user_id=?", (user_id,))
    row = c.fetchone()
    return row[0] if row else 0




# ---------------- LOGIN PAGE ----------------

def show_auth():

 if st.session_state.page == "login" and st.session_state.user is None:

    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    #st.markdown("<div class='auth-title'>Welcome back</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-sub'>Sign in to continue</div>", unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login", use_container_width=True)

        if login:
            c.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email, hash_password(password))
            )
            user = c.fetchone()

            if user:
              st.session_state.user = user
              st.session_state.page = "dashboard"
              st.rerun()

            else:
                st.error("Invalid email or password")

    if st.button("Go to Register", use_container_width=True):
        st.session_state.page = "register"

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# REGISTER PAGE
# --------------------------------------------------

    

 elif st.session_state.page == "register":

    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='auth-title'>Create account</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-sub'>Join AI Interview Mate</div>", unsafe_allow_html=True)

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        register = st.form_submit_button("Create Account", use_container_width=True)

        if register:
            if password != confirm:
                st.error("Passwords do not match")
            else:
                try:
                    c.execute(
                        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                        (name, email, hash_password(password))
                    )
                    conn.commit()
                    st.success("Account created successfully 🎉")
                    st.session_state.page = "login"
                    st.rerun()
                except:
                    st.error("Email already exists")

    if st.button("Go to Login", use_container_width=True):
        st.session_state.page = "login"

    st.markdown("</div>", unsafe_allow_html=True)

  