from gmail_client import get_gmail_service, list_recent_emails
from filters import load_preferences, check_email
from seen_store import load_seen, save_seen
from notifier import send_email

ALERT_TAG = "[mail-alert]"

def main():
    service = get_gmail_service()
    prefs = load_preferences()
    seen = load_seen()
    emails = list_recent_emails(service, max_results=20)

    matches = []
    for email in emails:
        if email["id"] in seen:
            continue
        seen.add(email["id"])

        if email["subject"].startswith(ALERT_TAG):
            continue

        decision, reason = check_email(email, prefs)
        if decision:
            matches.append(email)

    if matches:
        lines = [f"- {e['subject']} | {e['from']}" for e in matches]
        body = "\n".join(lines)
        send_email(service, f"{ALERT_TAG} {len(matches)} important email(s)", body)
        print("Notification sent for", len(matches), "email(s)")
    else:
        print("No new important emails.")

    save_seen(seen)

if __name__ == "__main__":
    main()