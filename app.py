import streamlit as st
import base64
import requests
import re

# 1. إعدادات المظهر
st.set_page_config(page_title="Bingo 90 Zone Granville", page_icon="🔮", layout="centered")

st.title("🔮 خوارزمية ضربة المعلم - العرض المتتالي الصافي")
st.write("تعمل الخوارزمية بنظام الكتلة الواحدة (بدون انحياز) مع دمج خاصية التجاور لبطاقتين كحد أقصى.")

# جلب المفتاح السري بأمان من إعدادات Streamlit
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

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

# 3. واجهة المستخدم والتنبيهات الذكية
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

# 4. المعالجة
if st.button("🚀 توليد البطاقات (النظام الموحد المتساوي)"):
    final_draw_1 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_1)]
    final_draw_2 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_2)]
    
    if len(final_draw_1) > 0 and len(final_draw_2) > 0:
        # حساب المجموعة المستهدفة
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
        
        # تقسيم النطاقات واختيار الأرقام بشكل متساوٍ لدمجها في مسبح رئيسي (Master Pool)
        zones = [[n for n in target if 1<=n<=30], [n for n in target if 31<=n<=60], [n for n in target if 61<=n<=90]]
        master_pool = []
        
        for z in zones:
            z_sorted = sorted(z)
            if len(z_sorted) > 10:
                step = len(z_sorted) / 10.0
                pool = [z_sorted[int(i * step)] for i in range(10)]
            else:
                pool = z_sorted
            master_pool.extend(pool)
            
        # معالجة التجاور على مستوى المجموعة ككل
        pairs = []
        working_pool = []
        skip = False
        master_pool = sorted(master_pool)
        
        for i in range(len(master_pool)):
            if skip:
                skip = False
                continue
            if i < len(master_pool)-1 and master_pool[i+1] == master_pool[i] + 1:
                pairs.append((master_pool[i], master_pool[i+1]))
                skip = True
            else:
                working_pool.append(master_pool[i])
                
        # تجهيز 6 بطاقات فارغة
        cards = [[] for _ in range(6)]
        
        # 1. وضع المتجاورات في بطاقتين كحد أقصى
        cards_with_pairs_count = 0
        for p in pairs:
            if cards_with_pairs_count < 2:
                cards[cards_with_pairs_count].extend(list(p))
                cards_with_pairs_count += 1
            else:
                # إذا زادت المتجاورات عن بطاقتين، تُفكك وتعود لوعاء التوزيع العادي
                working_pool.extend(list(p))
                
        # 2. التوزيع الدائري (Round-Robin) لضمان التنوع العادل والمنتظم
        working_pool = sorted(working_pool) 
        card_idx = 0
        
        for num in working_pool:
            start_idx = card_idx
            while len(cards[card_idx]) >= 5:
                card_idx = (card_idx + 1) % 6
                if card_idx == start_idx:
                    break 
                    
            if len(cards[card_idx]) < 5:
                cards[card_idx].append(num)
                card_idx = (card_idx + 1) % 6
                
        cards = [sorted(c) for c in cards]
        
        for i, c in enumerate(cards):
            st.info(f"🎴 بطاقة رقم {i+1}")
            st.markdown(f"## ` {c} `")
            
        st.markdown("---")
        st.write("🎯 **المجموعة المستهدفة الكلية:**")
        st.code(" , ".join(map(str, target)))
    else:
        st.warning("⚠️ أدخل الأرقام أولاً.")