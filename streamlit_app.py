import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GÜRai Dedektif", page_icon="🕵️")
st.title("🕵️ GÜRai - Model Dedektifi")

if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("Secrets kısmına GEMINI_KEY ekleyin!")
    st.stop()

# --- 1. ADIM: ÇALIŞAN MODELLERİ LİSTELE ---
@st.cache_resource
def get_available_models():
    models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)
        return models
    except Exception as e:
        st.error(f"Modeller listelenemedi: {e}")
        return []

st.write("🔎 Senin anahtarın için uygun olan modeller taranıyor...")
uygun_modeller = get_available_models()

if uygun_modeller:
    # Listede 'flash' veya 'pro' olanı bulmaya çalışalım
    secilen_model = uygun_modeller[0] # Varsayılan olarak ilkini seç
    for m in uygun_modeller:
        if 'gemini-1.5-flash' in m:
            secilen_model = m
            break
    
    st.success(f"✅ Başarılı! Şu modelle bağlanıyoruz: {secilen_model}")
    model = genai.GenerativeModel(secilen_model)
else:
    st.error("❌ Google hesabın şu an API üzerinden hiçbir modele erişim vermiyor.")
    st.info("Bu durum genellikle Google AI Studio'daki projenin 'Generative Language API' servisiyle tam eşleşmemesinden kaynaklanır.")
    st.stop()

# --- 2. ADIM: SOHBET ---
if prompt := st.chat_input("GÜRai'ye bir mesaj gönder..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Üretim Hatası: {e}")
