import streamlit as st
import base64
import requests
import re

# 1. إعدادات المظهر
st.set_page_config(page_title="Genius 2 Hybrid - Pure Victory", page_icon="🔮", layout="centered")

st.title("🔮 خوارزمية ضربة المعلم - إصدار الاستراتيجية المكتسحة")
st.write("النظام العشري (9 صناديق) | تمرير أعلى 4 صناديق مكررة | اعتماد الثانية النقية (الطازجة) وحظر الأولى النقية.")

# جلب المفتاح السري بالطريقة القديمة الشغالة مئة بالمئة عندك
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# 2. دالة الماسح الضوئي القديمة الشغالة والناجحة عندك 100% بدون أي تعديل
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

# 3. واجهة المستخدم والتنبيهات والتحقق التلقائي المتوافقة تماماً مع مشروعك
st.header("📸 خطوة 1: مسح السحبات وتحليل الجبهات")

img_file_1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg", "jpeg"], key="draw1")
raw_nums_1 = extract_numbers_from_uploaded_file(img_file_1) if img_file_1 else []

# فحص السحبة الأولى
if img_file_1:
    text_input_1 = st.text_area("أرقام السحبة الأولى (راجعها):", value=", ".join(map(str, raw_nums_1)))
    current_nums_1 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_1)]
    if len(current_nums_1) == 50:
        st.success(f"✅ قراءة مكتملة: تم رصد {len(current_nums_1)} رقماً.")
    else:
        st.warning(f"⚠️ انتبه: تم رصد {len(current_nums_1)} رقماً فقط! المطلوب 50.")
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
        st.warning(f"⚠️ انتبه: تم رصد {len(current_nums_2)} رقماً فقط! المطلوب 50.")
else:
    text_input_2 = ""

st.markdown("---")

# 4. المعالجة المركزية وهندسة الوعاء بناءً على استراتيجيتك الجديدة المكتسحة
if st.button("🚀 تشغيل الخوارزمية وتوليد البطاقات الستة"):
    d1 = [int(n) for n in re.findall(r'\b\d+\b', text_input_1)] if text_input_1 else []
    d2 = [int(n) for n in re.findall(r'\b\d+\b', text_input_2)] if text_input_2 else []
    
    if len(d1) > 0 and len(d2) > 0:
        
        # أ. تشريح الـ 4 مجاميع الصافية بدقة بالغة
        shared_numbers = set(d1).intersection(set(d2))
        all_possible = set(range(1, 91))
        hidden_numbers = all_possible.difference(set(d1).union(set(d2)))
        
        purified_draw_2 = set(d2).difference(shared_numbers)
        
        # ب. التوزيع العشري على 9 صناديق تماثل أعمدة البنغو الحقيقية
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
        
        # ج. ترتيب الصناديق تنازلياً وتمرير أرقام أعلى 4 صناديق مزدحمة بالمشترك
        sorted_boxes_by_len = sorted(boxes.keys(), key=lambda k: len(boxes[k]), reverse=True)
        top_4_boxes_to_keep = sorted_boxes_by_len[:4]
        
        allowed_shared_numbers = set()
        for b_id in top_4_boxes_to_keep:
            allowed_shared_numbers.update(boxes[b_id])
            
        # د. بناء الوعاء الكلي (Target Pool): الغائب + الثانية النقية الطازجة + المشترك المختار
        target = sorted(list(hidden_numbers.union(purified_draw_2).union(allowed_shared_numbers)))
        
        # هـ. تقسيم الوعاء الكلي إلى 3 مناطق واختيار عينات متساوية (Master Pool)
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
            
        working_pool = sorted(list(set(master_pool)))
        
        # و. التوزيع الدائري المحمي (Round-Robin) بالتساوي على 6 بطاقات (حد أقصى 5 أرقام)
        cards = [[] for _ in range(6)]
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
        
        # ز. عرض النتائج والعدادات الثلاثية المريحة للعين
        st.success(f"🎯 تم توليد البطاقات وتطهير الوعاء بنجاح! عدد أرقام الوعاء المستهدف: {len(target)} رقماً.")
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric(label="📊 الغائب المار للوعاء", value=f"{len(hidden_numbers)} رقم")
        with col2: st.metric(label="✨ الثانية النقية (طازجة)", value=f"{len(purified_draw_2)} رقم")
        with col3: st.metric(label="🔥 المشترك الناجي عبر 4 صناديق", value=f"{len(allowed_shared_numbers)} رقم")
            
        st.markdown("---")
        for i, c in enumerate(cards):
            if c:
                st.info(f"🎴 بطاقة رقم {i+1}")
                st.markdown(f"## ` {c} `")
            else:
                st.warning(f"🎴 بطاقة رقم {i+1} فارغة لعدم تطابق شروط الفرز")
            
        st.markdown("---")
        st.write("🎯 **المجموعة المستهدفة الكلية الصافية في الوعاء (Target Pool):**")
        st.code(" , ".join(map(str, target)))
    else:
        st.warning("⚠️ أدخل أو امسح الأرقام أولاً لبدء الحساب.")