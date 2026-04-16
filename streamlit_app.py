import streamlit as st
import google.generativeai as genai

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="GÜRai", page_icon="🛠️")
st.title("🛠️ GÜRai")

# --- 1. API BAĞLANTISI ---
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("Lütfen Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# --- 2. ÇALIŞAN MODELİ BULMA (DEDEKTİF) ---
@st.cache_resource
def get_model():
    # Sistemdeki tüm varyasyonları deniyoruz
    denenecek_modeller = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro', 'gemini-1.0-pro']
    
    for m_ad in denenecek_modeller:
        try:
            test_model = genai.GenerativeModel(
                model_name=m_ad,
                system_instruction="Senin adın GÜRai. Elektronik, lehimleme, Arduino, DC motorlar ve DIY projeleri konusunda uzmansın. Teknik ve net cevaplar ver."
            )
            # Modeli test etmek için çok kısa bir istek
            test_model.generate_content("t")
            return test_model
        except Exception:
            continue
    return None

model = get_model()

if model is None:
    st.error("❌ Google hesabınız şu an hiçbir modele izin vermiyor. Lütfen farklı bir Gmail hesabı ile yeni bir anahtar alın.")
    st.stop()

# --- 3. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CEVAP ÜRETİMİ VE KOTA KONTROLÜ ---
if prompt := st.chat_input("Bir mesaj yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            error_msg = str(e)
            # Kota aşımı kontrolü (429 Hatası)
            if "429" in error_msg:
                if "quota" in error_msg.lower():
                    st.error("🚫 Günlük kullanım kotası doldu. Lütfen daha sonra tekrar deneyin veya farklı bir API anahtarı kullanın.")
                else:
                    st.warning("⏱️ Dakikalık işlem sınırı aşıldı. Lütfen yaklaşık 30 saniye bekleyip tekrar deneyin.")
            # Model bulunamadı kontrolü (404 Hatası)
            elif "404" in error_msg:
                st.error("🔎 Seçilen modele şu an ulaşılamıyor. Lütfen API anahtarınızı veya model adını kontrol edin.")
            # Diğer tüm hatalar
            else:
                st.error("⚠️ Bir bağlantı sorunu oluştu. Lütfen sayfayı yenileyip tekrar deneyin.")
