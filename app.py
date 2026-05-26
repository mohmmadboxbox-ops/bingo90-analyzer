import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="العبقري 2", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=1200, scrolling=True)
except FileNotFoundError:
    st.error("🚨 ملف 'index.html' غير موجود!")