import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Arabi-Q", layout="centered")

st.markdown(f"""
    <style>
    /* الخلفية الأساسية - البنفسجي الداكن */
    .stApp {{
        background-color: #1A0B3F;
        color: #FFFFFF;
    }}
    
    /* القائمة الجانبية - البنفسجي الباهت */
    [data-testid="stSidebar"] {{
        background-color: #2D1B5E;
    }}
    
    /* العناوين الرئيسية - البنفسجي المتوسط مع توهج */
    h1 {{
        color: #6B37FF;
        text-shadow: 0 0 10px #A855F7;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* نصوص العناوين الجانبية والأزرار */
    h3, .stMarkdown p {{
        color: #FFFFFF;
    }}
    
    /* تلوين الروابط أو النصوص المميزة بالأزرق السماوي */
    .stInfo {{
        background-color: #2D1B5E;
        border: 1px solid #00D1FF;
        color: #00D1FF;
    }}

    /* تحسين شكل صندوق الإدخال */
    .stChatInput {{
        border-radius: 15px;
        border: 1px solid #6B37FF;
    }}
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00D1FF; text-shadow: 0 0 20px #6B37FF;'>🟣 Arabi-Q</h1>", unsafe_allow_html=True)
    st.write("This AI-powered tutor helps bridge the gap between Arabic and English.")
    st.divider()
    
    # معلومات الطالبة
    st.markdown("<p style='color: #A855F7; font-weight: bold;'>Student Name:</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px;'>Layan Hani</p>", unsafe_allow_html=True) 
    
    st.divider()
    
    # معلومات المعلمة
    st.markdown("<p style='color: #A855F7; font-weight: bold;'>Supervised by:</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px;'>Ms. Khawlah Alsuraihi </p>", unsafe_allow_html=True) 
    
    st.divider()
    st.write(" **Subject:** English Project")
    st.write(" **Class:** 10th Grade")

# الواجهة الرئيسية
st.markdown("<h1 style='color: #00D1FF;'>Arabi-Q: The AI Bridge</h1>", unsafe_allow_html=True)
st.info("مرحباً بك! أدخل أي نص من المناهج الدراسية العربية ليتم ترجمته وشرحه بالإنجليزية بدقة أكاديمية.")

# إعدادات المحرك والـ API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

try:
    # تصحيح المسافات (Indentation) هنا لتعمل بشكل صحيح داخل الـ try
    model = genai.GenerativeModel('gemini-2.5-flash')    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض المحادثة السابقة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # استقبال الأسئلة والمناهج
    if prompt := st.chat_input("أدخل النص الدراسي هنا لترجمته..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # تحسين الـ instruction ليركز على ترجمة المناهج والمصطلحات العلمية بدقة
            instruction = (
                f"You are an expert academic translator specializing in school curricula. "
                f"Translate the following Arabic educational text into accurate, professional English. "
                f"Ensure scientific or mathematical terms are translated into their proper technical equivalents "
                f"(not literal translations) and adapt symbols if needed (e.g., math variables). "
                f"Here is the text:\n\n{prompt}"
            )
            
            response = model.generate_content(instruction)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Technical Hint: {e}")
