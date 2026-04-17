import streamlit as st
from openai import OpenAI

# Sayfa tasarımı
st.set_page_config(page_title="GÜRai x OpenAI", page_icon="🚀")
st.title("🚀 GÜRai - Copilot Modu Aktif")

# ANAHTAR: Buraya sk- ile başlayan o uzun kodu hatasız yapıştır
API_KEY = "BURAYA_SK_ILE_BASLAYAN_ANAHTARI_YAPISTIR"

if "sk-" not in API_KEY:
    st.warning("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")
else:
    try:
        client = OpenAI(api_key=API_KEY.strip())
        
        # Sohbet geçmişini sakla
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Eski mesajları göster
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Kullanıcıdan soru al
        if prompt := st.chat_input("GÜRai'ye (OpenAI) bir şey sor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # En güncel ve hızlı model gpt-4o-mini (Hem ucuz hem hızlıdır)
                response = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    messages=[{"role": "user", "content": prompt}]
                )
                cevap = response.choices[0].message.content
                st.markdown(cevap)
                st.session_state.messages.append({"role": "assistant", "content": cevap})
                
    except Exception as e:
        # Hata türüne göre kullanıcıyı bilgilendir
        if "insufficient_quota" in str(e):
            st.error("❌ Hata: OpenAI hesabında bakiye bitmiş!")
        elif "invalid_api_key" in str(e):
            st.error("❌ Hata: Anahtar geçersiz, yanlış kopyalamış olabilirsin.")
        else:
            st.error(f"❌ Bir sorun oluştu: {e}")
