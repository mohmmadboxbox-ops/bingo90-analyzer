import streamlit as st
import base64
import requests
import re
import random

# 1. إعدادات المظهر
st.set_page_config(page_title="Genius 2 Hybrid", page_icon="🎯", layout="centered")

st.title("🎯 خوارزمية Genius 2 الهجينة")
st.write("تدمج بين التوزيع الدائري المستقر (توازن) ونظام التكتل (قنص) مع فحص ذكي لعدد الأرقام المقروءة.")

# جلب المفتاح السري
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# 2. دالة الماسح الضوئي (لم يتم المساس بها)
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

# 3. واجهة المستخدم والتنبيهات الذكية (لم يتم المساس بها)
st.header("📸 خطوة 1: مسح السحبات")

img_file_1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg", "jpeg"], key="draw1")
raw_nums_1 = extract_numbers_from_uploaded_file(img_file_1) if img_file_1 else []

if img_file_1:
    text_input_1 = st.text_area("أرقام السحبة الأولى (راجعها):", value=", ".join(map(str, raw_nums_1)))
    current_nums_1 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_1)]
    if len(current_nums_1) == 50:
        st.success(f"✅ قراءة مكتملة: تم رصد {len(current_nums_1)} رقماً.")
    else:
        st.warning(f"⚠️ انتبه: تم رصد {len(current_nums_1)} رقماً فقط! المطلوب 50. يرجى إضافة الرقم الناقص يدوياً.")
else:
    text_input_1 = ""

st.markdown("---")

img_file_2 = st.file_uploader("ارفع صورة السحبة الثانية:", type=["png", "jpg", "jpeg"], key="draw2")
raw_nums_2 = extract_numbers_from_uploaded_file(img_file_2) if img_file_2 else []

if img_file_2:
    text_input_2 = st.text_area("أرقام السحبة الثانية (راجعها):", value=", ".join(map(str, raw_nums_2)))
    current_nums_2 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_2)]
    if len(current_nums_2) == 50:
        st.success(f"✅ قراءة مكتملة: تم رصد {len(current_nums_2)} رقماً.")
    else:
        st.warning(f"⚠️ انتبه: تم رصد {len(current_nums_2)} رقماً فقط! المطلوب 50. يرجى إضافة الرقم الناقص يدوياً.")
else:
    text_input_2 = ""

st.markdown("---")

# 4. المعالجة الذكية (تم تغيير استراتيجية البطاقات فقط)
if st.button("🚀 توليد البطاقات الهجينة"):
    d1 = [int(n) for n in re.findall(r'\b\d+\b', text_input_1)]
    d2 = [int(n) for n in re.findall(r'\b\d+\b', text_input_2)]
    
    if len(d1) > 0 and len(d2) > 0:
        # حساب المجموعة المستهدفة (كما هي في كودك الأصلي)
        shared_numbers = set(d1).intersection(set(d2))
        all_possible = set(range(1, 91))
        hidden_numbers = all_possible.difference(set(d1).union(set(d2)))
        
        boxes = {1: [n for n in shared_numbers if 1<=n<=15], 2: [n for n in shared_numbers if 16<=n<=30],
                 3: [n for n in shared_numbers if 31<=n<=45], 4: [n for n in shared_numbers if 46<=n<=60],
                 5: [n for n in shared_numbers if 61<=n<=75], 6: [n for n in shared_numbers if 76<=n<=90]}
        
        retained = []
        for b_id in sorted(boxes.keys(), key=lambda k: len(boxes[k]))[3:]:
            retained.extend(boxes[b_id])
            
        target = sorted(list(set(d1).union(set(retained)).union(hidden_numbers)))
        
        # ==========================================
        # محرك الأكواد الستة الذكية + الحارس البرمجي
        # ==========================================
        cards = [[] for _ in range(6)]
        global_counter = {num: 0 for num in range(1, 91)}
        cards_with_dupes = set() # تتبع البطاقات التي تحتوي على مكررات (الحد الأقصى 4)

        def can_add(num, card_idx):
            # 1. منع تكرار الرقم أكثر من مرتين إجمالاً
            if global_counter[num] >= 2:
                return False
            # 2. إذا كان الرقم سيتكرر للمرة الثانية، نتحقق من شرط الـ 4 بطاقات
            if global_counter[num] == 1:
                other_card_idx = next(i for i, c in enumerate(cards) if num in c)
                potential_dupe_cards = cards_with_dupes.union({card_idx, other_card_idx})
                # إذا كانت إضافة هذا الرقم ستجعل أكثر من 4 بطاقات تحتوي على مكررات، ارفضه
                if len(potential_dupe_cards) > 4:
                    return False
            return True

        def execute_add(num, card_idx):
            if global_counter[num] == 1:
                other_card_idx = next(i for i, c in enumerate(cards) if num in c)
                cards_with_dupes.add(card_idx)
                cards_with_dupes.add(other_card_idx)
            cards[card_idx].append(num)
            global_counter[num] += 1

        # دوال مساعدة لجلب الأرقام بناءً على الكود (مع النسخ الاحتياطي إذا كانت الفئة فارغة)
        def get_pool(condition):
            pool = [n for n in target if condition(n)]
            return pool if pool else target.copy()

        # الأكواد الستة
        engines = [
            ("🔥 الغليان (Boiling)", get_pool(lambda x: x > 60)),
            ("📈 الامتداد (Extension)", get_pool(lambda x: 45 < x <= 60)),
            ("❄️ الصقيع (Frost)", get_pool(lambda x: x < 20)),
            ("🧊 التطويق (Lockdown)", get_pool(lambda x: 20 <= x <= 40)),
            ("🚀 الموجة الصاعدة (Wave)", get_pool(lambda x: 40 < x <= 45)),