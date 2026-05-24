import streamlit as st
import cv2
import pytesseract
import re
import numpy as np

# 1. إعدادات مظهر شاشة الهاتف وعنوان التطبيق الأساسي
st.set_page_config(page_title="Bingo 90 Zone Granville", page_icon="🔮", layout="centered")

st.title("🔮 خوارزمية ضربة المعلم - النسخة البرق الآمنة")
st.write("تم حل مشكلة التعليق نهائياً عبر تقنية تقليص الصور الذكية لحماية ذاكرة السيرفر السحابي!")

# 2. دالة الماسح الضوئي الذكية الخفيفة مع ميزة تصغير الحجم لحماية السيرفر
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # قراءة ملف الصورة
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        
        # 🛠️ السر الحاسم: تصغير أبعاد الصورة لـ 800 بكسل فقط لجعلها خفيفة جداً على السيرفر السحابي ومنع التعليق
        h, w = image.shape[:2]
        if w > 800:
            new_w = 800
            new_h = int((h / w) * 800)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # فلتر تنظيف حاد مباشر وسريع جداً
        threshold_image = cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 2
        )
        
        contours, _ = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
        
        extracted_set = set()
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # عزل الدوائر الرقمية ومنع التدميج
            if 10 < w < 100 and 10 < h < 100:
                roi = gray_image[y:y+h, x:x+w]
                text = pytesseract.image_to_string(roi, config=custom_config)
                clean_text = text.strip()
                if clean_text.isdigit():
                    num = int(clean_text)
                    if 1 <= num <= 90:
                        extracted_set.add(num)
                        
        return sorted(list(extracted_set))
    return []

# -------------------------------------------------------------
# 3. واجهة المستخدم على الهاتف (رفع الصور)
# -------------------------------------------------------------
st.header("📸 خطوة 1: مسح السحبات بالعين الإلكترونية")

img_file_1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg", "jpeg"], key="draw1")
img_file_2 = st.file_uploader("ارفع صورة السحبة الثانية:", type=["png", "jpg", "jpeg"], key="draw2")

# جلب الأرقام من الـ OCR الخفيف جداً
raw_nums_1 = extract_numbers_from_uploaded_file(img_file_1) if img_file_1 else []
raw_nums_2 = extract_numbers_from_uploaded_file(img_file_2) if img_file_2 else []

st.markdown("---")
st.header("✍️ خطوة 2: مراجعة وتعديل البيانات (تأكيد الأرقام)")

text_input_1 = st.text_area(f"أرقام السحبة الأولى المستخرجة [قراءة حية آلياً]:", value=", ".join(map(str, raw_nums_1)))
text_input_2 = st.text_area(f"أرقام السحبة الثانية المستخرجة [قراءة حية آلياً]:", value=", ".join(map(str, raw_nums_2)))

# 4. زر التشغيل الرئيسي والمعالجة الحسابية المحكمة الصارمة
if st.button("🚀 نخل الصناديق وتوليد بطاقات غرانفيل النطاقية"):
    final_draw_1 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_1)]
    final_draw_2 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_2)]
    
    if len(final_draw_1) > 0 and len(final_draw_2) > 0:
        with st.spinner("جاري تطبيق التصفية الصارمة وتوليد البطاقات..."):
            
            # أ. استخراج المكررات المشتركة فقط
            shared_numbers = set(final_draw_1).intersection(set(final_draw_2))
            
            # ب. حساب الأرقام المخفية كلياً من الـ 90
            all_possible_numbers = set(range(1, 91))
            appeared_so_far = set(final_draw_1).union(set(final_draw_2))
            hidden_numbers = all_possible_numbers.difference(appeared_so_far)
            
            # ج. توزيع ونخل المكررات جغرافياً عبر الصناديق الستة واختيار أعلى 3
            boxes = {
                1: [num for num in shared_numbers if 1 <= num <= 15],
                2: [num for num in shared_numbers if 16 <= num <= 30],
                3: [num for num in shared_numbers if 31 <= num <= 45],
                4: [num for num in shared_numbers if 46 <= num <= 60],
                5: [num for num in shared_numbers if 61 <= num <= 75],
                6: [num for num in shared_numbers if 76 <= num <= 90]
            }
            
            sorted_boxes_by_count = sorted(boxes.keys(), key=lambda k: len(boxes[k]))
            retained_boxes_ids = sorted_boxes_by_count[3:]
            
            retained_shared_numbers = []
            for box_id in retained_boxes_ids:
                retained_shared_numbers.extend(boxes[box_id])
                
            # د. المعادلة المحكمة الصافية: (كامل الصورة 1) + (المشتركات الساخنة) + (المخفية)
            target_sample_space = sorted(list(set(final_draw_1).union(set(retained_shared_numbers)).union(hidden_numbers)))
            
            # هـ. عزل الصندوق وتصنيفه إلى 3 نطاقات جغرافية حادة
            zone_1_30 = [num for num in target_sample_space if 1 <= num <= 30]
            zone_31_60 = [num for num in target_sample_space if 31 <= num <= 60]
            zone_61_90 = [num for num in target_sample_space if 61 <= num <= 90]
            
            def sort_by_granville(pool):
                return sorted(pool, key=lambda x: (x % 2, x > 45, x % 10))
            
            # و. فرز واقتطاع البطاقات لكل نطاق بالتناوب بنظام غرانفيل
            g_pool_1 = sort_by_granville(zone_1_30)[:10]
            card_1 = sorted([g_pool_1[i] for i in range(0, len(g_pool_1), 2)])
            card_2 = sorted([g_pool_1[i] for i in range(1, len(g_pool_1), 2)])
            
            g_pool_2 = sort_by_granville(zone_31_60)[:10]
            card_3 = sorted([g_pool_2[i] for i in range(0, len(g_pool_2), 2)])
            card_4 = sorted([g_pool_2[i] for i in range(1, len(g_pool_2), 2)])
            
            g_pool_3 = sort_by_granville(zone_61_90)[:10]
            card_5 = sorted([g_pool_3[i] for i in range(0, len(g_pool_3), 2)])
            card_6 = sorted([g_pool_3[i] for i in range(1, len(g_pool_3), 2)])
            
            # -------------------------------------------------------------
            # 5. العرض العمودي المتتالي الصافي (واحدة تلو الأخرى)
            # -------------------------------------------------------------
            st.success("🏁 تم الفرز وتوليد البطاقات بنجاح صاعق!")
            st.markdown("## 📋 قائمة البطاقات الستة الجاهزة للعب:")
            
            st.info("🎴 بطاقة رقم 1 [النطاق 1-30]")
            st.markdown(f"## ` {card_1} `")
            
            st.info("🎴 بطاقة رقم 2 [النطاق 1-30]")
            st.markdown(f"## ` {card_2} `")
            
            st.warning("🎴 بطاقة رقم 3 [النطاق 31-60]")
            st.markdown(f"## ` {card_3} `")
            
            st.warning("🎴 بطاقة رقم 4 [النطاق 31-60]")
            st.markdown(f"## ` {card_4} `")
            
            st.error("🎴 بطاقة رقم 5 [النطاق 61-90]")
            st.markdown(f"## ` {card_5} `")
            
            st.error("🎴 بطاقة رقم 6 [النطاق 61-90]")
            st.markdown(f"## ` {card_6} `")
            
            st.markdown("---")
            st.subheader("📋 كامل أرقام الصندوق المستهدف للرجوع إليها:")
            st.code(" , ".join(map(str, target_sample_space)), language="text")
            
    else:
        st.warning("⚠️ يرجى التأكد من إدخال الأرقام في السحبة الأولى والثانية أولاً.")