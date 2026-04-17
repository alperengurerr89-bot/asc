import streamlit as st
from openai import OpenAI

st.title("🚀 GÜRai - Güvenli Mod")

# Anahtarı kodun içine yazmıyoruz, Secrets'tan çekiyoruz
try:
    # Bu satır anahtarı otomatik olarak Streamlit ayarlarından alır
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if prompt := st.chat_input("GÜRai hazır, sor bakalım..."):
        st.chat_message("user").markdown(prompt)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        
        with st.chat_message("assistant"):
            st.markdown(response.choices[0].message.content)

except Exception as e:
    st.error(f"Hala 401 alıyorsan anahtarın aktif değildir: {e}")
