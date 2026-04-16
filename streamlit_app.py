import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="GÜRai", page_icon="🪄")

if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip().replace('"', '').replace("'", "")
    genai.configure(api_key=api_key)
else:
    st.error("Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# --- 2. MODEL SEÇİCİ (Hata Çözücü) ---
# Burada sırayla en çok çalışan modelleri listeliyoruz
model_listesi = ['gemini-1.5-pro', 'gemini-1.0-pro', 'models/gemini-1.5-flash', 'models/gemini-pro']

def cevap_uret(prompt):
    # Bu döngü, çalışan bir model bulana kadar hepsini tek tek dener
    for model_adi in model_listesi:
        try:
            model = genai.GenerativeModel(model_adi)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            continue # Bu model çalışmadıysa sonrakine geç
    return "Maalesef şu an hiçbir modele bağlanamadım. Lütfen anahtarınızı Google AI Studio'dan kontrol edin."

# --- 3. ARAYÜZ ---
st.title("🪄 GÜRai v2.0")

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
        with st.spinner("Modeller taranıyor ve cevap üretiliyor..."):
            cevap = cevap_uret(prompt)
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})
