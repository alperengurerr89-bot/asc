import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai v4.0")

# 1. Anahtar Bağlantısı
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("Secrets kısmına GEMINI_KEY ekleyin.")
    st.stop()

# 2. Çalışan Modeli Otomatik Bulma (Kritik Bölge)
@st.cache_resource # Modeli bir kez bulup hafızada tutar
def find_working_model():
    # Google'ın kabul edebileceği tüm isim varyasyonları
    test_list = [
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro',
        'gemini-1.0-pro'
    ]
    for m in test_list:
        try:
            model_test = genai.GenerativeModel(m)
            # Küçük bir test mesajı gönderiyoruz
            model_test.generate_content("test") 
            return m # Eğer hata vermezse çalışan model budur!
        except:
            continue
    return None

# Modeli belirle
active_model_name = find_working_model()

if active_model_name:
    model = genai.GenerativeModel(active_model_name)
    st.success(f"Bağlantı Başarılı! Aktif Model: {active_model_name}")
else:
    st.error("⚠️ HATA: Google hesabın şu an hiçbir modele izin vermiyor.")
    st.info("Lütfen Google AI Studio'da başka bir Gmail hesabı ile anahtar almayı dene.")
    st.stop()

# 3. Sohbet Kısmı
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("GÜRai seninle..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Cevap üretilemedi: {e}")
