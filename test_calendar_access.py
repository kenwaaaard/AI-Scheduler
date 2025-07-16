from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import datetime

# Load saved credentials
creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar.readonly'])

# Build Calendar API service
service = build('calendar', 'v3', credentials=creds)

# Get the current time
now = datetime.datetime.utcnow().isoformat() + 'Z'

# List all calendars the user has access to
calendar_list = service.calendarList().list().execute()

for calendar in calendar_list['items']:
    cal_id = calendar['id']
    cal_summary = calendar.get('summary', 'Unnamed Calendar')

    print(f"\n📅 Events from: {cal_summary}")

    events_result = (
        service.events()
        .list(
            calendarId=cal_id,
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        )
        .execute()
    )

    events = events_result.get('items', [])

    if not events:
        print("  No upcoming events found.")
        continue

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"  {start} — {event.get('summary', 'No Title')}")
