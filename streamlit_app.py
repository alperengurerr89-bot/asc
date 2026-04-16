import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai v3.0")

# --- 1. GÜVENLİK ---
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# --- 2. ÇALIŞAN MODELİ BULMA FONKSİYONU ---
def get_working_model(user_prompt):
    # En çok çalışan isimden en az çalışana doğru liste
    denenecek_modeller = [
        'gemini-1.5-flash',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    for m_ad in denenecek_modeller:
        try:
            test_model = genai.GenerativeModel(m_ad)
            res = test_model.generate_content(user_prompt)
            return res.text, m_ad # Çalışan modeli ve cevabı döndür
        except Exception:
            continue # Hata verirse bir sonrakine geç
            
    return None, None

# --- 3. SOHBET ARA YÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("GÜRai'ye yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Modeller taranıyor..."):
            cevap, aktif_model = get_working_model(prompt)
            
            if cevap:
                st.markdown(cevap)
                st.session_state.messages.append({"role": "assistant", "content": cevap})
                # Hangi modelin çalıştığını merak ediyorsan altta görebilirsin
                st.caption(f"Aktif Model: {aktif_model}")
            else:
                st.error("Maalesef şu an hiçbir modele ulaşılamıyor. Lütfen API anahtarınızı Google AI Studio'dan yenileyin.")
