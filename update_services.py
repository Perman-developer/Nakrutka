import requests
import json
import time
import datetime
from config import API_KEY, API_URL

def update_services_from_api():
    """API dan xizmatlarni yuklab JSON faylga saqlash"""
    payload = {
        "key": API_KEY,
        "action": "services"
    }
    
    try:
        response = requests.post(API_URL, data=payload)
        if response.status_code == 200:
            services = response.json()
            
            # JSON faylga saqlash
            with open('services_data.json', 'w', encoding='utf-8') as f:
                timestamp = int(time.time())
                dt = datetime.datetime.fromtimestamp(timestamp)
                update_time = dt.strftime("%Y-%m-%d %H:%M:%S")  # ✅ to'g'rilandi

                json.dump({
                    'services': services,
                    'last_updated': update_time
                }, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {len(services)} ta xizmat muvaffaqiyatli yangilandi")
            return True
        else:
            print(f"❌ API xatolik: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False

