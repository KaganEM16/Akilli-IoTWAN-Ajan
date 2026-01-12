import sqlite3
import os
import time
import random
from datetime import datetime

# Veri tabanı yolu (db_manager ile aynı olmalı)
base_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(base_dir, "src", "data", "iot_sensor_data.db")

def veri_gonder():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))

    print("🚀 Test verisi gönderiliyor (Durdurmak için Ctrl+C)...")
    try:
        while True:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Rastgele, değişken veriler
            temp = round(random.uniform(15.0, 42.0), 1)
            hum = round(random.uniform(20.0, 95.0), 1)
            aqi = random.randint(5, 250)
            dust = round(random.uniform(0.1, 60.0), 2)
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            cursor.execute("INSERT INTO sensor_readings VALUES (?, ?, ?, ?, ?)",
                           (timestamp, temp, hum, aqi, dust))
            conn.commit()
            conn.close()
            
            print(f"📥 Kaydedildi: {timestamp} -> Sıcaklık: {temp}°C, Toz: {dust}")
            time.sleep(5) # 5 saniyede bir yeni veri
    except KeyboardInterrupt:
        print("\n👋 Test durduruldu.")

if __name__ == "__main__":
    veri_gonder()
