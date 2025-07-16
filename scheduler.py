import openai
import json

def run_scheduler():
    with open("config.json") as f:
        config = json.load(f)

    client = openai.OpenAI(api_key=config["openai_api_key"])

    print("Running scheduler...")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful scheduling assistant."},
            {"role": "user", "content": "Can you help me plan my week?"}
        ]
    )

    print(response.choices[0].message.content)
