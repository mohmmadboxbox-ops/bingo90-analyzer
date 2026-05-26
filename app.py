import streamlit as st
import base64
import requests
import re

# 1. إعدادات المظهر الفني لواجهة التطبيق
st.set_page_config(page_title="Bingo 90 Zone Granville", page_icon="🔮", layout="centered")

st.title("🔮 خوارزمية ضربة المعلم - إصدار الاستراتيجية المكتسحة")
st.write("النظام العشري (9 صناديق) | تمرير أعلى 4 صناديق مكررة | اعتماد الثانية النقية (الطازجة) وحظر الأولى النقية.")

# جلب المفتاح السري بأمان من إعدادات Streamlit وحمايته من التوقف
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")

if not GOOGLE_API_KEY:
    st.error("🔑 خطأ أمني: لم يتم العثور على GOOGLE_API_KEY في إعدادات Secrets الخاصة بـ Streamlit!")

# 2. دالة الماسح الضوئي الذكي المحدثة بالكامل لحل مشكلة الـ 404
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is not None and GOOGLE_API_KEY:
        try:
            bytes_data = uploaded_file.getvalue()
            encoded_image = base64.b64encode(bytes_data).decode('utf-8')
            
            # تم تحديث الرابط إلى المسار الشامل لضمان التوافق التام وحل مشكلة 404
            url = f"https://googleapis.com{GOOGLE_API_KEY}"
            
            payload = {
                "requests": [{
                    "image": {"content": encoded_image},
                    "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
                }]
            }
            
            # إرسال الطلب مع تحديد الـ Headers لضمان استقبال البيانات كـ JSON بشكل سليم
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code != 200:
                st.warning(f"⚠️ تنبيه: يرجى التأكد من تفعيل خدمة Cloud Vision API في حساب جوجل الخاص بك (كود الحالة: {response.status_code}). يمكنك كتابة الأرقام يدوياً.")
                return []
                
            result = response.json()
            
            if 'error' in result:
                st.error(f"🚫 خطأ واجهة جوجل: {result['error']['message']}")
                return []
            
            if 'responses' in result and result['responses'] and 'fullTextAnnotation' in result['responses']:
                extracted_text = result['responses'][0]['fullTextAnnotation']['text']
                all_numbers = re.findall(r'\b\d+\b', extracted_text)
                valid_numbers = [int(num) for num in all_numbers if 1 <= int(num) <= 90]
                return sorted(list(set(valid_numbers)))
            else:
                st.warning("⚠️ تنبيه: لم يتم التعرف على أرقام داخل الصورة تلقائياً، يرجى كتابتها يدوياً.")
                return []
            
        except Exception as e:
            st.warning(f"⚠️ لم نتمكن من الاتصال بالماسح التلقائي: {e}. يمكنك الاعتماد على الإدخال اليدوي المباشر.")
            return []
    return []

# 3. واجهة المستخدم والتنبيهات والتحقق التلقائي أثناء إدخال البيانات
st.header("📸 خطوة 1: مسح السحبات وتحليل الجبهات")

# --- إدارة السحبة الأولى ---
img_file_1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg", "jpeg"], key="draw1")
raw_nums_1 = extract_numbers_from_uploaded_file(img_file_1) if img_file_1 else []

text_input_1 = st.text_area(
    "أرقام السحبة الأولى (راجعها وعدلها يدوياً إذا لزم الأمر):", 
    value=", ".join(map(str, raw_nums_1)),
    key="text_1"
)

current_nums_1 = [int(s) for s in re.findall(r'\b\d+\b', text_input_1)] if text_input_1 else []
if text_input_1:
    if len(current_nums_1) == 50:
        st.success(f"✅ السحبة الأولى مكتملة وصحيحة: تم رصد {len(current_nums_1)} رقماً.")
    else:
        st.warning(f"⚠️ انتبه: السحبة الأولى تحتوي على {len(current_nums_1)} رقماً فقط! المطلوب 50.")

st.markdown("---")

