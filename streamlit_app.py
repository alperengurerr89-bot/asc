import streamlit as st
import google.generativeai as genai

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="GÜRai Ultra", page_icon="🛠️")
st.title("🛠️ GÜRai: Beşli Güç Sistemi")

# --- 1. OTOMATİK ANAHTAR DÖNGÜSÜ ---
def initialize_engine():
    # 5 anahtarı da listeye alıyoruz
    available_keys = [
        st.secrets.get("GEMINI_KEY"),
        st.secrets.get("GEMINI_KEY_2"),
        st.secrets.get("GEMINI_KEY_3"),
        st.secrets.get("GEMINI_KEY_4"),
        st.secrets.get("GEMINI_KEY_5")
    ]
    
    # Boş olmayanları filtrele
    valid_keys = [k for k in available_keys if k]

    for key in valid_keys:
        try:
            genai.configure(api_key=key.strip())
            # En kararlı modeli seçiyoruz
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction="Senin adın GÜRai. Elektronik ve DIY projeleri uzmanısın."
            )
            # Anahtarın çalışıp çalışmadığını 1 harflik testle kontrol et
            model.generate_content("t")
            return model # Çalışan ilk anahtarı bulduk ve döndürdük
        except Exception:
            continue # Bu anahtar patlamış, sıradakine bak
            
    return None

model = initialize_engine()

# --- 2. HATA YÖNETİMİ ---
if model is None:
    st.error("🚫 Tüm 5 anahtarın da günlük kotası doldu. Yarın veya yeni anahtarlarla tekrar deneyin.")
    st.stop()

# --- 3. SOHBET ARA YÜZÜ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("GÜRai'ye sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ Mevcut anahtarın kotası az önce bitti. Lütfen sayfayı yenileyerek yedek anahtara geçiş yapın.")
            else:
                st.error("⚠️ Bir bağlantı sorunu oluştu.")
