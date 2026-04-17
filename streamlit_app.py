import streamlit as st
from openai import OpenAI

# Proje Kimliği
st.set_page_config(page_title="GÜRai x OpenAI", page_icon="🚀", layout="wide")
st.title("🚀 GÜRai - Copilot Gücüyle Çalışıyor")

# Paylaştığın anahtarı buraya güvenli bir şekilde ekliyoruz
client = OpenAI(api_key="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")

# Sohbet geçmişi kontrolü
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selam Alperen! Copilot modunda GÜRai hazır. Ne yapıyoruz bugün?"}
    ]

# Mesajları ekrana çiz
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("GÜRai'ye (GPT-4o) bir şey sor..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt üretme
    with st.chat_message("assistant"):
        try:
            # En hızlı model olan gpt-4o-mini'yi kullanıyoruz
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Senin adın GÜRai. Alperen tarafından geliştirildin. Çok zeki, yardımsever ve biraz da esprili bir asistansın."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ]
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"⚠️ Bir hata oluştu: {str(e)}")
            if "insufficient_quota" in str(e):
                st.warning("Not: OpenAI hesabında bakiye/kredi bitmiş olabilir.")
