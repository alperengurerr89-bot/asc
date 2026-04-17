import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="GÜRai Atölye", page_icon="🤖")
st.title("🤖 GÜRai - Bearer Modu")

# --- TOKEN GİRİŞİ ---
# Elindeki AQ... ile başlayan o uzun tokenı buraya yapıştır
BEARER_TOKEN = "AQ.Ab8RN6KswCKHhSH2tH0nSWE9xnvGBpI1iBdK_S7gAFzuy33dew"
def gurai_sorgu(soru):
    # Google Gemini REST API adresi
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    # Bearer Token tam olarak bu şekilde başlıkta (headers) gönderilir
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN.strip()}",
        "Content-Type": "application/json"
    }
    
    # Gönderilecek veri paketi
    payload = {
        "contents": [
            {
                "parts": [{"text": soru}]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Cevabı parçala ve metni al
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 401:
            return "❌ Hata: Token süresi dolmuş veya geçersiz. Lütfen yeni bir AQ kodu al."
        else:
            return f"⚠️ Hata oluştu: {response.status_code}\n{response.text}"
            
    except Exception as e:
        return f"📡 Bağlantı hatası: {str(e)}"

# --- SOHBET ARAYÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmişi ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
if prompt := st.chat_input("GÜRai'ye bir mesaj yaz..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # GÜRai'den cevap al
    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            cevap = gurai_sorgu(prompt)
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
