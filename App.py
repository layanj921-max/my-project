import streamlit as st
import google.generativeai as genai

# لا داعي لإضافة CSS معقد، لأن ملف config.toml سيتولى المهمة!
st.set_page_config(page_title="منصة المحاكاة الذكية", layout="wide")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# العنوان بتنسيق متناسق
st.markdown("<h1 style='color: #d68e7b;'>🚀 منصة المحاكاة الذكية</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("💡 نبذة عن البرنامج")
    st.write("مدربك الشخصي للمقابلات. اختاري وظيفتك وابدئي التدريب.")
    
    popular_jobs = ["اختر وظيفة...", "مطور برمجيات", "مصمم واجهات", "محاسب مالي"]
    job = st.selectbox("الوظائف الشائعة:", popular_jobs)
    
    if st.button("توليد سؤال"):
        # منطق الموديل هنا
        pass

with col2:
    st.info("هنا تظهر منطقة التدريب الخاصة بك، مع الألوان التي اخترتِها.")
    # بقية عناصر واجهة المستخدم
