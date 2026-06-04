import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مسار", layout="wide")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

if 'selected_job' not in st.session_state: st.session_state['selected_job'] = None

if st.session_state['selected_job'] is None:
    st.title(" منصة مسار")
    st.write("اختاري مسارك المهني أو حللي مهاراتك:")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("اختيار وظيفة للتدريب")
        jobs = ["مهندس", "طيار", "طبيب جراح", "مبرمج"]
        for job in jobs:
            if st.button(job, use_container_width=True):
                st.session_state['selected_job'] = job
                st.rerun()
        
        custom_job = st.text_input("أو اكتبي وظيفة مخصصة:")
        if st.button("بدء محاكاة الوظيفة"):
            if custom_job:
                st.session_state['selected_job'] = custom_job
                st.rerun()

    with col_b:
        st.subheader(" مستشار المهارات والرواتب")
        skills = st.text_area("أدخلي مهاراتك (مثلاً: البرمجة، الإنجليزية، إدارة الوقت...):")
        if st.button("تحليل المهارات واقتراح وظيفة وراتب"):
            with st.spinner('جاري تحليل السوق والرواتب...'):
                prompt = f"بناءً على المهارات التالية: {skills}. اقترحي 3 وظائف مناسبة، مع تقدير للراتب لكل منها، ونصيحة تربية مالية واحدة للادخار."
                response = model.generate_content(prompt)
                st.info(response.text)

else:
    job = st.session_state['selected_job']
    st.title(f" محاكاة مقابلة لـ: {job}")
    
    if st.button(" عودة"):
        st.session_state['selected_job'] = None
        st.rerun()

    if st.button("توليد سؤال مقابلة"):
        res = model.generate_content(f"اطرحي سؤال مقابلة لوظيفة {job}")
        st.session_state['question'] = res.text
        st.rerun()

    if 'question' in st.session_state:
        st.warning(f"سؤالك: {st.session_state['question']}")
        answer = st.text_area("أجيبي هنا:")
        if st.button("تحليل الإجابة مالياً ومهنياً"):
            res = model.generate_content(f"لوظيفة {job}، السؤال: {st.session_state['question']}، الإجابة: {answer}. حللي الأداء وقدمي نصيحة مالية تخص هذه الوظيفة.")
            st.success(res.text)
