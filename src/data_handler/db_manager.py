import sqlite3
import os

class DBManager:
    def __init__(self):
        # Dosya yolunu mutlak yol (absolute path) olarak ayarla
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, "data", "iot_sensor_data.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                timestamp TEXT,
                temp REAL,
                hum REAL,
                aqi INTEGER,
                dust REAL
            )
        ''')
        conn.commit()
        conn.close()

    def save_data(self, data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sensor_readings VALUES (?, ?, ?, ?, ?)",
                       (data['timestamp'], data['temp'], data['hum'], data['aqi'], data.get('dust', 0)))
        conn.commit()
        conn.close()

    def fetch_recent(self, limit=100):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except:
            return []

    def clear_all_data(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sensor_readings")
            conn.commit()
            conn.close()
            return True
        except:
            return False
