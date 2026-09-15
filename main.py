import json
import os
import html
from notifier import send_telegram_alert
from fetchers import FETCHERS

from config import COMPANIES, STATE_FILE

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def main():
    previous_state = load_state()
    current_state = {}
    notification_body = ""

    for company in COMPANIES:
        name = company["name"]
        company_type = company["type"]
        fetcher = FETCHERS.get(company_type)

        if not fetcher:
            print(f"Skipping {name}: Unknown type '{company_type}'")
            continue

        print(f"Checking {name}...")
        try:
            jobs = fetcher(company)
            current_state[name] = jobs

            prev_jobs = previous_state.get(name, {})
            new_urls = set(jobs.keys()) - set(prev_jobs.keys())

            if new_urls:
                notification_body += f"🏢 <b>{html.escape(name)}</b> - NEW JOBS:\n"
                for url in new_urls:
                    notification_body += f"• <b>{html.escape(jobs[url])}</b>\n  {html.escape(url)}\n\n"

        except Exception as e:
            print(f"Error checking {name}: {e}")

    if notification_body:
        print("New openings detected. Sending Telegram alert.")
        send_telegram_alert(notification_body)
    else:
        print("No new jobs detected.")

    save_state(current_state)

if __name__ == "__main__":
    main()