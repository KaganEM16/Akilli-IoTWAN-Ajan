import sys
import os
import streamlit as st
import pandas as pd
import json

# Path ayarları
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(src_dir)

from data_handler.db_manager import DBManager

# Sayfa Ayarları
st.set_page_config(page_title="🤖 Akıllı IoT Dashboard", layout="wide")
db = DBManager()

# --- YARDIMCI FONKSİYONLAR ---
def get_status_info(temp):
    """Sıcaklığa göre durum, renk ve bar genişliği döndürür."""
    if temp < 28:
        return "🟢 Güvenli", "green", "30%"
    elif 28 <= temp < 35:
        return "🟡 Dikkat", "orange", "65%"
    else:
        return "🔴 Tehlike", "red", "100%"

st.title("🤖 Akıllı IoT Görev Ajanı Dashboard")

# Veri tabanından son verileri çek
raw_data = db.fetch_recent(limit=50)

# --- DURUM BARI (STATUS BAR) ---
st.subheader("📊 Anlık Sistem Sağlık Durumu")
if raw_data and len(raw_data) > 0:
    # Veri tabanındaki en son kaydın sıcaklığını al
    last_temp = raw_data[0][1] 
    status_text, color, bar_width = get_status_info(last_temp)
    
    st.write(f"Mevcut Durum: **{status_text}** ({last_temp} °C)")
    
    # HTML/CSS ile Özel Progress Bar
    st.markdown(f"""
        <div style="width: 100%; background-color: #f0f2f6; border-radius: 10px; border: 1px solid #ddd;">
            <div style="width: {bar_width}; 
                        background-color: {color}; 
                        height: 25px; 
                        border-radius: 10px;
                        transition: width 0.8s ease-in-out;">
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("💡 Durum analizi için veri bekleniyor. Lütfen 'test_gonderici.py' dosyasını çalıştırın.")

st.divider()

# --- SEKMELER ---
tab1, tab2 = st.tabs(["📈 Canlı Veri İzleme", "📄 Geçmiş Analiz Raporları"])

with tab1:
    if raw_data and len(raw_data) > 0:
        # DataFrame oluştur (Toz sütunu dahil 5 sütun)
        df = pd.DataFrame(raw_data, columns=["Zaman", "Sıcaklık", "Nem", "AQI", "Toz"])
        df['Zaman'] = pd.to_datetime(df['Zaman'])
        
        # Üst Metrikler
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Sıcaklık", f"{df.iloc[0]['Sıcaklık']} °C")
        m2.metric("Nem", f"%{df.iloc[0]['Nem']}")
        m3.metric("Hava Kalitesi", f"{df.iloc[0]['AQI']} AQI")
        m4.metric("Toz (PM2.5)", f"{df.iloc[0]['Toz']} µg/m³")
        
        st.divider()
        st.subheader("Sensör Değişim Grafiği")
        # Grafiği çiz
        st.line_chart(df.set_index("Zaman")[["Sıcaklık", "Nem", "Toz"]])
    else:
        st.warning("⚠️ Grafik oluşturmak için henüz yeterli veri yok.")

with tab2:
    st.subheader("📂 Kayıtlı Analiz Raporları Arşivi")
    report_dir = os.path.join(os.path.dirname(src_dir), "agent_reports")
    
    if os.path.exists(report_dir):
        files = [f for f in os.listdir(report_dir) if f.endswith(".json")]
        files.sort(reverse=True)
        
        if files:
            selected_file = st.selectbox("Rapor Seçin:", files)
            with open(os.path.join(report_dir, selected_file), "r", encoding="utf-8") as f:
                content = json.load(f)
            
            st.divider()
            st.chat_message("assistant").write(content.get("report"))
            st.caption(f"📅 Rapor Tarihi: {content.get('date') or content.get('timestamp')}")
        else:
            st.info("💡 Henüz bir rapor oluşturulmadı.")
    else:
        st.error("❌ Rapor klasörü bulunamadı.")
