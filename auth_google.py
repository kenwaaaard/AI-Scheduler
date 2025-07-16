import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for Gmail and Google Calendar
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email"
]

def authenticate_google():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=8000)
        # Save the new credentials
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_gmail_service():
    creds = authenticate_google()
    return build("gmail", "v1", credentials=creds)

def get_calendar_service():
    creds = authenticate_google()
    return build("calendar", "v3", credentials=creds)

if __name__ == "__main__":
    # Triggers auth flow if run directly
    authenticate_google()
    print("✅ Authentication complete. Token saved as token.json.")
