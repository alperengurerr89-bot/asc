import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GÜRai", page_icon="🪄")
st.title("🪄 GÜRai")

# 1. Güvenlik ve Anahtar Yapılandırması
if "GEMINI_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_KEY"].strip()
    genai.configure(api_key=api_key)
else:
    st.error("Secrets kısmında GEMINI_KEY bulunamadı!")
    st.stop()

# 2. Esnek Model Tanımlama (404 Hatasını Geçmek İçin)
# Bazı sistemler 'models/' ön ekini zorunlu tutarken bazıları kabul etmez.
try:
    # En yeni ve en geniş kapsamlı model ismi
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    # Eğer hata verirse alternatif ismi dene
    model = genai.GenerativeModel('gemini-pro')

# 3. Sohbet Geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Soru ve Cevap
if prompt := st.chat_input("GÜRai'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Model isminde 404 almamak için generate_content'i doğrudan çağırıyoruz
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Hata devam ederse burası çalışacak
            st.error(f"Bağlantı Sorunu: {e}")
            st.info("İpucu: Eğer 404 devam ediyorsa, lütfen Google AI Studio'da anahtar aldığın projenin adını değiştirip yeni bir anahtar al.")
