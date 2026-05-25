import streamlit as st
import base64
import requests
import re
import random

# إعدادات الصفحة
st.set_page_config(page_title="Genius 2 Pro", page_icon="🎯", layout="centered")
st.title("🎯 Genius 2: النسخة الاحترافية")

# جلب المفتاح السري (تأكد من إعداده في Streamlit Secrets)
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# 1. دالة القراءة (OCR)
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is None: return []
    try:
        bytes_data = uploaded_file.getvalue()
        encoded_image = base64.b64encode(bytes_data).decode('utf-8')
        url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"
        payload = {"requests": [{"image": {"content": encoded_image}, "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]}]}
        response = requests.post(url, json=payload)
        result = response.json()
        text = result['responses'][0]['fullTextAnnotation']['text']
        nums = sorted(list(set([int(n) for n in re.findall(r'\b\d+\b', text) if 1 <= int(n) <= 90])))
        return nums
    except: return []

# 2. دالة التنبيه اللوني والمدخلات
def display_input_box(label, img_file, key):
    raw_nums = extract_numbers_from_uploaded_file(img_file) if img_file else []
    text_input = st.text_area(f"أرقام {label}:", value=",".join(map(str, raw_nums)), key=f"text_{key}")
    nums = [int(n) for n in re.findall(r'\b\d+\b', text_input)]
    
    count = len(nums)
    if count == 50:
        st.success(f"✅ {label} مكتملة (50 رقماً)")
    elif count > 0:
        st.error(f"⚠️ {label} ناقصة: قرأت {count} رقماً. يرجى إضافة {50 - count} رقم.")
    return nums

# 3. محرك الأكواد الستة الذكي
def generate_cards_with_engines(target_pool):
    cards = [[] for _ in range(6)]
    global_counter = {num: 0 for num in range(1, 91)}
    
    engines_logic = {
        0: lambda pool: [n for n in pool if n > 60],
        1: lambda pool: [n for n in pool if 45 < n <= 60],
        2: lambda pool: [n for n in pool if n < 20],
        3: lambda pool: [n for n in pool if 20 <= n < 40],
        4: lambda pool: [n for n in pool if 40 <= n <= 45],
        5: lambda pool: pool
    }

    for c_idx in range(6):
        available = engines_logic[c_idx](target_pool)
        random.shuffle(available)
        while len(cards[c_idx]) < 5 and available:
            candidate = available.pop(0)
            if global_counter[candidate] < 2:
                cards[c_idx].append(candidate)
                global_counter[candidate] += 1
    return cards

# --- الواجهة الرئيسية ---
img1 = st.file_uploader("ارفع السحبة الأولى:", type=["png", "jpg"], key="d1")
d1_list = display_input_box("السحبة الأولى", img1, "d1")

img2 = st.file_uploader("ارفع السحبة الثانية:", type=["png", "jpg"], key="d2")
d2_list = display_input_box("السحبة الثانية", img2, "d2")

if st.button("🚀 توليد البطاقات الستة الهجومية"):
    if len(d1_list) == 50 and len(d2_list) == 50:
        target = sorted(list(set(d1_list).union(set(d2_list))))
        final_cards = generate_cards_with_engines(target)
        
        engines_names = ["الغليان", "الامتداد", "الصقيع", "التطويق", "الموجة الصاعدة", "السحاب"]
        for i, c in enumerate(final_cards):
            st.info(f"استراتيجية ({engines_names[i]})")
            st.markdown(f"## ` {sorted(c)} `")
    else:
        st.error("❌ لا يمكن التوليد، البيانات غير مكتملة في السحبات!")