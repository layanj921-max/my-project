import streamlit as st
import google.generativeai as genai

# إعداد واجهة الموقع
st.set_page_config(page_title="مدرب المهنة والمالية الذكي", layout="centered")

# إعداد Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🚀 منصة المحاكاة الذكية للمقابلات الوظيفية")

# إعدادات الوظيفة في المنتصف
job = st.text_input("الوظيفة المستهدفة:")

# زر لتوليد أسئلة متعددة
if job:
    if st.button("توليد سؤال جديد"):
        with st.spinner('جاري تحضير سؤال احترافي...'):
            q_prompt = f"اطرحي سؤال مقابلة وظيفية واحد ومميز لوظيفة {job}. لا تضعي مقدمات."
            response = model.generate_content(q_prompt)
            st.session_state['question'] = response.text
            st.rerun()

    # عرض السؤال والإجابة
    if 'question' in st.session_state:
        st.subheader(f"سؤال المقابلة: {st.session_state['question']}")
        user_answer = st.text_area("أجيبي على السؤال هنا:")

        if st.button("تحليل الإجابة بذكاء"):
            with st.spinner('المحاور الذكي يحلل إجابتك...'):
                # تعديل البرومبت ليطلب الاختصار والتركيز على القوة والضعف
                prompt = f"أنتِ خبيرة توظيف. الطالبة تتقدم لوظيفة {job}. السؤال: {st.session_state['question']}. إجابتها: {user_answer}. حللي الإجابة تقنياً ومالياً وقدمي التحليل في نقاط مختصرة جداً: نقاط القوة، نقاط الضعف، ونصيحة واحدة للتحسين. لا تكتبي مقدمات."
                response = model.generate_content(prompt)
                st.write("### 📊 التقييم المهني والمالي:")
                st.info(response.text)
                st.balloons()
else:
    st.info("الرجاء إدخال اسم الوظيفة للبدء.")

with st.sidebar:
    st.write("---")
    st.write("تطوير: ليان هاني")
