import streamlit as st
import google.generativeai as genai

# --- 1. GÜVENLİK VE ANAHTAR AYARI ---
# Streamlit Secrets'tan anahtarı alıyoruz
if "GEMINI_KEY" in st.secrets:
    # Anahtarı tırnaklardan ve boşluklardan arındırarak alıyoruz
    api_key = st.secrets["GEMINI_KEY"].strip().replace('"', '').replace("'", "")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("🚨 HATA: Streamlit Secrets kısmında 'GEMINI_KEY' bulunamadı!")
    st.stop()

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai")
st.markdown("---")

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SORU VE CEVAP ---
if prompt := st.chat_input("GÜRai'ye sor..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # GÜRai cevap üretsin
    with st.chat_message("assistant"):
        try:
            # GÜRai'ye karakter tanımlıyoruz
            full_query = f"Senin adın GÜRai. Yardımsever bir yapay zekasın. Soru: {prompt}"
            response = model.generate_content(full_query)
            
            # Cevabı göster ve kaydet
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"⚠️ Bir sorun çıktı! Anahtarınızı kontrol edin.\nHata Detayı: {e}")
