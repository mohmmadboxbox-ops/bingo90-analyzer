import streamlit as st
import base64
import requests
import re

# 1. إعدادات المظهر
st.set_page_config(page_title="Genius 2 Hybrid", page_icon="🎯", layout="centered")

st.title("🎯 خوارزمية Genius 2 الهجينة")
st.write("تدمج بين التوزيع الدائري المستقر (توازن) ونظام التكتل (قنص) مع فحص ذكي لعدد الأرقام المقروءة.")

# جلب المفتاح السري
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# 2. دالة الماسح الضوئي
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

# 3. واجهة المستخدم والتنبيهات الذكية للـ 50 رقم
st.header("📸 خطوة 1: مسح السحبات")

img_file_1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg", "jpeg"], key="draw1")
raw_nums_1 = extract_numbers_from_uploaded_file(img_file_1) if img_file_1 else []

# فحص السحبة الأولى
if img_file_1:
    text_input_1 = st.text_area("أرقام السحبة الأولى (راجعها):", value=", ".join(map(str, raw_nums_1)))
    current_nums_1 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_1)]
    if len(current_nums_1) == 50:
        st.success(f"✅ قراءة مكتملة: تم رصد {len(current_nums_1)} رقماً.")
    else:
        st.warning(f"⚠️ انتبه: تم رصد {len(current_nums_1)} رقماً فقط! المطلوب 50. يرجى إضافة الرقم الناقص يدوياً في المربع أعلاه.")
else:
    text_input_1 = ""

st.markdown("---")

img_file_2 = st.file_uploader("ارفع صورة السحبة الثانية:", type=["png", "jpg", "jpeg"], key="draw2")
raw_nums_2 = extract_numbers_from_uploaded_file(img_file_2) if img_file_2 else []

# فحص السحبة الثانية
if img_file_2:
    text_input_2 = st.text_area("أرقام السحبة الثانية (راجعها):", value=", ".join(map(str, raw_nums_2)))
    current_nums_2 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_2)]
    if len(current_nums_2) == 50:
        st.success(f"✅ قراءة مكتملة: تم رصد {len(current_nums_2)} رقماً.")
    else:
        st.warning(f"⚠️ انتبه: تم رصد {len(current_nums_2)} رقماً فقط! المطلوب 50. يرجى إضافة الرقم الناقص يدوياً في المربع أعلاه.")
else:
    text_input_2 = ""

st.markdown("---")

# 4. المعالجة الهجينة
if st.button("🚀 توليد البطاقات الهجينة"):
    d1 = [int(n) for n in re.findall(r'\b\d+\b', text_input_1)]
    d2 = [int(n) for n in re.findall(r'\b\d+\b', text_input_2)]
    
    if len(d1) > 0 and len(d2) > 0:
        # حساب المجموعة المستهدفة
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
        
        # تجهيز البطاقات الستة
        cards = [[] for _ in range(6)]
        
        # 1. نظام التوازن (بطاقات 1-3)
        balanced_pool = target.copy()
        for i, num in enumerate(balanced_pool):
            if i < 30: # توزيع أول 30 رقم بالتساوي
                cards[i % 3].append(num)
                
        # 2. نظام القنص (بطاقات 4-6)
        sniper_pool = [n for n in target if n not in [n for c in cards[:3] for n in c]]
        sniper_pool.sort()
        for i, num in enumerate(sniper_pool):
            idx = 3 + (i // 5)
            if idx < 6:
                cards[idx].append(num)
                
        # ترتيب وعرض البطاقات
        for i, c in enumerate(cards):
            final_c = sorted(c)[:5]
            st.info(f"{'⚖️ فريق التوازن' if i < 3 else '🎯 فريق القنص'} - بطاقة رقم {i+1}")
            st.markdown(f"## ` {final_c} `")
            
        st.markdown("---")
        st.write("🎯 **المجموعة المستهدفة الكلية:**")
        st.code(" , ".join(map(str, target)))
    else:
        st.warning("⚠️ أدخل الأرقام أولاً.")