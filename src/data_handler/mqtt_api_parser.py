import base64
import json

def parse_lorawan_payload(payload_base64):
    """Base64 gelen veriyi cozer (Ornek sensor formatina gore)"""
    try:
        raw_bytes = base64.b64decode(payload_base64)
        # Ornek: Ilk 2 byte sicaklik, sonraki 2 byte nem (Sanal veri icin basittir)
        temp = int.from_bytes(raw_bytes[0:2], byteorder='big') / 10.0
        hum = int.from_bytes(raw_bytes[2:4], byteorder='big') / 10.0
        return {"temp": temp, "hum": hum}
    except Exception as e:
        print(f"Cozumleme hatasi: {e}")
        return None
