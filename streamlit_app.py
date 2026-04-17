import streamlit as st
import google.generativeai as genai

# Anahtarlarını buraya eksiksiz yapıştır
API_KEYS = [
    "AQ.Ab8RN6LZEbAIPR5Ui00yx94fo_CyaDavmCOtkycNFa-TD83tjQ", 
    "AQ.Ab8RN6KQS4CKzvRGKPdLhF0MyhS4F_X2U2pizq_f8epqVOvG-w", 
    "AQ.Ab8RN6KBe-8sOzW8_gFgsLxUJzdLOdRTMWkvZKqqNaTnt1yYqw", 
    "AQ.Ab8RN6KxerVobF7Ypxibx2_OE4eeCdxaAvv0356HoKKZmoptvg", 
    "AQ.Ab8RN6LnRJdb6cgjap5T0ka_h27886xje4_hCSskJFaKar0elg"
]

def generate_with_rest_api(user_prompt):
    for i, key in enumerate(API_KEYS):
        if "ANAHTAR_" in key or len(key) < 10:
            continue
            
        # Doğrudan Google'ın kapısına gidiyoruz (Kütüphane kullanmadan)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key.strip()}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": user_prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            # Eğer cevap geldiyse
            if response.status_code == 200:
                return result['candidates'][0]['content']['parts'][0]['text'], i + 1
            else:
                # Hatayı buraya yazdıralım ki ne olduğunu görelim
                error_msg = result.get('error', {}).get('message', 'Bilinmeyen Hata')
                print(f"Anahtar {i+1} Hatası: {error_msg}")
                continue
        except Exception as e:
            continue
            
    return None, None

# --- Arayüz ---
st.title("🤖 GÜRai Atölye (Kurtarma Modu)")

if prompt := st.chat_input("GÜRai'ye sor..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        cevap, aktif_no = generate_with_rest_api(prompt)
        if cevap:
            st.markdown(cevap)
            st.caption(f"Aktif Hat: {aktif_no} (REST Modu)")
        else:
            st.error("Hala bağlantı kurulamıyor. Anahtarları Google AI Studio'dan tekrar kopyalamayı dene.")
