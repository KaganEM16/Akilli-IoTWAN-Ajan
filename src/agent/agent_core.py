from data_handler.db_manager import DBManager
from .llm_module import get_ai_advice
from .tools import save_report
import os

class IOTAgent:
    def __init__(self):
        self.db = DBManager()

    def run_analysis(self):
        print("🧠 Etmen analiz yapıyor...")
        data = self.db.fetch_recent(limit=10)
        
        if len(data) < 2:
            print("❌ Analiz için yeterli veri yok (En az 2 kayıt gerekli).")
            return
        
        now = data[0] # (Zaman, Sıcaklık, Nem, AQI, Toz)
        prev = data[1]
        
        t_diff = now[1] - prev[1]
        d_diff = now[4] - prev[4]
        
        analysis_summary = (
            f"GÜNCEL DURUM: Sıcaklık {now[1]}°C, Nem %{now[2]}, AQI {now[3]}, Toz {now[4]} µg/m³.\n"
            f"DEĞİŞİM: Sıcaklık {t_diff:+.1f}°C, Toz {d_diff:+.2f} µg/m³.\n"
            "Talimat: Alerji uyarılarını içeren, teknik tavsiyeler sunan çok uzun bir rapor yaz."
        )
        
        ai_advice = get_ai_advice(analysis_summary)
        # tools.py içindeki save_report fonksiyonu çağrılır
        save_report(ai_advice)
        print(f"📝 Rapor kaydedildi. Mevcut Sıcaklık: {now[1]}°C")
