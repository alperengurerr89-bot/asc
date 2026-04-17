import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GÜRai", page_icon="🤖")
st.title("🤖 GÜRai - Son Kilidi Açıyoruz")

# DİKKAT: Buraya yapıştıracağın kod AIzaSy ile başlamalı!
# Örnek: "AIzaSyB1234567890-abcdefgh" gibi uzun bir şey olmalı.
API_KEY = "AQ.Ab8RN6L2uglN_2RNxE5JancJEfRDU4_f2CrJlzq6iNWyzjEaKg"

def gurai_calistir():
    try:
        # transport='rest' parametresi Unauthenticated hatalarını çözebilir
        genai.configure(api_key=API_KEY.strip(), transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Kurulum Hatası: {e}")
        return None

model = gurai_calistir()

if prompt := st.chat_input("Hadi, bu sefer konuş benimle..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Unauthenticated hatası tam burada patlıyordu:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error("❌ Anahtar Reddedildi!")
            st.warning("Girdiğin anahtar yanlış veya süresi dolmuş. Lütfen AI Studio'da anahtarın yanındaki kare (copy) simgesine basıp yeniden yapıştır.")
