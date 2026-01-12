import paho.mqtt.client as mqtt
import json
import os
import ssl
from datetime import datetime
from dotenv import load_dotenv
from .db_manager import DBManager

load_dotenv()
db = DBManager()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ [MQTT] Bağlantı Başarılı!")
        topic = os.getenv("LORA_MQTT_TOPIC", "akilli_iot/projem/sensor_veri")
        client.subscribe(topic)
    else:
        print(f"❌ [MQTT] Bağlantı Hatası! Kod: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload['timestamp'] = datetime.now().isoformat()
        db.save_data(payload)
        print(f"📥 Veri Alındı: {payload}")
    except Exception as e:
        print(f"⚠️ Mesaj Hatası: {e}")

def start_receiver():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    host = os.getenv("LORA_MQTT_BROKER_HOST", "broker.hivemq.com")
    
    port = int(os.getenv("LORA_MQTT_PORT", 1883))

    if port == 8883:
        try:
            client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
            print("🔒 Güvenli Port (8883) Modu Aktif")
        except Exception as e:
            print(f"⚠️ TLS Ayar Hatası: {e}")

    print(f"🔄 {host}:{port} bağlanılıyor...")
    try:
        client.connect(host, port, 60)
        client.loop_start()
        return client
    except Exception:
       
        print("⚠️ Port 8883 başarısız, standart Port 1883 deneniyor...")
        client = mqtt.Client() # Temiz bir client
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(host, 1883, 60)
        client.loop_start()
        return client
