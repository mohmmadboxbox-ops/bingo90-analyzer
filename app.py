import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتأخذ الشاشة بالكامل وبدون قوائم جانبية مزعجة
st.set_page_config(page_title="العبقري 2", layout="centered", initial_sidebar_state="collapsed")

# إخفاء العلامة المائية الخاصة بـ Streamlit لتبدو الواجهة احترافية
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# قراءة ملف الواجهة (الكرات والخوارزميات) وعرضه
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # عرض الكود داخل ستريملت مع إعطاء ارتفاع مناسب جداً للموبايل
    components.html(html_code, height=1100, scrolling=True)

except FileNotFoundError:
    st.error("🚨 ملف 'index.html' غير موجود! يرجى التأكد من رفعه في نفس المكان مع app.py")