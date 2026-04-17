import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="GÜRai x Adobe Mode", page_icon="🎨")
st.title("🎨 GÜRai - Adobe Sanat Modu")

# O meşhur AIzaSy ile başlayan anahtarı buraya koy
API_KEY = "AQ.Ab8RN6L2uglN_2RNxE5JancJEfRDU4_f2CrJlzq6iNWyzjEaKg"

def gurai_setup():
    try:
        genai.configure(api_key=API_KEY.strip())
        # En güçlü model olan 1.5 Pro'yu deneyelim (Adobe kadar zekidir)
        model = genai.GenerativeModel('gemini-1.5-pro')
        return model
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

model = gurai_setup()

# Adobe tarzı 'Creative' bir başlangıç mesajı
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Selam Alperen! Adobe kalitesinde fikirler üretmeye hazır mısın?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Tasarım veya kod fikrini buraya yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            # Adobe gibi yaratıcı cevaplar vermesi için bir 'System Instruction' ekleyebilirsin
            response = model.generate_content(f"Bir sanat yönetmeni gibi cevap ver: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
