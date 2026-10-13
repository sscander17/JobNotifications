# JobMonitor

JobMonitor is an automated job tracking and notification tool that monitors company career pages and Applicant Tracking Systems (ATS). It alerts you via Telegram when new, relevant technical jobs are posted.

> **Current Focus**: This repository is currently configured out-of-the-box to monitor **junior technical, software, and engineering roles in Munich, Germany**. However, the system is fully modular—anyone can use it for their own preferred cities, companies, and seniority levels by updating the company list in `config.py` and customizing the keyword filters in `ai_filter.py`.

## Features

- **Multi-ATS Support**: Fetches job listings from various platforms including Greenhouse, Workday, Eightfold, Ashby, Cornerstone OnDemand (CSOD), TalentBrew, Personio, Recruitee, Oracle Cloud, Avature, Jibe, SuccessFactors, and custom company career portals.
- **Smart Role & Seniority Filtering**:
  - **Excludes Senior & Lead Roles**: Automatically filters out positions containing terms like `senior`, `lead`, `head of`, `principal`, and `manager` to focus strictly on junior and entry-level positions.
  - **Excludes Non-Technical Domains**: Automatically discards roles in non-technical fields such as Human Resources (HR), Marketing, Sales, Legal, Finance, Accounting, and Facility Management.
  - **AI Ambiguity Resolution**: Uses Google Gemini as a secondary filter to evaluate ambiguous job titles and ensure relevant engineering, software, hardware, and IT positions are captured.
- **Automatic Translation**: Automatically translates German job titles into English (via MyMemory API) before evaluation and alerting, ensuring consistent keyword matching and readable notifications.
- **State Management**: Keeps track of previously seen jobs locally (`saved_jobs.json`) so it only alerts you about brand new postings.
- **Telegram Notifications**: Sends cleanly formatted alerts with high-contrast company headers and direct application links.

## Project Structure

- `main.py`: The entry point. Loads state, orchestrates fetching across all companies, translates titles, filters for relevance/seniority, sends Telegram notifications, and saves the updated state.
- `config.py`: Contains the list of companies to track and their ATS configurations.
- `fetchers.py`: Includes specific scraping and API fetching logic for different ATS platforms (Workday, Greenhouse, Eightfold, Ashby, etc.).
- `ai_filter.py`: Evaluates job titles using keyword pre-filtering (auto-keep / auto-reject) and the Google Gemini API.
- `translator.py`: Translates job titles from German to English.
- `notifier.py`: Handles sending alerts via the Telegram Bot API.
- `saved_jobs.json`: The local state file storing previously discovered job listings.

## Prerequisites

- Python 3.x
- Required Python packages: `requests`, `beautifulsoup4`, `google-genai`, `curl_cffi`.
- A Telegram Bot Token and Chat ID (configured in `notifier.py` or via environment variables).
- A Gemini API key (set as the `GEMINI_API_KEY` environment variable).

## Setup & Usage

1. **Install Dependencies**:
   Install the required libraries:
   ```bash
   pip install requests beautifulsoup4 curl_cffi google-genai
   ```

2. **Configure Companies & Filters**:
   - **Track Your Own Companies**: Edit `config.py` to add or remove companies and adjust location filters for your target area.
   - **Customize Roles & Seniority**: Adjust `AUTO_REJECT_WORDS` and `AUTO_KEEP_WORDS` in `ai_filter.py` if you wish to track senior positions, different fields, or specific keywords.

3. **Set Environment Variables**:
   Set your `GEMINI_API_KEY` for the AI filter to work:
   ```bash
   export GEMINI_API_KEY="your-api-key"
   ```
   *(Note: For Windows, use `set` or `$env:` in PowerShell)*

4. **Telegram Connection Setup**:
   Setting up the Telegram connection requires both a Bot Token and a Chat ID.
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
     Open `notifier.py` and replace the `token` and `chat_id` variables with your values, or pass them via `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID` environment variables.

5. **Run the Tracker**:
   Execute the main script to check for jobs:
   ```bash
   python main.py
   ```
   It is recommended to run this script periodically via a cron job or scheduled GitHub Actions workflow.
