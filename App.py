import streamlit as st
import google.generativeai as genai

# تصميم الصفحة بعرض كامل (Wide)
st.set_page_config(page_title="منصة المحاكاة الذكية", layout="wide")

# ألوان التصميم (CSS)
st.markdown("""
    <style>
    .main { background-color: #faf9f6; }
    h1 { color: #8e554a; text-align: center; font-family: 'Arial'; }
    .stButton>button { background-color: #8e554a; color: white; border-radius: 10px; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { border-color: #8e554a; }
    </style>
    """, unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.title(" منصة المحاكاة الذكية للمقابلات الوظيفية")

# تقسيم الشاشة إلى عمودين
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### : نبذة عن البرنامج")
    st.write("منصتك الشخصية للتدريب على المقابلات. اختاري وظيفتك، احصلي على أسئلة ذكية، وقيمي إجاباتك فوراً لتحسين فرصك في سوق العمل.")
    
    st.markdown("---")
    popular_jobs = ["اختر وظيفة...", "مطور برمجيات", "مصمم واجهات UI/UX", "محاسب مالي", "مدير مشاريع", "أخصائي تسويق"]
    selected_job = st.selectbox("الوظائف الشائعة:", popular_jobs)
    job_input = st.text_input("أو اكتبي وظيفتك المستهدفة:")
    
    job = job_input if job_input else (selected_job if selected_job != popular_jobs[0] else None)

with col2:
    if job:
        if st.button("توليد سؤال جديد للمقابلة"):
            with st.spinner('جاري تحضير سؤال احترافي...'):
                q_prompt = f"اطرحي سؤال مقابلة وظيفية واحد ومميز لوظيفة {job}. لا تضعي مقدمات."
                response = model.generate_content(q_prompt)
                st.session_state['question'] = response.text
                st.rerun()

        if 'question' in st.session_state:
            st.subheader("سؤال المقابلة:")
            st.info(st.session_state['question'])
            
            user_answer = st.text_area("أجيبي على السؤال هنا:", height=150)

            if st.button("تحليل الإجابة بذكاء"):
                with st.spinner('المحاور الذكي يحلل إجابتك...'):
                    prompt = f"لوظيفة {job}. السؤال: {st.session_state['question']}. الإجابة: {user_answer}. حللي الإجابة تقنياً ومالياً وقدمي التحليل في نقاط مختصرة جداً: نقاط القوة، نقاط الضعف، ونصيحة واحدة للتحسين. لا تكتبي مقدمات."
                    response = model.generate_content(prompt)
                    st.write("### 📊 التقييم المهني والمالي:")
                    st.success(response.text)
                    st.balloons()
    else:
        st.info(" ابدئي باختيار أو كتابة اسم الوظيفة المستهدفة من القائمة الجانبية.")

with st.sidebar:
    st.image("https://img.freepik.com/free-vector/job-interview-conversation_74855-7566.jpg")
    st.write("---")
    st.write(" تطوير: ليان هاني")
