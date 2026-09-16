# JobMonitor

JobMonitor is an automated job tracking script that monitors career pages and Applicant Tracking Systems (ATS) of various companies. It alerts you via Telegram when new, relevant technical jobs are posted.

## Features

- **Multi-ATS Support**: Fetches job listings from various platforms including Greenhouse, Workday, Eightfold, Recruitee, Oracle Cloud, Avature, Jibe, and custom company sites.
- **AI-Powered Filtering**: Uses Google Gemini to filter out non-technical roles (e.g., HR, Sales, Legal) and only keep engineering, software, and technical positions. It also includes a fast local keyword pre-filter.
- **State Management**: Keeps track of previously seen jobs locally (`saved_jobs.json`) so it only notifies you about new openings.
- **Telegram Notifications**: Sends formatted alerts directly to a configured Telegram chat with the company name, job title, and link.

## Project Structure

- `main.py`: The entry point. Loads the state, fetches jobs for all companies, filters them, sends notifications for new ones, and updates the state.
- `config.py`: Contains the list of companies to track and their ATS configurations.
- `fetchers.py`: Includes specific scraping and API fetching logic for different ATS platforms (Workday, Greenhouse, etc.).
- `ai_filter.py`: Evaluates job titles using keyword matching and the Google Gemini API to determine relevance.
- `notifier.py`: Handles sending alerts via the Telegram Bot API.
- `job_tracker.py`: Alternative entry point/legacy script.
- `saved_jobs.json`: The local state file storing previously discovered job listings.

## Prerequisites

- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`, `google-genai`, `curl_cffi`.
- A Telegram Bot Token and Chat ID (currently configured in `notifier.py`).
- A Gemini API key (set as the `GEMINI_API_KEY` environment variable).

## Setup & Usage

1. **Install Dependencies**:
   Install the required libraries:
   ```bash
   pip install requests beautifulsoup4 curl_cffi google-genai
   ```

2. **Configure Companies**:
   Edit `config.py` to add or remove companies you want to monitor.

3. **Set Environment Variables**:
   Set your `GEMINI_API_KEY` for the AI filter to work:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
   *(Note: For Windows, use `set` or `$env:` in PowerShell)*

4. **Telegram Connection Setup**:
   Setting up the Telegram connection requires both a Bot Token and a Chat ID. They need to be configured in `notifier.py`.
   - **Get a Bot Token**:
     1. Open Telegram and search for `@BotFather`.
     2. Send the `/newbot` command and follow the instructions to create your bot.
     3. Once created, BotFather will give you a token (e.g., `123456789:ABCdefGhIJKlmnopQRstUVwxyZ`).
   - **Get your Chat ID**:
     1. Start a chat with your newly created bot in Telegram and send a test message (e.g., "Hello").
     2. Open your web browser and navigate to: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` (Replace `<YOUR_BOT_TOKEN>` with the token from BotFather).
     3. Look for the `"chat":{"id":...}` part in the JSON response. That number is your Chat ID.
     *(Alternatively, you can use a bot like `@userinfobot` to get your Chat ID directly).*
   - **Configure `notifier.py`**:
     Open `notifier.py` and replace the `token` and `chat_id` variables with your values.

5. **Run the Tracker**:
   Execute the main script to check for jobs:
   ```bash
   python main.py
   ```
   It is recommended to run this script periodically via a cron job or scheduled task.
