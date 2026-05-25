import streamlit as st
import base64
import requests
import re
import random

# إعدادات الصفحة
st.set_page_config(page_title="Genius 2 - Core Engine", layout="centered")
st.title("🎯 Genius 2: قارئ السحبات والتحليل الذكي")

# 1. دالة قراءة OCR الأصلية (اللي كنت تعتمد عليها)
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is None: return []
    try:
        bytes_data = uploaded_file.getvalue()
        encoded_image = base64.b64encode(bytes_data).decode('utf-8')
        url = f"https://vision.googleapis.com/v1/images:annotate?key={st.secrets['GOOGLE_API_KEY']}"
        payload = {"requests": [{"image": {"content": encoded_image}, "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]}]}
        response = requests.post(url, json=payload)
        result = response.json()
        text = result['responses'][0]['fullTextAnnotation']['text']
        # استخراج الأرقام بدقة
        nums = sorted(list(set([int(n) for n in re.findall(r'\b\d+\b', text) if 1 <= int(n) <= 90])))
        return nums
    except:
        return []

# 2. نظام التنبيه والمدخلات
st.header("📸 معالجة السحبات")
img1 = st.file_uploader("ارفع السحبة الأولى:", type=["jpg", "png"])
d1 = extract_numbers_from_uploaded_file(img1)
text1 = st.text_area("أرقام السحبة الأولى:", value=",".join(map(str, d1)))
d1_list = [int(n) for n in re.findall(r'\b\d+\b', text1)]

if img1 and len(d1_list) != 50:
    st.warning(f"⚠️ تنبيه: تم قراءة {len(d1_list)} رقماً. يرجى التأكد من أن المجموع 50!")

img2 = st.file_uploader("ارفع السحبة الثانية:", type=["png", "jpg"])
d2 = extract_numbers_from_uploaded_file(img2)
text2 = st.text_area("أرقام السحبة الثانية:", value=",".join(map(str, d2)))
d2_list = [int(n) for n in re.findall(r'\b\d+\b', text2)]

if img2 and len(d2_list) != 50:
    st.warning(f"⚠️ تنبيه: تم قراءة {len(d2_list)} رقماً. يرجى التأكد من أن المجموع 50!")

# 3. المعالجة الذكية (محرك الأكواد الستة)
if st.button("🚀 توليد البطاقات الستة"):
    if len(d1_list) == 50 and len(d2_list) == 50:
        target = sorted(list(set(d1_list).union(set(d2_list))))
        
        # توزيع الأكواد الستة (النسخة النهائية)
        cards = [[] for _ in range(6)]
        global_count = {n: 0 for n in range(1, 91)}
        
        # منطق التوزيع الموجه
        logic = [lambda p: [n for n in p if n > 60], lambda p: [n for n in p if 45 < n <= 60],
                 lambda p: [n for n in p if n < 20], lambda p: [n for n in p if 20 <= n < 40],
                 lambda p: [n for n in p if 40 <= n <= 45], lambda p: p]
        
        for i in range(6):
            pool = logic[i](target)
            random.shuffle(pool)
            while len(cards[i]) < 5 and pool:
                n = pool.pop(0)
                if global_count[n] < 2:
                    cards[i].append(n)
                    global_count[n] += 1
        
        for i, c in enumerate(cards):
            st.info(f"البطاقة {i+1}: {sorted(c)}")
    else:
        st.error("❌ لا يمكن التوليد، البيانات غير مكتملة!")