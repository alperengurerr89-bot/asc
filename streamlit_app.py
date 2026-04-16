import streamlit as st
import google.generativeai as genai

# Sayfa Ayarı
st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai")

# 1. Anahtarı Al
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Secrets ayarı eksik!")
    st.stop()

# 2. Modeli Tanımla
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Basit Sohbet Arayüzü
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
