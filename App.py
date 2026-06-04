import streamlit as st

st.set_page_config(page_title="مدرب المهنة والمالية", layout="wide")

st.title("💼 منصة تقييم وتدريب المقابلات الذكي")

tab1, tab2, tab3 = st.tabs(["بياناتي المهنية", "محاكي المقابلة", "التقرير النهائي"])

with tab1:
    st.header("إدخال البيانات المهنية")
    name = st.text_input("الاسم الكريم:")
    job = st.text_input("الوظيفة المستهدفة:")
    st.write("جاهزة للمرحلة التالية؟ انتقلي لتب 'محاكي المقابلة'")

with tab2:
    st.header("محاكي المقابلة")
    answer = st.text_area("سؤال: كيف ستضيفين قيمة مالية ومهنية للشركة التي ستعملين بها؟")
    if st.button("تحليل الإجابة"):
        st.success("تم تحليل مهاراتك المهنية بنجاح!")

with tab3:
    st.header("التقرير الختامي")
    if st.button("عرض التقييم"):
        st.write("---")
        st.write("✅ **التقييم المهني:** متميزة في صياغة الأهداف.")
        st.write("✅ **التقييم المالي:** تم ربط مهاراتك بتوقعات السوق بنجاح.")
        st.balloons()

with st.sidebar:
    st.info("مشروع المهنية والمالية - 2026")
    st.write("تطوير: ليان هاني ")