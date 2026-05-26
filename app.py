import streamlit as st

st.set_page_config(page_title="العبقري 2", layout="centered")

st.title("لوحة تحكم العبقري 2")

# إدخال الأرقام عبر صندوق نص (مضمون 100% للموبايل)
st.write("### أدخل الأرقام (افصل بينها بمسافة):")
input_data = st.text_area("مثال: 1 5 12 20 45", height=100)

# تحويل النص إلى قائمة أرقام
selected_numbers = []
if input_data:
    try:
        selected_numbers = sorted([int(n) for n in input_data.split() if n.isdigit()])
    except:
        st.error("يرجى إدخال أرقام صحيحة فقط.")

# العداد
count = len(selected_numbers)
st.metric(label="عدد الأرقام المختارة", value=f"{count} / 50")

# الفلترة (تظهر فقط عند اكتمال العدد أو الرغبة)
if count >= 10:
    st.success("الآن يمكنك معالجة البيانات.")
    # هنا ستضع كود خوارزمياتك التي تكلمنا عنها سابقاً
    st.write("الأرقام مرتبة:", selected_numbers)