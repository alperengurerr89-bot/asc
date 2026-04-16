import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai")

# Anahtarı çekiyoruz
if "GEMINI_KEY" in st.secrets:
    # .strip() ile görünmez boşlukları siliyoruz
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("Secrets ayarı yapılamadı!")
    st.stop()

# Model tanımlama
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("GÜRai'ye yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Doğrudan cevap üret
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata: {e}")
