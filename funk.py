from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from xizmatlar import xizmatlar


import json
import os
import time

kurs = 160

# Cache uchun
_services_cache = None
_cache_timestamp = 0
CACHE_DURATION = 300  # 5 daqiqa

# JSON fayldan xizmatlarni yuklash
def load_services_from_json():
    """JSON fayldan xizmatlarni yuklash (cache bilan)"""
    global _services_cache, _cache_timestamp
    
    current_time = time.time()
    
    # Agar cache mavjud va yangi bo'lsa, cache qaytarish
    if _services_cache is not None and (current_time - _cache_timestamp) < CACHE_DURATION:
        return _services_cache
    
    try:
        if os.path.exists('services_data.json'):
            with open('services_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                _services_cache = data.get('services', [])
                _cache_timestamp = current_time
                return _services_cache
        else:
            print("⚠️ services_data.json fayli topilmadi")
            return []
    except Exception as e:
        print(f"❌ JSON fayl o'qishda xatolik: {e}")
        return []
def get_service_rate(service_id):
    """Xizmat narxini olish"""
    try:
        services = load_services_from_json()
        
        for service in services:
            if service.get("service") == str(service_id):
                rate = service.get("rate")
                if rate:
                    return rate
        
        print(f"⚠️ Service {service_id} uchun rate topilmadi")
        return None
    except Exception as e:
        print(f"❌ get_service_rate xatolik: {e}")
        return None

def get_service_min_max(service_id):
    """Xizmat narxini olish"""
    try:
        services = load_services_from_json()
        
        for service in services:
            if service.get("service") == str(service_id):
                min = service.get("min")
                max = service.get("max")
                if min and max:
                    return f"🔽Min: {min}\n🔼Max: {max}"
        
        print(f"⚠️ Service {service_id} uchun min, max topilmadi")
        return None
    except Exception as e:
        print(f"❌ get_service_min_max xatolik: {e}")
        return None

def toifa_tugmalari(platforma: str) -> InlineKeyboardMarkup:
    toifa_nomi_list = list(xizmatlar[platforma].keys())  # Masalan: ['followers', 'views', 'likes']

    tugmalar = [
        [InlineKeyboardButton(
            text=f"{toifa} ({len(xizmatlar[platforma][toifa])})",
            callback_data=f"{platforma}:{toifa}"
        )]
        for toifa in toifa_nomi_list
    ]

    # Orqaga tugmasi
    tugmalar.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")
    ])

    return InlineKeyboardMarkup(inline_keyboard=tugmalar)

#####################################################################################################
def get_xizmat_name_by_service(service_id: int) -> str | None:
    for platforma, toifalar in xizmatlar.items():
        for toifa, xizmatlar_list in toifalar.items():
            for xizmat in xizmatlar_list:
                if xizmat["service"] == service_id:
                    return xizmat["name"]
    return None  # Topilmasa



def xizmat_tugmalari(platforma: str, toifa: str) -> InlineKeyboardMarkup:
    xizmatlar_list = xizmatlar[platforma][toifa]

    tugmalar = []
    for xizmat in xizmatlar_list:
        rate_str = get_service_rate(xizmat['service'])
        if rate_str is not None:
            try:
                rate = float(rate_str)
                narx = int(rate * kurs)
                text = f"{xizmat['name']} - {narx} so'm"
            except ValueError:
                text = f"{xizmat['name']} - Narx aniqlanmadi"
        else:
            text = f"{xizmat['name']} - Narx aniqlanmadi"

        tugmalar.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"service:{xizmat['service']}"
            )
        ])

    # Orqaga tugmasi
    tugmalar.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"platforma:{platforma}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=tugmalar)

def get_platforma_toifa_by_service(service_id: int) -> tuple[str, str] | None:
    """
    Xizmat ID orqali unga tegishli platforma va toifani topish.
    """
    for platforma, toifalar in xizmatlar.items():
        for toifa, xizmatlar_list in toifalar.items():
            for xizmat in xizmatlar_list:
                if xizmat["service"] == service_id:
                    return platforma, toifa
    return None