# --- إدارة السحبة الثانية ---
img_file_2 = st.file_uploader("ارفع صورة السحبة الثانية:", type=["png", "jpg", "jpeg"], key="draw2")
raw_nums_2 = extract_numbers_from_uploaded_file(img_file_2) if img_file_2 else []

text_input_2 = st.text_area(
    "أرقام السحبة الثانية (راجعها وعدلها يدوياً):", 
    value=", ".join(map(str, raw_nums_2)),
    key="text_2"
)

current_nums_2 = [int(s) for s in re.findall(r'\b\d+\b', text_input_2)] if text_input_2 else []
if text_input_2:
    if len(current_nums_2) == 50:
        st.success(f"✅ السحبة الثانية مكتملة وصحيحة: تم رصد {len(current_nums_2)} رقماً.")
    else:
        st.warning(f"⚠️ انتبه: السحبة الثانية تحتوي على {len(current_nums_2)} رقماً فقط! المطلوب 50.")

st.markdown("---")

# 4. المعالجة المركزية الكبرى وتطبيق الفلترة وهندسة الوعاء المستهدف
if st.button("🚀 تشغيل الخوارزمية وتوليد البطاقات الستة"):
    final_draw_1 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_1)] if text_input_1 else []
    final_draw_2 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_2)] if text_input_2 else []
    
    if len(final_draw_1) > 0 and len(final_draw_2) > 0:
        
        # أ. تشريح الـ 4 مجاميع الرياضية الصافية بدقة
        shared_numbers = set(final_draw_1).intersection(set(final_draw_2))
        all_possible = set(range(1, 91))
        hidden_numbers = all_possible.difference(set(final_draw_1).union(set(final_draw_2)))
        
        # استخراج المجموعات النقية لكل صورة على حدة
        purified_draw_1 = set(final_draw_1).difference(shared_numbers)
        purified_draw_2 = set(final_draw_2).difference(shared_numbers)
        
        # ب. توزيع الأرقام المشتركة بدقة على 9 صناديق عشرية تطابق أعمدة البنغو
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
        
        # ج. ترتيب الصناديق تنازلياً حسب كثافة احتوائها على المشترك لفرزها
        sorted_boxes_by_len = sorted(boxes.keys(), key=lambda k: len(boxes[k]), reverse=True)
        top_4_boxes_to_keep = sorted_boxes_by_len[:4]  # اختيار أعلى 4 صناديق مزدحمة للتمرير
        
        # تجميع أرقام المشترك الناجية التي سمحت لها الخوارزمية بالعبور
        allowed_shared_numbers = set()
        for b_id in top_4_boxes_to_keep:
            allowed_shared_numbers.update(boxes[b_id])
            
        # د. هندسة الوعاء الكلي (Target Pool) وفقاً لقاعدتك الاستراتيجية المكتسحة:
        # (الغائب بالكامل يدخل) + (الثانية النقية الطازجة تدخل بالكامل) + (المشترك المختار يدخل) 
        target = sorted(list(hidden_numbers.union(purified_draw_2).union(allowed_shared_numbers)))
        
        # هـ. تقسيم الوعاء الكلي إلى 3 مناطق متساوية واختيار الأرقام بشكل متناسق (Master Pool)
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
        
        # و. توزيع وعاء العمل دائرياً (Round-Robin) بالتساوي على 6 بطاقات حظ (5 أرقام بحد أقصى لكل بطاقة)
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
        
        # ز. عرض النتائج والمخرجات على الواجهة بشكل كتل منسقة ومنظمة
        st.success(f"🎯 تم توليد البطاقات وتطهير الوعاء بنجاح! عدد أرقام الوعاء المستهدف: {len(target)} رقماً.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="📊 الغائب المار للوعاء", value=f"{len(hidden_numbers)} رقم")
        with col2:
            st.metric(label="✨ الثانية النقية (طازجة)", value=f"{len(purified_draw_2)} رقم")
        with col3:
            st.metric(label="🔥 المشترك الناجي عبر 4 صناديق", value=f"{len(allowed_shared_numbers)} رقم")
            
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
        st.error("⚠️ خطأ في الإدخال: يرجى التأكد من رفع أو كتابة أرقام السحبتين أولاً لبدء الفحص.")