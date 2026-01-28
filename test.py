import streamlit as st

st.title("Hello Streamlit")

st.write("If you see this, Streamlit is working.")

x = st.slider("Test Slider", 0, 100)
st.write("Value:", x)
