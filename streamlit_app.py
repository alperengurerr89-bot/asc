import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR VE GÜVENLİK ---
try:
    # Boşluklar burada çok önemli (4 boşluk içerde)
    if "GEMINI_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_KEY"]
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("Lütfen Secrets kısmına GEMINI_KEY ekleyin.")
        st.stop()
except Exception as e:
    st.error(f"Başlatma hatası: {e}")
    st.stop()

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai")
st.caption("Yapay Zeka Destekli Kişisel Asistan")

# --- 3. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. KULLANICI GİRDİSİ VE CEVAP ---
if prompt := st.chat_input("GÜRai'ye bir şeyler sor..."):
    # Kullanıcının mesajını göster ve kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # GÜRai'nin cevabını oluştur
    with st.chat_message("assistant"):
        try:
            # GÜRai'ye karakter veriyoruz
            full_prompt = f"Senin adın GÜRai. Zeki ve yardımsever bir asistansın. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            
            answer = response.text
            st.markdown(answer)
            
            # Cevabı geçmişe kaydet
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Cevap oluşturulurken hata çıktı: {e}")
