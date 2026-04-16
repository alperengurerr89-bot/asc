import streamlit as st
import google.generativeai as genai

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="GÜRai", page_icon="🛠️")
st.title("🛠️ GÜRai")

# --- 1. API BAĞLANTISI ---
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("Lütfen Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# --- 2. ÇALIŞAN MODELİ BULMA ---
@st.cache_resource
def get_model():
    # En çok çalışan isimden en az çalışana doğru liste
    denenecek_modeller = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro', 'gemini-1.0-pro']
    
    for m_ad in denenecek_modeller:
        try:
            test_model = genai.GenerativeModel(
                model_name=m_ad,
                system_instruction="Senin adın GÜRai. Elektronik ve DIY projeleri konusunda uzmansın."
            )
            # Modeli test etmek için boş bir istek gönderiyoruz
            test_model.generate_content("test")
            return test_model
        except:
            continue
    return None

model = get_model()

if model is None:
    st.error("❌ Google hesabınız şu an hiçbir modele izin vermiyor. Lütfen farklı bir Gmail hesabı ile yeni bir anahtar alın.")
    st.stop()

# --- 3. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CEVAP ÜRETİMİ ---
if prompt := st.chat_input("Bir mesaj yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                st.error("🚫 Kullanım kotası doldu. Lütfen daha sonra tekrar deneyin.")
            else:
                st.error(f"Bağlantı sorunu: {e}")
