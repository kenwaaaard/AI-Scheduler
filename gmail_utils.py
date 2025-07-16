
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import re

def search_threads_with_cc_or_to(service):
    query = 'cc:me OR to:me'
    response = service.users().threads().list(userId='me', q=query).execute()
    threads = response.get('threads', [])
    return threads

def get_thread_messages(service, thread_id):
    thread = service.users().threads().get(userId='me', id=thread_id, format='full').execute()
    return thread.get('messages', [])

def extract_email_from_headers(headers):
    for header in headers:
        if header['name'].lower() == 'from':
            return header['value']
    return None

def extract_subject(headers):
    for header in headers:
        if header['name'].lower() == 'subject':
            return header['value']
    return "No Subject"

def get_thread_recipients(messages):
    recipients = set()
    for msg in messages:
        headers = msg.get('payload', {}).get('headers', [])
        for header in headers:
            if header.get("name", "").lower() in ["to", "cc"]:
                recipients.add(header.get("value", ""))
    return list(recipients)
