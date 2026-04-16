import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GÜRai Dedektif", page_icon="🕵️")
st.title("🕵️ GÜRai - Model Dedektifi")

if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# --- 2. ADIM: SOHBET ---
if prompt := st.chat_input("GÜRai'ye bir mesaj gönder..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Üretim Hatası: {e}")
