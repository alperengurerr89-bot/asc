import streamlit as st
import google.generativeai as genai

# Sayfa Yapısı
st.set_page_config(page_title="GÜRai Donanım Asistanı", page_icon="🛠️")
st.title("🛠️ GÜRai: Maker Asistanı")

# 1. Anahtarı Bağla
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
    
    # GÜRai'ye Kimlik Tanımlıyoruz (System Instruction)
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Senin adın GÜRai. Elektronik, lehimleme, Arduino, DC motorlar ve DIY projeleri konusunda uzmansın. Kullanıcın bir 'maker'. Sorulara teknik ama anlaşılır cevaplar ver. Devre şemaları ve bileşen seçimleri konusunda yardımcı ol."
    )
else:
    st.error("Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# 2. Sohbet Sistemi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hangi proje üzerinde çalışıyoruz?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # GÜRai artık bir maker uzmanı gibi cevap verecek
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.warning("⏱️ Çok hızlı gidiyoruz! Google biraz beklememizi istiyor (30 sn).")
            else:
                st.error(f"Bağlantı Hatası: {e}")
