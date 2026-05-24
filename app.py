import streamlit as st
import base64
import requests
import re

# 1. إعدادات المظهر
st.set_page_config(page_title="Bingo 90 Zone Granville", page_icon="🔮", layout="centered")

st.title("🔮 خوارزمية ضربة المعلم - العرض المتتالي الصافي")

# تم وضع مفتاحك السري هنا
GOOGLE_API_KEY = "AIzaSyDO7s1G7zd-hX_I2hvv3Q3dppPSI2C3UXs"

# 2. دالة الماسح الضوئي المحدثة
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.getvalue()
            encoded_image = base64.b64encode(bytes_data).decode('utf-8')
            url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"
            
            payload = {
                "requests": [{
                    "image": {"content": encoded_image},
                    "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
                }]
            }
            
            response = requests.post(url, json=payload)
            result = response.json()
            
            if 'error' in result:
                st.error(f"🚫 خطأ من جوجل: {result['error']['message']}")
                return []
            
            extracted_text = result['responses'][0]['fullTextAnnotation']['text']
            all_numbers = re.findall(r'\b\d+\b', extracted_text)
            valid_numbers = [int(num) for num in all_numbers if 1 <= int(num) <= 90]
            
            return sorted(list(set(valid_numbers)))
            
        except Exception as e:
            st.error(f"⚠️ حدث خطأ تقني: {e}")
            return []
    return []

# 3. واجهة المستخدم
st.header("📸 خطوة 1: مسح السحبات")
img_file_1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg", "jpeg"], key="draw1")
img_file_2 = st.file_uploader("ارفع صورة السحبة الثانية:", type=["png", "jpg", "jpeg"], key="draw2")

raw_nums_1 = extract_numbers_from_uploaded_file(img_file_1) if img_file_1 else []
raw_nums_2 = extract_numbers_from_uploaded_file(img_file_2) if img_file_2 else []

st.markdown("---")
text_input_1 = st.text_area("أرقام السحبة الأولى (راجعها):", value=", ".join(map(str, raw_nums_1)))
text_input_2 = st.text_area("أرقام السحبة الثانية (راجعها):", value=", ".join(map(str, raw_nums_2)))

# 4. المعالجة
if st.button("🚀 توليد البطاقات"):
    final_draw_1 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_1)]
    final_draw_2 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_2)]
    
    if len(final_draw_1) > 0 and len(final_draw_2) > 0:
        shared_numbers = set(final_draw_1).intersection(set(final_draw_2))
        all_possible = set(range(1, 91))
        hidden_numbers = all_possible.difference(set(final_draw_1).union(set(final_draw_2)))
        
        boxes = {1: [n for n in shared_numbers if 1<=n<=15], 2: [n for n in shared_numbers if 16<=n<=30],
                 3: [n for n in shared_numbers if 31<=n<=45], 4: [n for n in shared_numbers if 46<=n<=60],
                 5: [n for n in shared_numbers if 61<=n<=75], 6: [n for n in shared_numbers if 76<=n<=90]}
        
        retained = []
        for b_id in sorted(boxes.keys(), key=lambda k: len(boxes[k]))[3:]:
            retained.extend(boxes[b_id])
            
        target = sorted(list(set(final_draw_1).union(set(retained)).union(hidden_numbers)))
        
        def sort_g(p): return sorted(p, key=lambda x: (x % 2, x > 45, x % 10))
        
        zones = [[n for n in target if 1<=n<=30], [n for n in target if 31<=n<=60], [n for n in target if 61<=n<=90]]
        cards = []
        for z in zones:
            pool = sort_g(z)[:10]
            cards.append(sorted(pool[0::2]))
            cards.append(sorted(pool[1::2]))
            
        for i, c in enumerate(cards):
            st.info(f"🎴 بطاقة رقم {i+1}")
            st.markdown(f"## ` {c} `")
            
        st.code(" , ".join(map(str, target)))
    else:
        st.warning("⚠️ أدخل الأرقام أولاً.")