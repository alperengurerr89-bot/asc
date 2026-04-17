import streamlit as st
import requests
import json

st.set_page_config(page_title="GÜRai", page_icon="🤖")
st.title("🤖 GÜRai - Son Çare Modu")

# Elindeki o AQ ile başlayan uzun metni buraya yapıştır
# Kopyaladığın metnin tamamını tırnak içine koy
TOKEN = "AQ.Ab8RN6LkwcuDwfM--InRjfTd2r3GESAAKtnW5qW9F97dxo_n6w"

def gurai_cevap_ver(soru):
    # Google'ın ham veri kapısı
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    headers = {
        "Authorization": f"Bearer {TOKEN.strip()}",
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{"parts": [{"text": soru}]}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 401:
            return "❌ Hata: Token süresi dolmuş. Sayfayı yenileyip yeni bir AQ kodu almalısın."
        else:
            return f"⚠️ Hata {response.status_code}: {response.text}"
    except Exception as e:
        return f"Sistem hatası: {str(e)}"

# Arayüz
if prompt := st.chat_input("GÜRai'ye bir şey sor..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        cevap = gurai_cevap_ver(prompt)
        st.markdown(cevap)
