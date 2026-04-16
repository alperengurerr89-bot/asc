import streamlit as st
import google.generativeai as genai

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="GÜRai", page_icon="🛠️")
st.title("🛠️ GÜRai")

# --- 1. API BAĞLANTISI ---
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
    
    # Maker ve Elektronik odaklı sistem talimatı
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Senin adın GÜRai. Elektronik, lehimleme, Arduino, DC motorlar ve DIY projeleri konusunda uzmansın. Sorulara teknik ve net cevaplar ver. Devre şemaları ve bileşen seçimleri konusunda yardımcı ol."
    )
else:
    st.error("Lütfen Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# --- 2. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. KULLANICI GİRİŞİ VE CEVAP ÜRETİMİ ---
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
                if "quota" in error_msg.lower():
                    st.error("🚫 Günlük kullanım kotası doldu. Lütfen daha sonra tekrar deneyin veya farklı bir API anahtarı kullanın.")
                else:
                    st.warning("⏱️ Dakikalık işlem sınırı aşıldı. Lütfen yaklaşık 30 saniye bekleyip tekrar deneyin.")
            elif "404" in error_msg:
                st.error("🔎 Seçilen modele şu an ulaşılamıyor. Lütfen API anahtarınızı veya model adını kontrol edin.")
            else:
                st.error("⚠️ Bir bağlantı sorunu oluştu. Lütfen sayfayı yenileyip tekrar deneyin.")
