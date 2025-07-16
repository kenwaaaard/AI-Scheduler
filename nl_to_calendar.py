import os
import json
from datetime import datetime
from openai import OpenAI
from auth_google import get_calendar_service

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_event_from_text(prompt):
    system_msg = "You are an assistant that extracts calendar event details. Return JSON with fields: summary, location, start (ISO 8601), end (ISO 8601)."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
    )
    try:
        return json.loads(response.choices[0].message.content.strip())
    except Exception:
        return None

def create_calendar_event(event_details, attendees=[]):
    service = get_calendar_service()
    event = {
        'summary': event_details['summary'],
        'location': event_details.get('location', ''),
        'start': {
            'dateTime': event_details['start'],
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': event_details['end'],
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [{'email': email} for email in attendees],
    }
    service.events().insert(calendarId='primary', body=event, sendUpdates="all").execute()