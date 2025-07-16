
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def update_event(event_id, new_start, new_end, creds):
    service = build("calendar", "v3", credentials=creds)
    event = service.events().get(calendarId="primary", eventId=event_id).execute()
    event['start'] = {"dateTime": new_start, "timeZone": "America/Los_Angeles"}
    event['end'] = {"dateTime": new_end, "timeZone": "America/Los_Angeles"}
    updated_event = service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
    return updated_event

def delete_event(event_id, creds):
    service = build("calendar", "v3", credentials=creds)
    service.events().delete(calendarId="primary", eventId=event_id).execute()
