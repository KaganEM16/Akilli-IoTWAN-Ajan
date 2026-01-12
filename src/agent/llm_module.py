import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_ai_advice(analysis_results: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key: return "Hata: API anahtarı yok."

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Sen dinamik bir analiz uzmanısın. Kullanıcıya uzun, teknik ve detaylı raporlar sunarsın. Eğer sıcaklık 30 derecenin üstündeyse 'sıcak', 20'nin altındaysa 'soğuk' vurgusu yapmalısın. Alerji ve nefes darlığı uyarılarını mutlaka PM2.5 (toz) verisine dayandır."
                },
                {
                    "role": "user",
                    "content": f"Sadece şu verilere odaklanarak çok detaylı bir Türkçe rapor yaz: {analysis_results}"
                }
            ],
            temperature=0.9, # Yaratıcılık ve değişkenlik için artırıldı
            max_tokens=2000
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Yapay Zeka Hatası: {e}"
