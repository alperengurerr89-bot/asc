import streamlit as st
import google.generativeai as genai

# Sayfa Konfigürasyonu (Tarayıcı sekmesindeki isim ve ikon)
st.set_page_config(page_title="GÜRai Atölye", page_icon="🤖", layout="centered")

# GÜRai Tasarımı (CSS ile fütüristik görünüm)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        color: #00d4ff;
    }
    h1 {
        color: #00d4ff;
        text-align: center;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("GÜRai: Yeni Nesil Yapay Zeka")

# API Anahtarı Ayarı (Kendi anahtarını buraya ekle)
# genai.configure(api_key="SENIN_API_ANAHTARIN")

# Model Ayarları
model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda tut (Farklı tarayıcı oturumları için)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan soru al
if prompt := st.chat_input("GÜRai'ye bir soru sor (Matematik, Kod, Elektronik...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Yapay zekadan cevap al
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
        except Exception as e:
            # Hata durumunda (Kota veya teknik sorun) kullanıcıya bilgi ver
            full_response = "Sistem şu an çok yoğun veya kota sınırında. Lütfen biraz bekleyip tekrar dene."
            message_placeholder.error(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
