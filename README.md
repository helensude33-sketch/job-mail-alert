# job-mail-alert

A small Python tool that reads your Gmail inbox, filters emails by **your own preferences**, and sends you a single summary email listing only the important ones — without ever notifying you twice about the same email.

I built it to stop missing relevant part-time job and internship emails among newsletters and noise, but the filter is fully user-configurable, so it works for any topic.

## How it works

```
Gmail inbox ──► gmail_client.py ──► filters.py ──► seen_store.py ──► notifier.py ──► summary email
               (read via API)      (your rules)   (skip duplicates)   (send via API)
```

`main.py` connects the pieces:

1. Fetches the 20 most recent emails (subject, sender, preview) via the Gmail API.
2. Skips emails it has already processed (IDs stored in `seen_ids.json`) and its own alert emails (`[mail-alert]` tag) to avoid loops.
3. Runs each email through the rule-based filter:
   - must contain a **topic word** → otherwise ignored
   - must **not** contain a **blocked word**
   - must contain a **wanted word** → match
4. Sends one summary email with all matches, then saves the processed IDs. If sending fails, IDs are not saved, so those emails are retried on the next run.

## Project structure

| File | Purpose |
|---|---|
| `gmail_client.py` | OAuth login (token reuse/refresh) and reading recent emails |
| `filters.py` | Loads preferences and decides if an email matches, with a reason |
| `preferences.json` | Your topic / wanted / blocked word lists |
| `setup_preferences.py` | Interactive setup that writes `preferences.json` |
| `seen_store.py` | Persists processed email IDs (duplicate protection) |
| `notifier.py` | Sends the summary email via the Gmail API |
| `main.py` | Orchestrates the full pipeline |

## Setup

1. Clone the repo and create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
2. In Google Cloud Console: create a project, enable the **Gmail API**, configure the OAuth consent screen (add yourself as a test user) and create a **Desktop** OAuth client. Download it as `credentials.json` into the project folder.
3. Set your preferences:
   ```
   python setup_preferences.py
   ```
4. Run:
   ```
   python main.py
   ```
   On first run a browser window asks for permission (read + send). A `token.json` is saved so you don't need to log in again.

`credentials.json`, `token.json` and `seen_ids.json` are git-ignored and never committed.

## Design decisions

- **Notification channel:** I first implemented WhatsApp notifications with Twilio. The trial account required pre-approved content templates (error 21654) and blocked template creation on trial accounts, and other WhatsApp options required paid plans or unofficial libraries that risk account bans. I switched to sending a summary email through the Gmail API, which reuses the existing OAuth connection, needs no extra account, and is free. The notifier is isolated in one module, so another channel can be swapped in later.
- **Least privilege:** only `gmail.readonly` and `gmail.send` scopes are requested.
- **Idempotency:** processed email IDs are stored, so re-running the script never sends duplicate alerts.

## Limitations & next steps

- Keyword matching is simple substring search, so it can produce false positives/negatives (e.g. "intern" also matches "international"). Next step: word-boundary matching, then an optional LLM-based classifier.
- Runs on demand; next step is scheduling (Windows Task Scheduler / cron).
- Add unit tests with `pytest` for `filters.py` and `seen_store.py`.
