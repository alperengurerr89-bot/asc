import streamlit as st
import google.generativeai as genai

# Sayfa Yapısı
st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai")

# 1. Anahtarı Bağla
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
    # En sağlam model ismi
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Lütfen Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# 2. Sohbet Sistemi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("GÜRai'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")
