import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

st.set_page_config(page_title="سِيَر | رواة وقصص الصحابة", layout="wide")

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    pdf_output = pdf.output(dest='S')
    return bytes(pdf_output)

# تصميم الواجهة بالألوان الإسلامية الفخمة ودعم اللغة العربية من اليمين لليسار
st.markdown("""
    <style>
    /* جعل الصفحة بأكملها تدعم الاتجاه من اليمين إلى اليسار */
    .stApp { 
        background-color: #0B1F19; 
        color: #FFFFFF; 
        direction: rtl; 
        text-align: right; 
    }
    
    /* ضبط القائمة الجانبية لتظهر بالاتجاه الصحيح */
    [data-testid="stSidebar"] { 
        background-color: #071410; 
        direction: rtl;
    }
    
    /* تنسيق العناوين والنصوص */
    h1 { 
        color: #D4AF37; 
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); 
        font-family: 'Segoe UI', sans-serif; 
        text-align: center; 
    }
    h3 { 
        color: #D4AF37; 
        text-align: right;
    }
    
    /* تنسيق صناديق المحتوى والبطاقات */
    .stContentBlock { 
        background-color: #113025; 
        border: 1px solid #D4AF37; 
        border-radius: 10px; 
        padding: 20px; 
        font-size: 16px; 
        line-height: 1.8; 
        text-align: right;
    }
    .companion-card { 
        background-color: #113025; 
        border: 1px solid #23604A; 
        border-radius: 12px; 
        padding: 20px; 
        text-align: center; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.2); 
        min-height: 140px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
    }
    </style>
    """, unsafe_allow_html=True)
# القائمة الجانبية الرسمية للمدرسة
with st.sidebar:
    st.markdown("<h1 style='color: #D4AF37;'>مِشْكَاة السِّيَر</h1>", unsafe_allow_html=True)
    st.write("منصة تفاعلية رقمية تحكي قصص وسير الصحابة الكرام وأدوارهم التاريخية .")
    st.divider()
    st.markdown("<p style='color: #D4AF37; font-weight: bold;'>الطالبة:</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px;'>ليان هاني</p>", unsafe_allow_html=True) 
    st.divider()
    st.markdown("<p style='color: #D4AF37; font-weight: bold;'>بإشراف المعلمة:</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px;'>أ.رجاء عبدالله</p>", unsafe_allow_html=True) 
    st.divider()
    st.write("**المادة:** الحديث الشريف")
    st.write("**الصف:** الاول ثانوي")

st.markdown("<h1>سِيَر: قصص الصحابة الكرام</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #A4C2B7;'>انقري إحدى البطاقات الجاهزة أو ابحثي عن أي صحابي في الأسفل للاستماع إلى قصته الشيقة </p>", unsafe_allow_html=True)
st.divider()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

try:
    model = genai.GenerativeModel('gemini-2.5-flash')

    companions = [
        {"name": "أبو هريرة رضي الله عنه", "title": "حافظ الأمة", "id": "abu_hurairah"},
        {"name": "عائشة بنت أبي بكر رضي الله عنهما", "title": "فقيهة النساء", "id": "aisha"},
        {"name": "حمزة بن عبد المطلب رضي الله عنه", "title": "أسد الله وسيد الشهداء", "id": "hamzah"},
        {"name": "خالد بن الوليد رضي الله عنه", "title": "سيف الله المسلول", "id": "khalid"},
        {"name": "عبد الله بن عمر رضي الله عنهما", "title": "المتَّبع للأثر", "id": "ibn_umar"},
        {"name": "أنس بن مالك رضي الله عنه", "title": "خادم الرسول ﷺ", "id": "anas"}
    ]

    if "search_target" not in st.session_state:
        st.session_state.search_target = None

    rows = [companions[0:3], companions[3:6]]
    for row in rows:
        cols = st.columns(3)
        for idx, companion in enumerate(row):
            with cols[idx]:
                st.markdown(f"""
                <div class="companion-card">
                    <h3 style='margin-bottom: 5px; font-size: 20px;'>{companion['name']}</h3>
                    <p style='color: #A4C2B7; font-style: italic; margin-bottom: 15px;'>{companion['title']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"اقرأ القصة", key=companion['id'], use_container_width=True):
                    st.session_state.search_target = companion['name']

    st.write("")
    st.divider()
    
    st.markdown("###  ابحثي عن صحابي آخر:")
    custom_name = st.text_input("اكتبي اسم أي صحابي أو صحابية هنا (مثال: سلمان الفارسي، خديجة بنت خويلد، بلال بن رباح...):")
    
    if st.button(" توليد القصة للصحابي المكتوب", use_container_width=True):
        if custom_name.strip() != "":
            st.session_state.search_target = custom_name
        else:
            st.warning("الرجاء كتابة اسم الصحابي أولاً في الخانة.")

    # عرض قصة الصحابي المحدد ديناميكياً (سواء من البطاقات أو من البحث الحر)
    if st.session_state.search_target:
        st.divider()
        st.markdown(f"###  الرواية والقصة الكاملة لـ: {st.session_state.search_target}")
        
        with st.spinner("جاري صياغة الأحداث والمواقف التاريخية ..."):
            story_prompt = (
                f"أنت راوٍ بارع ومؤرخ تاريخي إسلامي. احكِ قصة شيقة ومؤثرة وملهمة ومناسبة لطلاب الثانوية عن الصحابي: {st.session_state.search_target}.\n\n"
                f"يجب أن تُصاغ القصة كـ رواية سردية متكاملة وممتعة تحتوي على:\n"
                f"1. مقدمة قصصية تصف البيئة أو الموقف المثير في حياته وعمله أو لحظة إسلامه.\n"
                f"2. نقطة التحول والموقف البطولي الأبرز أو ميزته التنافسية الكبرى التي خلّدها التاريخ (مثل مواقفه العسكرية، أو شغفه الفائق بالحفظ ورواية الحديث عن النبي ﷺ).\n"
                f"3. العبرة المستفادة من هذه القصة والملخص التاريخي لحياته في نقاط مقتضبة بآخر القصة.\n\n"
                f"اجعل الأسلوب سردياً مشوقاً وجاذباً جداً لغوياً وبصرياً، مع الابتعاد تماماً عن الجداول الجافة، والالتزام بالحقائق التاريخية الموثقة."
            )
            
            response = model.generate_content(story_prompt)
            
            st.markdown(f"<div class='stContentBlock'>{response.text}</div>", unsafe_allow_html=True)
            
            st.write("")
            pdf_bytes = create_pdf(response.text)
            st.download_button(
                label=f" تحميل قصة {st.session_state.search_target} كملف PDF",
                data=pdf_bytes,
                file_name=f"Story_{st.session_state.search_target}.pdf",
                mime="application/pdf"
            )

except Exception as e:
    st.error(f"Technical Hint: {e}")
