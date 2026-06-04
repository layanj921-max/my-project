import streamlit as st
import google.generativeai as genai

# إعداد واجهة الموقع
st.set_page_config(page_title="مدرب المقابلات الذكي", layout="wide")

# إعداد مفتاح Gemini من الخزنة
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    gemini-1.5-flashgemini-1.5-flash # هذا النموذج هو 
else:
    st.error("لم يتم العثور على مفتاح API في الخزنة. يرجى إضافته في الإعدادات.")
    st.stop()

st.title("🚀 منصة المحاكاة الذكية")

with st.sidebar:
    job = st.text_input("الوظيفة المستهدفة:")

if job:
    if 'question' not in st.session_state:
        with st.spinner('جاري توليد سؤالك...'):
            try:
                response = model.generate_content(f"اطرحي سؤال مقابلة لوظيفة {job} يركز على الجانب المهني والمالي.")
                st.session_state['question'] = response.text
            except Exception as e:
                st.error(f"خطأ في الاتصال بجوجل: {e}")
                st.stop()

    st.subheader(f"سؤال المقابلة: {st.session_state.get('question', '')}")
    user_answer = st.text_area("أجيبي على السؤال:")

    if st.button("تحليل الإجابة"):
        with st.spinner('جاري التحليل...'):
            prompt = f"حللي إجابة الطالبة للوظيفة {job}: {user_answer}"
            analysis = model.generate_content(prompt)
            st.info(analysis.text)
            st.balloons()
