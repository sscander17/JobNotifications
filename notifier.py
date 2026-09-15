import os
import requests

def send_telegram_alert(text):
    token = "8730019825:AAFsyA5z9KdI6mDOoJVGVpnvz3vRGRilzFE"
    chat_id = "7167683949"
    
    if not token or not chat_id:
        print("Telegram credentials missing, skipping notification.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    max_chunk_size = 4000
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    for chunk in chunks:
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "disable_web_page_preview": True,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload)
        if not response.ok:
            print(f"❌ Telegram API Error ({response.status_code}): {response.text}")