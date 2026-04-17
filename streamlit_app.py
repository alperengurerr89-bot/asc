import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="GÜRai x Copilot", page_icon="🚀")
st.title("🚀 GÜRai - Copilot Gücüyle")

# OpenAI anahtarın (sk-... ile başlayan)
client = OpenAI(api_key="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")

if prompt := st.chat_input("Copilot modunda GÜRai'ye sor..."):
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o", # En hızlı ve yeni model
            messages=[{"role": "user", "content": prompt}]
        )
        cevap = response.choices[0].message.content
        st.markdown(cevap)
