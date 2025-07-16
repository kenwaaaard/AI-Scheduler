from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText

def create_gmail_service():
    creds = Credentials.from_authorized_user_file("token.json")
    return build("gmail", "v1", credentials=creds)

def send_email(service, sender, to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw}

    message = service.users().messages().send(userId="me", body=body).execute()
    print(f"✅ Email sent! Message ID: {message['id']}")

if __name__ == "__main__":
    service = create_gmail_service()
    send_email(
        service,
        sender="your_email@gmail.com",  # Replace with your Gmail
        to="recipient@example.com",     # Replace with test recipient
        subject="AI Scheduler Test",
        message_text="This is a test email sent via the AI Scheduler Gmail API integration."
    )
