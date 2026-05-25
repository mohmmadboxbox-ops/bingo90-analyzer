import streamlit as st
import base64
import requests
import re
import random

# إعدادات المظهر
st.set_page_config(page_title="Genius 2 Pro", page_icon="🎯", layout="centered")
st.title("🎯 خوارزمية Genius 2 - النسخة الذكية")

# جلب المفتاح السري
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# [دالة المسح تبقى كما هي في كودك الأصلي...]
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            encoded_image = base64.b64encode(bytes_data).decode('utf-8')
            url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"
            payload = {"requests": [{"image": {"content": encoded_image}, "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]}]}
            response = requests.post(url, json=payload)
            result = response.json()
            extracted_text = result['responses'][0]['fullTextAnnotation']['text']
            all_numbers = re.findall(r'\b\d+\b', extracted_text)
            return sorted(list(set([int(num) for num in all_numbers if 1 <= int(num) <= 90])))
        except: return []
    return []

# --- قلب الخوارزمية الجديد (الأكواد الستة) ---
def generate_cards_with_engines(target_pool):
    cards = [[] for _ in range(6)]
    global_counter = {num: 0 for num in range(1, 91)}
    
    # تعريف استراتيجيات الأكواد
    engines_logic = {
        0: lambda pool: [n for n in pool if n > 60], # الغليان
        1: lambda pool: [n for n in pool if 45 < n <= 60], # الامتداد
        2: lambda pool: [n for n in pool if n < 20], # الصقيع
        3: lambda pool: [n for n in pool if 20 <= n < 40], # التطويق
        4: lambda pool: [n for n in pool if 40 <= n <= 45], # الموجة
        5: lambda pool: pool # السحاب (عشوائي موجه)
    }

    for c_idx in range(6):
        available = engines_logic[c_idx](target_pool)
        random.shuffle(available)
        
        while len(cards[c_idx]) < 5 and available:
            candidate = available.pop(0)
            # الحارس: لا يتكرر أكثر من مرتين في كل البطاقات
            if global_counter[candidate] < 2:
                cards[c_idx].append(candidate)
                global_counter[candidate] += 1
    return cards

# واجهة المستخدم
img_file_1 = st.file_uploader("السحبة الأولى:", type=["png", "jpg"], key="d1")
text_input_1 = st.text_area("أرقام السحبة الأولى:", value=",".join(map(str, extract_numbers_from_uploaded_file(img_file_1))))

img_file_2 = st.file_uploader("السحبة الثانية:", type=["png", "jpg"], key="d2")
text_input_2 = st.text_area("أرقام السحبة الثانية:", value=",".join(map(str, extract_numbers_from_uploaded_file(img_file_2))))

if st.button("🚀 توليد البطاقات الستة الهجومية"):
    d1 = [int(n) for n in re.findall(r'\b\d+\b', text_input_1)]
    d2 = [int(n) for n in re.findall(r'\b\d+\b', text_input_2)]
    
    if d1 and d2:
        target = sorted(list(set(d1).union(set(d2))))
        final_cards = generate_cards_with_engines(target)
        
        engines_names = ["الغليان", "الامتداد", "الصقيع", "التطويق", "الموجة الصاعدة", "السحاب"]
        for i, c in enumerate(final_cards):
            st.info(f"استراتيجية ({engines_names[i]})")
            st.markdown(f"## ` {sorted(c)} `")
    else:
        st.warning("يرجى إدخال أرقام السحبات.")