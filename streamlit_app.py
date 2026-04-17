import streamlit as st
import google.generativeai as genai

# Senin 5 anahtarını buraya liste olarak ekliyoruz
API_KEYS = [
    "AQ.Ab8RN6LZEbAIPR5Ui00yx94fo_CyaDavmCOtkycNFa-TD83tjQ", 
    "AQ.Ab8RN6KQS4CKzvRGKPdLhF0MyhS4F_X2U2pizq_f8epqVOvG-w", 
    "AQ.Ab8RN6KBe-8sOzW8_gFgsLxUJzdLOdRTMWkvZKqqNaTnt1yYqw", 
    "AQ.Ab8RN6KxerVobF7Ypxibx2_OE4eeCdxaAvv0356HoKKZmoptvg", 
    "AQ.Ab8RN6LnRJdb6cgjap5T0ka_h27886xje4_hCSskJFaKar0elg"
]

def generate_with_fallback(prompt):
    # Sırayla her anahtarı dener
    for key in API_KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception:
            # Eğer bu anahtar hata verirse (kota bittiyse vb.), bir sonrakine geçer
            continue
    return "Maalesef tüm anahtarların kotası dolmuş. Lütfen biraz bekleyin."

# --- Streamlit Arayüzü ---
st.title("GÜRai: 5 Kat Güçlü Yapay Zeka")

if prompt := st.chat_input("GÜRai'ye sor..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("GÜRai anahtarları kontrol ediyor..."):
            cevap = generate_with_fallback(prompt)
            st.markdown(cevap)
