import streamlit as st
import google.generativeai as genai

# Anahtarlarını buraya eksiksiz yapıştır
API_KEYS = [
    "AQ.Ab8RN6LZEbAIPR5Ui00yx94fo_CyaDavmCOtkycNFa-TD83tjQ", 
    "AQ.Ab8RN6KQS4CKzvRGKPdLhF0MyhS4F_X2U2pizq_f8epqVOvG-w", 
    "AQ.Ab8RN6KBe-8sOzW8_gFgsLxUJzdLOdRTMWkvZKqqNaTnt1yYqw", 
    "AQ.Ab8RN6KxerVobF7Ypxibx2_OE4eeCdxaAvv0356HoKKZmoptvg", 
    "AQ.Ab8RN6LnRJdb6cgjap5T0ka_h27886xje4_hCSskJFaKar0elg"
]

# --- 1. FONKSİYON: ANAHTARLARI SIRAYLA DENEYEN MEKANİZMA ---
def generate_with_fallback(user_prompt):
    for i, key in enumerate(API_KEYS):
        if "ANAHTAR_" in key or len(key) < 10:
            continue
            
        try:
            # ÖNEMLİ: transport='rest' ekleyerek OAuth hatasını devre dışı bırakıyoruz
            genai.configure(api_key=key.strip(), transport='rest') 
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(user_prompt)
            
            if response and response.text:
                return response.text, i + 1
                
        except Exception as e:
            st.warning(f"Sistem Notu (Anahtar {i+1}): {str(e)}")
            continue
    
    return None, None
# --- 2. ARAYÜZ VE SOHBET GEÇMİŞİ ---
st.title("🤖 GÜRai Atölye")

# Mesaj geçmişini başlat (Hafıza)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. KULLANICI GİRİŞİ VE CEVAPLAMA ---
if prompt := st.chat_input("GÜRai'ye bir soru sor..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # GÜRai cevabını oluştur
    with st.chat_message("assistant"):
        with st.spinner("GÜRai veri tabanına bağlanıyor..."):
            cevap, aktif_no = generate_with_fallback(prompt)
            
            if cevap:
                st.markdown(cevap)
                st.caption(f"⚡ Kaynak: Hat {aktif_no}")
                st.session_state.messages.append({"role": "assistant", "content": cevap})
            else:
                # Tüm anahtarlar çökerse bu mesaj çıkar
                st.error("Görünüşe göre tüm yollar kapalı.")
                st.info("💡 ÇÖZÜM: Bilgisayarı telefonunun mobil verisine bağla ve sayfayı yenile!")
