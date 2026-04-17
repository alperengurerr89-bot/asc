import streamlit as st
import google.generativeai as genai

# Sayfa Yapılandırması
st.set_page_config(page_title="GÜRai Atölye", page_icon="🤖")
st.title("🤖 GÜRai - Canlı")

# BURAYA DİKKAT: Anahtarını tırnak içine yapıştır
# Eğer AIzaSy ile başlıyorsa sorunsuz çalışacaktır
API_KEY = "AQ.Ab8RN6L2uglN_2RNxE5JancJEfRDU4_f2CrJlzq6iNWyzjEaKg"

def gurai_cevap_ver(soru):
    try:
        genai.configure(api_key=API_KEY.strip())
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(soru)
        return response.text
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# --- Arayüz Kısmı ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi ve cevap üretme
if prompt := st.chat_input("GÜRai'ye yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Buradaki girintiler (boşluklar) hayati önem taşır!
        cevap = gurai_cevap_ver(prompt)
        st.markdown(cevap)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
