import streamlit as st
import requests

# Sayfa Başlığı
st.set_page_config(page_title="GÜRai Atölye", page_icon="🤖")
st.title("🤖 GÜRai - Kesin Çözüm")

# O elindeki "AQ." ile başlayan uzun kodu buraya yapıştır
# Not: Bu kod yaklaşık 1 saat çalışır, sonra yenilemen gerekir.
TOKEN = "AQ.Ab8RN6KswCKHhSH2tH0nSWE9xnvGBpI1iBdK_S7gAFzuy33dew"
def gurai_cevap_ver(soru):
    # Google'ın ana kapısı (REST API)
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    # AQ kodları 'Bearer' başlığıyla gönderilir
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{"parts": [{"text": soru}]}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Hata: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Sistem hatası: {str(e)}"

# --- Arayüz ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("GÜRai'ye yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        cevap = gurai_cevap_ver(prompt)
        st.markdown(cevap)
        st.session_state.messages.append({"role": "assistant", "content": cevap})
