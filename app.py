def extract_numbers_from_uploaded_file(uploaded_file):
    if uploaded_file is None: return []
    try:
        bytes_data = uploaded_file.getvalue()
        encoded_image = base64.b64encode(bytes_data).decode('utf-8')
        url = f"https://vision.googleapis.com/v1/images:annotate?key={st.secrets['GOOGLE_API_KEY']}"
        payload = {"requests": [{"image": {"content": encoded_image}, "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]}]}
        
        response = requests.post(url, json=payload)
        
        # --- فحص التشخيص ---
        if response.status_code != 200:
            st.error(f"فشل الاتصال بجوجل: كود {response.status_code}")
            return []
            
        result = response.json()
        
        # التأكد من وجود نص
        if 'responses' in result and 'fullTextAnnotation' in result['responses'][0]:
            text = result['responses'][0]['fullTextAnnotation']['text']
            # الطباعة للتشخيص
            st.write(f"نص القراءة الخام: {text[:100]}...") # يظهر أول 100 حرف
            nums = [int(n) for n in re.findall(r'\b\d+\b', text) if 1 <= int(n) <= 90]
            return sorted(list(set(nums)))
        else:
            st.error("جوجل لم تعثر على أي نص في الصورة.")
            return []
    except Exception as e:
        st.error(f"خطأ غير متوقع: {e}")
        return []