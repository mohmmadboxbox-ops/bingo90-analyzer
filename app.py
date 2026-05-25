import streamlit as st
import base64
import requests
import re
import random

# إعدادات الصفحة
st.set_page_config(page_title="Genius 2 Pro", layout="centered")

# --- دالة القراءة الأصلية (كما كانت تشتغل عندك سابقاً) ---
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is None: return []
    try:
        bytes_data = uploaded_file.getvalue()
        encoded_image = base64.b64encode(bytes_data).decode('utf-8')
        url = f"https://vision.googleapis.com/v1/images:annotate?key={st.secrets['GOOGLE_API_KEY']}"
        payload = {"requests": [{"image": {"content": encoded_image}, "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]}]}
        response = requests.post(url, json=payload)
        result = response.json()
        
        # القراءة الأصلية التي كنت تعتمد عليها
        text = result['responses'][0]['fullTextAnnotation']['text']
        nums = [int(n) for n in re.findall(r'\b\d+\b', text) if 1 <= int(n) <= 90]
        return sorted(list(set(nums)))
    except: return []

# --- دالة التنبيه (الخاصية التي طلبتها) ---
def display_input_box(label, img_file, key):
    raw_nums = extract_numbers_from_uploaded_file(img_file) if img_file else []
    text_input = st.text_area(f"أرقام {label}:", value=",".join(map(str, raw_nums)), key=f"text_{key}")
    nums = [int(n) for n in re.findall(r'\b\d+\b', text_input)]
    
    count = len(nums)
    if count == 50:
        st.success(f"✅ القراءة مكتملة: تم رصد {count} رقماً.")
    elif count > 0:
        st.warning(f"⚠️ انتبه: تم رصد {count} رقماً فقط! المطلوب 50. يرجى التعديل يدوياً حتى يكتمل العدد.")
    return nums

# --- محرك الأكواد الستة (بدون مساس بالقراءة) ---
def generate_cards_with_engines(target_pool):
    cards = [[] for _ in range(6)]
    global_counter = {num: 0 for num in range(1, 91)}
    engines_logic = [
        lambda p: [n for n in p if n > 60], lambda p: [n for n in p if 45 < n <= 60],
        lambda p: [n for n in p if n < 20], lambda p: [n for n in p if 20 <= n < 40],
        lambda p: [n for n in p if 40 <= n <= 45], lambda p: p
    ]
    for i in range(6):
        pool = engines_logic[i](target_pool)
        random.shuffle(pool)
        while len(cards[i]) < 5 and pool:
            n = pool.pop(0)
            if global_counter[n] < 2:
                cards[i].append(n)
                global_counter[n] += 1
    return cards

# --- الواجهة ---
img1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg"], key="d1")
d1_list = display_input_box("السحبة الأولى", img1, "d1")

img2 = st.file_uploader("ارفع صورة السحبة الثانية:", type=["png", "jpg"], key="d2")
d2_list = display_input_box("السحبة الثانية", img2, "d2")

if st.button("🚀 توليد البطاقات الستة"):
    if len(d1_list) == 50 and len(d2_list) == 50:
        target = sorted(list(set(d1_list).union(set(d2_list))))
        final_cards = generate_cards_with_engines(target)
        for i, c in enumerate(final_cards):
            st.info(f"البطاقة {i+1}: {sorted(c)}")
    else:
        st.error("❌ لا يمكن التوليد، السحبات غير مكتملة!")