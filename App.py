import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="منصة المحاكاة الذكية", layout="wide")

# إعداد الموديل
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# تهيئة الحالة لنقل المعلومات بين الصفحات
if 'selected_job' not in st.session_state:
    st.session_state['selected_job'] = None

# --- الصفحة الرئيسية (بوابة الوظائف) ---
if st.session_state['selected_job'] is None:
    st.title("🚀 مرحباً بكِ في منصة المحاكاة الذكية")
    st.write("اختاري وظيفتك من القائمة أدناه أو أدخليها يدوياً للبدء:")
    
    # شبكة المربعات (الوظائف الشائعة)
    cols = st.columns(4)
    jobs = ["مهندس", "طيار", "طبيب جراح", "مبرمج"]
    
    for i, job in enumerate(jobs):
        if cols[i % 4].button(job, use_container_width=True):
            st.session_state['selected_job'] = job
            st.rerun()

    # خيار الوظيفة المخصصة
    st.write("---")
    custom_job = st.text_input("أو اكتبي وظيفتك الخاصة هنا:")
    if st.button("بدء المحاكاة للوظيفة المكتوبة"):
        if custom_job:
            st.session_state['selected_job'] = custom_job
            st.rerun()

# --- صفحة المحادثة (بعد اختيار الوظيفة) ---
else:
    job = st.session_state['selected_job']
    st.title(f"💼 محاكاة مقابلة لـ: {job}")
    
    if st.button("⬅️ عودة لاختيار وظيفة أخرى"):
        st.session_state['selected_job'] = None
        st.session_state.pop('question', None)
        st.rerun()

    if st.button("توليد سؤال مقابلة"):
        with st.spinner('جاري التحضير...'):
            res = model.generate_content(f"اطرحي سؤال مقابلة لوظيفة {job}")
            st.session_state['question'] = res.text
            st.rerun()

    if 'question' in st.session_state:
        st.info(st.session_state['question'])
        answer = st.text_area("أجيبي هنا:")
        if st.button("تحليل الإجابة"):
            analysis = model.generate_content(f"حللي إجابة: {answer} لوظيفة {job}")
            st.success(analysis.text)
