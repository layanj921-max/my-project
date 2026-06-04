import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="مدرب المهنة والمالية الذكي", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.title("🚀 منصة المحاكاة الذكية للمقابلات الوظيفية")

with st.sidebar:
    st.header("إعدادات المقابلة")
    job = st.text_input("الوظيفة المستهدفة:")
    if st.button("توليد سؤال جديد"):
        if 'question' in st.session_state:
            del st.session_state['question']
        st.rerun()

if 'question' not in st.session_state and job:
    with st.spinner('جاري تحضير سؤال احترافي يناسب وظيفتك...'):
        q_prompt = f"اطرحي سؤال مقابلة وظيفية واحد ومميز لوظيفة {job} يركز على الجانب المهني والمالي. لا تضعي مقدمات، فقط اطرحي السؤال."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": q_prompt}]
        )
        st.session_state['question'] = response.choices[0].message.content

if 'question' in st.session_state:
    st.subheader(f"سؤال المقابلة: {st.session_state['question']}")
    user_answer = st.text_area("أجيبي على السؤال هنا:")

    if st.button("تحليل الإجابة بذكاء"):
        with st.spinner('المحاور الذكي يحلل إجابتك...'):
            prompt = f"أنتِ خبيرة توظيف. الطالبة تتقدم لوظيفة {job}. السؤال هو: {st.session_state['question']}. إجابتها هي: {user_answer}. حللي الإجابة تقنياً ومالياً وقدمي نصائح دقيقة للتحسين."
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            st.write("### 📊 التقييم المهني والمالي:")
            st.info(response.choices[0].message.content)
            st.balloons()
else:
    st.info("الرجاء إدخال اسم الوظيفة في القائمة الجانبية للبدء.")

with st.sidebar:
    st.write("---")
    st.write("تطوير: ليان هاني")
