import streamlit as st
import base64
import requests
import re
import random

st.set_page_config(page_title="Genius 2 Hybrid", page_icon="🎯", layout="centered")
st.title("🎯 خوارزمية Genius 2 الهجينة")

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

def extract_numbers(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        encoded_image = base64.b64encode(bytes_data).decode('utf-8')
        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"
        payload = {"requests": [{"image": {"content": encoded_image}, "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]}]}
        res = requests.post(url, json=payload).json()
        text = res['responses'][0]['fullTextAnnotation']['text']
        nums = [int(n) for n in re.findall(r'\b\d+\b', text) if 1 <= int(n) <= 90]
        return sorted(list(set(nums)))
    return []

# الواجهة
img1 = st.file_uploader("السحبة الأولى:", type=["png", "jpg"], key="d1")
nums1 = extract_numbers(img1) if img1 else []
txt1 = st.text_area("أرقام 1:", value=", ".join(map(str, nums1)))

img2 = st.file_uploader("السحبة الثانية:", type=["png", "jpg"], key="d2")
nums2 = extract_numbers(img2) if img2 else []
txt2 = st.text_area("أرقام 2:", value=", ".join(map(str, nums2)))

if st.button("🚀 توليد البطاقات الهجينة"):
    d1 = [int(n) for n in re.findall(r'\b\d+\b', txt1)]
    d2 = [int(n) for n in re.findall(r'\b\d+\b', txt2)]
    
    # تحضير وعاء الأرقام
    master_pool = sorted(list(set(d1).union(set(d2))))
    
    # 1. نظام التوازن (بطاقات 1-3)
    cards = [[] for _ in range(6)]
    balanced_pool = master_pool.copy()
    for i, num in enumerate(balanced_pool):
        if i < 30: # توزيع أول 30 رقم بالتساوي
            cards[i % 3].append(num)
            
    # 2. نظام القنص (بطاقات 4-6 - تجميع متكتل)
    sniper_pool = [n for n in master_pool if n not in [n for c in cards[:3] for n in c]]
    # ترتيب الأرقام للبحث عن المتتالية
    sniper_pool.sort()
    for i, num in enumerate(sniper_pool):
        # يضع كل 5 أرقام متتالية في بطاقة قنص
        idx = 3 + (i // 5)
        if idx < 6:
            cards[idx].append(num)
            
    # تنظيف وتجهيز العرض
    for i, c in enumerate(cards):
        final_c = sorted(c)[:5] # نأخذ أول 5 إذا زاد العدد
        st.info(f"{'⚖️ توازن' if i < 3 else '🎯 قنص'} - بطاقة {i+1}")
        st.markdown(f"## ` {final_c} `")