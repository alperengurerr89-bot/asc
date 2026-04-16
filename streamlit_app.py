import streamlit as st
import google.generativeai as genai

# --- 1. ANAHTAR VE MODEL AYARI ---
if "GEMINI_KEY" in st.secrets:
    try:
        # Secrets'tan anahtarı al ve temizle
        api_key = st.secrets["GEMINI_KEY"].strip().replace('"', '').replace("'", "")
        genai.configure(api_key=api_key)
        
        # En stabil model ismini kullanıyoruz
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Kurulum hatası: {e}")
        st.stop()
else:
    st.error("🚨 Secrets kısmında GEMINI_KEY bulunamadı!")
    st.stop()

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai")
st.caption("Google Gemini Destekli Asistan")

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SORU VE CEVAP ---
if prompt := st.chat_input("GÜRai'ye sor..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # GÜRai cevap üretsin
    with st.chat_message("assistant"):
        try:
            # GÜRai'ye karakter tanımlıyoruz
            full_prompt = f"Senin adın GÜRai. Yardımsever bir yapay zekasın. Soru: {prompt}"
            response = model.generate_content(full_prompt)
            
            # Cevabı yazdır ve kaydet
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            # Eğer model ismiyle ilgili hala sorun çıkarsa alternatif modeli dene uyarısı
            st.error(f"⚠️ Bir sorun çıktı! Detay: {e}")
