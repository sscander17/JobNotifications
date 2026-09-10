import requests
from bs4 import BeautifulSoup
import json
import os

# 1. Configuration
URL = "https://career.quantum-systems.com/"
STATE_FILE = "saved_jobs.json"

# Add your companies here. Specify "greenhouse", "lever", or "scrape"
COMPANIES_TO_TRACK = [
    {
        "name": "Helsing",
        "type": "greenhouse",
        "id_or_url": "helsing" # Their Greenhouse board ID
    },
    {
        "name": "Quantum-Systems",
        "type": "scrape",
        "id_or_url": "https://career.quantum-systems.com/",
        "url_filter": "/o/" # The unique text in their job URLs
    }
]


def send_telegram_message(text):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram credentials missing, skipping notification.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Telegram limit is 4096 chars; split message into safe chunks
    max_chunk_size = 4000
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    for chunk in chunks:
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "disable_web_page_preview": True
        }
        response = requests.post(url, json=payload)
        if not response.ok:
            print(f"❌ Telegram API Error ({response.status_code}): {response.text}")

def fetch_greenhouse(board_id):
    """Fetches jobs via Greenhouse hidden JSON API"""
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_id}/jobs"
    response = requests.get(url)
    response.raise_for_status()
    jobs = response.json().get("jobs", [])

    # Return dictionary of { URL : Title }
    return {job["absolute_url"]: job["title"] for job in jobs}


def fetch_scrape(url, url_filter):
    """Fetches jobs by reading HTML for custom websites"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    current_jobs = {}
    for link in soup.find_all('a'):
        href = link.get('href')
        title = link.get_text(strip=True)

        if href and url_filter in href and title:
            if title.lower() not in ["view job", "apply now", "read more"]:
                if not href.startswith("http"):
                    href = url.rstrip("/") + href
                current_jobs[href] = title

    return current_jobs


def main():
    # Load previous state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            previous_state = json.load(f)
    else:
        previous_state = {}

    current_state = {}
    master_notification_text = ""

    # Loop through all our companies
    for company in COMPANIES_TO_TRACK:
        name = company["name"]
        print(f"Checking {name}...")

        try:
            # Route to the correct fetcher
            if company["type"] == "greenhouse":
                jobs = fetch_greenhouse(company["id_or_url"])
            elif company["type"] == "scrape":
                jobs = fetch_scrape(company["id_or_url"], company["url_filter"])
            else:
                print(f"Unknown type for {name}")
                continue

            current_state[name] = jobs

            # Compare to previous state
            prev_jobs = previous_state.get(name, {})
            current_urls = set(jobs.keys())
            prev_urls = set(prev_jobs.keys())

            new_urls = current_urls - prev_urls

            if new_urls:
                master_notification_text += f"🏢 **{name}** - NEW JOBS:\n\n"
                for url in new_urls:
                    master_notification_text += f"• {jobs[url]}\n  {url}\n\n"

        except Exception as e:
            print(f"Error checking {name}: {e}")

    # Send a single combined Telegram message if there are any new jobs
    if master_notification_text:
        print("🚨 Sending Telegram Alert!")
        send_telegram_message(master_notification_text)
    else:
        print("No new jobs found across any companies.")

    # Save current state
    with open(STATE_FILE, "w") as f:
        json.dump(current_state, f, indent=2)


if __name__ == "__main__":
    main()