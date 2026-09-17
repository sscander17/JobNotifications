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
    chunks = []
    current_chunk = ""
    
    for block in text.split("\n\n"):
        if len(current_chunk) + len(block) + 2 <= max_chunk_size:
            current_chunk += block + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = block + "\n\n"
            
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    for chunk in chunks:
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "disable_web_page_preview": True,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload)
        if not response.ok:
            print(f"Telegram API Error ({response.status_code}): {response.text}")