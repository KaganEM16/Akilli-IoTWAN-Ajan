import json
from datetime import datetime
import os

def save_report(content):
    # Ana dizinde agent_reports klasörü oluşturur
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(os.path.dirname(base_dir), "agent_reports")
    os.makedirs(report_path, exist_ok=True)
    
    timestamp_filename = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(report_path, f"report_{timestamp_filename}.json")
    
    # Rapor içeriğini JSON olarak kaydeder
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "report": content, 
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, f, ensure_ascii=False, indent=4)
