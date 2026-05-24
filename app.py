import streamlit as st
import base64
import requests
import re

# 1. إعدادات مظهر شاشة الهاتف وعنوان التطبيق الأساسي
st.set_page_config(page_title="Bingo 90 Zone Granville", page_icon="🔮", layout="centered")

st.title("🔮 خوارزمية ضربة المعلم - العرض المتتالي الصافي")
st.write("تمت إزالة الفواصل النصية! عرض البطاقات الستة متتالية بالترتيب من 1 إلى 6 لسهولة النقل السريع.")

# 💡 ضع المفتاح السري (API Key) الخاص بك هنا بين علامتي الاقتباس
GOOGLE_API_KEY = "ضع_مفتاح_جوجل_كلاود_هنا"

# 2. دالة الماسح الضوئي الاحترافية باستخدام Google Cloud Vision
def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            # قراءة ملف الصورة وتحويله إلى صيغة Base64 لإرسالها لجوجل
            bytes_data = uploaded_file.getvalue()
            encoded_image = base64.b64encode(bytes_data).decode('utf-8')
            
            # رابط طلب الخدمة من جوجل مدمج مع مفتاحك
            url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_API_KEY}"
            
            payload = {
                "requests": [
                    {
                        "image": {"content": encoded_image},
                        "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
                    }
                ]
            }
            
            # إرسال الصورة واستلام النتيجة
            response = requests.post(url, json=payload)
            result = response.json()
            
            # 🔍 فحص إذا كان هناك رفض من جوجل (الخطأ الذي ظهر لك سابقاً)
            if 'error' in result:
                st.error(f"🚫 جوجل رفضت الطلب والسبب: {result['error']['message']}")
                return []
            
            # استخراج النص المقروء
            extracted_text = result['responses'][0]['fullTextAnnotation']['text']
            
            # استخراج الأرقام فقط، والتحقق الذكي بأنها تقع بين 1 و 90 لحماية الحسابات
            all_numbers = re.findall(r'\b\d+\b', extracted_text)
            valid_numbers = [int(num) for num in all_numbers if 1 <= int(num) <= 90]
            
            # إرجاع قائمة مرتبة وبدون تكرار
            return sorted(list(set(valid_numbers)))
            
        except Exception as e:
            st.error(f"⚠️ حدث خطأ أثناء معالجة النتيجة: {e}")
            return []
    return []

# -------------------------------------------------------------
# 3. واجهة المستخدم على الهاتف (رفع الصور)
# -------------------------------------------------------------
st.header("📸 خطوة 1: مسح السحبات بالعين الإلكترونية")

img_file_1 = st.file_uploader("ارفع صورة السحبة الأولى:", type=["png", "jpg", "jpeg"], key="draw1")
img_file_2 = st.file_uploader("ارفع صورة السحبة الثانية:", type=["png", "jpg", "jpeg"], key="draw2")

# جلب الأرقام المبدئية من الـ OCR المطور
raw_nums_1 = extract_numbers_from_uploaded_file(img_file_1) if img_file_1 else []
raw_nums_2 = extract_numbers_from_uploaded_file(img_file_2) if img_file_2 else []

st.markdown("---")
st.header("✍️ خطوة 2: مراجعة وتعديل البيانات (حماية ضد خطأ الماسح)")
st.caption("إذا كانت هناك أرقام خاطئة أو مفقودة من القراءة الآلية، قم بتعديلها في المربعات أدناه يفصل بينها فاصلة ( , )")

# تحويل القوائم إلى نصوص يفصل بينها فاصلة ليسهل على المستخدم تعديلها يدوياً
text_input_1 = st.text_area("أرقام السحبة الأولى المستخرجة (راجعها وعدلها):", value=", ".join(map(str, raw_nums_1)))
text_input_2 = st.text_area("أرقام السحبة الثانية المستخرجة (راجعها وعدلها):", value=", ".join(map(str, raw_nums_2)))

# 4. زر التشغيل الرئيسي والمعالجة الحسابية المعتمدة
if st.button("🚀 نخل الصناديق وتوليد بطاقات غرانفيل النطاقية"):
    # تحويل النصوص المعدلة يدوياً إلى قوائم أرقام حقيقية للحسابات
    final_draw_1 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_1)]
    final_draw_2 = [int(s.strip()) for s in re.findall(r'\b\d+\b', text_input_2)]
    
    if len(final_draw_1) > 0 and len(final_draw_2) > 0:
        with st.spinner("جاري نخل الصندوق وتطبيق التقسيم الجغرافي النهائي لغرانفيل..."):
            
            # أ. حساب الصندوق المستهدف الشامل (المعادلة الثابتة المستقرة 82% نجاح كلي)
            shared_numbers = set(final_draw_1).intersection(set(final_draw_2))
            all_possible_numbers = set(range(1, 91))
            appeared_so_far = set(final_draw_1).union(set(final_draw_2))
            hidden_numbers = all_possible_numbers.difference(appeared_so_far)
            
            boxes = {
                1: [num for num in shared_numbers if 1 <= num <= 15],
                2: [num for num in shared_numbers if 16 <= num <= 30],
                3: [num for num in shared_numbers if 31 <= num <= 45],
                4: [num for num in shared_numbers if 46 <= num <= 60],
                5: [num for num in shared_numbers if 61 <= num <= 75],
                6: [num for num in shared_numbers if 76 <= num <= 90]
            }
            
            sorted_boxes_by_count = sorted(boxes.keys(), key=lambda k: len(boxes[k]))
            retained_boxes_ids = sorted_boxes_by