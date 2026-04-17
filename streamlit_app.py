import streamlit as st
from openai import OpenAI

# Sayfa Yapılandırması
st.set_page_config(page_title="GÜRai", page_icon="🚀")
st.title("🚀 GÜRai - Copilot Bağlantısı")

# Senin az önce paylaştığın yeni anahtar (Boşlukları temizleyerek)
API_KEY = "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".strip()

try:
    client = OpenAI(api_key=API_KEY)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("GÜRai'ye sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # En kararlı model olan gpt-3.5-turbo'yu deneyelim (Garanti olsun)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            cevap = response.choices[0].message.content
            st.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})

except Exception as e:
    st.error(f"❌ Bağlantı Hatası: {e}")
    if "401" in str(e):
        st.info("İpucu: OpenAI bu anahtarı 'geçersiz' sayıyor. Lütfen yeni bir anahtar al ve buraya yapıştırma, doğrudan koduna ekle.")
