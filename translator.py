import os
import requests
import urllib.parse

def translate_to_english(text: str) -> str:
    """
    Translates text to English using the MyMemory API.
    Fails gracefully by returning the original text if the API fails or limits are reached.
    """
    email = os.environ.get("MYMEMORY_EMAIL", "sscander17@example.com")
    
    # We use de|en to force German to English. If the text is already English, it usually passes it through unchanged.
    url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=de|en&de={urllib.parse.quote(email)}"
    
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("responseStatus") == 200:
                translated = data["responseData"]["translatedText"]
                
                # Check if it was an exact match in English or successfully translated
                # MyMemory adds some boilerplate error messages into translatedText if it fails
                if "MYMEMORY WARNING" not in translated:
                    return translated
        return text
    except Exception as e:
        print(f"Translation warning for '{text}': {e}")
        return text
