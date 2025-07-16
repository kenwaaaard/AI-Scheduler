
def classify_intent(text):
    text = text.lower()
    if "reschedul" in text or "another time" in text:
        return "reschedule"
    elif "cancel" in text:
        return "cancel"
    elif "schedule" in text or "book" in text:
        return "schedule"
    return "unknown"
