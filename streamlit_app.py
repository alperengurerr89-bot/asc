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

def generate_with_fallback(prompt):
    hatalar = []
    for i, key in enumerate(API_KEYS):
        # Anahtar boşsa veya tırnak içinde kalmışsa atla
        if "ANAHTAR_" in key or len(key) < 5:
            continue
            
        try:
            genai.configure(api_key=key)
            # Daha yüksek kotalı olan 'gemini-1.5-flash' modelini deniyoruz
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response.text, i + 1 # Başarılı anahtar nosunu da döndür
        except Exception as e:
            hatalar.append(f"Anahtar {i+1} Hatası: {str(e)}")
            continue
    
    # Eğer buraya kadar geldiyse hiçbir anahtar çalışmamıştır
    st.error("Detaylı Hata Raporu:")
    for h in hatal: st.write(h)
    return None, None

# --- Arayüz ---
st.title("🤖 GÜRai Atölye")

if prompt := st.chat_input("GÜRai'ye sor..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        cevap, aktif_no = generate_with_fallback(prompt)
        if cevap:
            st.success(f"GÜRai Aktif! (Kullanılan Güç: Anahtar {aktif_no})")
            st.markdown(cevap)
        else:
            st.warning("Görünüşe göre tüm yollar kapalı. Lütfen yukarıdaki hata raporuna bak.")
