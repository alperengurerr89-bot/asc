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

def generate_with_fallback(user_prompt):
    # Bu liste, anahtarları sırayla deneyecek
    for i, key in enumerate(API_KEYS):
        # Geçersiz veya boş anahtarları kontrol et
        if "ANAHTAR_" in key or len(key) < 10:
            continue
            
        try:
            # Mevcut anahtarı yapılandır
            genai.configure(api_key=key)
            
            # Kotaları daha geniş olan 1.5-flash modelini kullanıyoruz
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            # Cevabı almayı dene
            response = model.generate_content(user_prompt)
            
            # Eğer cevap başarılıysa metni ve hangi anahtarın çalıştığını döndür
            if response and response.text:
                return response.text, i + 1
                
except Exception as e:
            # Burası çok önemli! Hatayı ekrana yazdır ki ne olduğunu görelim:
            st.warning(f"Sistem Notu: Anahtar {i+1} şu hatayı verdi: {str(e)}")
            continue
    
    # Eğer döngü biter ve hiç cevap dönmezse None döndür
    return None, None

# --- Arayüz ve Sohbet Bölümü ---
st.title("🤖 GÜRai Atölye")

if prompt := st.chat_input("GÜRai'ye bir soru sor..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # Yukarıdaki fonksiyonu çağırıyoruz
        cevap, aktif_no = generate_with_fallback(prompt)
        
        if cevap:
            st.markdown(cevap)
            st.caption(f"Güç Kaynağı: Hat {aktif_no} aktif.")
        else:
            # Tüm anahtarlar başarısız olursa çıkacak mesaj
            st.error("Görünüşe göre tüm API anahtarlarının günlük sınırı dolmuş veya bir bağlantı sorunu var. Lütfen 15-20 dakika sonra tekrar dene.")
