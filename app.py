import streamlit as st
import base64
import requests
import re

# إصدار السرعة القصوى والمضمون للقراءة والتوليد
st.set_page_config(page_title="Bingo 90 Zone Granville", page_icon="🔮", layout="centered")

st.title("🔮 خوارزمية ضربة المعلم - إصدار السرعة القصوى المصحح")
st.write("النظام العشري (9 صناديق) | تمرير أعلى 4 صناديق مكررة | اعتماد الثانية النقية وحظر الأولى.")

raw_key = st.secrets.get("GOOGLE_API_KEY", "")
GOOGLE_API_KEY = "".join(re.findall(r'[a-zA-Z0-9_\-]+', raw_key))

# دالة الماسح الضوئي المضمونة والمصححة لقراءة ردود جوجل بالكامل
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is not None and GOOGLE_API_KEY:
        try:
            bytes_data = uploaded_file.getvalue()
            encoded_image = base64.b64encode(bytes_data).decode('utf-8')
            
            url = f"https://googleapis.com{GOOGLE_API_KEY}"
            
            payload = {
                "requests": [{
                    "image": {"content": encoded_image},
                    "features": [{"type": "TEXT_DETECTION"}]
                }]
            }
            
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                # تصحيح طريقة القراءة لجلب النص الكلي من مصفوفة جوجل بدقة وموثوقية
                if 'responses' in result and result['responses']:
                    res = result['responses'][0]
                    if 'textAnnotations' in res and res['textAnnotations']:
                        extracted_text = res['textAnnotations'][0]['description']
                        all_numbers = re.findall(r'\b\d+\b', extracted_text)
                        valid_numbers = [int(num) for num in all_numbers if 1 <= int(num) <= 90]
                        return sorted(list(set(valid_numbers)))
            return []
        except Exception:
            return []
    return []

# 3. واجهة المستخدم السريعة والمباشرة
st.header("📸 خطوة 1: مسح السحبات الخاطف")

img_file_1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg", "jpeg"], key="draw1")
raw_nums_1 = extract_numbers_from_uploaded_file(img_file_1) if img_file_1 else []

text_input_1 = st.text_area("أرقام السحبة الأولى الرصد التلقائي:", value=", ".join(map(str, raw_nums_1)), key="text_1")
current_nums_1 = [int(s) for s in re.findall(r'\b\d+\b', text_input_1)] if text_input_1 else []
if text_input_1: st.caption(f"تم رصد: {len(current_nums_1)} رقماً.")

st.markdown("---")

img_file_2 = st.file_uploader("ارفع صورة السحبة الثانية:", type=["png", "jpg", "jpeg"], key="draw2")
raw_nums_2 = extract_numbers_from_uploaded_file(img_file_2) if img_file_2 else []

text_input_2 = st.text_area("أرقام السحبة الثانية الرصد التلقائي:", value=", ".join(map(str, raw_nums_2)), key="text_2")
current_nums_2 = [int(s) for s in re.findall(r'\b\d+\b', text_input_2)] if text_input_2 else []
if text_input_2: st.caption(f"تم رصد: {len(current_nums_2)} رقماً.")

st.markdown("---")

if st.button("🚀 تشغيل الخوارزمية وتوليد البطاقات الستة"):
    final_draw_1 = current_nums_1
    final_draw_2 = current_nums_2
    
    if len(final_draw_1) > 0 and len(final_draw_2) > 0:
        shared_numbers = set(final_draw_1).intersection(set(final_draw_2))
        all_possible = set(range(1, 91))
        hidden_numbers = all_possible.difference(set(final_draw_1).union(set(final_draw_2)))
        
        purified_draw_2 = set(final_draw_2).difference(shared_numbers)
        
        boxes = {
            1: [n for n in shared_numbers if 1 <= n <= 10],
            2: [n for n in shared_numbers if 11 <= n <= 20],
            3: [n for n in shared_numbers if 21 <= n <= 30],
            4: [n for n in shared_numbers if 31 <= n <= 40],
            5: [n for n in shared_numbers if 41 <= n <= 50],
            6: [n for n in shared_numbers if 51 <= n <= 60],
            7: [n for n in shared_numbers if 61 <= n <= 70],
            8: [n for n in shared_numbers if 71 <= n <= 80],
            9: [n for n in shared_numbers if 81 <= n <= 90]
        }
        
        sorted_boxes_by_len = sorted(boxes.keys(), key=lambda k: len(boxes[k]), reverse=True)
        top_4_boxes_to_keep = sorted_boxes_by_len[:4]
        
        allowed_shared_numbers = set()
        for b_id in top_4_boxes_to_keep:
            allowed_shared_numbers.update(boxes[b_id])
            
        target = sorted(list(hidden_numbers.union(purified_draw_2).union(allowed_shared_numbers)))
        
        zones = [[n for n in target if 1<=n<=30], [n for n in target if 31<=n<=60], [n for n in target if 61<=n<=90]]
        master_pool = []
        for z in zones:
            z_sorted = sorted(z)
            if len(z_sorted) > 10:
                step = len(z_sorted) / 10.0
                pool = [z_sorted[int(i * step)] for i in range(10)]
            else: z_sorted
            master_pool.extend(pool)
            
        working_pool = sorted(list(set(master_pool)))
        cards = [[] for _ in range(6)]
        card_idx = 0
        
        for num in working_pool:
            start_idx = card_idx
            while len(cards[card_idx]) >= 5:
                card_idx = (card_idx + 1) % 6
                if card_idx == start_idx: break
            if len(cards[card_idx]) < 5:
                cards[card_idx].append(num)
                card_idx = (card_idx + 1) % 6
                
        cards = [sorted(c) for c in cards]
        st.success(f"🎯 تم الحساب المكتسح! الوعاء المستهدف: {len(target)} رقماً.")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric(label="📊 غائب", value=f"{len(hidden_numbers)}")
        with col2: st.metric(label="✨ ثانية نقية", value=f"{len(purified_draw_2)}")
        with col3: st.metric(label="🔥 مشترك ناجٍ", value=f"{len(allowed_shared_numbers)}")
            
        st.markdown("---")
        for i, c in enumerate(cards):
            if c:
                st.info(f"🎴 بطاقة رقم {i+1}")
                st.markdown(f"## ` {c} `")
        st.markdown("---")
        st.code(" , ".join(map(str, target)))
    else:
        st.error("⚠️ يرجى رفع الصور أولاً.")