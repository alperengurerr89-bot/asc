import streamlit as st
import google.generativeai as genai

# Kare simgesine basıp kopyaladığın o UZUN kodu buraya yapıştır
# Başı AIzaSy ile başlar, yaklaşık 40 karakterdir.
API_KEY = "AQ.Ab8RN6L2uglN_2RNxE5JancJEfRDU4_f2CrJlzq6iNWyzjEaKg"

def gurai_uyandir():
    try:
        # 'rest' modu senin bağlantı sorunlarını çözer
        genai.configure(api_key=API_KEY.strip(), transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Test mesajı gönderelim
        response = model.generate_content("Merhaba, çalışıyor musun?")
        return model, response.text
    except Exception as e:
        return None, str(e)

st.title("🤖 GÜRai - Son Durum")

model, mesaj = gurai_uyandir()

if model:
    st.success("✅ GÜRai Bağlandı! İlk Mesaj: " + mesaj)
    if prompt := st.chat_input("Hadi bir şey sor..."):
        res = model.generate_content(prompt)
        st.write(res.text)
else:
    st.error(f"❌ Hala Bağlanamadı. Hata: {mesaj}")
    st.info("Kare simgesine bastığından ve Google Translate'in KAPALI olduğundan emin ol.")
        cevap = gurai_cevap_ver(prompt)
        st.markdown(cevap)
