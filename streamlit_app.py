import streamlit as st
import google.generativeai as genai

# --- 1. GÜVENLİK VE ANAHTAR KONTROLÜ ---
if "GEMINI_KEY" in st.secrets:
    try:
        # Anahtarı çek ve temizle
        api_key = st.secrets["GEMINI_KEY"].strip()
        genai.configure(api_key=api_key)
        
        # Modeli başlat (Hata alırsak aşağıda düzelteceğiz)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Başlatma hatası: {e}")
        st.stop()
else:
    st.error("🚨 Secrets kısmına GEMINI_KEY eklenmemiş!")
    st.stop()

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai")
st.caption("Gelişmiş Yapay Zeka Asistanı")

# --- 3. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. SORU VE CEVAP (404 HATASINI ÇÖZEN KISIM) ---
if prompt := st.chat_input("GÜRai'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Düşünüyorum..."):
            try:
                # Önce en güncel modeli dene
                try:
                    response = model.generate_content(prompt)
                except:
                    # Eğer 404 verirse 'models/' ön ekiyle zorla
                    temp_model = genai.GenerativeModel('models/gemini-1.5-flash')
                    response = temp_model.generate_content(prompt)
                
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error("⚠️ Bir sorun çıktı. Lütfen şunları yapın:")
                st.info("1. Google AI Studio'dan yepyeni bir anahtar alın.")
                st.info("2. Secrets kısmına yapıştırıp kaydedin.")
                st.info("3. Sağ alttan 'Reboot App' yapın.")
                st.write(f"Hata detayı: {e}")
