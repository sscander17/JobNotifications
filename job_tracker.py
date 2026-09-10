import requests
from bs4 import BeautifulSoup
import json
import os

# 1. Configuration
URL = "https://career.quantum-systems.com/"
STATE_FILE = "saved_jobs.json"


def send_telegram_message(text):
    # It pulls these secrets from GitHub Actions later
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram credentials missing, skipping notification.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def get_current_jobs():
    # Pretend to be a normal web browser (some sites block automated scripts)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # Download the webpage
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    current_jobs = {}

    # Find all links on the page
    for link in soup.find_all('a'):
        href = link.get('href')
        title = link.get_text(strip=True)

        # Filter: We only want links that go to a specific job page.
        # On Quantum-Systems (and many sites), job URLs contain "/jobs/"
        if href and "/o/" in href and title:
            # Sometimes a link is just a button saying "View job".
            # We skip those so we only capture the actual Job Titles.
            if title.lower() not in ["view job", "apply now", "read more"]:
                # Ensure it's a full URL
                if not href.startswith("http"):
                    href = URL.rstrip("/") + href

                # Use the URL as the unique ID, and the text as the Title
                current_jobs[href] = title

    return current_jobs


def main():
    # 2. Load previous state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            previous_jobs = json.load(f)
    else:
        previous_jobs = {}

    # 3. Fetch current jobs via scraping
    current_jobs = get_current_jobs()

    # 4. Compare URLs (using URLs as unique IDs instead of API IDs)
    previous_urls = set(previous_jobs.keys())
    current_urls = set(current_jobs.keys())

    new_urls = current_urls - previous_urls
    closed_urls = previous_urls - current_urls

    # 5. Alert on changes
    if new_urls:
        print("🚨 NEW JOBS FOUND:")
        msg = "🚨 NEW JOBS FOUND:\n"
        for url in new_urls:
            print(f"- {current_jobs[url]}")
            print(f"  Link: {url}")
            msg += f"- {current_jobs[url]}\n{url}\n\n"
        send_telegram_message(msg)  # <--- ADD THIS LINE

    if closed_urls:
        print("🛑 JOBS CLOSED:")
        for url in closed_urls:
            print(f"- {previous_jobs[url]}")
            print(f"  Link: {url}")

    if not new_urls and not closed_urls:
        print("No changes since last check. Currently open jobs:", len(current_urls))

    # 6. Save state
    with open(STATE_FILE, "w") as f:
        json.dump(current_jobs, f, indent=2)


if __name__ == "__main__":
    main()