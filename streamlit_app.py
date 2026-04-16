import streamlit as st
import google.generativeai as genai

# Sayfa Yapısı
st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai - Son Deneme")

# 1. Anahtarı En Sade Halde Bağla
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
    # EN ÖNEMLİ SATIR: Sadece gemini-pro ismini kullanıyoruz (Flash değil)
    model = genai.GenerativeModel('gemini-pro') 
else:
    st.error("Secrets kısmına GEMINI_KEY ekle!")
    st.stop()

# 2. Mesajlaşma
if prompt := st.chat_input("GÜRai burada..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # v1beta yerine doğrudan v1 protokolünü zorla
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Hata Devam Ediyor: {e}")
            st.info("Eğer hala 404 veriyorsa, Streamlit panelinde sağ üstten 'Delete App' yapıp uygulamayı baştan kurmak gerekebilir. Bazen Streamlit sunucuları IP kısıtlamasına takılıyor.")
