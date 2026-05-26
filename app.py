import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="العبقري 2", layout="centered", initial_sidebar_state="collapsed")

# إخفاء قوائم ستريملت
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# قراءة الواجهة من داخل مجلد templates
try:
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # عرض الواجهة
    components.html(html_code, height=1300, scrolling=True)

except FileNotFoundError:
    st.error("🚨 ملف الواجهة غير موجود! تأكد أن الملف اسمه index.html وموجود داخل مجلد templates.")