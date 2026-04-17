import streamlit as st
import google.generativeai as genai

# Bu kod, bağlantı hatalarını (401/404) engellemek için tasarlandı
st.title("🤖 GÜRai - Kesin Bağlantı")

# Buraya kopyaladığın o uzun AIzaSy... kodunu yapıştır
API_KEY = "AQ.Ab8RN6L2uglN_2RNxE5JancJEfRDU4_f2CrJlzq6iNWyzjEaKg"

if API_KEY != "AQ.Ab8RN6L2uglN_2RNxE5JancJEfRDU4_f2CrJlzq6iNWyzjEaKg"
    try:
        # transport='rest' kullanarak 'Unauthenticated' hatasını bypass ediyoruz
        genai.configure(api_key=API_KEY.strip(), transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if prompt := st.chat_input("Yaz bakalım, GÜRai hazır mı?"):
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"Anahtar yine reddedildi: {e}")
else:
    st.warning("Lütfen tırnak içine API anahtarını yapıştır.")
