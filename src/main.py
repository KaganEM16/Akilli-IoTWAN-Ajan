import os
import threading
import time
import subprocess
import sys
import signal
from dotenv import load_dotenv
from data_handler.db_manager import DBManager
from agent.agent_core import IOTAgent

load_dotenv()
db = DBManager()
agent = IOTAgent()

running = True
dashboard_process = None

def cleanup_and_exit(sig=None, frame=None):
    global running, dashboard_process
    print("\n🛑 Sistem kapatılıyor...")
    running = False
    
    if dashboard_process:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(dashboard_process.pid)], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            dashboard_process.terminate()
            
    print("👋 Hoşça kalın.")
    os._exit(0)

signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

def run_dashboard():
    global dashboard_process
    cmd = f'"{sys.executable}" -m streamlit run src/ui/app.py'
    try:
        dashboard_process = subprocess.Popen(cmd, shell=True)
    except Exception as e:
        print(f"❌ Arayüz başlatılamadı: {e}")

def run_agent_loop():
    while running:
        try:
            agent.run_analysis()
        except Exception as e:
            print(f"❌ Analiz hatası: {e}")
        
        interval = int(os.getenv("AGENT_CYCLE_INTERVAL", 60))
        for _ in range(interval):
            if not running: break
            time.sleep(1)

if __name__ == "__main__":
    print("-" * 30)
    print("🚀 IoT SİSTEMİ ÇALIŞIYOR")
    print("-" * 30)

    run_dashboard()

    agent_thread = threading.Thread(target=run_agent_loop, daemon=True)
    agent_thread.start()

    print("\n💡 Durdurmak için Ctrl+C tuşuna basın.")
    
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup_and_exit()
