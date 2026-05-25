def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            # 1. فتح الصورة الأصلية
            img = Image.open(uploaded_file)
            
            # 2. تحويل الصورة إلى أبيض وأسود (Grayscale)
            gray_img = img.convert('L')
            
            # 3. حفظ الصورة المعدلة في الذاكرة المؤقتة للبرنامج
            buffered = io.BytesIO()
            gray_img.save(buffered, format="PNG")
            
            # 4. تحويل الصورة "المعدلة" إلى Base64 لإرسالها لجوجل
            encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # 5. إرسالها إلى سيرفرات جوجل (نفس كودك الأصلي تماماً)
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
            st.error(f"⚠️ حدث خطأ تقني في القراءة: {e}")
            return []
    return []