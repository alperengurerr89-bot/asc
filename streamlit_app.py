import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GÜRai", page_icon="🛠️")
st.title("🛠️ GÜRai (Yedekli Sistem)")

# --- ANAHTARLARI KONTROL ET VE BAĞLAN ---
def connect_to_genai():
    # Mevcut tüm anahtarları listeye al
    keys = []
    if "GEMINI_KEY" in st.secrets:
        keys.append(st.secrets["GEMINI_KEY"])
    if "GEMINI_KEY_2" in st.secrets:
        keys.append(st.secrets["GEMINI_KEY_2"])
    
    for key in keys:
        try:
            genai.configure(api_key=key.strip())
            # En sağlam model ismini dene
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="Senin adın GÜRai. Elektronik ve DIY projeleri uzmanısın."
            )
            # Test isteği (Kota dolup dolmadığını anlamak için)
            model.generate_content("t")
            return model # Çalışan anahtarı bulduk!
        except Exception:
            continue # Bu anahtar hatalı veya kotası dolmuş, sıradakine geç
    return None

model = connect_to_genai()

if model is None:
    st.error("🚫 Tüm API anahtarlarının günlük kotası doldu. Lütfen yarın tekrar deneyin.")
    st.stop()

# --- SOHBET SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
            if "429" in str(e):
                st.error("🚫 Bu anahtarın da kotası doldu. Lütfen sayfayı yenileyin veya yarın deneyin.")
            else:
                st.error(f"Bağlantı hatası: {e}")
