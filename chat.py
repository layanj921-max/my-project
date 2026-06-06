import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import io

st.set_page_config(page_title="Arabi-Q", layout="centered")

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    return pdf.output(dest='S') 

st.markdown(f"""
    <style>
    .stApp {{ background-color: #1A0B3F; color: #FFFFFF; }}
    [data-testid="stSidebar"] {{ background-color: #2D1B5E; }}
    h1 {{ color: #00D1FF; text-shadow: 0 0 10px #A855F7; font-family: 'Segoe UI', sans-serif; }}
    h3, .stMarkdown p {{ color: #FFFFFF; }}
    .stInfo {{ background-color: #2D1B5E; border: 1px solid #00D1FF; color: #00D1FF; }}
    .stChatInput {{ border-radius: 15px; border: 1px solid #6B37FF; }}
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00D1FF;'> Arabi-Q</h1>", unsafe_allow_html=True)
    st.write("This AI-powered tutor helps bridge the gap between Arabic and English.")
    st.divider()
    st.markdown("<p style='color: #A855F7; font-weight: bold;'>Student Name:</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px;'>Layan Hani</p>", unsafe_allow_html=True) 
    st.divider()
    st.markdown("<p style='color: #A855F7; font-weight: bold;'>Supervised by:</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px;'>Ms. Khawlah Alsuraihi </p>", unsafe_allow_html=True) 
    st.divider()
    st.write("**Subject:** English Project")
    st.write("**Class:** 10th Grade")

st.markdown("<h1>Arabi-Q: The AI Bridge</h1>", unsafe_allow_html=True)
st.info("Welcome! Enter any text, or upload an image/PDF from Arabic school curricula to have it translated and explained with academic precision.")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

try:
    model = genai.GenerativeModel('gemini-2.5-flash')    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    uploaded_file = st.file_uploader("Upload an image or PDF of your curriculum", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file is not None:
        if st.button(" Translate Uploaded File"):
            with st.spinner("Analyzing and translating your file..."):
                file_type = uploaded_file.type
                instruction = (
                    "You are an expert academic translator specializing in school curricula. "
                    "Analyze this uploaded document/image, extract the Arabic educational text, "
                    "and translate it into accurate, professional English. "
                    "Ensure scientific or mathematical terms are translated into their proper technical equivalents "
                    "and provide a clear academic explanation."
                )

                if "image" in file_type:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Uploaded Image", use_container_width=True)
                    response = model.generate_content([instruction, image])
                elif "pdf" in file_type:
                    pdf_data = uploaded_file.read()
                    pdf_part = {"mime_type": "application/pdf", "data": pdf_data}
                    response = model.generate_content([instruction, pdf_part])

                st.session_state.messages.append({"role": "user", "content": f"📝 [Uploaded File: {uploaded_file.name}]"})
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    st.divider()

    # --- عرض المحادثة وتنظيم الأزرار بشكل صحيح وسليم ---
    for index, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
            # التعديل هنا: يظهر الصندوق النظيف والزر السليم بدون أي تكرار أو أخطاء برمجية
            if msg["role"] == "assistant":
                st.write("📋 **Copy the text below:**")
                st.code(msg["content"], language="markdown")
                
                # توليد الـ PDF وتحميله بشكل أنيق ومباشر
                pdf_bytes = create_pdf(msg["content"])
                st.download_button(
                    label="📥 Download Explanation as PDF",
                    data=pdf_bytes,
                    file_name=f"ArabiQ_Explanation_{index}.pdf",
                    mime="application/pdf",
                    key=f"pdf_btn_{index}" # مفتاح فريد لكل زر لتجنب تداخل الأزرار
                )

    # استقبال النصوص العادية
    if prompt := st.chat_input("Or enter educational text here to translate..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            instruction = (
                f"You are an expert academic translator specializing in school curricula. "
                f"Translate the following Arabic educational text into accurate, professional English. "
                f"Ensure scientific or mathematical terms are translated into their proper technical equivalents "
                f"and adapt symbols if needed. Here is the text:\n\n{prompt}"
            )
            
            response = model.generate_content(instruction)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun() 

except Exception as e:
    st.error(f"Technical Hint: {e}")
