import os
import openai
import time

from auth_google import get_gmail_service
from gmail_utils import (
    get_thread_messages,
    search_threads_with_cc_or_to,
    extract_email_from_headers,
    extract_subject,
    get_thread_recipients,
    send_reply,
)

from nl_to_calendar import parse_event_from_text, create_calendar_event

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    client = openai.OpenAI()
    chat_completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that schedules meetings using the user's calendar."},
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content

def parse_and_reply():
    service = get_gmail_service()
    print("📬 Checking for CC’d or To: emails...")
    threads = search_threads_with_cc_or_to(service)

    if not threads:
        print("📭 No relevant threads found.")
        return

    print("✅ Found thread with CC or To:")
    thread = threads[0]
    thread_id = thread["id"]
    messages = get_thread_messages(service, thread_id)

    if not messages:
        print("📪 No messages in thread.")
        return

    latest_message = messages[-1]
    snippet = latest_message.get("snippet", "")
    message_id = latest_message["id"]
    headers = latest_message["payload"]["headers"]
    to_email = extract_email_from_headers(headers)
    subject = extract_subject(headers)
    all_recipients = get_thread_recipients(messages)

    # Skip if supposed to reply to self or from our own scheduler address
    if to_email == "kenward.scheduler@gmail.com":
        print("🚫 Skipping self-reply.")
        return

    # Only jump in after receiving a reply from someone who isn’t the original sender
    original_sender = extract_email_from_headers(messages[0]["payload"]["headers"])
    latest_sender = extract_email_from_headers(latest_message["payload"]["headers"])

    if latest_sender == original_sender:
        print("⏳ Waiting for counterparty to reply before jumping in.")
        return

    print("🧠 Parsing for calendar intent...")
    event_data = parse_event_from_text(snippet)
    if event_data:
        create_calendar_event(event_data, attendees=[to_email])
        reply_body = generate_response(snippet)
        send_reply(service, thread_id, message_id, reply_body, to_email, subject, reply_all=True, cc_list=all_recipients)

if __name__ == "__main__":
    while True:
        parse_and_reply()
        print("⏰ Done. Sleeping for 3 minutes.")
        time.sleep(180)
