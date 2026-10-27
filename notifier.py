import base64
from email.message import EmailMessage
from gmail_client import get_gmail_service

def send_email(service, subject, body):
    my_address = service.users().getProfile(userId="me").execute()["emailAddress"]

    msg = EmailMessage()
    msg["To"] = my_address
    msg["From"] = my_address
    msg["Subject"] = subject
    msg.set_content(body)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    sent = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return sent["id"]

if __name__ == "__main__":
    service = get_gmail_service()
    msg_id = send_email(service, "[mail-alert] Test", "Hello from job-mail-alert 👋")
    print("Sent! Message ID:", msg_id)